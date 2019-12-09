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

from annofabapi.models import GraphType, TaskPhase, TaskStatus


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
    """タスク数"""

    work_timespan: int
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
    date: str
    """"""

    tasks_completed: int
    """教師付を担当したタスクが完了状態になった回数"""

    tasks_rejected: int
    """教師付を担当したタスクが差し戻された回数"""

    worktime: str
    """作業時間（ISO 8601 duration）"""


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
class InspectionStatisticsPhrases:
    """
    ラベル外指摘の集計結果
    """
    phrases: Dict[str, int]
    """定型指摘ごとの合計数。キーは定型指摘ID、値は指摘数"""

    no_phrase: int
    """非定型指摘の合計数"""


@dataclass_json
@dataclass
class InspectionStatisticsBreakdown:
    """
    検査コメント数の集計結果
    """
    labels: Dict[str, InspectionStatisticsPhrases]
    """ラベルごとの指摘集計結果。キーは`label_id`"""

    no_label: InspectionStatisticsPhrases
    """"""


@dataclass_json
@dataclass
class InspectionStatistics:
    """
    
    """
    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    date: str
    """集計日"""

    breakdown: InspectionStatisticsBreakdown
    """"""


@dataclass_json
@dataclass
class PhaseStatistics:
    """
    
    """
    phase: TaskPhase
    """"""

    worktime: str
    """累積作業時間（ISO 8601 duration）"""


@dataclass_json
@dataclass
class TaskPhaseStatistics:
    """
    
    """
    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    date: str
    """"""

    phases: List[PhaseStatistics]
    """タスクのフェーズごとの集計結果"""


@dataclass_json
@dataclass
class LabelStatistics:
    """
    
    """
    label_id: str
    """"""

    completed: int
    """ラベルごとの受入が完了したアノテーション数"""

    wip: int
    """ラベルごとの受入が完了していないアノテーション数"""


@dataclass_json
@dataclass
class HistogramItem:
    """
    
    """
    begin: float
    """"""

    end: float
    """"""

    count: int
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
    """作業時間の平均（ISO 8601 duration）"""

    standard_deviation: str
    """作業時間の標準偏差（ISO 8601 duration）"""


@dataclass_json
@dataclass
class AccountWorktimeStatistics:
    """
    
    """
    account_id: str
    """"""

    by_tasks: List[WorktimeStatisticsItem]
    """ユーザごとのタスク1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）"""

    by_inputs: List[WorktimeStatisticsItem]
    """ユーザごとの画像1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）"""

    by_minutes: List[WorktimeStatisticsItem]
    """ユーザごとの動画1分当たりの作業時間情報（画像プロジェクトの場合は空リスト）"""


@dataclass_json
@dataclass
class WorktimeStatistics:
    """
    
    """
    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    date: str
    """"""

    by_tasks: List[WorktimeStatisticsItem]
    """タスク1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）"""

    by_inputs: List[WorktimeStatisticsItem]
    """画像1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）"""

    by_minutes: List[WorktimeStatisticsItem]
    """動画1分当たりの作業時間情報（画像プロジェクトの場合は空リスト）"""

    accounts: List[AccountWorktimeStatistics]
    """ユーザごとの作業時間情報"""


@dataclass_json
@dataclass
class Marker:
    """
    
    """
    marker_id: Optional[str]
    """マーカーID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    title: Optional[str]
    """"""

    graph_type: Optional[GraphType]
    """"""

    marked_at: Optional[str]
    """グラフ上のマーカー位置(x軸)"""


@dataclass_json
@dataclass
class Markers:
    """
    
    """
    project_id: Optional[str]
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    markers: Optional[List[Marker]]
    """"""

    updated_datetime: Optional[str]
    """"""
