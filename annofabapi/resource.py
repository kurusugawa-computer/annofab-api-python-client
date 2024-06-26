import logging
import netrc
import os
from typing import Optional
from urllib.parse import urlparse

from annofabapi import AnnofabApi, AnnofabApi2, Wrapper
from annofabapi.api import DEFAULT_ENDPOINT_URL
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

    """

    def __init__(
        self, login_user_id: str, login_password: str, *, endpoint_url: str = DEFAULT_ENDPOINT_URL, input_mfa_code_via_stdin: bool = False
    ) -> None:
        #: AnnofabApi Instance
        self.api = AnnofabApi(
            login_user_id=login_user_id, login_password=login_password, endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin
        )

        #: Wrapper Instance
        self.wrapper = Wrapper(self.api)

        #: AnnofabApi2 Instance
        self.api2 = AnnofabApi2(self.api)

        logger.debug("Create annofabapi resource instance :: %s", {"login_user_id": login_user_id, "endpoint_url": endpoint_url})


def build(
    login_user_id: Optional[str] = None,
    login_password: Optional[str] = None,
    *,
    endpoint_url: str = DEFAULT_ENDPOINT_URL,
    input_mfa_code_via_stdin: bool = False,
) -> Resource:
    """
    AnnofabApi, Wrapperのインスタンスを保持するインスタンスを生成する。

    ``login_user_id`` と ``login_password`` の両方がNoneの場合は、``.netrc`` ファイルまたは環境変数から認証情報を取得する。
    認証情報は、環境変数, ``.netrc`` ファイルの順に読み込む。

    環境変数は``ANNOFAB_USER_ID`` , ``ANNOFAB_PASSWORD`` を参照する。

    Args:
        login_user_id: AnnofabにログインするときのユーザID
        login_password: Annofabにログインするときのパスワード
        endpoint_url: Annofab APIのエンドポイント。
        input_mfa_code_via_stdin: MFAコードを標準入力から入力するかどうか

    Returns:
        AnnofabApi, Wrapperのインスタンスを保持するインスタンス

    Raises:
        CredentialsNotFoundError: `.netrc`ファイルまたは環境変数にAnnofabの認証情報がなかった

    """
    if login_user_id is not None and login_password is not None:
        return Resource(login_user_id, login_password, endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin)

    elif login_user_id is None and login_password is None:
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

    return Resource(login_user_id, login_password, endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin)


def build_from_env(*, endpoint_url: str = DEFAULT_ENDPOINT_URL, input_mfa_code_via_stdin: bool = False) -> Resource:
    """
    環境変数 ``ANNOFAB_USER_ID`` , ``ANNOFAB_PASSWORD`` から、annofabapi.Resourceインスタンスを生成する。

    Args:
        endpoint_url: Annofab APIのエンドポイント。
        input_mfa_code_via_stdin: MFAコードを標準入力から入力するかどうか

    Returns:
        annofabapi.Resourceインスタンス

    Raises:
        CredentialsNotFoundError: 環境変数にAnnofabの認証情報がなかった
    """
    login_user_id = os.environ.get("ANNOFAB_USER_ID")
    login_password = os.environ.get("ANNOFAB_PASSWORD")
    if login_user_id is None or login_password is None:
        raise CredentialsNotFoundError("`ANNOFAB_USER_ID` or `ANNOFAB_PASSWORD`  environment variable are empty.")

    return Resource(login_user_id, login_password, endpoint_url=endpoint_url, input_mfa_code_via_stdin=input_mfa_code_via_stdin)
