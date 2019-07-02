import netrc
import os

from annofabapi import AnnofabApi, AnnofabApi2, Wrapper
from annofabapi.exceptions import AnnofabApiException


class Resource:
    """
    AnnofabApi, Wrapperのインスタンスを保持するクラス
    """

    def __init__(self, login_user_id: str, login_password: str):
        """
        Args:
            login_user_id: AnnoFabにログインするときのユーザID
            login_password: AnnoFabにログインするときのパスワード

        """

        #: AnnofabApi Instance
        self.api = AnnofabApi(login_user_id, login_password)

        #: Wrapper Instance
        self.wrapper = Wrapper(self.api)

        #: AnnofabApi2 Instance
        self.api2 = AnnofabApi2(self.api)


def build(login_user_id: str, login_password: str) -> Resource:
    """
    AnnofabApi, Wrapperのインスタンスを保持するインスタンスを生成する。

    Args:
        login_user_id: AnnoFabにログインするときのユーザID
        login_password: AnnoFabにログインするときのパスワード

    Returns:
        AnnofabApi, Wrapperのインスタンスを保持するインスタンス

    """
    return Resource(login_user_id, login_password)


def build_from_netrc() -> Resource:
    """
    `.netrc` ファイルから、annnofabapi.Resourceインスタンスを生成する。

    Returns:
        annnofabapi.Resourceインスタンス

    """
    netrc_hosts = netrc.netrc().hosts
    if 'annofab.com' not in netrc_hosts:
        raise AnnofabApiException("The `.netrc` file does not contain the machine name `annofab.com`")

    host = netrc_hosts['annofab.com']
    login_user_id = host[0]
    login_password = host[2]
    if login_user_id is None or login_password is None:
        raise AnnofabApiException("User ID or password in the .netrc file are None.")

    return Resource(login_user_id, login_password)


def build_from_env() -> Resource:
    """
    環境変数`ANNOFAB_USER_ID` , `ANNOFAB_PASSWORD`から、annnofabapi.Resourceインスタンスを生成する。

    Returns:
        annnofabapi.Resourceインスタンス

    """
    login_user_id = os.environ.get("ANNOFAB_USER_ID")
    login_password = os.environ.get("ANNOFAB_PASSWORD")
    if login_user_id is None or login_password is None:
        raise AnnofabApiException("`ANNOFAB_USER_ID` or `ANNOFAB_PASSWORD`  environment variable are empty.")

    return Resource(login_user_id, login_password)
