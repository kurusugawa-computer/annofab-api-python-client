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

from dataclasses_json import dataclass_json

from annofabapi.models import PricePlan


@dataclass_json
@dataclass
class OrganizationActivity:
    """
    
    """
    organization_id: str
    """"""

    created_datetime: str
    """"""

    storage_usage_bytes: float
    """"""
@dataclass_json
@dataclass
class OrganizationSummary:
    """
    
    """
    last_tasks_updated_datetime: Optional[str]
    """"""
@dataclass_json
@dataclass
class Organization:
    """
    
    """
    organization_id: str
    """"""

    organization_name: str
    """"""

    email: str
    """"""

    price_plan: PricePlan
    """"""

    summary: OrganizationSummary
    """"""

    created_datetime: str
    """"""

    updated_datetime: str
    """"""
