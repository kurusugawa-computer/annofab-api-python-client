import logging
import os

from annofabapi import AnnofabApi, AnnofabApi2, Wrapper
from annofabapi.api import DEFAULT_ENDPOINT_URL
from annofabapi.credentials import IdPass, Pat
from annofabapi.exceptions import CredentialsNotFoundError

logger = logging.getLogger(__name__)


class Resource:
    """
    AnnofabApi, Wrapperのインスタンスを保持するクラス

    Args:
        login_user_id: AnnofabにログインするときのユーザID
        login_password: Annofabにログインするときのパスワード
        endpoint_url: Annofab APIのエンドポイント。
        input_mfa_code_via_stdin: MFAコードを標準入力から入力するかどうか
                                  Falseを渡して且つMFAコードの入力を求められるアカウントを利用する場合、mfa_codeを引数にloginメソッドを直接呼び出さなければならず、そうしない場合は例外を送出する

    Attributes:
        api: ``annofabapi.AnnofabApi`` のインスタンス
        wrapper: ``annofabapi.Wrapper`` のインスタンス
        api2: ``annofabapi.AnnofabApi2`` のインスタンス

    """

    def __init__(self, credentials: IdPass | Pat, *, endpoint_url: str = DEFAULT_ENDPOINT_URL, input_mfa_code_via_stdin: bool = False) -> None:
        self.api = AnnofabApi(
            credentials=credentials,
            endpoint_url=endpoint_url,
            input_mfa_code_via_stdin=input_mfa_code_via_stdin,
        )

        self.wrapper = Wrapper(self.api)

        self.api2 = AnnofabApi2(self.api)

        id_or_token = credentials.user_id if isinstance(credentials, IdPass) else "PersonalAccessToken"
        logger.debug("Create annofabapi resource instance :: %s", {"user_id_or_token": id_or_token, "endpoint_url": endpoint_url})


def build(
    login_user_id: str | None = None,
    login_password: str | None = None,
    pat: str | None = None,
    *,
    endpoint_url: str = DEFAULT_ENDPOINT_URL,
    input_mfa_code_via_stdin: bool = False,
) -> Resource:
    """
    AnnofabApi, Wrapperのインスタンスを保持するインスタンスを生成する。

    ``pat``が渡された場合はそれが優先して利用される。
    ``pat`` / ``login_user_id`` / ``login_password`` の全てがNoneの場合は、環境変数から認証情報を取得する。

    環境変数は``ANNOFAB_USER_ID`` , ``ANNOFAB_PASSWORD``, ``ANNOFAB_PAT`` を参照し、``ANNOFAB_PAT``が設定されている場合はそれ以外を無視する。

    Args:
        login_user_id: AnnofabにログインするときのユーザID
        login_password: Annofabにログインするときのパスワード
        pat: パーソナルアクセストークン。 この値を渡した場合、login_user_idとlogin_passwordは無視される
        endpoint_url: Annofab APIのエンドポイント。
        input_mfa_code_via_stdin: MFAコードを標準入力から入力するかどうか
                                  Falseを渡して且つMFAコードの入力を求められるアカウントを利用する場合、mfa_codeを引数にloginメソッドを直接呼び出さなければならず、そうしない場合は例外を送出する

    Returns:
        AnnofabApi, Wrapperのインスタンスを保持するインスタンス

    Raises:
        CredentialsNotFoundError: 環境変数にAnnofabの認証情報がなかった

    """
    if pat is not None:
        return Resource(credentials=Pat(pat), endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin)
    if login_user_id is not None and login_password is not None:
        return Resource(
            credentials=IdPass(login_user_id, login_password), endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin
        )

    elif login_user_id is None and login_password is None and pat is None:
        return build_from_env(endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin)
    else:
        raise ValueError("引数`login_user_id`か`login_password`のどちらか一方がNoneです。両方Noneでないか、両方Noneである必要があります。")


def build_from_env(*, endpoint_url: str = DEFAULT_ENDPOINT_URL, input_mfa_code_via_stdin: bool = False) -> Resource:
    """
    環境変数 ``ANNOFAB_USER_ID`` , ``ANNOFAB_PASSWORD``, ``ANNOFAB_PAT`` から、annofabapi.Resourceインスタンスを生成する。
    ``ANNOFAB_PAT``が設定されている場合はそれが優先して利用される。

    Args:
        endpoint_url: Annofab APIのエンドポイント。
        input_mfa_code_via_stdin: MFAコードを標準入力から入力するかどうか
                                  Falseを渡して且つMFAコードの入力を求められるアカウントを利用する場合、mfa_codeを引数にloginメソッドを直接呼び出さなければならず、そうしない場合は例外を送出する

    Returns:
        annofabapi.Resourceインスタンス

    Raises:
        CredentialsNotFoundError: 環境変数にAnnofabの認証情報がなかった
    """
    login_user_id = os.environ.get("ANNOFAB_USER_ID")
    login_password = os.environ.get("ANNOFAB_PASSWORD")
    pat = os.environ.get("ANNOFAB_PAT")

    if pat is not None:
        return Resource(credentials=Pat(pat), endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin)
    if login_user_id is not None and login_password is not None:
        return Resource(
            credentials=IdPass(login_user_id, login_password), endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin
        )

    raise CredentialsNotFoundError("`ANNOFAB_PAT` and `ANNOFAB_USER_ID / ANNOFAB_PASSWORD` environment variable are empty.")
