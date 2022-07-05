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
    """タスク履歴ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    started_datetime: Optional[str]
    """開始日時"""

    ended_datetime: Optional[str]
    """終了日時"""

    accumulated_labor_time_milliseconds: str
    """累計実作業時間（ISO 8601 duration）"""

    phase: TaskPhase
    """"""

    phase_stage: int
    """タスクのフェーズのステージ番号"""

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
    """タスクのフェーズのステージ番号"""

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
    """現在のフェーズが開始された日時"""

    updated_datetime: str
    """更新日時"""

    operation_updated_datetime: str
    """タスクのステータスやフェーズ、担当者などが更新されたときの日時"""

    sampling: Optional[str]
    """検査抜取検査/抜取受入によって、どのフェーズがスキップされたか  * `inspection_skipped` - 抜取検査の対象外となり、検査フェーズがスキップされた * `inspection_stages_skipped` - 抜取検査の対象外となり、検査フェーズのステージの一部がスキップされた * `acceptance_skipped` - 抜取受入の対象外となり、受入フェーズがスキップされた * `inspection_and_acceptance_skipped` - 抜取検査・抜取受入の対象外となり、検査・受入フェーズがスキップされた  未指定ならば、どのフェーズもスキップされていません。 """

    metadata: Optional[Dict[str, Any]]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 keyにはメタデータ名、valueには値を指定してください。  keyに指定できる文字種は次の通りです。  * 半角英数字 * `_` (アンダースコア) * `-` (ハイフン)  valueに指定できる値は次の通りです。  * 文字列 * 数値 * 真偽値 """
