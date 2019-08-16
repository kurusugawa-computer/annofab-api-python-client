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

from annofabapi.models import InspectionStatus, TaskPhase

OneOfInspectionDataPointInspectionDataPolylineInspectionDataTime = Dict[str, Any]


@dataclass_json
@dataclass
class Inspection:
    """
    検査コメント
    """
    project_id: str
    """"""

    task_id: str
    """"""

    input_data_id: str
    """"""

    inspection_id: str
    """"""

    phase: TaskPhase
    """"""

    phase_stage: Optional[int]
    """"""

    commenter_account_id: str
    """"""

    annotation_id: Optional[str]
    """"""

    data: OneOfInspectionDataPointInspectionDataPolylineInspectionDataTime
    """"""

    parent_inspection_id: Optional[str]
    """"""

    phrases: Optional[List[str]]
    """選択された定型指摘ID. 未選択時は空"""

    comment: Optional[str]
    """"""

    status: InspectionStatus
    """"""

    created_datetime: str
    """"""

    updated_datetime: Optional[str]
    """新規作成時は未指定、更新時は必須（更新前の日時） """
