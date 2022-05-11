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

    job_execution: Optional[Dict[str, Any]]
    """ジョブの内部情報"""

    job_detail: Optional[Dict[str, Any]]
    """ジョブ結果の内部情報"""

    errors: Errors
    """"""

    created_datetime: str
    """作成日時"""

    updated_datetime: str
    """更新日時"""
