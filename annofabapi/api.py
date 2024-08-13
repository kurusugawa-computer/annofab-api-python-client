import copy
import json
import logging
import time
from functools import wraps
from json import JSONDecodeError
from typing import Any, Callable, Collection, Dict, Optional, Tuple

import backoff
import requests
from requests.auth import AuthBase
from requests.cookies import RequestsCookieJar

from annofabapi.exceptions import InvalidMfaCodeError, MfaEnabledUserExecutionError, NotLoggedInError
from annofabapi.generated_api import AbstractAnnofabApi

logger = logging.getLogger(__name__)

DEFAULT_ENDPOINT_URL = "https://annofab.com"
"""Annofab WebAPIのデフォルトのエンドポイントURL"""

DEFAULT_WAITING_TIME_SECONDS_WITH_429_STATUS_CODE = 300
"""HTTP Status Codeが429のときの、デフォルト（Retry-Afterヘッダがないとき）の待ち時間です。"""


def _read_mfa_code_from_stdin() -> str:
    """標準入力からMFAコードを読み込みます。"""
    inputted_mfa_code = ""
    while inputted_mfa_code == "":
        inputted_mfa_code = input("Enter Annofab MFA Code: ")
    return inputted_mfa_code


def _mask_senritive_value_for_dict(data: Dict[str, Any], keys: Collection[str]) -> Dict[str, Any]:
    """
    dictに含まれているセンシティブな情報を"***"でマスクします。

    Args:
        data: マスク対象のdict
        keys: マスク対象の複数のkey

    Returns:
        センシティブな情報がマスクされたdict。
        1つ以上の値をマスクした場合は、複製されたdictが返ります。
        1つもマスクしていない場合は、引数`data`そのものが返ります。

    """
    MASKED_VALUE = "***"
    diff_keys = set(keys) - set(data.keys())
    if len(diff_keys) == len(keys):
        # マスク対象のキーがない
        return data

    copied_data = copy.deepcopy(data)
    for key in keys:
        if key in copied_data:
            copied_data[key] = MASKED_VALUE

    return copied_data


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

    def mask_str_rquest_body(str_request_body: str) -> Any:  # noqa: ANN401
        """
        文字列型であるrequest_bodyがJSON形式だとみなして、センシティブな情報をマスクします。
        """
        try:
            # JSON文字列だとみなして、Pythonオブジェクトへの変換を試みる
            json_request_body = json.loads(str_request_body)
        except JSONDecodeError:
            return str_request_body

        return _create_request_body_for_logger(json_request_body)

    if 400 <= response.status_code < 600:
        # logにAuthorizationを出力しないようにマスクする
        headers_for_logger = _mask_senritive_value_for_dict(dict(response.request.headers), {"Authorization"})

        # request_bodyのpassword関係をマスクして、logに出力する
        request_body_for_logger: Optional[Any] = None
        if isinstance(response.request.body, bytes):
            try:
                # 文字列への変換を試みる
                str_request_body = response.request.body.decode()
                request_body_for_logger = mask_str_rquest_body(str_request_body)
            except UnicodeError:
                request_body_for_logger = response.request.body

        elif isinstance(response.request.body, str):
            request_body_for_logger = mask_str_rquest_body(response.request.body)

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
                    "headers": headers_for_logger,
                },
            },
        )


def _create_request_body_for_logger(data: Any) -> Any:  # noqa: ANN401
    """
    ログに出力するためのreqest_bodyを生成する。
     * パスワードやトークンなどの機密情報をマスクする
     * bytes型の場合は `(bytes)`と記載する。


    Args:
        data: request_body

    Returns:
        ログ出力用のrequest_body
    """
    if not isinstance(data, dict):
        return data
    elif isinstance(data, bytes):
        # bytes型のときは値を出力しても意味がないので、bytesであることが分かるようにする
        return "(bytes)"

    return _mask_senritive_value_for_dict(
        data, keys={"password", "old_password", "new_password", "id_token", "refresh_token", "access_token", "session", "mfa_code"}
    )


