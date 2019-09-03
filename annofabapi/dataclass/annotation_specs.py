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
class LabelBoundingBoxMetadata:
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

    tolerance: Optional[int]
    """"""
@dataclass_json
@dataclass
class LabelSegmentationMetadata:
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
class AdditionalDataDefinitionChoices:
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
class AdditionalDataDefinition:
    """
    
    """
    additional_data_definition_id: Optional[str]
    """"""

    read_only: Optional[bool]
    """"""

    name: Optional[InternationalizationMessage]
    """"""

    keybind: Optional[List[Keybind]]
    """"""

    type: Optional[AdditionalDataDefinitionType]
    """"""

    choices: Optional[List[AdditionalDataDefinitionChoices]]
    """"""

    regex: Optional[str]
    """"""

    label_ids: Optional[List[str]]
    """リンク属性において、リンク先として指定可能なラベルID（空の場合制限なし）"""

    required: Optional[bool]
    """リンク属性において、入力を必須とするかどうか"""
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
class Label:
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

    bounding_box_metadata: Optional[LabelBoundingBoxMetadata]
    """"""

    segmentation_metadata: Optional[LabelSegmentationMetadata]
    """"""

    additional_data_definitions: Optional[List[AdditionalDataDefinition]]
    """"""

    color: Optional[Color]
    """"""

    annotation_editor_feature: Optional[AnnotationEditorFeature]
    """"""

    allow_out_of_image_bounds: Optional[bool]
    """"""
@dataclass_json
@dataclass
class AnnotationSpecs:
    """
    
    """
    project_id: Optional[str]
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    labels: Optional[List[Label]]
    """"""

    inspection_phrases: Optional[List[InspectionPhrase]]
    """"""
