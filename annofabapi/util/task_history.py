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


def get_task_creation_datetime(task: dict[str, Any], task_history_list: list[dict[str, Any]]) -> str:
    """タスクが作成された日時を取得します。

    Args:
        task: タスク情報。
            タスクが作成された直後は ``task_history_list`` に有効な日時が格納されていないので、
            ``operation_updated_datetime`` をタスク作成日時とします。
        task_history_list: ``get_task_histories`` APIのレスポンス

    Returns:
        タスクの作成日時

    Notes:
        2020-12-08以前に作成されたタスクでは、タスクの作成日時を取得できません。
        2020-12-08以前に作成されたタスクでは、先頭のタスク履歴は「タスク作成」ではなく、「教師付け作業」の履歴だからです。
        https://annofab.com/docs/releases/2020.html#v01020

    Raises:
        ValueError: 2020-12-08以前に作成されたタスクの情報を指定した場合
    """
    assert len(task_history_list) > 0
    first_history = task_history_list[0]

    if (
        first_history["account_id"] is None
        and first_history["accumulated_labor_time_milliseconds"] == "PT0S"
        and first_history["phase"] == TaskPhase.ANNOTATION.value
    ):
        if len(task_history_list) == 1:
            # 一度も作業されていないタスクは、先頭のタスク履歴のstarted_datetimeはNoneである
            # 替わりにタスクの`operation_updated_datetime`をタスク作成日時とする
            assert task["operation_updated_datetime"] is not None
            return task["operation_updated_datetime"]

        assert first_history["started_datetime"] is not None
        return first_history["started_datetime"]

    raise ValueError("2020-12-08以前に作成されたタスクのため、タスクの作成日時を取得できません。")
