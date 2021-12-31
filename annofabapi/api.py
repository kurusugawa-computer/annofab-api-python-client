import json
import logging
import warnings
from typing import Any, Dict, Optional, Tuple

import requests
from requests.auth import AuthBase
from requests.cookies import RequestsCookieJar

from annofabapi.exceptions import NotLoggedInError
from annofabapi.generated_api import AbstractAnnofabApi
from annofabapi.utils import _log_error_response, _mask_confidential_info, _raise_for_status, my_backoff

logger = logging.getLogger(__name__)

DEFAULT_ENDPOINT_URL = "https://annofab.com"
"""AnnoFab WebAPIのデフォルトのエンドポイントURL"""


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

    def _execute_http_request(
        self,
        http_method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Session情報を使って、HTTP Requestを投げる。
        引数は `requests.Session.request <https://docs.python-requests.org/en/latest/api/#requests.Session.request>`_ 関数に加工せずにそのまま渡す。

        Returns:
            requests.Response: [description]

        Raises:
            requests.exceptions.HTTPError: http status codeが4XXX,5XXXのとき

        """

        @my_backoff
        def execute():
            logger.debug(
                "Sending a request :: %s",
                {
                    "http_method": http_method,
                    "url": url,
                    "query_params": params,
                    "request_body_json": _mask_confidential_info(json),
                    "request_body_data": _mask_confidential_info(data),
                    "header_params": headers,
                },
            )

            response = self.session.request(
                method=http_method, url=url, params=params, data=data, headers=headers, json=json, **kwargs
            )
            _raise_for_status(response)
            return response

        # 数回retryしてもリクエストが成功しない場合は、リクエスト情報を出力する。
        try:
            response = execute()
        except requests.exceptions.HTTPError as e:
            response = e.response
            _log_error_response(logger, response)
            raise e
        return response



    @my_backoff
    def __request_wrapper2(
        self,
        http_method: str,
        url_path: str,
        query_params: Optional[dict[str, Any]] = None,
        header_params: Optional[dict[str, Any]] = None,
        request_body: Optional[Any] = None,
    ) -> Any:
        """
        HTTP Requestを投げて、Responseを返す。
        Args:
            http_method:
            url_path:
            query_params:
            header_params:
            request_body:
        Returns:
            responseの中身。content_typeにより型が変わる。
            application/jsonならdict型, text/*ならばstr型, それ以外ならばbite型。
        """
        url = f"{self.base_url}{url_path}"

        kwargs = self._create_kwargs(query_params, header_params, request_body)

        masked_request_body = copy.deepcopy(request_body)
        if masked_request_body is not None:
            _mask_password(masked_request_body)
        # HTTP Requestを投げる
        logger.debug(
            "Sending a request :: %s",
            {
                "http_method": http_method,
                "url": url,
                "query_params": query_params,
                "header_params": header_params,
                "request_body": masked_request_body,
            },
        )
        response = getattr(self.session, http_method.lower())(url, **kwargs)

        # Unauthorized Errorならば、ログイン後に再度実行する
        if response.status_code == requests.codes.unauthorized:
            self.login()
            return self._request_wrapper(http_method, url_path, query_params, header_params, request_body)

        _log_error_response(logger, response)

        response.encoding = "utf-8"
        _raise_for_status(response)

        content = self._response_to_content(response)
        return content




    def _request_wrapper(
        self,
        http_method: str,
        url_path: str,
        query_params: Optional[Dict[str, Any]] = None,
        header_params: Optional[Dict[str, Any]] = None,
        request_body: Optional[Any] = None,
    ) -> Tuple[Any, requests.Response]:
        """
        HTTP Requestを投げて、Responseを返す。

        Args:
            http_method:
            url_path:
            query_params:
            header_params:
            request_body:

        Returns:
            Tuple[content, Response]. contentはcontent_typeにより型が変わる。
            application/jsonならDict型, text/*ならばstr型, それ以外ならばbite型。

        """
        if url_path.startswith("/labor-control") or url_path.startswith("/internal/"):
            url = f"{self.endpoint_url}/api{url_path}"
        else:
            url = f"{self.url_prefix}{url_path}"

        kwargs = self._create_kwargs(query_params, header_params, request_body)
        if self.token_dict is not None:
            kwargs.update({"auth": self._MyToken(self.token_dict["id_token"])})

        try:
            response = self._execute_http_request(http_method.lower(), url, **kwargs)
        except requests.exceptions.HTTPError as e:
            # Unauthorized Errorならば、ログイン後に再度実行する
            if e.response.status_code == requests.codes.unauthorized:
                self.login()
                kwargs.update({"auth": self._MyToken(self.token_dict["id_token"])})
                response = self._execute_http_request(http_method.lower(), url, **kwargs)
            else:
                raise e

        response.encoding = "utf-8"
        content = self._response_to_content(response)
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
        logger.debug(
            "Sending a request :: %s",
            {
                "http_method": "get",
                "url": url,
            },
        )
        response = self._execute_http_request("get",url)

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
            response = self._execute_http_request("get",url)

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
