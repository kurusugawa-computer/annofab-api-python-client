import warnings  # pylint: disable=unused-import
from dataclasses import dataclass
from typing import Any, Dict, List, NewType, Optional, Tuple, Union  # pylint: disable=unused-import

from dataclasses_json import dataclass_json

from annofabapi.models import (AccountAuthority, AdditionalDataDefinitionType, AnnotationDataHoldingType,
                               AnnotationType, AssigneeRuleOfResubmittedTask, InputDataOrder, InputDataType,
                               InspectionStatus, OrganizationMemberRole, OrganizationMemberStatus, PricePlan,
                               ProjectMemberRole, ProjectMemberStatus, ProjectStatus, TaskPhase, TaskStatus)


### 以下は自動生成の部分


@dataclass_json
@dataclass
class Account:
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

    updated_datetime: str
    """"""