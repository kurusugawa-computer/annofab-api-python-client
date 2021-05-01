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

from annofabapi.models import AdditionalDataDefinitionType, AnnotationType

AdditionalDataDefaultType = Union[bool, int, str]

AdditionalDataRestrictionCondition = Dict[str, Any]

AnnotationSpecsOption = Dict[str, Any]


@dataclass
class Keybind(DataClassJsonMixin):
    """ """

    code: str
    """"""

    shift: bool
    """"""

    ctrl: bool
    """"""

    alt: bool
    """"""


@dataclass
class PositionForMinimumBoundingBoxInsertion(DataClassJsonMixin):
    """
    `annotation_type` が `bounding_box` かつ `min_warn_rule` が `and` または `or` の場合のみ、挿入する最小矩形アノテーションの原点を指定できます。 画像左上の座標が「x=0, y=0」です。 未指定、もしくは「画像外に飛び出たアノテーション」を許可していないにも関わらず飛び出してしまう場合は、表示範囲の中央に挿入されます。 「スキャンした帳票の記入欄」や「定点カメラで撮影した製品ラベル」など、アノテーションしたい位置やサイズが多くの画像で共通している場合に便利です。  `annotation_type` が `bounding_box` 以外の場合は必ず未指定となります。
    """

    x: int
    """"""

    y: int
    """"""


@dataclass
class LabelV1BoundingBoxMetadata(DataClassJsonMixin):
    """ """

    min_width: int
    """"""

    min_height: int
    """"""

    min_warn_rule: str
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

    has_direction: Optional[bool]
    """`annotation_type` が `polyline` の場合、アノテーションに向きを持たせるかどうかを指定できます。 この値が `true` の場合、AnnoFabの標準画像エディタ上ではポリラインの向きを示す矢印が描画されるようになります。  `annotationType` が `polyline` 以外の場合は必ず `false` となります。 """


@dataclass
class LabelV1SegmentationMetadata(DataClassJsonMixin):
    """ """

    min_width: int
    """"""

    min_height: int
    """"""

    min_warn_rule: str
    """"""

    tolerance: Optional[int]
    """"""


@dataclass
class InternationalizationMessageMessages(DataClassJsonMixin):
    """ """

    lang: str
    """"""

    message: str
    """"""


@dataclass
class InternationalizationMessage(DataClassJsonMixin):
    """ """

    messages: List[InternationalizationMessageMessages]
    """"""

    default_lang: str
    """"""


@dataclass
class InspectionPhrase(DataClassJsonMixin):
    """ """

    id: str
    """"""

    text: InternationalizationMessage
    """"""


@dataclass
class AnnotationSpecsHistory(DataClassJsonMixin):
    """ """

    history_id: str
    """"""

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    updated_datetime: str
    """"""

    url: str
    """"""

    account_id: Optional[str]
    """"""

    comment: Optional[str]
    """"""


@dataclass
class Color(DataClassJsonMixin):
    """ """

    red: int
    """"""

    green: int
    """"""

    blue: int
    """"""


@dataclass
class AdditionalDataDefinitionV1Choices(DataClassJsonMixin):
    """ """

    choice_id: str
    """"""

    name: InternationalizationMessage
    """"""

    keybind: Optional[List[Keybind]]
    """"""


@dataclass
class AdditionalDataDefinitionV1(DataClassJsonMixin):
    """ """

    additional_data_definition_id: str
    """"""

    read_only: Optional[bool]
    """"""

    name: Optional[InternationalizationMessage]
    """"""

    default: Optional[AdditionalDataDefaultType]
    """"""

    keybind: Optional[List[Keybind]]
    """"""

    type: AdditionalDataDefinitionType
    """"""

    choices: Optional[List[AdditionalDataDefinitionV1Choices]]
    """"""

    regex: Optional[str]
    """"""

    label_ids: Optional[List[str]]
    """リンク属性において、リンク先として指定可能なラベルID（空の場合制限なし）"""

    required: Optional[bool]
    """リンク属性において、入力を必須とするかどうか"""

    metadata: Optional[Dict[str, str]]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class AdditionalDataDefinitionV2(DataClassJsonMixin):
    """ """

    additional_data_definition_id: str
    """"""

    read_only: Optional[bool]
    """"""

    name: InternationalizationMessage
    """"""

    default: Optional[AdditionalDataDefaultType]
    """"""

    keybind: Optional[List[Keybind]]
    """"""

    type: AdditionalDataDefinitionType
    """"""

    choices: Optional[List[AdditionalDataDefinitionV1Choices]]
    """"""

    metadata: Optional[Dict[str, str]]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class AnnotationEditorFeature(DataClassJsonMixin):
    """ """

    append: bool
    """"""

    erase: bool
    """"""

    freehand: bool
    """"""

    rectangle_fill: bool
    """"""

    polygon_fill: bool
    """"""

    fill_near: bool
    """"""


@dataclass
class LabelV1(DataClassJsonMixin):
    """ """

    label_id: str
    """"""

    label_name: InternationalizationMessage
    """"""

    keybind: List[Keybind]
    """"""

    annotation_type: AnnotationType
    """"""

    bounding_box_metadata: Optional[LabelV1BoundingBoxMetadata]
    """"""

    segmentation_metadata: Optional[LabelV1SegmentationMetadata]
    """"""

    additional_data_definitions: List[AdditionalDataDefinitionV1]
    """"""

    color: Color
    """"""

    annotation_editor_feature: AnnotationEditorFeature
    """"""

    allow_out_of_image_bounds: Optional[bool]
    """"""

    metadata: Optional[Dict[str, str]]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class LabelV2(DataClassJsonMixin):
    """ """

    label_id: str
    """"""

    label_name: InternationalizationMessage
    """"""

    keybind: List[Keybind]
    """"""

    annotation_type: AnnotationType
    """"""

    bounding_box_metadata: Optional[LabelV1BoundingBoxMetadata]
    """"""

    segmentation_metadata: Optional[LabelV1SegmentationMetadata]
    """"""

    additional_data_definitions: List[str]
    """"""

    color: Color
    """"""

    annotation_editor_feature: AnnotationEditorFeature
    """"""

    allow_out_of_image_bounds: Optional[bool]
    """"""

    metadata: Optional[Dict[str, str]]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class AdditionalDataRestriction(DataClassJsonMixin):
    """ """

    additional_data_definition_id: str
    """"""

    condition: AdditionalDataRestrictionCondition
    """"""


@dataclass
class AnnotationSpecsV1(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    labels: List[LabelV1]
    """"""

    inspection_phrases: List[InspectionPhrase]
    """"""

    updated_datetime: Optional[str]
    """アノテーション仕様の最終更新時刻 """

    option: Optional[AnnotationSpecsOption]
    """"""

    metadata: Dict[str, str]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class AnnotationSpecsV2(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    labels: List[LabelV2]
    """"""

    additionals: List[AdditionalDataDefinitionV2]
    """"""

    restrictions: List[AdditionalDataRestriction]
    """"""

    inspection_phrases: List[InspectionPhrase]
    """"""

    format_version: str
    """"""

    updated_datetime: Optional[str]
    """アノテーション仕様の最終更新時刻 """

    option: Optional[AnnotationSpecsOption]
    """"""

    metadata: Dict[str, str]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """
