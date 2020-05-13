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

from annofabapi.models import JobStatus, JobType


@dataclass_json
@dataclass
class JobInfo:
    """
    
    """

    project_id: Optional[str]
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    job_type: Optional[JobType]
    """"""

    job_id: Optional[str]
    """"""

    job_status: Optional[JobStatus]
    """"""

    job_execution: Optional[Dict[str, Any]]
    """ジョブの内部情報"""

    job_detail: Optional[Dict[str, Any]]
    """ジョブ結果の内部情報"""

    created_datetime: Optional[str]
    """"""

    updated_datetime: Optional[str]
    """"""
