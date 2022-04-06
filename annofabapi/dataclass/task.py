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

from annofabapi.models import TaskPhase, TaskStatus


@dataclass
class TaskHistory(DataClassJsonMixin):
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
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """


@dataclass
class TaskHistoryShort(DataClassJsonMixin):
    """
    タスクのあるフェーズを誰が担当したかを表します。
    """

    phase: TaskPhase
    """"""

    phase_stage: int
    """"""

    account_id: str
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    worked: Optional[bool]
    """そのフェーズでタスクの作業を行ったかどうか（行った場合はtrue）"""


@dataclass
class Task(DataClassJsonMixin):
    """ """

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
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    histories_by_phase: List[TaskHistoryShort]
    """簡易的なタスク履歴（あるフェーズを誰が担当したか）"""

    work_time_span: int
    """累計実作業時間(ミリ秒)"""

    number_of_rejections: int
    """このタスクが差戻しされた回数（すべてのフェーズでの差戻し回数の合計  このフィールドは、どのフェーズで何回差戻されたかを区別できないため、廃止予定です。 `histories_by_phase` で各フェーズの回数を計算することで、差戻し回数が分かります。  例）`acceptance`フェーズが3回ある場合、`acceptance`フェーズで2回差し戻しされたことになります。 """

    started_datetime: Optional[str]
    """"""

    updated_datetime: str
    """"""

    sampling: Optional[str]
    """* `inspection_skipped` - このタスクが抜取検査の対象外となり、検査フェーズをスキップしたことを表す。 * `inspection_stages_skipped` - このタスクが抜取検査の対象外となり、検査フェーズのステージを一部スキップしたことを表す。 * `acceptance_skipped` - このタスクが抜取検査の対象外となり、受入フェーズをスキップしたことを表す。 * `inspection_and_acceptance_skipped` - このタスクが抜取検査の対象外となり、検査・受入フェーズをスキップしたことを表す  未指定時はこのタスクが抜取検査の対象となったことを表す。(通常のワークフローを通過する) """

    metadata: Optional[Dict[str, Any]]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 keyにはメタデータ名、valueには値を指定してください。  keyに指定できる文字種は次の通りです。  * 半角英数字 * `_` (アンダースコア) * `-` (ハイフン)  valueに指定できる値は次の通りです。  * 文字列 * 数値 * 真偽値 """
