import logging  # noqa: A005
import netrc
import os
from typing import Optional, Union
from urllib.parse import urlparse

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

    def __init__(self, credentials: Union[IdPass, Pat], *, endpoint_url: str = DEFAULT_ENDPOINT_URL, input_mfa_code_via_stdin: bool = False) -> None:
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
    login_user_id: Optional[str] = None,
    login_password: Optional[str] = None,
    pat: Optional[str] = None,
    *,
    endpoint_url: str = DEFAULT_ENDPOINT_URL,
    input_mfa_code_via_stdin: bool = False,
) -> Resource:
    """
    AnnofabApi, Wrapperのインスタンスを保持するインスタンスを生成する。

    ``pat``が渡された場合はそれが優先して利用される。
    ``pat`` / ``login_user_id`` / ``login_password`` の全てがNoneの場合は、``.netrc`` ファイルまたは環境変数から認証情報を取得する。
    認証情報は、環境変数, ``.netrc`` ファイルの順に読み込む。

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
        CredentialsNotFoundError: `.netrc`ファイルまたは環境変数にAnnofabの認証情報がなかった

    """
    if pat is not None:
        return Resource(credentials=Pat(pat), endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin)
    if login_user_id is not None and login_password is not None:
        return Resource(
            credentials=IdPass(login_user_id, login_password), endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin
        )

    elif login_user_id is None and login_password is None and pat is None:
        try:
            return build_from_env(endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin)
        except CredentialsNotFoundError:
            try:
                return build_from_netrc(endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin)
            except CredentialsNotFoundError as e:
                raise CredentialsNotFoundError("環境変数または`.netrc`ファイルにAnnofab認証情報はありませんでした。") from e
    else:
        raise ValueError("引数`login_user_id`か`login_password`のどちらか一方がNoneです。両方Noneでないか、両方Noneである必要があります。")


def build_from_netrc(*, endpoint_url: str = DEFAULT_ENDPOINT_URL, input_mfa_code_via_stdin: bool = False) -> Resource:
    """
    ``.netrc`` ファイルから、annofabapi.Resourceインスタンスを生成する。

    Args:
        endpoint_url: Annofab APIのエンドポイント。
        input_mfa_code_via_stdin: MFAコードを標準入力から入力するかどうか
                                  Falseを渡して且つMFAコードの入力を求められるアカウントを利用する場合、mfa_codeを引数にloginメソッドを直接呼び出さなければならず、そうしない場合は例外を送出する

    Returns:
        annofabapi.Resourceインスタンス

    Raises:
        CredentialsNotFoundError: `.netrc`ファイルにAnnofabの認証情報がなかった

    """
    try:
        netrc_hosts = netrc.netrc().hosts
    except FileNotFoundError as e:
        raise CredentialsNotFoundError("`.netrc`ファイルは見つかりません。") from e

    annofab_hostname = (urlparse(endpoint_url)).hostname

    if annofab_hostname not in netrc_hosts:
        raise CredentialsNotFoundError(f"The `.netrc` file does not contain the machine name '{annofab_hostname}'")

    host = netrc_hosts[annofab_hostname]
    login_user_id = host[0]
    login_password = host[2]
    if login_user_id is None or login_password is None:
        raise CredentialsNotFoundError("User ID or password in the .netrc file are None.")

    return Resource(credentials=IdPass(login_user_id, login_password), endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin)


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
