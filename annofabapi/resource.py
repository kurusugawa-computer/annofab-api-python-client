import logging
import netrc
import os
from urllib.parse import urlparse

from annofabapi import AnnofabApi, AnnofabApi2, Wrapper
from annofabapi.api import DEFAULT_ENDPOINT_URL
from annofabapi.exceptions import AnnofabApiException

logger = logging.getLogger(__name__)


class Resource:
    """
    AnnofabApi, Wrapperのインスタンスを保持するクラス

    Args:
        login_user_id: AnnoFabにログインするときのユーザID
        login_password: AnnoFabにログインするときのパスワード
        endpoint_url: AnnoFab APIのエンドポイント。

    """

    def __init__(self, login_user_id: str, login_password: str, endpoint_url: str = DEFAULT_ENDPOINT_URL):
        #: AnnofabApi Instance
        self.api = AnnofabApi(login_user_id=login_user_id, login_password=login_password, endpoint_url=endpoint_url)

        #: Wrapper Instance
        self.wrapper = Wrapper(self.api)

        #: AnnofabApi2 Instance
        self.api2 = AnnofabApi2(self.api)


def build(login_user_id: str, login_password: str, endpoint_url: str = DEFAULT_ENDPOINT_URL) -> Resource:
    """
    AnnofabApi, Wrapperのインスタンスを保持するインスタンスを生成する。

    Args:
        login_user_id: AnnoFabにログインするときのユーザID
        login_password: AnnoFabにログインするときのパスワード
        endpoint_url: AnnoFab APIのエンドポイント。

    Returns:
        AnnofabApi, Wrapperのインスタンスを保持するインスタンス

    """
    return Resource(login_user_id, login_password, endpoint_url=endpoint_url)


def build_from_netrc(endpoint_url: str = DEFAULT_ENDPOINT_URL) -> Resource:
    """
    ``.netrc`` ファイルから、annnofabapi.Resourceインスタンスを生成する。

    Args:
        endpoint_url: AnnoFab APIのエンドポイント。

    Returns:
        annnofabapi.Resourceインスタンス

    """
    try:
        netrc_hosts = netrc.netrc().hosts
    except FileNotFoundError as e:
        raise AnnofabApiException(e)

    annofab_hostname = (urlparse(endpoint_url)).hostname

    if annofab_hostname not in netrc_hosts:
        raise AnnofabApiException(f"The `.netrc` file does not contain the machine name '{annofab_hostname}'")

    host = netrc_hosts[annofab_hostname]
    login_user_id = host[0]
    login_password = host[2]
    if login_user_id is None or login_password is None:
        raise AnnofabApiException("User ID or password in the .netrc file are None.")

    logger.debug(".netrcファイルからAnnoFab認証情報を読み込みました。")
    return Resource(login_user_id, login_password, endpoint_url=endpoint_url)


def build_from_env(endpoint_url: str = DEFAULT_ENDPOINT_URL) -> Resource:
    """
    環境変数 ``ANNOFAB_USER_ID`` , ``ANNOFAB_PASSWORD`` から、annnofabapi.Resourceインスタンスを生成する。

    Args:
        endpoint_url: AnnoFab APIのエンドポイント。

    Returns:
        annnofabapi.Resourceインスタンス

    """
    login_user_id = os.environ.get("ANNOFAB_USER_ID")
    login_password = os.environ.get("ANNOFAB_PASSWORD")
    if login_user_id is None or login_password is None:
        raise AnnofabApiException("`ANNOFAB_USER_ID` or `ANNOFAB_PASSWORD`  environment variable are empty.")

    logger.debug("環境変数からAnnoFab認証情報を読み込みました。")
    return Resource(login_user_id, login_password, endpoint_url=endpoint_url)


def build_from_netrc_or_env(endpoint_url: str = DEFAULT_ENDPOINT_URL) -> Resource:
    """
    `.netrc`ファイルまたは環境変数からAnnoFab認証情報を取得し、annnofabapi.Resourceインスタンスを生成します。
    netrc, 環境変数の順に認証情報を読み込みます。

    Args:
        endpoint_url:

    Returns:

    """
    # '.netrc'ファイルから認証情報を取得する
    try:
        return build_from_netrc(endpoint_url)
    except AnnofabApiException:
        pass

    # 環境変数から認証情報を取得する
    try:
        return build_from_env(endpoint_url)
    except AnnofabApiException:
        pass

    raise AnnofabApiException("`.netrc`ファイルまたは環境変数にAnnoFab認証情報はありませんでした。")
