import functools
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import

import backoff
import requests
from requests.auth import AuthBase

import annofabapi.utils
from annofabapi.generated_api import AbstractAnnofabApi

logger = logging.getLogger(__name__)


def my_backoff(function):
    """
    HTTP Status Codeが429 or 5XXのときはリトライする. 最大5分間リトライする。
    """
    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        def fatal_code(e):
            """Too many Requests(429)のときはリトライする。それ以外の4XXはretryしない"""
            if e.response is None:
                return True
            code = e.response.status_code
            return 400 <= code < 500 and code != 429

        return backoff.on_exception(backoff.expo, requests.exceptions.RequestException, jitter=backoff.full_jitter,
                                    max_time=300, giveup=fatal_code)(function)(*args, **kwargs)

    return wrapped


class AnnofabApi(AbstractAnnofabApi):
    """
    Web APIに対応したメソッドが存在するクラス。

    Args:
        login_user_id: AnnoFabにログインするときのユーザID
        login_password: AnnoFabにログインするときのパスワード

    """
    def __init__(self, login_user_id: str, login_password: str):

        if not login_user_id or not login_password:
            raise ValueError("login_user_id or login_password is empty.")

        self.login_user_id = login_user_id
        self.login_password = login_password

        self.session = requests.Session()

    #: アクセスするURL
    URL_PREFIX = "https://annofab.com/api/v1"

    #: login, refresh_tokenで取得したtoken情報
    token_dict: Optional[Dict[str, Any]] = None

    class __MyToken(AuthBase):
        """
        requestsモジュールのauthに渡す情報。
        http://docs.python-requests.org/en/master/user/advanced/#custom-authentication
        """
        def __init__(self, id_token: str):
            self.id_token = id_token

        def __call__(self, req):
            req.headers['Authorization'] = self.id_token
            return req

    #########################################
    # Private Method
    #########################################
    def _create_kwargs(self, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None,
                       request_body: Optional[Any] = None) -> Dict[str, Any]:
        """
        requestsモジュールのget,...メソッドに渡すkwargsを生成する。
        Args:
            params: クエリパラメタに設定する情報
            headers: リクエストヘッダに設定する情報

        Returns:
            kwargs情報

        """

        # query_param
        new_params = {}
        if params is not None:
            for key, value in params.items():
                if isinstance(value, (list, dict)):
                    new_params[key] = json.dumps(value)
                else:
                    new_params[key] = value

        kwargs: Dict[str, Any] = {
            'params': new_params,
            'headers': headers,
        }
        if self.token_dict is not None:
            kwargs.update({'auth': self.__MyToken(self.token_dict['id_token'])})

        if request_body is not None:
            if isinstance(request_body, (dict, list)):
                kwargs.update({'json': request_body})

            elif isinstance(request_body, str):
                kwargs.update({'data': request_body.encode("utf-8")})

            else:
                kwargs.update({'data': request_body})

        return kwargs

    @staticmethod
    def _response_to_content(response: requests.Response) -> Any:
        """
        Reponseのcontentを、Content-Typeに対応した型に変換する。

        Args:
            response:

        Returns:
            JSONの場合はDict, textの場合はstringのcontent

        """

        content_type = response.headers['Content-Type']
        if content_type == 'application/json':
            content = response.json() if len(response.content) != 0 else {}

        elif content_type.find('text/') >= 0:
            content = response.text

        else:
            content = response.content

        return content

    @my_backoff
    def _request_wrapper(self, http_method: str, url_path: str, query_params: Optional[Dict[str, Any]] = None,
                         header_params: Optional[Dict[str, Any]] = None,
                         request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:
        """
        HTTP　Requestを投げて、Reponseを返す。

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

        url = f'{self.URL_PREFIX}{url_path}'
        kwargs = self._create_kwargs(query_params, header_params, request_body)

        # HTTP Requestを投げる
        response = getattr(self.session, http_method.lower())(url, **kwargs)

        # Unauthorized Errorならば、ログイン後に再度実行する
        if response.status_code == requests.codes.unauthorized:
            self.login()
            return self._request_wrapper(http_method, url_path, query_params, header_params, request_body)

        annofabapi.utils.log_error_response(logger, response)

        response.encoding = 'utf-8'
        annofabapi.utils.raise_for_status(response)

        content = self._response_to_content(response)
        return content, response

    def _get_signed_cookie(self, project_id):
        """
        アノテーション仕様の履歴情報を取得するために、非公開APIにアクセスする。
        変更される可能性あり.

        .. deprecated:: X

        Args:
            project_id: プロジェクトID

        Returns:
            Tuple[Content, Reponse)

        """
        url_path = f'/private/projects/{project_id}/sign-headers'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {}
        return self._request_wrapper(http_method, url_path, **keyword_params)

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
        login_info = {'user_id': self.login_user_id, 'password': self.login_password}

        url = f"{self.URL_PREFIX}/login"
        response = self.session.post(url, json=login_info)
        annofabapi.utils.raise_for_status(response)

        json_obj = response.json()
        self.token_dict = json_obj["token"]

        logger.debug("Logined successfully. user_id = %s", self.login_user_id)
        return json_obj, response

    def logout(self) -> Optional[Tuple[Dict[str, Any], requests.Response]]:
        """
        ログアウト
        ログインしていないときはNoneを返す。



        Returns:
            Tuple[Token, requests.Response]. ログインしていないときはNone.

        """

        if self.token_dict is None:
            logger.info("You are not logged in.")
            return None

        request_body = self.token_dict
        content, response = self._request_wrapper('POST', '/logout', request_body=request_body)
        self.token_dict = None
        return content, response

    def refresh_token(self) -> Optional[Tuple[Dict[str, Any], requests.Response]]:
        """
        トークン リフレッシュ
        ログインしていないときはNoneを返す。



        Returns:
            Tuple[Token, requests.Response]. ログインしていないときはNone.
        """

        if self.token_dict is None:
            logger.info("You are not logged in.")
            return None

        request_body = {'refresh_token': self.token_dict['refresh_token']}
        content, response = self._request_wrapper('POST', '/refresh-token', request_body=request_body)
        self.token_dict = content
        return content, response

    #########################################
    # Public Method : 労務関係API (将来的に大きく変更される可能性があります）
    # 労務管理がりようできる組織は限られています。利用する場合は、AnnoFabにお問い合わせください。
    #########################################
    def get_labor_control(self, query_params: Optional[Dict[str, Any]] = None) -> Tuple[Any, requests.Response]:
        """労務管理関連データを一括で取得します。


        Args:
            query_params: Query Parameters

        Returns:
            Tuple[Task, requests.Response]


        """
        url_path = f'/labor-control'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def put_labor_control(self, request_body: Dict[str, Any]) -> Tuple[Any, requests.Response]:
        """労務管理関連データを更新します。


        Args:
            request_body: Request Body

        Returns:
            Tuple[Task, requests.Response]


        """
        url_path = f'/labor-control'
        http_method = 'PUT'
        keyword_params: Dict[str, Any] = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def delete_labor_control(self, data_id: str) -> Tuple[Any, requests.Response]:
        """労務管理関連データを削除します。


        Args:
            data_id: 削除したい労務管理関連データID。

        Returns:
            Tuple[Task, None]


        """
        url_path = f'/labor-control/{data_id}'
        http_method = 'DELETE'
        keyword_params: Dict[str, Any] = {}
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def _get_annotations_for_annotation_editor(self, project_id: str, task_id: str,
                                               input_data_id: str) -> Tuple[Any, requests.Response]:
        """【エディタ用】タスク/入力データのアノテーション一括取得

        このAPIが返すアノテーションは、エディタ用です。 機械学習などで利用する成果物としてのアノテーションを取得するには、以下をご利用いただけます。
        * getAnnotation: 特定のタスク - 入力データのアノテーション取得
        * getAnnotationArchive: プロジェクト全体のアノテーション（ZIP）

        Notes:
            非公開のAPIのため、メソッド仕様が変わる可能性があります。

        Args:
            project_id:
            task_id:
            input_data_id:

        Returns:
            Tuple[Annotation, requests.Response]

        """
        url_path = f'/projects/{project_id}/tasks/{task_id}/inputs/{input_data_id}/annotation'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {}
        return self._request_wrapper(http_method, url_path, **keyword_params)
