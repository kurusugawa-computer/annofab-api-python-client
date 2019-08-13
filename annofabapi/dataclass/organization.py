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
    last_tasks_updated_datetime: str
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
