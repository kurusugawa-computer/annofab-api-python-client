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

from annofabapi.models import AdditionalDataDefinitionType, AnnotationType

AdditionalDataDefaultType = Union[bool, int, str]

AdditionalDataRestrictionCondition = Dict[str, Any]

AnnotationSpecsOption = Dict[str, Any]


@dataclass_json
@dataclass
class Keybind:
    """
    
    """

    code: Optional[str]
    """"""

    shift: Optional[bool]
    """"""

    ctrl: Optional[bool]
    """"""

    alt: Optional[bool]
    """"""


@dataclass_json
@dataclass
class PositionForMinimumBoundingBoxInsertion:
    """
    `annotation_type` が `bounding_box` かつ `min_warn_rule` が `and` または `or` の場合のみ、挿入する最小矩形アノテーションの原点を指定できます。 画像左上の座標が「x=0, y=0」です。 未指定、もしくは「画像外に飛び出たアノテーション」を許可していないにも関わらず飛び出してしまう場合は、表示範囲の中央に挿入されます。 「スキャンした帳票の記入欄」や「定点カメラで撮影した製品ラベル」など、アノテーションしたい位置やサイズが多くの画像で共通している場合に便利です。  `annotation_type` が `bounding_box` 以外の場合は必ず未指定となります。 
    """

    x: int
    """"""

    y: int
    """"""


@dataclass_json
@dataclass
class LabelV1BoundingBoxMetadata:
    """
    
    """

    min_width: Optional[int]
    """"""

    min_height: Optional[int]
    """"""

    min_warn_rule: Optional[str]
    """"""

    min_area: Optional[int]
    """"""

    max_vertices: Optional[int]
    """"""

    min_vertices: Optional[int]
    """"""

    position_for_minimum_bounding_box_insertion: Optional[PositionForMinimumBoundingBoxInsertion]
    """"""

    tolerance: Optional[int]
    """"""


@dataclass_json
@dataclass
class LabelV1SegmentationMetadata:
    """
    
    """

    min_width: Optional[int]
    """"""

    min_height: Optional[int]
    """"""

    min_warn_rule: Optional[str]
    """"""

    tolerance: Optional[int]
    """"""


@dataclass_json
@dataclass
class InternationalizationMessageMessages:
    """
    
    """

    lang: Optional[str]
    """"""

    message: Optional[str]
    """"""


@dataclass_json
@dataclass
class InternationalizationMessage:
    """
    
    """

    messages: Optional[List[InternationalizationMessageMessages]]
    """"""

    default_lang: Optional[str]
    """"""


@dataclass_json
@dataclass
class InspectionPhrase:
    """
    
    """

    id: Optional[str]
    """"""

    text: Optional[InternationalizationMessage]
    """"""


@dataclass_json
@dataclass
class AnnotationSpecsHistory:
    """
    
    """

    history_id: Optional[str]
    """"""

    project_id: Optional[str]
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    updated_datetime: Optional[str]
    """"""

    url: Optional[str]
    """"""

    account_id: Optional[str]
    """"""

    comment: Optional[str]
    """"""


@dataclass_json
@dataclass
class Color:
    """
    
    """

    red: Optional[int]
    """"""

    green: Optional[int]
    """"""

    blue: Optional[int]
    """"""


@dataclass_json
@dataclass
class AdditionalDataDefinitionV1Choices:
    """
    
    """

    choice_id: Optional[str]
    """"""

    name: Optional[InternationalizationMessage]
    """"""

    keybind: Optional[List[Keybind]]
    """"""


@dataclass_json
@dataclass
class AdditionalDataDefinitionV1:
    """
    
    """

    additional_data_definition_id: Optional[str]
    """"""

    read_only: Optional[bool]
    """"""

    name: Optional[InternationalizationMessage]
    """"""

    default: Optional[AdditionalDataDefaultType]
    """"""

    keybind: Optional[List[Keybind]]
    """"""

    type: Optional[AdditionalDataDefinitionType]
    """"""

    choices: Optional[List[AdditionalDataDefinitionV1Choices]]
    """"""

    regex: Optional[str]
    """"""

    label_ids: Optional[List[str]]
    """リンク属性において、リンク先として指定可能なラベルID（空の場合制限なし）"""

    required: Optional[bool]
    """リンク属性において、入力を必須とするかどうか"""


