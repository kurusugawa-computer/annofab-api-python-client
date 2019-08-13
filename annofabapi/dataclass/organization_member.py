import warnings  # pylint: disable=unused-import
from dataclasses import dataclass
from typing import Any, Dict, List, NewType, Optional, Tuple, Union  # pylint: disable=unused-import

from dataclasses_json import dataclass_json

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

    created_datetime: str
    """"""

    updated_datetime: str
    """"""
