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

from annofabapi.models import (AdditionalDataDefinitionType, AnnotationDataHoldingType, AnnotationType,
                               InternationalizationMessage, TaskPhase, TaskStatus)

OneOfstringFullAnnotationData = Dict[str, Any]
FullAnnotationData = Dict[str, Any]


@dataclass_json
@dataclass
class Point:
    """
    座標
    """
    x: int
    """"""

    y: int
    """"""
@dataclass_json
@dataclass
class AdditionalData:
    """
    
    """
    additional_data_definition_id: str
    """"""

    flag: Optional[bool]
    """"""

    interger: Optional[int]
    """"""

    comment: Optional[str]
    """"""

    choice: Optional[str]
    """"""
@dataclass_json
@dataclass
class FullAnnotationAdditionalData:
    """
    
    """
    additional_data_definition_id: Optional[str]
    """"""

    additional_data_definition_name: Optional[InternationalizationMessage]
    """"""

    type: Optional[AdditionalDataDefinitionType]
    """"""

    flag: Optional[bool]
    """typeがflagの場合に、フラグのON(true)またはOFF(false)が格納される"""

    integer: Optional[int]
    """typeがintegerの場合に、整数値が格納される"""

    comment: Optional[str]
    """* typeがcommentの場合、コメントの値 * typeがtrackingの場合、トラッキングID * typeがlinkの場合、リンク先のアノテーションID """

    choice: Optional[str]
    """"""

    choice_name: Optional[InternationalizationMessage]
    """"""
@dataclass_json
@dataclass
class FullAnnotationDetail:
    """
    
    """
    annotation_id: Optional[str]
    """annotation_type が classification の場合は label_id と同じ値が格納されます。 """

    user_id: Optional[str]
    """"""

    label_id: Optional[str]
    """"""

    label_name: Optional[InternationalizationMessage]
    """"""

    annotation_type: Optional[AnnotationType]
    """"""

    data_holding_type: Optional[AnnotationDataHoldingType]
    """"""

    data: Optional[FullAnnotationData]
    """"""

    additional_data_list: Optional[List[FullAnnotationAdditionalData]]
    """"""
@dataclass_json
@dataclass
class FullAnnotation:
    """
    
    """
    project_id: Optional[str]
    """"""

    task_id: Optional[str]
    """"""

    task_phase: Optional[TaskPhase]
    """"""

    task_phase_stage: Optional[int]
    """"""

    task_status: Optional[TaskStatus]
    """"""

    input_data_id: Optional[str]
    """"""

    input_data_name: Optional[str]
    """"""

    detail: Optional[List[FullAnnotationDetail]]
    """"""

    updated_datetime: Optional[str]
    """"""
@dataclass_json
@dataclass
class SimpleAnnotationDetail:
    """
    
    """
    label: Optional[str]
    """アノテーション仕様のラベル名です。 """

    annotation_id: Optional[str]
    """個々のアノテーションにつけられたIDです。 """

    data: Optional[FullAnnotationData]
    """"""

    attributes: Optional[Dict]
    """キーに属性の名前、値に各属性の値が入った辞書構造です。 """
@dataclass_json
@dataclass
class SimpleAnnotation:
    """
    
    """
    annotation_format_version: Optional[str]
    """アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、AnnoFabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 """

    project_id: Optional[str]
    """"""

    task_id: Optional[str]
    """"""

    task_phase: Optional[TaskPhase]
    """"""

    task_phase_stage: Optional[int]
    """"""

    task_status: Optional[TaskStatus]
    """"""

    input_data_id: Optional[str]
    """"""

    input_data_name: Optional[str]
    """"""

    details: Optional[List[SimpleAnnotationDetail]]
    """"""
@dataclass_json
@dataclass
class SingleAnnotationDetail:
    """
    
    """
    annotation_id: Optional[str]
    """annotation_type が classification の場合は label_id と同じ値が格納されます。 """

    account_id: Optional[str]
    """"""

    label_id: Optional[str]
    """"""

    data_holding_type: Optional[AnnotationDataHoldingType]
    """"""

    data: Optional[FullAnnotationData]
    """"""

    etag: Optional[str]
    """data_holding_typeがouterの場合のみ存在し、データのETagが格納される"""

    url: Optional[str]
    """data_holding_typeがouterの場合のみ存在し、データへの一時URLが格納される"""

    additional_data_list: Optional[List[FullAnnotationAdditionalData]]
    """"""

    created_datetime: Optional[str]
    """"""

    updated_datetime: Optional[str]
    """"""
@dataclass_json
@dataclass
class SingleAnnotation:
    """
    
    """
    project_id: Optional[str]
    """"""

    task_id: Optional[str]
    """"""

    input_data_id: Optional[str]
    """"""

    detail: Optional[SingleAnnotationDetail]
    """"""

    updated_datetime: Optional[str]
    """"""
