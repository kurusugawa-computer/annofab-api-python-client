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

from annofabapi.dataclass.organization import OrganizationSummary
from annofabapi.models import AccountAuthority, OrganizationMemberRole, OrganizationMemberStatus, PricePlan


@dataclass_json
@dataclass
class MyOrganization:
    """
    
    """
    organization_id: Optional[str]
    """"""

    name: Optional[str]
    """"""

    email: Optional[str]
    """"""

    price_plan: Optional[PricePlan]
    """"""

    summary: Optional[OrganizationSummary]
    """"""

    created_datetime: Optional[str]
    """"""

    updated_datetime: Optional[str]
    """"""

    my_role: Optional[OrganizationMemberRole]
    """"""

    my_status: Optional[OrganizationMemberStatus]
    """"""
@dataclass_json
@dataclass
class MyAccount:
    """
    
    """
    account_id: str
    """"""

    user_id: str
    """"""

    username: str
    """"""

    email: str
    """"""

    lang: str
    """"""

    keylayout: str
    """"""

    authority: AccountAuthority
    """"""

    updated_datetime: Optional[str]
    """"""

    reset_requested_email: Optional[str]
    """"""

    errors: List[str]
    """"""
