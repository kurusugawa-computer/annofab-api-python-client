# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace
"""
annofabapiのmodelをDataClassで定義したクラス。(swagger.yamlの ``components.schemes`` )

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照.

    oneOf, allOfなどは正しく表現できない可能性がある。

"""

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
class JobInfo:
    """

    """
    project_id: str
    """"""

    job_type: str
    """"""

    job_id: str
    """"""

    job_status: str
    """"""

    job_execution: object
    """ジョブの内部情報"""

    job_detail: object
    """ジョブ結果の内部情報"""

    created_datetime: str
    """"""

    updated_datetime: str
    """"""
