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

InspectionData = Dict[str, Any]


@dataclass_json
@dataclass
class Inspection:
    """
    検査コメント
    """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    inspection_id: str
    """検査ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    phase: TaskPhase
    """"""

    phase_stage: int
    """検査コメントを付与したときのフェーズのステージ"""

    commenter_account_id: str
    """"""

    annotation_id: Optional[str]
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 """

    data: InspectionData
    """"""

    parent_inspection_id: Optional[str]
    """検査ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    phrases: Optional[List[str]]
    """参照している定型指摘のID。"""

    comment: str
    """検査コメントの中身 """

    status: InspectionStatus
    """"""

    created_datetime: str
    """"""

    updated_datetime: Optional[str]
    """"""
