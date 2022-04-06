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
    """言語コード。`en-US` (英語) または `ja-JP` (日本語) のみサポートしています。"""

    message: str
    """lang で指定された言語でのメッセージ"""


@dataclass
class InternationalizationMessage(DataClassJsonMixin):
    """ """

    messages: List[InternationalizationMessageMessages]
    """言語コードとメッセージ（テキスト）のリスト。  * アノテーションエディタなどでは、AnnoFabの表示言語（各ユーザーが個人設定で選んだ言語）のメッセージが使われます * [Simple Annotation](#section/Simple-Annotation-ZIP) では `en-US` のメッセージが使われます * いずれの場合でも、表示しようとした言語が `messages` に含まれない場合、 `default_lang` に指定した言語のメッセージが使われます """

    default_lang: str
    """希望された言語のメッセージが存在しない場合に、フォールバック先として使われる言語コード"""


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
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

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
    """選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    name: InternationalizationMessage
    """"""

    keybind: Optional[List[Keybind]]
    """"""


@dataclass
class AdditionalDataDefinitionV1(DataClassJsonMixin):
    """ """

    additional_data_definition_id: str
    """属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

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
    """ドロップダウンまたはラジオボタンの選択肢"""

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
    """属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

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
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

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
    """属性"""

    color: Color
    """"""

    annotation_editor_feature: AnnotationEditorFeature
    """"""

    allow_out_of_image_bounds: Optional[bool]
    """枠内制御がなくなったため値の設定は出来ません。値の取得では、必ず`true`が入ります。[廃止](/docs/releases/deprecation-announcements.html#notice25)までは互換性のため残されています。 """

    metadata: Optional[Dict[str, str]]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class LabelV2(DataClassJsonMixin):
    """ """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

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
    """ラベルに所属する属性のID"""

    color: Color
    """"""

    annotation_editor_feature: AnnotationEditorFeature
    """"""

    allow_out_of_image_bounds: Optional[bool]
    """枠内制御がなくなったため値の設定は出来ません。値の取得では、必ず`true`が入ります。[廃止](/docs/releases/deprecation-announcements.html#notice25)までは互換性のため残されています。 """

    metadata: Optional[Dict[str, str]]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class AdditionalDataRestriction(DataClassJsonMixin):
    """ """

    additional_data_definition_id: str
    """属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    condition: AdditionalDataRestrictionCondition
    """"""


@dataclass
class AnnotationSpecsV1(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    labels: List[LabelV1]
    """ラベル"""

    inspection_phrases: List[InspectionPhrase]
    """定型指摘"""

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
    """ラベル"""

    additionals: List[AdditionalDataDefinitionV2]
    """属性"""

    restrictions: List[AdditionalDataRestriction]
    """属性の制約"""

    inspection_phrases: List[InspectionPhrase]
    """定型指摘"""

    format_version: str
    """"""

    updated_datetime: Optional[str]
    """アノテーション仕様の最終更新時刻 """

    option: Optional[AnnotationSpecsOption]
    """"""

    metadata: Dict[str, str]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """
