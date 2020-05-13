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

from annofabapi.models import AssigneeRuleOfResubmittedTask, InputDataType, ProjectStatus, TaskAssignmentType


@dataclass_json
@dataclass
class ProjectSummary:
    """
    
    """

    last_tasks_updated_datetime: Optional[str]
    """タスクの最終更新日時"""


@dataclass_json
@dataclass
class ProjectConfiguration:
    """
    
    """

    number_of_inspections: Optional[int]
    """検査回数。 * 0回：教師付け -> 受入 * 1回：教師付け -> 検査 -> 受入 * n回(n >= 2)：教師付け -> 検査1 -> ... -> 検査n -> 受入 """

    assignee_rule_of_resubmitted_task: Optional[AssigneeRuleOfResubmittedTask]
    """"""

    task_assignment_type: Optional[TaskAssignmentType]
    """"""

    max_tasks_per_member: Optional[int]
    """保留中のタスクを除き、1人（オーナー以外）に割り当てられるタスク数上限。未指定の場合は10件として扱う。"""

    max_tasks_per_member_including_hold: Optional[int]
    """保留中のタスクを含めて、1人（オーナー以外）に割り当てられるタスク数上限。未指定の場合は20件として扱う。"""

    input_data_set_id_list: Optional[List[str]]
    """このフィールドは内部用でまだ何も意味を成しません。今は空配列を指定してください。"""

    input_data_max_long_side_length: Optional[int]
    """入力データ画像の長辺の最大値（未指定時は4096px）。  画像をアップロードすると、長辺がこの値になるように画像が自動で圧縮されます。 アノテーションの座標は、もとの解像度の画像でつけたものに復元されます。  大きな数値を設定すると入力データ画像のサイズが大きくなり、生産性低下やブラウザで画像を表示できない懸念があります。注意して設定してください。 """

    sampling_inspection_rate: Optional[int]
    """抜取検査率。0-100のパーセント値で指定し、未指定の場合は100%として扱う。"""

    sampling_acceptance_rate: Optional[int]
    """抜取受入率。0-100のパーセント値で指定し、未指定の場合は100%として扱う。"""

    private_storage_aws_iam_role_arn: Optional[str]
    """AWS IAMロール。ビジネスプランでのS3プライベートストレージの認可で使います。 [S3プライベートストレージの認可の設定についてはこちら](/docs/faq/#m0b240)をご覧ください。 """


@dataclass_json
@dataclass
class Project:
    """
    
    """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    organization_id: str
    """組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    title: str
    """プロジェクトのタイトル"""

    overview: Optional[str]
    """プロジェクトの概要"""

    project_status: ProjectStatus
    """"""

    input_data_type: InputDataType
    """"""

    configuration: ProjectConfiguration
    """"""

    created_datetime: str
    """"""

    updated_datetime: str
    """"""

    summary: ProjectSummary
    """"""
