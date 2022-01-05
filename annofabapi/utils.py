import datetime
import logging
from typing import List, Optional

import dateutil
import dateutil.tz

from annofabapi.models import Task, TaskHistory, TaskHistoryShort, TaskPhase

logger = logging.getLogger(__name__)


#########################################
# Public Method
#########################################


def str_now() -> str:
    """
    現在日時をISO8601 拡張形式で取得する。

    Returns:
        ISO 8601 formatの現在日時

    """
    return to_iso8601_extension(datetime.datetime.now())


def to_iso8601_extension(d: datetime.datetime, tz: Optional[datetime.tzinfo] = None) -> str:
    """
    datetime.datetimeを、ISO8601 拡張形式のstringに変換する。
    ``2019-05-08T10:00:00.000+09:00``

    Args:
        d: datetimeオブジェクト
        tz: タイムゾーンオブジェクト。Noneの場合、ローカルのタイムゾーンを設定する。

    Returns:
        ISO 8601 拡張形式の日時
    """
    if tz is None:
        tz = dateutil.tz.tzlocal()
    d = d.astimezone(tz)
    return d.isoformat(timespec="milliseconds")


def get_task_history_index_skipped_acceptance(task_history_list: List[TaskHistory]) -> List[int]:
    """
    受入がスキップされたタスク履歴のインデックス番号（0始まり）を返す。

    Args:
        task_history_list: タスク履歴List

    Returns:
        受入フェーズがスキップされた履歴のインデックス番号（0始まり）。受入がスキップされていない場合は空リストを返す。

    """
    index_list = []
    for index, history in enumerate(task_history_list):
        if not (
            TaskPhase(history["phase"]) == TaskPhase.ACCEPTANCE
            and history["account_id"] is None
            and history["accumulated_labor_time_milliseconds"] == "PT0S"
            and history["started_datetime"] is not None
            and history["ended_datetime"] is not None
        ):
            continue

        if index + 1 < len(task_history_list):
            # 直後の履歴あり
            next_history = task_history_list[index + 1]
            if TaskPhase(next_history["phase"]) in [TaskPhase.ANNOTATION, TaskPhase.INSPECTION]:
                # 教師付フェーズ or 検査フェーズでの提出取消（直後が前段のフェーズ）
                pass
            else:
                # 受入スキップ
                index_list.append(index)
        else:
            # 直後の履歴がない
            index_list.append(index)

    return index_list


def get_task_history_index_skipped_inspection(task_history_list: List[TaskHistory]) -> List[int]:
    """
    検査フェーズがスキップされたタスク履歴のインデックス番号（0始まり）を返す。

    Args:
        task_history_list: タスク履歴List

    Returns:
        検査フェーズがスキップされた履歴のインデックス番号（0始まり）。検査がスキップされていない場合は空リストを返す。
    """
    index_list = []
    for index, history in enumerate(task_history_list):
        if not (
            TaskPhase(history["phase"]) == TaskPhase.INSPECTION
            and history["account_id"] is None
            and history["accumulated_labor_time_milliseconds"] == "PT0S"
            and history["started_datetime"] is not None
            and history["ended_datetime"] is not None
        ):
            continue

        if index + 1 < len(task_history_list):
            # 直後の履歴あり
            next_history = task_history_list[index + 1]
            if TaskPhase(next_history["phase"]) in [TaskPhase.ANNOTATION, TaskPhase.INSPECTION]:
                # 教師付フェーズ or 検査フェーズでの提出取消（直後が前段のフェーズ）
                pass
            else:
                # 検査スキップ
                index_list.append(index)
        else:
            # 直後の履歴がない
            index_list.append(index)

    return index_list


def get_number_of_rejections(task_histories: List[TaskHistoryShort], phase: TaskPhase, phase_stage: int = 1) -> int:
    """
    タスク履歴から、指定されたタスクフェーズでの差し戻し回数を取得する。

    Args:
        task_histories: タスク履歴
        phase: どのフェーズで差し戻されたか(TaskPhase.INSPECTIONかTaskPhase.ACCEPTANCE)
        phase_stage: どのフェーズステージで差し戻されたか。デフォルトは1。

    Returns:
        差し戻し回数
    """
    if phase not in [TaskPhase.INSPECTION, TaskPhase.ACCEPTANCE]:
        raise ValueError("引数'phase'には、'TaskPhase.INSPECTION'か'TaskPhase.ACCEPTANCE'を指定してください。")

    rejections_by_phase = 0
    for i, history in enumerate(task_histories):
        if not (history["phase"] == phase.value and history["phase_stage"] == phase_stage and history["worked"]):
            continue

        if i + 1 < len(task_histories) and task_histories[i + 1]["phase"] == TaskPhase.ANNOTATION.value:
            rejections_by_phase += 1

    return rejections_by_phase


def can_put_annotation(task: Task, my_account_id: str) -> bool:
    """
    対象タスクが、`put_annotation` APIで、アノテーションを更新できる状態かどうか。
    過去に担当者が割り当たっている場合、または現在の担当者が自分自身の場合は、アノテーションを更新できる。

    Args:
        task: 対象タスク
        my_account_id: 自分（ログインしているユーザ）のアカウントID

    Returns:
        Trueならば、タスクの状態を変更せずに`put_annotation` APIを実行できる。
    """
    # ログインユーザはプロジェクトオーナであること前提
    return len(task["histories_by_phase"]) == 0 or task["account_id"] == my_account_id
