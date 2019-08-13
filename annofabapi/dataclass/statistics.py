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


### 以下は自動生成の部分

@dataclass_json
@dataclass
class LabelStatistics:
    """

    """
    label_id: str
    """"""

    completed_labels: int
    """ラベルごとの受入が完了したアノテーション数"""

    wip_labels: int
    """ラベルごとの受入が完了していないアノテーション数"""


@dataclass_json
@dataclass
class WorktimeStatistics:
    """

    """
    project_id: str
    """"""

    date: str
    """"""

    by_tasks: List[WorktimeStatisticsItem]
    """"""

    by_inputs: List[WorktimeStatisticsItem]
    """"""

    accounts: List[AccountWorktimeStatistics]
    """"""


@dataclass_json
@dataclass
class WorktimeStatisticsItem:
    """

    """
    phase: TaskPhase
    """"""

    histogram: List[HistogramItem]
    """"""

    average: str
    """"""

    standard_deviation: str
    """"""



@dataclass_json
@dataclass
class AccountWorktimeStatistics:
    """

    """
    account_id: str
    """"""

    by_tasks: List[WorktimeStatisticsItem]
    """"""

    by_inputs: List[WorktimeStatisticsItem]
    """"""


@dataclass_json
@dataclass
class TaskPhaseStatistics:
    """

    """
    project_id: str
    """"""

    date: str
    """"""

    phases: List[PhaseStatistics]
    """"""


@dataclass_json
@dataclass
class ProjectTaskStatistics:
    """

    """
    phase: TaskPhase
    """"""

    status: TaskStatus
    """"""

    count: int
    """"""

    work_timespan: int
    """累計実作業時間(ミリ秒)"""


@dataclass_json
@dataclass
class ProjectTaskStatisticsHistory:
    """

    """
    date: str
    """"""

    tasks: List[ProjectTaskStatistics]
    """"""


@dataclass_json
@dataclass
class PhaseStatistics:
    """

    """
    phase: str
    """"""

    worktime: str
    """"""


@dataclass_json
@dataclass
class ProjectAccountStatistics:
    """

    """
    account_id: str
    """"""

    histories: List[ProjectAccountStatisticsHistory]
    """"""


@dataclass_json
@dataclass
class ProjectAccountStatisticsHistory:
    """

    """
    date: str
    """"""

    tasks_completed: int
    """"""

    tasks_rejected: int
    """"""

    worktime: str
    """"""

