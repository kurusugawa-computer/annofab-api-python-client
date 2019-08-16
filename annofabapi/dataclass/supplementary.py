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

# 列挙体の一覧
from annofabapi.models import (AccountAuthority, AdditionalDataDefinitionType, AnnotationDataHoldingType,
                               AnnotationType, AssigneeRuleOfResubmittedTask, InputDataOrder, InputDataType,
                               InspectionStatus, OrganizationMemberRole, OrganizationMemberStatus, PricePlan,
                               ProjectMemberRole, ProjectMemberStatus, ProjectStatus, TaskPhase, TaskStatus)




@dataclass_json
@dataclass
class SupplementaryData:
    """
    
    """
    project_id: Optional[str]
    """"""



    input_data_id: Optional[str]
    """"""



    supplementary_data_id: Optional[str]
    """"""



    supplementary_data_name: Optional[str]
    """表示用の名前"""



    supplementary_data_path: Optional[str]
    """補助情報の実体が保存されたパスです。 s3スキーマまたはhttpsスキーマのみサポートしています。 """



    url: Optional[str]
    """このフィールドはAF内部での利用のみを想定しており、依存しないでください。"""



    etag: Optional[str]
    """"""



    supplementary_data_type: Optional[str]
    """"""



    supplementary_data_number: Optional[int]
    """表示順を表す数値（昇順）。同じ入力データに対して複数の補助情報で表示順が重複する場合、順序不定になります。"""



    updated_datetime: Optional[str]
    """"""







