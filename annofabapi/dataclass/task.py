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
class TaskHistory:
    """
    タスクのあるフェーズで、誰がいつどれくらいの作業時間を費やしたかを表すタスク履歴です。
    """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_history_id: str
    """"""

    started_datetime: Optional[str]
    """"""

    ended_datetime: Optional[str]
    """"""

    accumulated_labor_time_milliseconds: str
    """累計実作業時間（ISO 8601 duration）"""

    phase: TaskPhase
    """"""

    phase_stage: int
    """"""

    account_id: Optional[str]
    """"""


@dataclass_json
@dataclass
class TaskHistoryShort:
    """
    タスクのあるフェーズを誰が担当したかを表します。
    """

    phase: TaskPhase
    """"""

    phase_stage: int
    """"""

    account_id: str
    """"""

    worked: Optional[bool]
    """そのフェーズでタスクの作業を行ったかどうか（行った場合はtrue）"""


@dataclass_json
@dataclass
class Task:
    """
    
    """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    phase: TaskPhase
    """"""

    phase_stage: int
    """"""

    status: TaskStatus
    """"""

    input_data_id_list: List[str]
    """タスクに含まれる入力データのID"""

    account_id: Optional[str]
    """"""

    histories_by_phase: Optional[List[TaskHistoryShort]]
    """簡易的なタスク履歴（あるフェーズを誰が担当したか）"""

    work_time_span: int
    """累計実作業時間(ミリ秒)"""

    number_of_rejections: Optional[int]
    """このタスクが差戻しされた回数（すべてのフェーズでの差戻し回数の合計  このフィールドは、どのフェーズで何回差戻されたかを区別できないため、廃止予定です。 `histories_by_phase` で各フェーズの回数を計算することで、差戻し回数が分かります。  例）`acceptance`フェーズが3回ある場合、`acceptance`フェーズで2回差し戻しされたことになります。 """

    started_datetime: Optional[str]
    """"""

    updated_datetime: str
    """"""

    sampling: Optional[str]
    """* `inspection_skipped` - このタスクが抜取検査の対象外となり、検査フェーズをスキップしたことを表す。 * `inspection_stages_skipped` - このタスクが抜取検査の対象外となり、検査フェーズのステージを一部スキップしたことを表す。 * `acceptance_skipped` - このタスクが抜取検査の対象外となり、受入フェーズをスキップしたことを表す。 * `inspection_and_acceptance_skipped` - このタスクが抜取検査の対象外となり、検査・受入フェーズをスキップしたことを表す  未指定時はこのタスクが抜取検査の対象となったことを表す。(通常のワークフローを通過する) """
