import warnings  # pylint: disable=unused-import
from dataclasses import dataclass
from typing import Any, Dict, List, NewType, Optional, Tuple, Union  # pylint: disable=unused-import

from dataclasses_json import dataclass_json

from annofabapi.models import (AccountAuthority, AdditionalDataDefinitionType, AnnotationDataHoldingType,
                               AnnotationType, AssigneeRuleOfResubmittedTask, InputDataOrder, InputDataType,
                               InspectionStatus, OrganizationMemberRole, OrganizationMemberStatus, PricePlan,
                               ProjectMemberRole, ProjectMemberStatus, ProjectStatus, TaskPhase, TaskStatus)



@dataclass_json
@dataclass
class TaskHistory:
    """
    タスクのあるフェーズで、誰がいつどれくらいの作業時間を費やしたかを表すタスク履歴です。
    """
    project_id: str
    """"""

    task_id: str
    """"""

    task_history_id: str
    """"""

    started_datetime: str
    """"""

    ended_datetime: str
    """"""

    accumulated_labor_time_milliseconds: str
    """"""

    phase: TaskPhase
    """"""

    phase_stage: int
    """"""

    account_id: str
    """"""


@dataclass_json
@dataclass
class TaskHistoryEvent:
    """
    タスク履歴イベントは、タスクの状態が変化した１時点を表します。作業時間は、複数のこれらイベントを集約して計算するものなので、このオブジェクトには含まれません。
    """
    project_id: str
    """"""

    task_id: str
    """"""

    task_history_id: str
    """"""

    created_datetime: str
    """"""

    phase: TaskPhase
    """"""

    phase_stage: int
    """"""

    status: TaskStatus
    """"""

    account_id: str
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





@dataclass_json
@dataclass
class Task:
    """

    """
    project_id: str
    """"""

    task_id: str
    """"""

    phase: TaskPhase
    """"""

    phase_stage: int
    """"""

    status: TaskStatus
    """"""

    input_data_id_list: List[str]
    """"""

    account_id: str
    """"""

    histories_by_phase: List[TaskHistoryShort]
    """"""

    # work_timespan: int
    work_time_span: int
    """累計実作業時間(ミリ秒)"""

    number_of_rejections: int
    """このタスクが差戻しされた回数（すべてのフェーズでの差戻し回数の合計  このフィールドは、どのフェーズで何回差戻されたかを区別できないため、廃止予定です。 `histories_by_phase` で各フェーズの回数を計算することで、差戻し回数が分かります。  例）`acceptance`フェーズが3回ある場合、`acceptance`フェーズで2回差し戻しされたことになります。 """

    started_datetime: str
    """"""

    updated_datetime: str
    """"""

    sampling: str
    """* 'inspection_skipped' - このタスクが抜取検査の対象外となり、検査フェーズをスキップしたことを表す。 * 'inspection_stages_skipped' - このタスクが抜取検査の対象外となり、検査フェーズのステージを一部スキップしたことを表す。 * `acceptance_skipped` - このタスクが抜取検査の対象外となり、受入フェーズをスキップしたことを表す。 * `inspection_and_acceptance_skipped` - このタスクが抜取検査の対象外となり、検査・受入フェーズをスキップしたことを表す  未指定時はこのタスクが抜取検査の対象となったことを表す。(通常のワークフローを通過する) """

