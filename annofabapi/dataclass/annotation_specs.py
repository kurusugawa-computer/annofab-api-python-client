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

from annofabapi.models import AdditionalDataDefinitionType, AnnotationTypeFieldMinWarnRule

AdditionalDataDefaultType = Union[bool, int, str]

AdditionalDataRestrictionCondition = Dict[str, Any]

AnnotationSpecsOption = Dict[str, Any]
AnnotationType = str
AnnotationTypeFieldValue = Dict[str, Any]


@dataclass
class Keybind(DataClassJsonMixin):
    """ """

    code: str
    """[KeyboardEvent.code](https://developer.mozilla.org/ja/docs/Web/API/KeyboardEvent/code)に相当する値です。 """

    shift: bool
    """Shiftキーを押しているかどうか"""

    ctrl: bool
    """Ctrlキーを押しているかどうか"""

    alt: bool
    """Altキーを押しているかどうか"""


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
class BoundingBoxMetadata(DataClassJsonMixin):
    """
    ベクター形式のアノテーション（矩形、ポリゴン、ポリライン、点）のメタデータ
    """

    min_width: int
    """幅の最小値[ピクセル]"""

    min_height: int
    """高さの最小値[ピクセル]"""

    min_warn_rule: str
    """サイズの制約に関する情報 * `none` - 制約なし * `or` - 幅と高さの両方が最小値以上 * `and` - 幅と高さのどちらか一方が最小値以上 """

    min_area: Optional[int]
    """面積の最小値[平方ピクセル]"""

    max_vertices: Optional[int]
    """頂点数の最大値"""

    min_vertices: Optional[int]
    """頂点数の最小値"""

    position_for_minimum_bounding_box_insertion: Optional[PositionForMinimumBoundingBoxInsertion]
    """"""

    tolerance: Optional[int]
    """許容誤差[ピクセル]"""

    has_direction: Optional[bool]
    """`annotation_type` が `polyline` の場合、アノテーションに向きを持たせるかどうかを指定できます。 この値が `true` の場合、Annofabの標準画像エディタ上ではポリラインの向きを示す矢印が描画されるようになります。  `annotationType` が `polyline` 以外の場合は必ず `false` となります。 """


@dataclass
class SegmentationMetadata(DataClassJsonMixin):
    """
    塗りつぶしアノテーションのメタデータ
    """

    min_width: int
    """幅の最小値[ピクセル]"""

    min_height: int
    """高さの最小値[ピクセル]"""

    min_warn_rule: str
    """サイズの制約に関する情報 * `none` - 制約なし * `or` - 幅と高さの両方が最小値以上 * `and` - 幅と高さのどちらか一方が最小値以上 """

    tolerance: Optional[int]
    """許容誤差[ピクセル]"""


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
    """言語コードとメッセージ（テキスト）のリスト。  * アノテーションエディタなどでは、Annofabの表示言語（各ユーザーが個人設定で選んだ言語）のメッセージが使われます * 以下の名前は、[Simple Annotation](#section/Simple-Annotation-ZIP) では `en-US` のメッセージが使われます     * ラベル名     * 属性名     * 選択肢名 * いずれの場合でも、表示しようとした言語が `messages` に含まれない場合、 `default_lang` に指定した言語のメッセージが使われます """

    default_lang: str
    """希望された言語のメッセージが存在しない場合に、フォールバック先として使われる言語コード"""


@dataclass
class InspectionPhrase(DataClassJsonMixin):
    """ """

    id: str
    """定型指摘ID"""

    text: InternationalizationMessage
    """"""


@dataclass
class AnnotationSpecsHistory(DataClassJsonMixin):
    """ """

    history_id: str
    """アノテーション仕様の履歴ID"""

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    updated_datetime: str
    """更新日時"""

    url: str
    """アノテーション仕様が格納されたJSONのURL。URLにアクセスするには認証認可が必要です。"""

    account_id: Optional[str]
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    comment: Optional[str]
    """変更内容のコメント"""


@dataclass
class Color(DataClassJsonMixin):
    """
    RGBで表現される色情報
    """

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
    """ショートカットキー"""


