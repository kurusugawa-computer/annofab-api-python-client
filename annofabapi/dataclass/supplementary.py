# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace

"""
annofabapiのmodelをDataClassで定義したクラス

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照.
    oneOf, allOfなどは正しく表現できない可能性がある。
"""

import warnings  # pylint: disable=unused-import
from dataclasses import dataclass
from typing import Any, Dict, List, NewType, Optional, Tuple, Union  # pylint: disable=unused-import

from dataclasses_json import DataClassJsonMixin

from annofabapi.models import SupplementaryDataType


@dataclass
class SupplementaryData(DataClassJsonMixin):
    """ """

    organization_id: str
    """組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_set_id: str
    """入力データセットID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    supplementary_data_id: str
    """補助情報ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    supplementary_data_name: str
    """補助情報の名前"""

    supplementary_data_path: str
    """補助情報の実体が存在するパスです。 s3スキーマまたはhttpsスキーマのみサポートしています。 """

    url: str
    """システム内部用のプロパティ"""

    etag: Optional[str]
    """[HTTPレスポンスヘッダー ETag](https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/ETag)に相当する値です。 """

    supplementary_data_type: SupplementaryDataType
    """"""

    supplementary_data_number: int
    """補助情報の表示順を表す数値。"""

    updated_datetime: str
    """更新日時"""
