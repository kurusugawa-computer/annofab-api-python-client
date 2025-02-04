# ruff: noqa: E501
# pylint: disable=too-many-lines,trailing-whitespace

"""
annofabapiのmodelをDataClassで定義したクラス

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照.
    oneOf, allOfなどは正しく表現できない可能性がある。
"""

from dataclasses import dataclass
from typing import Any  # pylint: disable=unused-import

from dataclasses_json import DataClassJsonMixin

from annofabapi.models import PricePlan


@dataclass
class Organization(DataClassJsonMixin):
    """ """

    organization_id: str
    """組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    organization_name: str
    """組織名。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    email: str
    """メールアドレス"""

    price_plan: PricePlan
    """"""

    summary: dict[str, Any]
    """廃止予定のプロパティです。常に中身は空です。 """

    created_datetime: str
    """作成日時"""

    updated_datetime: str
    """更新日時"""
