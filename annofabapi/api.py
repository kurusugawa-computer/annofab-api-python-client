import copy
import json
import logging
import time
from functools import wraps
from json import JSONDecodeError
from typing import Any, Dict, Optional, Tuple

import backoff
import requests
from requests.auth import AuthBase
from requests.cookies import RequestsCookieJar

from annofabapi.exceptions import NotLoggedInError
from annofabapi.generated_api import AbstractAnnofabApi

logger = logging.getLogger(__name__)

DEFAULT_ENDPOINT_URL = "https://annofab.com"
"""Annofab WebAPIのデフォルトのエンドポイントURL"""

DEFAULT_WAITING_TIME_SECONDS_WITH_429_STATUS_CODE = 300
"""HTTP Status Codeが429のときの、デフォルト（Retry-Afterヘッダがないとき）の待ち時間です。"""


def _raise_for_status(response: requests.Response) -> None:
    """
    HTTP Status CodeがErrorの場合、``requests.exceptions.HTTPError`` を発生させる。
    そのとき ``response.text`` もHTTPErrorに加えて、HTTPError発生時にエラーの原因が分かるようにする。


    Args:
        response: Response

    Raises:
        requests.exceptions.HTTPError:

    """
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        http_error_msg = f"{e.args[0]} , {response.text}"
        e.args = (http_error_msg,)
        raise e


def _log_error_response(arg_logger: logging.Logger, response: requests.Response) -> None:
    """
    HTTP Statusが400以上ならば、loggerにresponse/request情報を出力する


    Args:
        arg_logger: logger
        response: Response

    """

    def mask_key(d, key: str):
        if key in d:
            d[key] = "***"

    if 400 <= response.status_code < 600:
        headers = copy.deepcopy(response.request.headers)
        # logにAuthorizationを出力しないようにマスクする
        mask_key(headers, "Authorization")

        # request_bodyのpassword関係をマスクして、logに出力する
        request_body = response.request.body
        request_body_for_logger: Optional[Any]
        if request_body is not None and request_body != "":
            if isinstance(request_body, str):
                try:
                    dict_request_body = json.loads(request_body)
                    request_body_for_logger = _create_request_body_for_logger(dict_request_body)
                except JSONDecodeError:
                    request_body_for_logger = request_body
            else:
                request_body_for_logger = _create_request_body_for_logger(request_body)
        else:
            request_body_for_logger = request_body

        arg_logger.error(
            "HTTP error occurred :: %s",
            {
                "response": {
                    "status_code": response.status_code,
                    "text": response.text,
                },
                "request": {
                    "http_method": response.request.method,
                    "url": response.request.url,
                    "body": request_body_for_logger,
                    "headers": headers,
                },
            },
        )


def _create_request_body_for_logger(data: Any) -> Any:
    """
    ログに出力するためのreqest_bodyを生成する。
     * パスワードやトークンなどの機密情報をマスクする
     * bytes型の場合は `(bytes)`と記載する。


    Args:
        data: request_body

    Returns:
        ログ出力用のrequest_body
    """

    def mask_key(d, key: str):
        if key in d:
            d[key] = "***"

    if not isinstance(data, dict):
        return data
    elif isinstance(data, bytes):
        # bytes型のときは値を出力しても意味がないので、bytesであることが分かるようにする
        return "(bytes)"

    MASKED_KEYS = {"password", "old_password", "new_password", "id_token", "refresh_token", "access_token"}
    diff = MASKED_KEYS - set(data.keys())
    if len(diff) == len(MASKED_KEYS):
        # マスク対象のキーがない
        return data

    copied_data = copy.deepcopy(data)
    for key in MASKED_KEYS:
        mask_key(copied_data, key)

    return copied_data


