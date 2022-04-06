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

from dataclasses_json import DataClassJsonMixin

from annofabapi.models import GraphType, TaskPhase, TaskStatus


@dataclass
class ProjectTaskStatistics(DataClassJsonMixin):
    """ """

    phase: TaskPhase
    """"""

    status: TaskStatus
    """"""

    count: int
    """タスク数"""

    work_timespan: int
    """累計実作業時間(ミリ秒)"""


@dataclass
class ProjectTaskStatisticsHistory(DataClassJsonMixin):
    """ """

    date: Optional[str]
    """"""

    tasks: Optional[List[ProjectTaskStatistics]]
    """"""


@dataclass
class ProjectAccountStatisticsHistory(DataClassJsonMixin):
    """ """

    date: str
    """"""

    tasks_completed: int
    """教師付フェーズのタスクを提出した回数、または検査/受入フェーズのタスクを合格/差戻にした回数。  たとえば、あるタスクのタスク履歴が下表の状態だった場合、2020-04-01の`tasks_completed`は以下の通りになります。  * Alice: 1 * Bob: 1 * Chris: 2   <table>   <tr>     <th>担当者</th>     <th>フェーズ</th>     <th>作業内容</th>     <th>完了日時</th>   </tr>   <tr>     <td>Alice</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 09:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>差し戻す</td>     <td>2020-04-01 10:00</td>   </tr>   <tr>     <td>Bob</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 11:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>合格にする</td>     <td>2020-04-01 12:00</td>   </tr> </table> """

    tasks_rejected: int
    """教師付フェーズを担当したタスクが差し戻された回数、または受入フェーズを担当したタスクが受入完了を取り消された回数。  たとえば、あるタスクのタスク履歴が下表の状態だった場合、2020-04-01の`tasks_rejected`は以下の通りになります。  * Alice: 1 * Bob: 1 * Chris: 1   <table>   <tr>     <th>担当者</th>     <th>フェーズ</th>     <th>作業内容</th>     <th>完了日時</th>   </tr>   <tr>     <td>Alice</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 09:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>差し戻す</td>     <td>2020-04-01 10:00</td>   </tr>   <tr>     <td>Bob</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 11:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>差し戻す</td>     <td>2020-04-01 12:00</td>   </tr>   <tr>     <td>Bob</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 13:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>合格にする</td>     <td>2020-04-01 14:00</td>   </tr>   <tr>     <td>Dave</td>     <td>受入</td>     <td>受入完了状態を取り消して、再度合格にする</td>     <td>2020-04-01 15:00</td>   </tr> </table> """

    worktime: str
    """作業時間（ISO 8601 duration）"""


@dataclass
class ProjectAccountStatistics(DataClassJsonMixin):
    """ """

    account_id: str
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    histories: List[ProjectAccountStatisticsHistory]
    """"""


@dataclass
class InspectionStatisticsPhrases(DataClassJsonMixin):
    """
    ラベル外指摘の集計結果
    """

    phrases: Dict[str, int]
    """定型指摘ごとの合計数。キーは定型指摘ID、値は指摘数"""

    no_phrase: int
    """非定型指摘の合計数"""


@dataclass
class InspectionStatisticsBreakdown(DataClassJsonMixin):
    """
    検査コメント数の集計結果
    """

    labels: Dict[str, InspectionStatisticsPhrases]
    """ラベルごとの指摘集計結果。キーは`label_id`"""

    no_label: InspectionStatisticsPhrases
    """"""


@dataclass
class InspectionStatistics(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    date: str
    """集計日"""

    breakdown: InspectionStatisticsBreakdown
    """"""


@dataclass
class PhaseStatistics(DataClassJsonMixin):
    """ """

    phase: TaskPhase
    """"""

    worktime: str
    """累積作業時間（ISO 8601 duration）"""


@dataclass
class TaskPhaseStatistics(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    date: str
    """"""

    phases: List[PhaseStatistics]
    """タスクのフェーズごとの集計結果"""


@dataclass
class LabelStatistics(DataClassJsonMixin):
    """ """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    completed: int
    """ラベルごとの受入が完了したアノテーション数"""

    wip: int
    """ラベルごとの受入が完了していないアノテーション数"""


@dataclass
class HistogramItem(DataClassJsonMixin):
    """ """

    begin: float
    """"""

    end: float
    """"""

    count: int
    """"""


@dataclass
class WorktimeStatisticsItem(DataClassJsonMixin):
    """ """

    phase: TaskPhase
    """"""

    histogram: List[HistogramItem]
    """"""

    average: str
    """作業時間の平均（ISO 8601 duration）"""

    standard_deviation: str
    """作業時間の標準偏差（ISO 8601 duration）"""


@dataclass
class AccountWorktimeStatistics(DataClassJsonMixin):
    """ """

    account_id: str
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    by_tasks: List[WorktimeStatisticsItem]
    """ユーザごとのタスク1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）"""

    by_inputs: List[WorktimeStatisticsItem]
    """ユーザごとの画像1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）"""

    by_minutes: List[WorktimeStatisticsItem]
    """ユーザごとの動画1分当たりの作業時間情報（画像プロジェクトの場合は空リスト）"""


@dataclass
class WorktimeStatistics(DataClassJsonMixin):
    """ """

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


@dataclass
class Marker(DataClassJsonMixin):
    """ """

    marker_id: Optional[str]
    """マーカーID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    title: Optional[str]
    """"""

    graph_type: Optional[GraphType]
    """"""

    marked_at: Optional[str]
    """グラフ上のマーカー位置(x軸)"""


@dataclass
class Markers(DataClassJsonMixin):
    """ """

    project_id: Optional[str]
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    markers: Optional[List[Marker]]
    """"""

    updated_datetime: Optional[str]
    """"""
