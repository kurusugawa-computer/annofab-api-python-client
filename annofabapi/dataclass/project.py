# ruff: noqa: E501
# pylint: disable=too-many-lines,trailing-whitespace

"""
annofabapiのmodelをDataClassで定義したクラス

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照.
    oneOf, allOfなどは正しく表現できない可能性がある。
"""

from dataclasses import dataclass
from typing import Any, Optional  # pylint: disable=unused-import

from dataclasses_json import DataClassJsonMixin

from annofabapi.models import InputDataType, ProjectStatus

ProjectConfigurationGet = dict[str, Any]


@dataclass
class ProjectSummary(DataClassJsonMixin):
    """
    プロジェクトのサマリー情報
    """

    last_tasks_updated_datetime: Optional[str]
    """タスクの最終更新日時"""


@dataclass
class Project(DataClassJsonMixin):
    """ """

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

    configuration: ProjectConfigurationGet
    """"""

    created_datetime: str
    """作成日時"""

    updated_datetime: str
    """更新日時"""

    summary: ProjectSummary
    """"""