def _create_query_params_for_logger(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    ログに出力するためのquery_paramsを生成する。
     * AWS関係のcredential情報をマスクする。

    Args:
        params: query_params

    Returns:
        ログ出力用のparams
    """

    def mask_key(d, key: str):
        if key in d:
            d[key] = "***"

    MASKED_KEYS = {"X-Amz-Security-Token", "X-Amz-Credential"}
    diff = MASKED_KEYS - set(params.keys())
    if len(diff) == len(MASKED_KEYS):
        # マスク対象のキーがない
        return params

    copied_params = copy.deepcopy(params)
    for key in MASKED_KEYS:
        mask_key(copied_params, key)

    return copied_params


def _should_retry_with_status(status_code: int) -> bool:
    """
    HTTP Status Codeからリトライすべきかどうかを返す。
    """
    # 注意：429(Too many requests)の場合は、backoffモジュール外でリトライするため、このメソッドでは判定しない
    if status_code == requests.codes.not_implemented:
        return False
    if 500 <= status_code < 600:
        return True
    return False


def my_backoff(function):
    """
    HTTP Status Codeが429 or 5XXのときはリトライする. 最大5分間リトライする。
    """

    @wraps(function)
    def wrapped(*args, **kwargs):
        def fatal_code(e):
            """
            リトライするかどうか
            status codeが5xxのとき、またはToo many Requests(429)のときはリトライする。429以外の4XXはリトライしない
            https://requests.kennethreitz.org/en/master/user/quickstart/#errors-and-exceptions

            Args:
                e: exception

            Returns:
                True: give up(リトライしない), False: リトライする

            """
            if isinstance(e, requests.exceptions.HTTPError):
                if e.response is None:
                    return True
                return not _should_retry_with_status(e.response.status_code)

            else:
                # リトライする
                return False

        return backoff.on_exception(
            backoff.expo,
            (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, ConnectionError),
            jitter=backoff.full_jitter,
            max_time=300,
            giveup=fatal_code,
            # loggerの名前をbackoffからannofabapiに変更する
            logger=logger,
        )(function)(*args, **kwargs)

    return wrapped


class AnnofabApi(AbstractAnnofabApi):
    """
    Web APIに対応したメソッドが存在するクラス。

    Args:
        login_user_id: AnnofabにログインするときのユーザID
        login_password: Annofabにログインするときのパスワード
        endpoint_url: Annofab APIのエンドポイント。

    Attributes:
        token_dict: login, refresh_tokenで取得したtoken情報
        cookies: Signed Cookie情報
    """

    def __init__(self, login_user_id: str, login_password: str, endpoint_url: str = DEFAULT_ENDPOINT_URL):

        if not login_user_id or not login_password:
            raise ValueError("login_user_id or login_password is empty.")

        self.login_user_id = login_user_id
        self.login_password = login_password
        self.endpoint_url = endpoint_url
        self.url_prefix = f"{endpoint_url}/api/v1"
        self.session = requests.Session()

        #: login, refresh_tokenで取得したtoken情報
        self.token_dict: Optional[Dict[str, Any]] = None

        #: Signed Cookie情報
        self.cookies: Optional[RequestsCookieJar] = None

        self.__account_id: Optional[str] = None

    class _MyToken(AuthBase):
        """
        requestsモジュールのauthに渡す情報。
        http://docs.python-requests.org/en/master/user/advanced/#custom-authentication
        """

        def __init__(self, id_token: str):
            self.id_token = id_token

        def __call__(self, req):
            req.headers["Authorization"] = self.id_token
            return req

    #########################################
    # Private Method
    #########################################
    @staticmethod
    def _encode_query_params(query_params: Dict[str, Any]) -> Dict[str, Any]:
        """query_paramsのvalueがlist or dictのときは、JSON形式の文字列に変換する。
        `getAnnotationList` webapiで指定できる `query`などのように、2階層のquery_paramsに対応させる。

        Args:
            query_params (Dict[str,Any]): [description]

        Returns:
            Dict[str, str]: [description]
        """
        new_params = {}
        if query_params is not None:
            for key, value in query_params.items():
                if isinstance(value, (list, dict)):
                    new_params[key] = json.dumps(value)
                else:
                    new_params[key] = value
        return new_params

    def _create_kwargs(
        self,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        request_body: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        requestsモジュールのget,...メソッドに渡すkwargsを生成する。

        Returns:
            kwargs情報

        """

        # query_param
        # query_paramsのvalueがlist or dictのときは、JSON形式の文字列に変換する。
        # `getAnnotationList` webapiで指定できる `query`などのように、2階層のquery_paramsに対応させる。
        new_params = {}
        if params is not None:
            for key, value in params.items():
                if isinstance(value, (list, dict)):
                    new_params[key] = json.dumps(value)
                else:
                    new_params[key] = value

        kwargs: Dict[str, Any] = {
            "params": new_params,
            "headers": headers,
        }
        if self.token_dict is not None:
            kwargs.update({"auth": self._MyToken(self.token_dict["id_token"])})

        if request_body is not None:
            if isinstance(request_body, (dict, list)):
                kwargs.update({"json": request_body})

            elif isinstance(request_body, str):
                kwargs.update({"data": request_body.encode("utf-8")})

            else:
                kwargs.update({"data": request_body})

        return kwargs

    @staticmethod
    def _response_to_content(response: requests.Response) -> Any:
        """
        Responseのcontentを、Content-Typeに対応した型に変換する。

        Args:
            response:

        Returns:
            JSONの場合はDict, textの場合はstringのcontent

        """

        content_type = response.headers["Content-Type"]
        # `Content-Type: application/json;charset=utf-8`などcharsetが含まれている場合にも対応できるようにする。
        tokens = content_type.split(";")
        media_type = tokens[0].strip()

        if media_type == "application/json":
            content = response.json() if len(response.content) != 0 else {}

        elif media_type.find("text/") >= 0:
            content = response.text

        else:
            content = response.content

        return content

    @my_backoff
    def _execute_http_request(
        self,
        http_method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,  # pylint: disable=redefined-outer-name
        headers: Optional[Dict[str, Any]] = None,
        raise_for_status: bool = True,
        **kwargs,
    ) -> requests.Response:
        """
        Session情報を使って、HTTP Requestを投げます。Annofab WebAPIで取得したAWS S3のURLなどに、アクセスすることを想定しています。
        引数は ``requests.Session.request`` にそのまま渡します。

        Args:
            raise_for_status: Trueの場合HTTP Status Codeが4XX,5XXのときはHTTPErrorをスローします

        Returns:
            requests.Response: [description]

        Raises:
            requests.exceptions.HTTPError: http status codeが4XXX,5XXXのとき

        """
        response = self.session.request(
            method=http_method, url=url, params=params, data=data, headers=headers, json=json, **kwargs
        )

        # response.requestよりメソッド引数のrequest情報の方が分かりやすいので、メソッド引数のrequest情報を出力する。
        logger.debug(
            "Sent a request :: %s",
            {
                "requests": {
                    "http_method": http_method,
                    "url": url,
                    "query_params": _create_query_params_for_logger(params) if params is not None else None,
                    "request_body_json": _create_request_body_for_logger(json) if json is not None else None,
                    "request_body_data": _create_request_body_for_logger(data) if data is not None else None,
                    "header_params": headers,
                },
                "response": {
                    "status_code": response.status_code,
                    "content_length": len(response.content),
                },
            },
        )

        # リクエスト過多の場合、待ってから再度アクセスする
        if response.status_code == requests.codes.too_many_requests:
            retry_after_value = response.headers.get("Retry-After")
            waiting_time_seconds = (
                float(retry_after_value)
                if retry_after_value is not None
                else DEFAULT_WAITING_TIME_SECONDS_WITH_429_STATUS_CODE
            )

            logger.warning(
                "HTTPステータスコードが'%s'なので、%s秒待ってからリトライします。 :: %s",
                response.status_code,
                waiting_time_seconds,
                {
                    "response": {
                        "status_code": response.status_code,
                        "text": response.text,
                        "headers": {"Retry-After": retry_after_value},
                    },
                    "request": {
                        "http_method": http_method,
                        "url": url,
                        "query_params": _create_query_params_for_logger(params) if params is not None else None,
                    },
                },
            )

            time.sleep(float(waiting_time_seconds))
            return self._execute_http_request(
                http_method=http_method,
                url=url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                raise_for_status=raise_for_status,
                **kwargs,
            )

        # リトライが必要な場合は、backoffがリトライできるようにするため、Exceptionをスローする
        if raise_for_status or _should_retry_with_status(response.status_code):
            _log_error_response(logger, response)
            _raise_for_status(response)

        return response

    @my_backoff
    def _request_wrapper(
        self,
        http_method: str,
        url_path: str,
        *,
        query_params: Optional[Dict[str, Any]] = None,
        header_params: Optional[Dict[str, Any]] = None,
        request_body: Optional[Any] = None,
        raise_for_status: bool = True,
    ) -> Tuple[Any, requests.Response]:
        """
        Annofab WebAPIにアクセスして、レスポンスの中身とレスポンスを取得します。

        Args:
            http_method:
            url_path: Annofab WebAPIのパス（例：``/my/account``）
            query_params: クエリパラメタ
            header_params: リクエストヘッダ
            request_body: リクエストボディ
            raise_for_status: Trueの場合HTTP Status Codeが4XX,5XXのときはHTTPErrorをスローします。Falseの場合はtuple[None, Response]を返します。

        Returns:
            Tuple[content, Response]. contentはcontent_typeにより型が変わる。
            application/jsonならDict型, text/*ならばstr型, それ以外ならばbite型。

        Raises:
            HTTPError: 引数 ``raise_for_status`` がTrueで、HTTP status codeが4xxx,5xxのときにスローします。

        """

        # TODO 判定条件が不明
        if url_path.startswith("/internal/"):
            url = f"{self.endpoint_url}/api{url_path}"
        else:
            url = f"{self.url_prefix}{url_path}"

        kwargs = self._create_kwargs(query_params, header_params, request_body)
        response = self.session.request(method=http_method.lower(), url=url, **kwargs)
        # response.requestよりメソッド引数のrequest情報の方が分かりやすいので、メソッド引数のrequest情報を出力する。
        logger.debug(
            "Sent a request :: %s",
            {
                "request": {
                    "http_method": http_method.lower(),
                    "url": url,
                    "query_params": query_params,
                    "header_params": header_params,
                    "request_body": _create_request_body_for_logger(request_body) if request_body is not None else None,
                },
                "response": {
                    "status_code": response.status_code,
                    "content_length": len(response.content),
                },
            },
        )

        # Unauthorized Errorならば、ログイン後に再度実行する
        if response.status_code == requests.codes.unauthorized:
            self.login()
            return self._request_wrapper(
                http_method,
                url_path,
                query_params=query_params,
                header_params=header_params,
                request_body=request_body,
                raise_for_status=raise_for_status,
            )
        elif response.status_code == requests.codes.too_many_requests:
            retry_after_value = response.headers.get("Retry-After")
            waiting_time_seconds = (
                float(retry_after_value)
                if retry_after_value is not None
                else DEFAULT_WAITING_TIME_SECONDS_WITH_429_STATUS_CODE
            )

            logger.warning(
                "HTTPステータスコードが'%s'なので、%s秒待ってからリトライします。 :: %s",
                response.status_code,
                waiting_time_seconds,
                {
                    "response": {
                        "status_code": response.status_code,
                        "text": response.text,
                        "headers": {"Retry-After": retry_after_value},
                    },
                    "request": {
                        "http_method": http_method.lower(),
                        "url": url,
                        "query_params": query_params,
                    },
                },
            )

            time.sleep(waiting_time_seconds)
            return self._request_wrapper(
                http_method,
                url_path,
                query_params=query_params,
                header_params=header_params,
                request_body=request_body,
                raise_for_status=raise_for_status,
            )

        response.encoding = "utf-8"
        content = self._response_to_content(response)

        # リトライすべき場合はExceptionを返す
        if raise_for_status or _should_retry_with_status(response.status_code):
            _log_error_response(logger, response)
            _raise_for_status(response)

        return content, response

    def _get_signed_cookie(
        self, project_id, query_params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, Any], requests.Response]:
        """
        アノテーション仕様の履歴情報を取得するために、非公開APIにアクセスする。
        変更される可能性あり.

        Args:
            project_id: プロジェクトID

        Returns:
            Tuple[Content, Response)

        """
        url_path = f"/internal/projects/{project_id}/sign-headers"
        http_method = "GET"
        keyword_params: Dict[str, Any] = {"query_params": query_params}
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def _request_get_with_cookie(self, project_id: str, url: str) -> requests.Response:
        """
        Signed Cookie を使って、AnnofabのURLにGET requestを投げる。

        Args:
            project_id: プロジェクトID
            url: アクセス対象のURL

        Returns:
            Response

        """
        # Sessionオブジェクトに保存されているCookieを利用して、URLにアクセスする
        response = self._execute_http_request("get", url, raise_for_status=False)

        # CloudFrontから403 Errorが発生したときは、別プロジェクトのcookieを渡している可能性があるので、
        # Signed Cookieを発行して、再度リクエストを投げる
        if response.status_code == requests.codes.forbidden and response.headers.get("server") == "CloudFront":
            query_params = {}
            if "/input_data_set/" in url:
                query_params.update({"resource": "input_data_set"})
            else:
                query_params.update({"resource": "project"})

            _, r = self._get_signed_cookie(project_id, query_params=query_params)
            for cookie in r.cookies:
                self.session.cookies.set_cookie(cookie)
            response = self._execute_http_request("get", url)

        return response

    #########################################
    # Public Method : Login
    #########################################
    @my_backoff
    def login(self) -> Tuple[Dict[str, Any], requests.Response]:
        """
        ログイン



        Returns:
            Tuple[Token, requests.Response]

        """
        login_info = {"user_id": self.login_user_id, "password": self.login_password}

        url = f"{self.url_prefix}/login"

        response = self._execute_http_request("post", url, json=login_info)
        json_obj = response.json()
        self.token_dict = json_obj["token"]

        logger.debug("Logged in successfully. user_id = %s", self.login_user_id)
        return json_obj, response

    def logout(self) -> Tuple[Dict[str, Any], requests.Response]:
        """
        ログアウト
        ログインしていないときはNoneを返す。



        Returns:
            Tuple[Token, requests.Response]

        Raises:
            NotLoggedInError: ログインしてない状態で関数を呼び出したときのエラー
        """

        if self.token_dict is None:
            raise NotLoggedInError

        request_body = self.token_dict
        content, response = self._request_wrapper("POST", "/logout", request_body=request_body)
        self.token_dict = None
        return content, response

    def refresh_token(self) -> Tuple[Dict[str, Any], requests.Response]:
        """
        トークン リフレッシュ
        ログインしていないときはNoneを返す。



        Returns:
            Tuple[Token, requests.Response]

        Raises:
            NotLoggedInError: ログインしてない状態で関数を呼び出したときのエラー

        """

        if self.token_dict is None:
            raise NotLoggedInError

        request_body = {"refresh_token": self.token_dict["refresh_token"]}
        content, response = self._request_wrapper("POST", "/refresh-token", request_body=request_body)
        self.token_dict = content
        return content, response

    #########################################
    # Public Method : Other
    #########################################
    @property
    def account_id(self) -> str:
        """
        Annofabにログインするユーザのaccount_id
        """
        if self.__account_id is not None:
            return self.__account_id
        else:
            content, _ = self.get_my_account()
            account_id = content["account_id"]
            self.__account_id = account_id
            return account_id
