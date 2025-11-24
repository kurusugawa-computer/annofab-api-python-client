# pylint: disable=too-many-lines,trailing-whitespace

"""
Deprecated: 2025-02-01 以降に廃止します
"""

from dataclasses import dataclass
from typing import Any  # pylint: disable=unused-import

from dataclasses_json import DataClassJsonMixin

from annofabapi.models import Errors, JobStatus, ProjectJobType


@dataclass
class ProjectJobInfo(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    job_type: ProjectJobType
    """"""

    job_id: str
    """ジョブID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    job_status: JobStatus
    """"""

    job_execution: dict[str, Any] | None
    """ジョブの内部情報"""

    job_detail: dict[str, Any] | None
    """ジョブ結果の内部情報"""

    errors: Errors
    """"""

    created_datetime: str
    """作成日時"""

    updated_datetime: str
    """更新日時"""
