import netrc

from annofabapi import AnnofabApi, Wrapper


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
        self.api = AnnofabApi(login_user_id, login_password)
        self.wrapper = Wrapper(self.api)


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
    `.netrc`ファイルから、annnofabapi.Resourceインスタンスを生成する。

    Returns:
        annnofabapi.Resourceインスタンス
    """
    netrc_hosts = netrc.netrc().hosts["annofab.com"]
    login_user_id = netrc_hosts[0]
    login_password = netrc_hosts[2]
    return Resource(login_user_id, login_password)
