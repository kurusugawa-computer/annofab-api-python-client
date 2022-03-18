import logging
import time
from typing import Any, Dict, Optional, Tuple

import requests
from requests.cookies import RequestsCookieJar

import annofabapi.utils
from annofabapi.api import (
    DEFAULT_WAITING_TIME_SECONDS_WITH_429_STATUS_CODE,
    AnnofabApi,
    _create_request_body_for_logger,
    _log_error_response,
    _raise_for_status,
    _should_retry_with_status,
)
from annofabapi.generated_api2 import AbstractAnnofabApi2

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
        *,
        query_params: Optional[Dict[str, Any]] = None,
        header_params: Optional[Dict[str, Any]] = None,
        request_body: Optional[Any] = None,
        raise_for_status: bool = True,
    ) -> Tuple[Any, requests.Response]:
        """
        HTTP　Requestを投げて、Responseを返す。
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

        """

        url = f"{self.url_prefix}{url_path}"
        kwargs = self.api._create_kwargs(query_params, header_params)

        if url_path == "/sign-url":
            # HTTP Requestを投げる
            response = getattr(self.api.session, http_method.lower())(url, **kwargs)

            # Unauthorized Errorならば、ログイン後に再度実行する
            if response.status_code == requests.codes.unauthorized:
                self.api.login()
                return self._request_wrapper(
                    http_method,
                    url_path,
                    query_params=query_params,
                    header_params=header_params,
                    request_body=request_body,
                    raise_for_status=raise_for_status,
                )

        else:
            kwargs.update({"cookies": self.cookies})

            # HTTP Requestを投げる
            response = self.api.session.request(method=http_method.lower(), url=url, **kwargs)

            logger.debug(
                "Sent a request :: %s",
                {
                    "request": {
                        "http_method": http_method.lower(),
                        "url": url,
                        "query_params": query_params,
                        "header_params": header_params,
                        "request_body": _create_request_body_for_logger(request_body)
                        if request_body is not None
                        else None,
                    },
                    "response": {
                        "status_code": response.status_code,
                        "content_length": len(response.content),
                    },
                },
            )

            # CloudFrontから403 Errorが発生したとき
            if response.status_code == requests.codes.forbidden and response.headers.get("server") == "CloudFront":

                self._get_signed_access_v2(url_path)
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
        content = self.api._response_to_content(response)

        # リトライすべき場合はExceptionを返す
        if raise_for_status or _should_retry_with_status(response.status_code):
            _log_error_response(logger, response)
            _raise_for_status(response)

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
