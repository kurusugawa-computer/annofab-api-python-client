from typing import Any

import isodate

from annofabapi.pydantic_models.task_phase import TaskPhase


def find_rejected_task_history_indices(task_history_list: list[dict[str, Any]]) -> list[int]:
    """
    差し戻されたタスク履歴のインデックス番号（0始まり）を返します。

    Args:
        task_history_list: `get_task_histories` APIのレスポンス

    Returns:
        差し戻されたタスク履歴のインデックス番号のリスト
    """
    index_list = []
    for index, history in enumerate(task_history_list):
        # 検査/受入フェーズで作業が行われているか
        if not (
            history["phase"] in {TaskPhase.INSPECTION.value, TaskPhase.ACCEPTANCE.value}
            and isodate.parse_duration(history["accumulated_labor_time_milliseconds"]).total_seconds() > 0
            and history["account_id"] is not None
            and history["started_datetime"] is not None
            and history["ended_datetime"] is not None
        ):
            continue
        # 直後の履歴が教師付フェーズならば、差し戻されたとみなす
        next_index = index + 1
        if next_index >= len(task_history_list):
            # 対象の履歴は最後の履歴
            continue

        next_history = task_history_list[next_index]
        if next_history["phase"] == TaskPhase.ANNOTATION.value:
            index_list.append(index)

    return index_list
