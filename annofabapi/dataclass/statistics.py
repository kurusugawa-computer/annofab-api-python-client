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

from annofabapi.models import TaskPhase, TaskStatus


@dataclass_json
@dataclass
class ProjectTaskStatistics:
    """
    
    """
    phase: Optional[TaskPhase]
    """"""

    status: Optional[TaskStatus]
    """"""

    count: Optional[int]
    """"""

    work_timespan: Optional[int]
    """累計実作業時間(ミリ秒)"""
@dataclass_json
@dataclass
class ProjectTaskStatisticsHistory:
    """
    
    """
    date: Optional[str]
    """"""

    tasks: Optional[List[ProjectTaskStatistics]]
    """"""
@dataclass_json
@dataclass
class ProjectAccountStatisticsHistory:
    """
    
    """
    date: Optional[str]
    """"""

    tasks_completed: Optional[int]
    """"""

    tasks_rejected: Optional[int]
    """"""

    worktime: Optional[str]
    """"""
@dataclass_json
@dataclass
class ProjectAccountStatistics:
    """
    
    """
    account_id: Optional[str]
    """"""

    histories: Optional[List[ProjectAccountStatisticsHistory]]
    """"""
@dataclass_json
@dataclass
class InspectionStatisticsPhrases:
    """
    
    """
    phrases: Optional[Dict[str, int]]
    """定型指摘ごとの合計数"""

    no_phrase: Optional[int]
    """非定型指摘の合計数"""
@dataclass_json
@dataclass
class InspectionStatisticsBreakdown:
    """
    
    """
    labels: Optional[Dict[str, InspectionStatisticsPhrases]]
    """ラベルごとの指摘集計結果"""

    no_label: Optional[InspectionStatisticsPhrases]
    """"""
@dataclass_json
@dataclass
class InspectionStatistics:
    """
    
    """
    project_id: Optional[str]
    """"""

    date: Optional[str]
    """集計日"""

    breakdown: Optional[InspectionStatisticsBreakdown]
    """"""
@dataclass_json
@dataclass
class PhaseStatistics:
    """
    
    """
    phase: Optional[str]
    """"""

    worktime: Optional[str]
    """"""
@dataclass_json
@dataclass
class TaskPhaseStatistics:
    """
    
    """
    project_id: Optional[str]
    """"""

    date: Optional[str]
    """"""

    phases: Optional[List[PhaseStatistics]]
    """"""
@dataclass_json
@dataclass
class LabelStatistics:
    """
    
    """
    label_id: Optional[str]
    """"""

    completed: Optional[int]
    """ラベルごとの受入が完了したアノテーション数"""

    wip: Optional[int]
    """ラベルごとの受入が完了していないアノテーション数"""
@dataclass_json
@dataclass
class HistogramItem:
    """
    
    """
    begin: Optional[float]
    """"""

    end: Optional[float]
    """"""

    count: Optional[int]
    """"""
@dataclass_json
@dataclass
class WorktimeStatisticsItem:
    """
    
    """
    phase: Optional[TaskPhase]
    """"""

    histogram: Optional[List[HistogramItem]]
    """"""

    average: Optional[str]
    """"""

    standard_deviation: Optional[str]
    """"""
@dataclass_json
@dataclass
class AccountWorktimeStatistics:
    """
    
    """
    account_id: Optional[str]
    """"""

    by_tasks: Optional[List[WorktimeStatisticsItem]]
    """"""

    by_inputs: Optional[List[WorktimeStatisticsItem]]
    """"""
@dataclass_json
@dataclass
class HistogramItem:
    """
    
    """
    begin: Optional[float]
    """"""

    end: Optional[float]
    """"""

    count: Optional[int]
    """"""
@dataclass_json
@dataclass
class WorktimeStatistics:
    """
    
    """
    project_id: Optional[str]
    """"""

    date: Optional[str]
    """"""

    by_tasks: Optional[List[WorktimeStatisticsItem]]
    """"""

    by_inputs: Optional[List[WorktimeStatisticsItem]]
    """"""

    accounts: Optional[List[AccountWorktimeStatistics]]
    """"""
