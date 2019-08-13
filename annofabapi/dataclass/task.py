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
class TaskGenerateRequest:
    """

    """
    task_generate_rule: OneOfTaskGenerateRuleByCountTaskGenerateRuleByDirectoryTaskGenerateRuleByInputDataCsv
    """* `TaskGenerateRuleByCount`: 1つのタスクに割りあてる入力データの個数を指定してタスクを生成します。 * `TaskGenerateRuleByDirectory`: 入力データ名をファイルパスに見立て、ディレクトリ単位でタスクを生成します。 """

    task_id_prefix: str
    """生成するタスクIDのプレフィックス"""

    project_last_updated_datetime: str
    """プロジェクトの最終更新日時。タスク生成の排他制御に使用。"""


@dataclass_json
@dataclass
class TaskGenerateRuleByCount:
    """
    1つのタスクに割りあてる入力データの個数を指定してタスクを生成します。
    """
    allow_duplicate_input_data: bool
    """falseのときは、既にタスクに使われている入力データを除外し、まだタスクに使われていない入力データだけを新しいタスクに割り当てます。trueのときは、既にタスクに使われている入力データを除外しません。"""

    input_data_count: int
    """1つのタスクに割り当てる入力データの個数"""

    input_data_order: InputDataOrder
    """"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """


@dataclass_json
@dataclass
class TaskGenerateRuleByDirectory:
    """
    入力データ名をファイルパスに見立て、ディレクトリ単位でタスクを生成します。<br>
    """
    input_data_name_prefix: str
    """タスク生成対象の入力データ名プレフィックス"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """


@dataclass_json
@dataclass
class TaskGenerateRuleByInputDataCsv:
    """
    各タスクへの入力データへの割当を記入したCSVへのS3上のパスを指定してタスクを生成します。
    """
    csv_data_path: str
    """各タスクへの入力データへの割当を記入したCSVへのS3上のパス"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """


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
class TaskValidation:
    """
    タスクの全入力データに対するバリデーション結果です。
    """
    project_id: str
    """"""

    task_id: str
    """"""

    inputs: List[InputDataSummary]
    """"""



@dataclass_json
@dataclass
class TasksInputsTask:
    """

    """
    task_id: str
    """"""

    phase: TaskPhase
    """"""

    status: TaskStatus
    """"""

    input_data_id_list: List[str]
    """"""



@dataclass_json
@dataclass
class TasksInputs:
    """

    """
    project_id: str
    """"""

    tasks: List[TasksInputsTask]
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

    work_timespan: int
    """累計実作業時間(ミリ秒)"""

    number_of_rejections: int
    """このタスクが差戻しされた回数（すべてのフェーズでの差戻し回数の合計  このフィールドは、どのフェーズで何回差戻されたかを区別できないため、廃止予定です。 `histories_by_phase` で各フェーズの回数を計算することで、差戻し回数が分かります。  例）`acceptance`フェーズが3回ある場合、`acceptance`フェーズで2回差し戻しされたことになります。 """

    started_datetime: str
    """"""

    updated_datetime: str
    """"""

    sampling: str
    """* 'inspection_skipped' - このタスクが抜取検査の対象外となり、検査フェーズをスキップしたことを表す。 * 'inspection_stages_skipped' - このタスクが抜取検査の対象外となり、検査フェーズのステージを一部スキップしたことを表す。 * `acceptance_skipped` - このタスクが抜取検査の対象外となり、受入フェーズをスキップしたことを表す。 * `inspection_and_acceptance_skipped` - このタスクが抜取検査の対象外となり、検査・受入フェーズをスキップしたことを表す  未指定時はこのタスクが抜取検査の対象となったことを表す。(通常のワークフローを通過する) """



@dataclass_json
@dataclass
class ValidationError:
    """

    """
    label_id: str
    """"""

    annotation_id: str
    """"""

    message: str
    """"""

    type: str
    """UnknownLabel"""

    annotation_ids: List[str]
    """"""

    additional_data_definition_id: str
    """"""

    additional_data: AdditionalData
    """"""


@dataclass_json
@dataclass
class InputDataSummary:
    """
    ある入力データのバリデーション結果です。入力データIDをキーに引けるようにMap[入力データID, バリデーション結果]となっています
    """
    input_data_id: str
    """"""

    inspection_summary: str
    """"""

    annotation_summaries: List[ValidationError]
    """"""
