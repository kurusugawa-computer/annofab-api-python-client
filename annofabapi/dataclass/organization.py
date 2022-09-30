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

from annofabapi._utils import deprecated_class
from annofabapi.models import PricePlan


@deprecated_class(deprecated_date="2022-12-01")
@dataclass
class OrganizationActivity(DataClassJsonMixin):
    """ """

    organization_id: str
    """組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    created_datetime: str
    """作成日時"""

    storage_usage_bytes: int
    """Annofabストレージの使用量[バイト]"""


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

    summary: Dict[str, Any]
    """廃止予定のプロパティです。常に中身は空です。 """

    created_datetime: str
    """作成日時"""

    updated_datetime: str
    """更新日時"""
