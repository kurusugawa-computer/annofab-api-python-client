"""
annofabapi.exceptions

This module contains the set of annofabapi exceptions.
"""

from typing import Optional


class AnnofabApiException(Exception):
    """
    annofabapiに関するException
    """


class CredentialsNotFoundError(AnnofabApiException):
    """
    Annofabの認証情報が見つからないときのエラー
    """


class AnnotationOuterFileNotFoundError(AnnofabApiException):
    """
    アノテーション情報の外部ファイル（塗りつぶしの画像ファイルなど）が、存在しない場合のエラー

    Args:
        outer_file_path: 存在しなかった外部ファイルのパス
        zipfile_path: 指定した場合、「zipファイル内に外部ファイルが存在しなかった」という旨のメッセージを設定する。

    """

    def __init__(self, outer_file_path: str, zipfile_path: Optional[str] = None) -> None:
        if zipfile_path is None:
            message = f"No such file or directory: '{outer_file_path}'"
        else:
            message = f"There is no item named '{outer_file_path!s}' in the archive '{zipfile_path}'"

        super().__init__(message)


class NotLoggedInError(AnnofabApiException):
    """
    ログインしていない状態で、ログインしていることが前提のwebapiを実行したときのエラー

    Args:
        outer_file_path: 存在しなかった外部ファイルのパス
        zipfile_path: 指定した場合、「zipファイル内に外部ファイルが存在しなかった」という旨のメッセージを設定する。

    """

    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = "You are not logged in."
        super().__init__(message)


class CheckSumError(AnnofabApiException):
    """
    アップロードしたデータ（ファイルやバイナリデータ）の整合性が一致していないときのエラー。

    Args:
        uploaded_data_hash: アップロード対象のデータのハッシュ値（MD5）
        response_etag: アップロードしたときのレスポンスヘッダ'ETag'の値

    Attributes:
        uploaded_data_hash: アップロード対象のデータのハッシュ値（MD5）
        response_etag: アップロードしたときのレスポンスヘッダ'ETag'の値
    """

    def __init__(self, message: str, uploaded_data_hash: str, response_etag: str) -> None:
        self.uploaded_data_hash = uploaded_data_hash
        self.response_etag = response_etag

        super().__init__(message)


class MfaEnabledUserExecutionError(Exception):
    """
    MFAが有効化されたユーザーが実行したことを示すエラー
    """

    def __init__(self, user_id: str) -> None:
        message = f"User (User ID: {user_id}) cannot use annofab-api-python-client because MFA is enabled."
        super().__init__(message)


class InvalidMfaCodeError(AnnofabApiException):
    """
    MFAコードが間違っている場合のエラー
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