@dataclass_json
@dataclass
class AdditionalDataDefinitionV2:
    """
    
    """

    additional_data_definition_id: Optional[str]
    """"""

    read_only: Optional[bool]
    """"""

    name: Optional[InternationalizationMessage]
    """"""

    default: Optional[AdditionalDataDefaultType]
    """"""

    keybind: Optional[List[Keybind]]
    """"""

    type: Optional[AdditionalDataDefinitionType]
    """"""

    choices: Optional[List[AdditionalDataDefinitionV1Choices]]
    """"""


@dataclass_json
@dataclass
class AnnotationEditorFeature:
    """
    
    """

    append: Optional[bool]
    """"""

    erase: Optional[bool]
    """"""

    freehand: Optional[bool]
    """"""

    rectangle_fill: Optional[bool]
    """"""

    polygon_fill: Optional[bool]
    """"""

    fill_near: Optional[bool]
    """"""


@dataclass_json
@dataclass
class LabelV1:
    """
    
    """

    label_id: Optional[str]
    """"""

    label_name: Optional[InternationalizationMessage]
    """"""

    keybind: Optional[List[Keybind]]
    """"""

    annotation_type: Optional[AnnotationType]
    """"""

    bounding_box_metadata: Optional[LabelV1BoundingBoxMetadata]
    """"""

    segmentation_metadata: Optional[LabelV1SegmentationMetadata]
    """"""

    additional_data_definitions: Optional[List[AdditionalDataDefinitionV1]]
    """"""

    color: Optional[Color]
    """"""

    annotation_editor_feature: Optional[AnnotationEditorFeature]
    """"""

    allow_out_of_image_bounds: Optional[bool]
    """"""


@dataclass_json
@dataclass
class LabelV2:
    """
    
    """

    label_id: Optional[str]
    """"""

    label_name: Optional[InternationalizationMessage]
    """"""

    keybind: Optional[List[Keybind]]
    """"""

    annotation_type: Optional[AnnotationType]
    """"""

    bounding_box_metadata: Optional[LabelV1BoundingBoxMetadata]
    """"""

    segmentation_metadata: Optional[LabelV1SegmentationMetadata]
    """"""

    additional_data_definitions: Optional[List[str]]
    """"""

    color: Optional[Color]
    """"""

    annotation_editor_feature: Optional[AnnotationEditorFeature]
    """"""

    allow_out_of_image_bounds: Optional[bool]
    """"""


@dataclass_json
@dataclass
class AdditionalDataRestriction:
    """
    
    """

    additional_data_definition_id: Optional[str]
    """"""

    condition: Optional[AdditionalDataRestrictionCondition]
    """"""


@dataclass_json
@dataclass
class AnnotationSpecsV1:
    """
    
    """

    project_id: Optional[str]
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    labels: Optional[List[LabelV1]]
    """"""

    inspection_phrases: Optional[List[InspectionPhrase]]
    """"""

    updated_datetime: Optional[str]
    """アノテーション仕様の最終更新時刻 """

    option: Optional[AnnotationSpecsOption]
    """"""


@dataclass_json
@dataclass
class AnnotationSpecsV2:
    """
    
    """

    project_id: Optional[str]
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    labels: Optional[List[LabelV2]]
    """"""

    additionals: Optional[List[AdditionalDataDefinitionV2]]
    """"""

    restrictions: Optional[List[AdditionalDataRestriction]]
    """"""

    inspection_phrases: Optional[List[InspectionPhrase]]
    """"""

    format_version: Optional[str]
    """"""

    updated_datetime: Optional[str]
    """アノテーション仕様の最終更新時刻 """

    option: Optional[AnnotationSpecsOption]
    """"""