def _create_query_params_for_logger(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    ログに出力するためのquery_paramsを生成する。
     * AWS関係のcredential情報をマスクする。

    Args:
        params: query_params

    Returns:
        ログ出力用のparams
    """
    return _mask_senritive_value_for_dict(params, keys={"X-Amz-Security-Token", "X-Amz-Credential"})


def _should_retry_with_status(status_code: int) -> bool:
    """
    HTTP Status Codeからリトライすべきかどうかを返す。
    """
    # 注意：429(Too many requests)の場合は、backoffモジュール外でリトライするため、このメソッドでは判定しない
    if status_code == requests.codes.not_implemented:
        return False
    if 500 <= status_code < 600:  # noqa: SIM103
        return True
    return False


def my_backoff(function) -> Callable:  # noqa: ANN001
    """
    HTTP Status Codeが429 or 5XXのときはリトライする. 最大5分間リトライする。
    """

    @wraps(function)
    def wrapped(*args, **kwargs):  # noqa: ANN202
        def fatal_code(e):  # noqa: ANN001, ANN202
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
        input_mfa_code_via_stdin: MFAコードを標準入力から入力するかどうか

    Attributes:
        token_dict: login, refresh_tokenで取得したtoken情報
        cookies: Signed Cookie情報
    """

    def __init__(
        self, login_user_id: str, login_password: str, *, endpoint_url: str = DEFAULT_ENDPOINT_URL, input_mfa_code_via_stdin: bool = False
    ) -> None:
        if not login_user_id or not login_password:
            raise ValueError("login_user_id or login_password is empty.")

        self.login_user_id = login_user_id
        self.login_password = login_password
        self.endpoint_url = endpoint_url
        self.input_mfa_code_via_stdin = input_mfa_code_via_stdin
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

        def __init__(self, id_token: str) -> None:
            self.id_token = id_token

        def __call__(self, req):  # noqa: ANN001, ANN204
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
        request_body: Optional[Any] = None,  # noqa: ANN401
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
    def _response_to_content(response: requests.Response) -> Any:  # noqa: ANN401
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
        data: Optional[Any] = None,  # noqa: ANN401
        json: Optional[Any] = None,  # pylint: disable=redefined-outer-name  # noqa: ANN401
        headers: Optional[Dict[str, Any]] = None,
        stream: bool = False,
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
        response = self.session.request(method=http_method, url=url, params=params, data=data, headers=headers, json=json, stream=stream, **kwargs)
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
                "response": {"status_code": response.status_code, "headers": {"Content-Length": response.headers.get("Content-Length")}},
            },
        )
        # リクエスト過多の場合、待ってから再度アクセスする
        if response.status_code == requests.codes.too_many_requests:
            retry_after_value = response.headers.get("Retry-After")
            waiting_time_seconds = float(retry_after_value) if retry_after_value is not None else DEFAULT_WAITING_TIME_SECONDS_WITH_429_STATUS_CODE

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
                stream=stream,
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
        request_body: Optional[Any] = None,  # noqa: ANN401
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
                "response": {"status_code": response.status_code, "headers": {"Content-Length": response.headers.get("Content-Length")}},
            },
        )

        # Unauthorized Errorならば、ログイン後に再度実行する
        if response.status_code == requests.codes.unauthorized:
            self.refresh_token()
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
            waiting_time_seconds = float(retry_after_value) if retry_after_value is not None else DEFAULT_WAITING_TIME_SECONDS_WITH_429_STATUS_CODE

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

    def _get_signed_cookie(self, project_id, query_params: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], requests.Response]:  # noqa: ANN001
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
    def _login_respond_to_auth_challenge(self, mfa_code: str, session: str) -> Dict[str, Any]:
        """
        MFAコードによるログインを実行します。

        ``self.input_mfa_code_via_stdin`` が ``True`` AND ``mfa_code`` が正しくない場合は、標準入力から再度MFAコードの入力を求めます。

        Args:
            mfa_code: MFAコード
            session: `login` APIのレスポンスに格納されている`session`

        Raises:
            InvalidMfaCodeError: ``self.input_mfa_code_via_stdin`` が ``False`` AND ``mfa_code`` が正しくない場合
        """
        request_body = {"user_id": self.login_user_id, "mfa_code": mfa_code, "session": session}
        url = f"{self.url_prefix}/login-respond-to-auth-challenge"

        response = self._execute_http_request("post", url, json=request_body, raise_for_status=False)

        json_obj = response.json()
        # MFAコードが間違っているかどうかの判定が、メッセージでしかできなかったので、暫定的にメッセージで判定する
        if response.status_code == requests.codes.bad_request:
            assert len(json_obj["errors"]) > 0
            error_message = json_obj["errors"][0]["message"]
            if error_message in {"検証コードが間違っています", "検証コードの期限が切れています"}:
                # 分かりやすいメッセージにするため「検証コード」を「MFAコード」に置き換える
                new_error_message = error_message.replace("検証コード", "MFAコード")
                if self.input_mfa_code_via_stdin:
                    logger.info(new_error_message)
                    new_mfa_code = _read_mfa_code_from_stdin()
                    return self._login_respond_to_auth_challenge(new_mfa_code, session)
                else:
                    raise InvalidMfaCodeError(new_error_message)

        _log_error_response(logger, response)
        _raise_for_status(response)
        return response.json()

    def login(self, mfa_code: Optional[str] = None) -> None:
        """
        ログインして、トークンをインスタンスに保持します。
        MFAが有効化されている場合は、loginRespondToAuthChallenge APIを実行してトークンを取得します。

        ``self.input_mfa_code_via_stdin == True`` の場合は、標準入力からMFAコードの入力を求めます。


        Args:
            mfa_code: ``loginRespondToAuthChallenge``のレスポンスから取得したMFAコード。この引数はexperimentalです。将来削除される可能性があります。

        Returns:
            Tuple[Token, requests.Response]

        Raises:
            InvalidMfaCodeError: ``self.input_mfa_code_via_stdin`` が ``False`` AND ``mfa_code`` が正しくない場合
            MfaEnabledUserExecutionError: ``self.input_mfa_code_via_stdin`` が ``False`` AND ``mfa_code`` が未指定の場合
        """
        login_info = {"user_id": self.login_user_id, "password": self.login_password}

        url = f"{self.url_prefix}/login"

        login_response = self._execute_http_request("post", url, json=login_info)
        login_json_obj = login_response.json()
        if "token" not in login_json_obj:
            # `login` APIのレスポンスのスキーマがLoginNeedChallengeResponseのとき
            if mfa_code is None:
                if self.input_mfa_code_via_stdin:
                    mfa_code = _read_mfa_code_from_stdin()
                else:
                    raise MfaEnabledUserExecutionError(self.login_user_id)

            mfa_json_obj = self._login_respond_to_auth_challenge(mfa_code, login_json_obj["session"])
            token_dict = mfa_json_obj["token"]
        else:
            # `login` APIのレスポンスのスキーマがloginRespondToAuthChallengeのとき
            token_dict = login_json_obj["token"]

        self.token_dict = token_dict
        logger.debug("Logged in successfully. user_id = %s", self.login_user_id)

    def logout(self) -> None:
        """
        ログアウトします。
        ログアウト後は、インスタンス変数 ``token_dict`` をNoneにします。



        Returns:
            Tuple[Token, requests.Response]

        Raises:
            NotLoggedInError: ログインしてない状態で関数を呼び出したときのエラー
        """

        if self.token_dict is None:
            raise NotLoggedInError

        request_body = self.token_dict
        url = f"{self.url_prefix}/logout"
        self._execute_http_request("POST", url, json=request_body)
        self.token_dict = None

    def refresh_token(self) -> None:
        """
        トークンを再発行して、新しいトークン情報をインスタンスに保持します。
        ログインしていない場合やリフレッシュトークンの有効期限が切れている場合は、login APIを実行して新しいトークン情報をインスタンスに保持します。

        """

        if self.token_dict is None:
            # 一度もログインしていないときは、login APIを実行して、トークン情報をインスタンスに保持する（login関数内でインスタンスに保持している）
            self.login()
            return

        request_body = {"refresh_token": self.token_dict["refresh_token"]}
        url = f"{self.url_prefix}/refresh-token"
        response = self._execute_http_request("POST", url, json=request_body)

        # Unauthorized Errorならば、login APIを実行して、取得したトークン情報をインスタンスに保持する
        if response.status_code == requests.codes.unauthorized:
            self.login()
            return

        self.token_dict = response.json()

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
