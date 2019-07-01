import functools
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import

import backoff
import requests
from requests.auth import AuthBase

import annofabapi.utils
from annofabapi.api import AnnofabApi
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

        return backoff.on_exception(backoff.expo,
                                    requests.exceptions.RequestException,
                                    jitter=backoff.full_jitter,
                                    max_time=300,
                                    giveup=fatal_code)(function)(*args,
                                                                 **kwargs)

    return wrapped


class AnnofabApi2:
    """
    Web APIに対応したメソッドが存在するクラス。
    """

    def __init__(self, api: AnnofabApi):
        """


        """

        self.api = api

    #: アクセスするURL
    URL_PREFIX = "https://annofab.com/api/v2"

    cookies: Optional[Dict[str, Any]] = None

    #########################################
    # Private Method
    #########################################
    class __NoAuth(AuthBase):
        """
        netrcの有無にかかわらず、authorizationヘッダを空にする
        http://docs.python-requests.org/en/master/user/advanced/#custom-authentication
        """

        def __call__(self, req):
            req.headers['Authorization'] = None
            return req

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

        url = f'{self.URL_PREFIX}{url_path}'
        kwargs = self.api._create_kwargs(query_params, header_params)

        if url_path != "/sign-url":
            kwargs.update({"cookies": self.cookies})
            kwargs.pop("auth", self.__NoAuth())

        # HTTP Requestを投げる
        response = getattr(self.api.session, http_method.lower())(url,
                                                                  **kwargs)

        # Unauthorized Errorならば、ログイン後に再度実行する
        if response.status_code == requests.codes.unauthorized:
            self.api.login()
            return self._request_wrapper(http_method, url_path, query_params,
                                         header_params, request_body)

        annofabapi.utils.log_error_response(logger, response)

        response.encoding = 'utf-8'
        response.raise_for_status()

        content = self.api._response_to_content(response)
        return content, response

    #########################################
    # Public Method : Cache
    #########################################
    def get_signed_access_v2(self, query_params):
        """
        """

        url_path = f'/sign-url'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }

        content, response = self._request_wrapper(http_method, url_path,
                                                  **keyword_params)
        self.cookies = content
        return content, response

    def get_project_cache_v2(
            self, project_id: str
    ) -> Optional[Tuple[Dict[str, Any], requests.Response]]:

        url_path = f'/projects/{project_id}/cache'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {}
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_task_statistics_v2(
            self, project_id: str
    ) -> Optional[Tuple[Dict[str, Any], requests.Response]]:

        url_path = f'/projects/{project_id}/statistics/tasks'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {}
        return self._request_wrapper(http_method, url_path, **keyword_params)