@dataclass
class AdditionalDataDefinitionV1(DataClassJsonMixin):
    """ """

    additional_data_definition_id: str
    """属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    read_only: Optional[bool]
    """読み込み専用"""

    name: Optional[InternationalizationMessage]
    """"""

    default: Optional[AdditionalDataDefaultType]
    """"""

    keybind: Optional[List[Keybind]]
    """ショートカットキー"""

    type: AdditionalDataDefinitionType
    """"""

    choices: Optional[List[AdditionalDataDefinitionV1Choices]]
    """ドロップダウンまたはラジオボタンの選択肢"""

    regex: Optional[str]
    """属性の値が、指定した正規表現に一致している必要があります。"""

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
    """読み込み専用"""

    name: InternationalizationMessage
    """"""

    default: Optional[AdditionalDataDefaultType]
    """"""

    keybind: Optional[List[Keybind]]
    """ショートカットキー"""

    type: AdditionalDataDefinitionType
    """"""

    choices: Optional[List[AdditionalDataDefinitionV1Choices]]
    """ドロップダウンまたはラジオボタンの選択肢"""

    metadata: Optional[Dict[str, str]]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class AnnotationEditorFeature(DataClassJsonMixin):
    """
    塗りつぶしの作図機能に関する情報
    """

    append: bool
    """塗りつぶしの「追記」機能が使えるか否か"""

    erase: bool
    """塗りつぶしの「消しゴム」機能が使えるか否か"""

    freehand: bool
    """塗りつぶしの「フリーハンド」機能が使えるか否か"""

    rectangle_fill: bool
    """塗りつぶしの「矩形」機能が使えるか否か"""

    polygon_fill: bool
    """塗りつぶしの「ポリゴン」機能が使えるか否か"""

    fill_near: bool
    """「近似色塗りつぶし」機能を有効にするかどうか"""


@dataclass
class AnnotationTypeFieldValueMinimumSize(DataClassJsonMixin):
    """
    アノテーションの最小サイズに関する設定
    """

    type: str
    """"""

    min_warn_rule: AnnotationTypeFieldMinWarnRule
    """"""

    min_width: int
    """"""

    min_height: int
    """"""


@dataclass
class AnnotationTypeFieldValueMinimumSize2dWithDefaultInsertPosition(DataClassJsonMixin):
    """ """

    type: str
    """"""

    min_warn_rule: AnnotationTypeFieldMinWarnRule
    """"""

    min_width: int
    """"""

    min_height: int
    """"""

    position_for_minimum_bounding_box_insertion: Optional[List[int]]
    """最小矩形の挿入位置を、要素が2の配列で指定します。 """


@dataclass
class AnnotationTypeFieldValueMarginOfErrorTolerance(DataClassJsonMixin):
    """
    誤差許容範囲
    """

    type: str
    """"""

    max_pixel: int
    """"""


@dataclass
class AnnotationTypeFieldValueVertexCountMinMax(DataClassJsonMixin):
    """
    頂点数の最大・最小
    """

    type: str
    """"""

    min: int
    """"""

    max: int
    """"""


@dataclass
class AnnotationTypeFieldValueMinimumArea2d(DataClassJsonMixin):
    """
    最小の面積
    """

    type: str
    """"""

    min_area: int
    """"""


@dataclass
class AnnotationTypeFieldValueDisplayLineDirection(DataClassJsonMixin):
    """
    線の向き表示/非表示の設定
    """

    type: str
    """"""

    has_direction: bool
    """"""


@dataclass
class AnnotationTypeFieldValueAnnotationEditorFeature(DataClassJsonMixin):
    """
    作図ツール・作図モード
    """

    type: str
    """"""

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
class AnnotationTypeFieldValueOneIntegerFieldValue(DataClassJsonMixin):
    """
    数値をひとつだけ持つフィールド
    """

    type: str
    """"""

    value: int
    """"""


@dataclass
class AnnotationTypeFieldValueOneStringFieldValue(DataClassJsonMixin):
    """
    文字列を一つだけ持つフィールド
    """

    type: str
    """"""

    value: str
    """"""


@dataclass
class AnnotationTypeFieldValueOneBooleanFieldValue(DataClassJsonMixin):
    """
    真偽値をひとつだけ持つフィールド
    """

    type: str
    """"""

    value: bool
    """"""


@dataclass
class AnnotationTypeFieldValueEmptyFieldValue(DataClassJsonMixin):
    """
    値を持たないフィールド。　アノテーション仕様上に定義が存在すること自体に意味がある場合のフィールド値に利用します。
    """

    type: str
    """"""


@dataclass
class LabelV1(DataClassJsonMixin):
    """ """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    label_name: InternationalizationMessage
    """"""

    keybind: List[Keybind]
    """ショートカットキー"""

    annotation_type: AnnotationType
    """"""

    bounding_box_metadata: Optional[BoundingBoxMetadata]
    """"""

    segmentation_metadata: Optional[SegmentationMetadata]
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
    """ショートカットキー"""

    annotation_type: AnnotationType
    """"""

    bounding_box_metadata: Optional[BoundingBoxMetadata]
    """"""

    segmentation_metadata: Optional[SegmentationMetadata]
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
    """更新日時 """

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
    """アノテーション仕様のフォーマットのバージョン"""

    updated_datetime: Optional[str]
    """更新日時 """

    option: Optional[AnnotationSpecsOption]
    """"""

    metadata: Dict[str, str]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class LabelV3(DataClassJsonMixin):
    """ """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    label_name: InternationalizationMessage
    """"""

    keybind: List[Keybind]
    """ショートカットキー"""

    annotation_type: AnnotationType
    """"""

    field_values: Dict[str, AnnotationTypeFieldValue]
    """KeyがフィールドIdであるDictionaryです。  カスタムの[組織プラグイン](#operation/putOrganizationPlugin)で利用される[UserDefinedAnnotationTypeDefinition](#section/UserDefinedAnnotationTypeDefinition).`field_definitions`で定義されます。 """

    additional_data_definitions: List[str]
    """ラベルに所属する属性のID"""

    color: Color
    """"""

    metadata: Optional[Dict[str, str]]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class AnnotationSpecsV3(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    labels: List[LabelV3]
    """ラベル"""

    additionals: List[AdditionalDataDefinitionV2]
    """属性"""

    restrictions: List[AdditionalDataRestriction]
    """属性の制約"""

    inspection_phrases: List[InspectionPhrase]
    """定型指摘"""

    annotation_type_version: Optional[str]
    """アノテーション種別のバージョン。  拡張仕様プラグインで定義した値が転写されます。プロジェクトに拡張仕様プラグインが設定されていない場合は未指定です。 """

    format_version: str
    """アノテーション仕様のフォーマットのバージョン"""

    updated_datetime: Optional[str]
    """更新日時 """

    option: Optional[AnnotationSpecsOption]
    """"""

    metadata: Dict[str, str]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """
