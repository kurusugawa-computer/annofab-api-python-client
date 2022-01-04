"""
annofabapi.exceptions

This module contains the set of annofabapi exceptions.
"""

from typing import Optional


class AnnofabApiException(Exception):
    """
    annofabapiに関するException
    """


class AnnotationOuterFileNotFoundError(AnnofabApiException):
    """
    アノテーション情報の外部ファイル（塗りつぶしの画像ファイルなど）が、存在しない場合のエラー

    Args:
        outer_file_path: 存在しなかった外部ファイルのパス
        zipfile_path: 指定した場合、「zipファイル内に外部ファイルが存在しなかった」という旨のメッセージを設定する。

    """

    def __init__(self, outer_file_path: str, zipfile_path: Optional[str] = None):
        if zipfile_path is None:
            message = f"No such file or directory: '{outer_file_path}'"
        else:
            message = f"There is no item named '{str(outer_file_path)}' in the archive '{zipfile_path}'"

        super().__init__(message)


class NotLoggedInError(AnnofabApiException):
    """
    ログインしていない状態で、ログインしていることが前提のwebapiを実行したときのエラー

    Args:
        outer_file_path: 存在しなかった外部ファイルのパス
        zipfile_path: 指定した場合、「zipファイル内に外部ファイルが存在しなかった」という旨のメッセージを設定する。

    """

    def __init__(self, message: Optional[str] = None):
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

    def __init__(self, message: str, uploaded_data_hash: str, response_etag: str):
        self.uploaded_data_hash = uploaded_data_hash
        self.response_etag = response_etag

        super().__init__(message)
