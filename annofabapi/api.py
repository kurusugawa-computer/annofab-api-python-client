import json
import logging
import warnings
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
"""AnnoFab WebAPIのデフォルトのエンドポイントURL"""


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
            try:
                dict_request_body = json.loads(request_body)
            except JSONDecodeError:
                request_body_for_logger = request_body
            else:
                request_body_for_logger = _create_request_body_for_logger(dict_request_body)
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


def _should_retry_with_status(status_code: int) -> bool:
    """HTTP Status Codeからリトライすべきかどうかを返す。"""
    if status_code == 429:
        return True
    elif 500 <= status_code < 600:
        return True
    else:
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
            (requests.exceptions.RequestException, ConnectionError),
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
        login_user_id: AnnoFabにログインするときのユーザID
        login_password: AnnoFabにログインするときのパスワード
        endpoint_url: AnnoFab APIのエンドポイント。

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
        """Session情報を使って、HTTP Requestを投げる。
        引数は ``requests.Session.request`` にそのまま渡す。

        Args:
            raise_for_status: Trueの場合HTTP Status Codeが4XX,5XXのときはHTTPErrorをスローします

        Returns:
            requests.Response: [description]

        Raises:
            requests.exceptions.HTTPError: http status codeが4XXX,5XXXのとき

        """

        logger.debug(
            "Sending a request :: %s",
            {
                "http_method": http_method,
                "url": url,
                "query_params": params,
                "request_body_json": _create_request_body_for_logger(json),
                "request_body_data": _create_request_body_for_logger(data),
                "header_params": headers,
            },
        )

        response = self.session.request(
            method=http_method, url=url, params=params, data=data, headers=headers, json=json, **kwargs
        )

        # リトライすべき場合はExceptionを返す
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
        HTTP Requestを投げて、Responseを返す。

        Args:
            http_method:
            url_path:
            query_params:
            header_params:
            request_body:
            raise_for_status: Trueの場合HTTP Status Codeが4XX,5XXのときはHTTPErrorをスローします。Falseの場合はtuple[None, Response]を返します。

        Returns:
            Tuple[content, Response]. contentはcontent_typeにより型が変わる。
            application/jsonならDict型, text/*ならばstr型, それ以外ならばbite型。

        Raises:
            HTTPError: 引数 ``raise_for_status`` がTrueで、HTTP status codeが4xxx,5xxのときにスローします。

        """
        if url_path.startswith("/labor-control") or url_path.startswith("/internal/"):
            url = f"{self.endpoint_url}/api{url_path}"
        else:
            url = f"{self.url_prefix}{url_path}"

        kwargs = self._create_kwargs(query_params, header_params, request_body)

        # HTTP Requestを投げる
        logger.debug(
            "Sending a request :: %s",
            {
                "http_method": http_method.lower(),
                "url": url,
                "query_params": query_params,
                "header_params": header_params,
                "request_body": _create_request_body_for_logger(request_body) if request_body is not None else None,
            },
        )
        response = self.session.request(method=http_method.lower(), url=url, **kwargs)

        # Unauthorized Errorならば、ログイン後に再度実行する
        if response.status_code == requests.codes.unauthorized:
            self.login()
            return self._request_wrapper(
                http_method,
                url_path,
                query_params=query_params,
                header_params=query_params,
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
        Signed Cookie を使って、AnnoFabのURLにGET requestを投げる。

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
    # Public Method : 労務関係API (将来的に大きく変更される可能性があります）
    # 労務管理がりようできる組織は限られています。利用する場合は、AnnoFabにお問い合わせください。
    #########################################
    def get_labor_control(self, query_params: Optional[Dict[str, Any]] = None) -> Tuple[Any, requests.Response]:
        """労務管理関連データを一括で取得します。

        .. deprecated:: 2022-02-01 以降に削除する予定です

        Args:
            query_params: Query Parameters

        Returns:
            Tuple[Task, requests.Response]


        """
        warnings.warn(
            "annofabapi.AnnofabApi.get_labor_control() is deprecated and will be removed.", FutureWarning, stacklevel=2
        )
        url_path = "/labor-control"
        http_method = "GET"
        keyword_params: Dict[str, Any] = {
            "query_params": query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def put_labor_control(self, request_body: Dict[str, Any]) -> Tuple[Any, requests.Response]:
        """労務管理関連データを更新します。


        Args:
            request_body: Request Body

        Returns:
            Tuple[Task, requests.Response]


        """
        url_path = "/labor-control"
        http_method = "PUT"
        keyword_params: Dict[str, Any] = {
            "request_body": request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def delete_labor_control(self, data_id: str) -> Tuple[Any, requests.Response]:
        """労務管理関連データを削除します。


        Args:
            data_id: 削除したい労務管理関連データID。

        Returns:
            Tuple[Task, None]


        """
        url_path = f"/labor-control/{data_id}"
        http_method = "DELETE"
        keyword_params: Dict[str, Any] = {}
        return self._request_wrapper(http_method, url_path, **keyword_params)

    #########################################
    # Public Method : Other
    #########################################
    @property
    def account_id(self) -> str:
        """
        AnnoFabにログインするユーザのaccount_id
        """
        if self.__account_id is not None:
            return self.__account_id
        else:
            content, _ = self.get_my_account()
            account_id = content["account_id"]
            self.__account_id = account_id
            return account_id
