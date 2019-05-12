import functools
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import backoff
import requests

import annofabapi.utils
from annofabapi.exceptions import AnnofabApiException

logger = logging.getLogger(__name__)


def my_backoff(function):
    """
    HTTP Status Codeが429 or 5XXのときはリトライする. 最大5分間リトライする。
    """

    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        def fatal_code(e):
            """Too many Request以外の4XXはretryしない"""
            code = e.response.status_code
            return code != 429 and code < 500

        return backoff.on_exception(backoff.expo,
                                    requests.exceptions.RequestException,
                                    jitter=backoff.full_jitter,
                                    max_time=300,
                                    giveup=fatal_code)(function)(*args,
                                                                 **kwargs)

    return wrapped


class AnnofabApiMixin:
    """
    AnnofabApiのmixinクラス。
    OpenAPI Generatorで生成される部分と、そうでない部分を分けるため、mixinクラスを作成した。
    """

    def __init__(self, login_user_id: str, login_password: str):
        """
        Args:
            login_user_id: AnnoFabにログインするときのユーザID
            login_password: AnnoFabにログインするときのパスワード
        """

        if not login_user_id or not login_password:
            raise ValueError("login_user_id or login_password is empty.")

        self.login_user_id = login_user_id
        self.login_password = login_password

        self.session = requests.Session()

    #: アクセスするURL
    URL_PREFIX = "https://annofab.com/api/v1"

    #: login, refresh_tokenで取得したtoken情報
    token_dict: Optional[Dict[str, Any]] = None

    class __MyToken:
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
    def _create_kwargs(self,
                       params: Optional[Dict[str, Any]] = None,
                       headers: Optional[Dict[str, Any]] = None
                       ) -> Dict[str, Any]:
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
                if type(value) in [list, dict]:
                    new_params[key] = json.dumps(value)
                else:
                    new_params[key] = value

        kwargs: Dict[str, Any] = {
            'params': new_params,
            'headers': headers,
        }
        if self.token_dict is not None:
            kwargs.update(
                {'auth': self.__MyToken(self.token_dict['id_token'])})

        return kwargs

    @my_backoff
    def _request_wrapper(self,
                         http_method: str,
                         url_path: str,
                         query_params: Optional[Dict[str, Any]] = None,
                         header_params: Optional[Dict[str, Any]] = None,
                         request_body: Optional[Any] = None
                         ) -> Tuple[Any, requests.Response]:
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

        def execute_request():
            if http_method == 'GET':
                return self.session.get(url, **kwargs)

            elif http_method == 'DELETE':
                return self.session.delete(url, **kwargs)

            elif http_method == 'PUT':
                return self.session.put(url, **kwargs)

            elif http_method == 'POST':
                return self.session.post(url, **kwargs)

            elif http_method == 'OPTIONS':
                return self.session.options(url, **kwargs)

            elif http_method == 'HEAD':
                return self.session.head(url, **kwargs)

            else:
                raise AnnofabApiException(
                    f"HTTP Method '{http_method}' is not supported")

        url = f'{self.URL_PREFIX}{url_path}'
        kwargs = self._create_kwargs(query_params, header_params)
        if request_body is not None:
            if type(request_body) == dict or type(request_body) == list:
                kwargs.update({'json': request_body})

            elif type(request_body) == str:
                kwargs.update({'data': request_body.encode("utf-8")})

            else:
                kwargs.update({'data': request_body})

        # HTTP Requestを投げる
        response = execute_request()

        # Unauthorized Errorならば、ログイン後に再度実行する
        if response.status_code == requests.codes.unauthorized:
            logger.debug(response.text)
            self.login()
            return self._request_wrapper(http_method, url_path, query_params,
                                         header_params, request_body)

        annofabapi.utils.log_error_response(logger, response)

        response.encoding = 'utf-8'
        response.raise_for_status()

        content_type = response.headers['Content-Type']
        if content_type == 'application/json':
            content = response.json() if len(response.content) != 0 else {}

        elif content_type.find('text/') >= 0:
            content = response.text

        else:
            content = response.content

        return content, response

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
        login_info = {
            'user_id': self.login_user_id,
            'password': self.login_password
        }

        url = f"{self.URL_PREFIX}/login"
        response = self.session.post(url, json=login_info)
        response.raise_for_status()

        json_obj = response.json()
        self.token_dict = json_obj["token"]
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
        content, response = self._request_wrapper('POST',
                                                  '/logout',
                                                  request_body=request_body)
        self.token_dict = None
        return content, response

    def refresh_token(self
                      ) -> Optional[Tuple[Dict[str, Any], requests.Response]]:
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
        content, response = self._request_wrapper('POST',
                                                  '/refresh-token',
                                                  request_body=request_body)
        self.token_dict = content
        return content, response
