# ruff: noqa: E501
# pylint: disable=too-many-lines,trailing-whitespace

"""
annofabapiのmodelをDataClassで定義したクラス

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照.
    oneOf, allOfなどは正しく表現できない可能性がある。
"""

from dataclasses import dataclass
from typing import Any, Optional  # pylint: disable=unused-import

from dataclasses_json import DataClassJsonMixin

SystemMetadata = dict[str, Any]


@dataclass
class Resolution(DataClassJsonMixin):
    """ """

    width: int
    """画像の幅[ピクセル]"""

    height: int
    """画像の高さ[ピクセル]"""


@dataclass
class InputData(DataClassJsonMixin):
    """
    入力データの情報を表すデータ構造です。
    """

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    organization_id: str
    """組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_set_id: str
    """入力データセットID(システム内部用のプロパティ)。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_name: str
    """入力データ名"""

    input_data_path: str
    """入力データの実体が保存されたURLです。 URLスキームが s3 もしくは https であるもののみをサポートしています。 """

    url: Optional[str]
    """システム内部用のプロパティ"""

    etag: Optional[str]
    """[HTTPレスポンスヘッダー ETag](https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/ETag)に相当する値です。 """

    original_input_data_path: Optional[str]
    """システム内部用のプロパティ """

    updated_datetime: str
    """更新日時"""

    sign_required: bool
    """CloudFrontのSignedCookieを使ったプライベートストレージを利用するかどうか """

    metadata: dict[str, str]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """

    system_metadata: SystemMetadata
    """"""
