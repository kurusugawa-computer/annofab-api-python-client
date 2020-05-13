import logging
from typing import Any, Dict, Optional, Tuple

import requests
from requests.cookies import RequestsCookieJar

import annofabapi.utils
from annofabapi.api import AnnofabApi
from annofabapi.generated_api2 import AbstractAnnofabApi2
from annofabapi.utils import _log_error_response, _raise_for_status

logger = logging.getLogger(__name__)


class AnnofabApi2(AbstractAnnofabApi2):
    """
    Web API v2に対応したメソッドが存在するクラス。

    Note:
        開発途上版のため、互換性のない変更がある可能性があります。

    Args:
        api: API v1のインスタンス（一部のAPIは、v1のログインメソッドを利用するため）

    """

    def __init__(self, api: AnnofabApi):
        self.api = api
        self.url_prefix = f"{api.endpoint_url}/api/v2"

    #: Signed Cookie情報
    cookies: Optional[RequestsCookieJar] = None

    #########################################
    # Private Method
    #########################################

    @annofabapi.api.my_backoff
    def _request_wrapper(
        self,
        http_method: str,
        url_path: str,
        query_params: Optional[Dict[str, Any]] = None,
        header_params: Optional[Dict[str, Any]] = None,
        request_body: Optional[Any] = None,
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

        url = f"{self.url_prefix}{url_path}"
        kwargs = self.api._create_kwargs(query_params, header_params)

        if url_path == "/sign-url":
            # HTTP Requestを投げる
            response = getattr(self.api.session, http_method.lower())(url, **kwargs)

            # Unauthorized Errorならば、ログイン後に再度実行する
            if response.status_code == requests.codes.unauthorized:
                self.api.login()
                return self._request_wrapper(http_method, url_path, query_params, header_params, request_body)

        else:
            kwargs.update({"cookies": self.cookies})

            # HTTP Requestを投げる
            response = getattr(self.api.session, http_method.lower())(url, **kwargs)

            # CloudFrontから403 Errorが発生したとき
            if response.status_code == requests.codes.forbidden and response.headers.get("server") == "CloudFront":

                self._get_signed_access_v2(url_path)
                return self._request_wrapper(http_method, url_path, query_params, header_params, request_body)

        _log_error_response(logger, response)

        response.encoding = "utf-8"
        _raise_for_status(response)

        content = self.api._response_to_content(response)
        return content, response

    def _get_signed_access_v2(self, url_path: str):
        query_params = {"url": f"/api/v2{url_path}"}
        self.get_signed_access_v2(query_params)

    #########################################
    # Public Method : Cache
    #########################################
    def get_signed_access_v2(self, query_params: Dict[str, Any]) -> Tuple[Dict[str, Any], requests.Response]:
        """
        Signed Cookieを取得して、インスタンスに保持する。

        Args:
            query_params (Dict[str, Any]): Query Parameters
                url (str): アクセスするページのURL

        Returns:
            Tuple[SignedCookie, requests.Response]

        """

        url_path = "/sign-url"
        http_method = "GET"
        keyword_params: Dict[str, Any] = {
            "query_params": query_params,
        }

        content, response = self._request_wrapper(http_method, url_path, **keyword_params)
        # Signed Cookieをインスタンスに保持する
        self.cookies = response.cookies
        return content, response
