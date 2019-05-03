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


def build(login_user_id: str, login_password: str, version: str = "v1") -> Resource:
    """
    AnnofabApi, Wrapperのインスタンスを保持するインスタンスを生成する。

    Args:
        login_user_id: AnnoFabにログインするときのユーザID
        login_password: AnnoFabにログインするときのパスワード
        version: APIのバージョン。2019/05時点ではv1のみ対応

    Returns:
        AnnofabApi, Wrapperのインスタンスを保持するインスタンス
    """
    return Resource(login_user_id, login_password)
