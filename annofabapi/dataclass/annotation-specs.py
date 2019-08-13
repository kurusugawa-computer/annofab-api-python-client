import warnings  # pylint: disable=unused-import
from dataclasses import dataclass
from typing import Any, Dict, List, NewType, Optional, Tuple, Union  # pylint: disable=unused-import

from dataclasses_json import dataclass_json

from annofabapi.models import (AccountAuthority, AdditionalDataDefinitionType, AnnotationDataHoldingType,
                               AnnotationType, AssigneeRuleOfResubmittedTask, InputDataOrder, InputDataType,
                               InspectionStatus, OrganizationMemberRole, OrganizationMemberStatus, PricePlan,
                               ProjectMemberRole, ProjectMemberStatus, ProjectStatus, TaskPhase, TaskStatus)


@dataclass_json
@dataclass
class Keybind:
    """

    """
    code: str
    """"""

    shift: bool
    """"""

    ctrl: bool
    """"""

    alt: bool
    """"""


@dataclass_json
@dataclass
class LabelBoundingBoxMetadata:
    """

    """
    min_width: int
    """"""

    min_height: int
    """"""

    min_warn_rule: str
    """"""

    min_area: int
    """"""

    max_vertices: int
    """"""

    min_vertices: int
    """"""

    tolerance: int
    """"""


@dataclass_json
@dataclass
class LabelSegmentationMetadata:
    """

    """
    min_width: int
    """"""

    min_height: int
    """"""

    min_warn_rule: str
    """"""

    tolerance: int
    """"""


@dataclass_json
@dataclass
class InternationalizationMessageMessages:
    """

    """
    lang: str
    """"""

    message: str
    """"""


@dataclass_json
@dataclass
class InternationalizationMessage:
    """

    """
    messages: List[InternationalizationMessageMessages]
    """"""

    default_lang: str
    """"""


@dataclass_json
@dataclass
class InspectionPhrase:
    """

    """
    id: str
    """"""

    text: InternationalizationMessage
    """"""

@dataclass_json
@dataclass
class AnnotationSpecsHistory:
    """

    """
    project_id: str
    """"""

    updated_datetime: str
    """"""

    url: str
    """"""

    account_id: str
    """"""

    comment: str
    """"""


@dataclass_json
@dataclass
class Color:
    """

    """
    red: int
    """"""

    green: int
    """"""

    blue: int
    """"""


@dataclass_json
@dataclass
class AdditionalDataDefinitionChoices:
    """

    """
    choice_id: str
    """"""

    name: InternationalizationMessage
    """"""

    keybind: List[Keybind]
    """"""

@dataclass_json
@dataclass
class AdditionalDataDefinition:
    """

    """
    additional_data_definition_id: str
    """"""

    read_only: bool
    """"""

    name: InternationalizationMessage
    """"""

    keybind: List[Keybind]
    """"""

    type: AdditionalDataDefinitionType
    """"""

    choices: List[AdditionalDataDefinitionChoices]
    """"""

    regex: str
    """"""

    label_ids: List[str]
    """リンク属性において、リンク先として指定可能なラベルID（空の場合制限なし）"""

    required: bool
    """リンク属性において、入力を必須とするかどうか"""

@dataclass_json
@dataclass
class Label:
    """

    """
    label_id: str
    """"""

    label_name: InternationalizationMessage
    """"""

    keybind: List[Keybind]
    """"""

    annotation_type: AnnotationType
    """"""

    bounding_box_metadata: LabelBoundingBoxMetadata
    """"""

    segmentation_metadata: LabelSegmentationMetadata
    """"""

    additional_data_definitions: List[AdditionalDataDefinition]
    """"""

    color: Color
    """"""

    annotation_editor_feature: AnnotationEditorFeature
    """"""

    allow_out_of_image_bounds: bool
    """"""



@dataclass_json
@dataclass
class AnnotationSpecs:
    """

    """
    project_id: str
    """"""

    labels: List[Label]
    """"""

    inspection_phrases: List[InspectionPhrase]
    """"""
