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

# 列挙体の一覧
from annofabapi.models import (AccountAuthority, AdditionalDataDefinitionType, AnnotationDataHoldingType,
                               AnnotationType, AssigneeRuleOfResubmittedTask, InputDataOrder, InputDataType,
                               InspectionStatus, OrganizationMemberRole, OrganizationMemberStatus, PricePlan,
                               ProjectMemberRole, ProjectMemberStatus, ProjectStatus, TaskPhase, TaskStatus)




@dataclass_json
@dataclass
class OrganizationMember:
    """
    
    """
    organization_id: str
    """"""



    account_id: str
    """"""



    user_id: str
    """"""



    username: str
    """"""



    role: OrganizationMemberRole
    """"""



    status: OrganizationMemberStatus
    """"""



    created_datetime: Optional[str]
    """"""



    updated_datetime: Optional[str]
    """"""







