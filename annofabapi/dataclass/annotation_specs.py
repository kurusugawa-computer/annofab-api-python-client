# ruff: noqa: E501
# pylint: disable=too-many-lines,trailing-whitespace

"""
annofabapiのmodelをDataClassで定義したクラス

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照.
    oneOf, allOfなどは正しく表現できない可能性がある。
"""

from dataclasses import dataclass
from typing import Any  # pylint: disable=unused-import

from dataclasses_json import DataClassJsonMixin

from annofabapi.models import AdditionalDataDefinitionType, AnnotationTypeFieldMinWarnRule

AdditionalDataDefaultType = bool | int | str

AdditionalDataRestrictionCondition = dict[str, Any]

AnnotationSpecsOption = dict[str, Any]
AnnotationType = str
AnnotationTypeFieldValue = dict[str, Any]


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
    `annotation_type` が `bounding_box` かつ `min_warn_rule` が `and` または `or` の場合のみ、挿入する最小矩形アノテーションの原点を指定できます。 画像左上の座標が「x=0, y=0」です。未指定の場合は、表示範囲の中央に挿入されます。  「スキャンした帳票の記入欄」や「定点カメラで撮影した製品ラベル」など、アノテーションしたい位置やサイズが多くの画像で共通している場合に便利です。  `annotation_type` が `bounding_box` 以外の場合は必ず未指定となります。
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

    min_area: int | None
    """面積の最小値[平方ピクセル]"""

    max_vertices: int | None
    """頂点数の最大値"""

    min_vertices: int | None
    """頂点数の最小値"""

    position_for_minimum_bounding_box_insertion: PositionForMinimumBoundingBoxInsertion | None
    """"""

    tolerance: int | None
    """許容誤差[ピクセル]"""

    has_direction: bool | None
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

    tolerance: int | None
    """許容誤差[ピクセル]"""


@dataclass
class InternationalizationMessageMessages(DataClassJsonMixin):
    """ """

    lang: str
    """言語コード。`en-US` (英語) 、`ja-JP` (日本語)、 `vi-VN`（ベトナム語）のみサポートしています。"""

    message: str
    """lang で指定された言語でのメッセージ"""


@dataclass
class InternationalizationMessage(DataClassJsonMixin):
    """ """

    messages: list[InternationalizationMessageMessages]
    """言語コードとメッセージ（テキスト）のリスト。  * アノテーションエディタなどでは、Annofabの表示言語（各ユーザーが個人設定で選んだ言語）のメッセージが使われます * 以下の名前は、[Simple Annotation](#tag/x-annotation-zip/Simple-Annotation-ZIP) では `en-US` のメッセージが使われます     * ラベル名     * 属性名     * 選択肢名 * いずれの場合でも、表示しようとした言語が `messages` に含まれない場合、 `default_lang` に指定した言語のメッセージが使われます """

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

    account_id: str | None
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    comment: str | None
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

    keybind: list[Keybind] | None
    """ショートカットキー"""


@dataclass
class AdditionalDataDefinitionV1(DataClassJsonMixin):
    """ """

    additional_data_definition_id: str
    """属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    read_only: bool | None
    """読み込み専用"""

    name: InternationalizationMessage | None
    """"""

    default: AdditionalDataDefaultType | None
    """"""

    keybind: list[Keybind] | None
    """ショートカットキー"""

    type: AdditionalDataDefinitionType
    """"""

    choices: list[AdditionalDataDefinitionV1Choices] | None
    """ドロップダウンまたはラジオボタンの選択肢"""

    regex: str | None
    """属性の値が、指定した正規表現に一致している必要があります。"""

    label_ids: list[str] | None
    """リンク属性において、リンク先として指定可能なラベルID（空の場合制限なし）"""

    required: bool | None
    """リンク属性において、入力を必須とするかどうか"""

    metadata: dict[str, str] | None
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class AdditionalDataDefinitionV2(DataClassJsonMixin):
    """ """

    additional_data_definition_id: str
    """属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    read_only: bool | None
    """読み込み専用"""

    name: InternationalizationMessage
    """"""

    default: AdditionalDataDefaultType | None
    """"""

    keybind: list[Keybind] | None
    """ショートカットキー"""

    type: AdditionalDataDefinitionType
    """"""

    choices: list[AdditionalDataDefinitionV1Choices] | None
    """ドロップダウンまたはラジオボタンの選択肢"""

    metadata: dict[str, str] | None
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
    """塗りつぶしの「自由形状」機能が使えるか否か"""

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
    """最小の幅。標準の矩形種別では0以上を指定します。ユーザー定義種別では、現在、下限は検証されません。 """

    min_height: int
    """最小の高さ。標準の矩形種別では0以上を指定します。ユーザー定義種別では、現在、下限は検証されません。 """

    position_for_minimum_bounding_box_insertion: list[int] | None
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

    min: int | None
    """頂点数の最小値。データ型が `Polyline2d` の場合は2以上、`Polygon2d` の場合は3以上を指定します。 """

    max: int | None
    """頂点数の最大値。標準種別ではポリラインは2以上、ポリゴンは3以上を指定します。ユーザー定義種別では、`max` のみ指定した場合、下限は検証されません。 """


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

    keybind: list[Keybind]
    """ショートカットキー"""

    annotation_type: AnnotationType
    """"""

    bounding_box_metadata: BoundingBoxMetadata | None
    """"""

    segmentation_metadata: SegmentationMetadata | None
    """"""

    additional_data_definitions: list[AdditionalDataDefinitionV1]
    """属性"""

    color: Color
    """"""

    annotation_editor_feature: AnnotationEditorFeature
    """"""

    metadata: dict[str, str] | None
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class LabelV2(DataClassJsonMixin):
    """ """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    label_name: InternationalizationMessage
    """"""

    keybind: list[Keybind]
    """ショートカットキー"""

    annotation_type: AnnotationType
    """"""

    bounding_box_metadata: BoundingBoxMetadata | None
    """"""

    segmentation_metadata: SegmentationMetadata | None
    """"""

    additional_data_definitions: list[str]
    """ラベルに所属する属性のID"""

    color: Color
    """"""

    annotation_editor_feature: AnnotationEditorFeature
    """"""

    metadata: dict[str, str] | None
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

    labels: list[LabelV1]
    """ラベル"""

    inspection_phrases: list[InspectionPhrase]
    """定型指摘"""

    updated_datetime: str | None
    """更新日時 """

    option: AnnotationSpecsOption | None
    """"""

    metadata: dict[str, str]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class AnnotationSpecsV2(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    labels: list[LabelV2]
    """ラベル"""

    additionals: list[AdditionalDataDefinitionV2]
    """属性"""

    restrictions: list[AdditionalDataRestriction]
    """属性の制約"""

    inspection_phrases: list[InspectionPhrase]
    """定型指摘"""

    format_version: str
    """アノテーション仕様のフォーマットのバージョン"""

    updated_datetime: str | None
    """更新日時 """

    option: AnnotationSpecsOption | None
    """"""

    metadata: dict[str, str]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class LabelV3(DataClassJsonMixin):
    """ """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    label_name: InternationalizationMessage
    """"""

    keybind: list[Keybind]
    """ショートカットキー"""

    annotation_type: AnnotationType
    """"""

    field_values: dict[str, AnnotationTypeFieldValue]
    """ラベルごとの制約や設定値を保持するオブジェクトです。 キーには設定項目を識別するフィールドIDを指定し、値にはそのフィールドに設定する制約やオプションを表すオブジェクトを指定します。 例えば頂点数制約は、`\"vertex_count_min_max\": {\"_type\": \"VertexCountMinMax\", \"max\": 20}` のように指定します。  Annofabの標準エディタでは、アノテーション種別ごとに、使用可能なフィールドIDと設定値の構造があらかじめ決まっています。設定値の構造は、値オブジェクトの `_type` に設定値の構造を示す名前を指定することで示します。以下の表に、フィールドIDと設定値の構造を示す名前を示します。  | エディタ | アノテーション種別（`annotation_type`） | フィールドID → 設定値の構造を示す名前 | | --- | --- | --- | | 画像 | 矩形（`bounding_box`） | `minimum_size_2d_with_default_insert_position` → `MinimumSize2dWithDefaultInsertPosition`<br>`margin_of_error_tolerance` → `MarginOfErrorTolerance` | | 画像 | ポリゴン（`polygon`） | `minimum_size_2d` → `MinimumSize2d`<br>`minimum_area_2d` → `MinimumArea2d`<br>`vertex_count_min_max` → `VertexCountMinMax`<br>`margin_of_error_tolerance` → `MarginOfErrorTolerance` | | 画像 | ポリライン（`polyline`） | `minimum_size_2d` → `MinimumSize2d`<br>`vertex_count_min_max` → `VertexCountMinMax`<br>`display_line_direction` → `DisplayLineDirection`<br>`margin_of_error_tolerance` → `MarginOfErrorTolerance` | | 画像 | 点（`point`） | `margin_of_error_tolerance` → `MarginOfErrorTolerance` | | 画像 | 塗りつぶし（`segmentation`）・塗りつぶしv2（`segmentation_v2`） | `minimum_size_2d` → `MinimumSize2d`<br>`margin_of_error_tolerance` → `MarginOfErrorTolerance`<br>`annotation_editor_feature` → `AnnotationEditorFeature` | | 画像・動画 | 全体（`classification`） | なし | | 動画 | 区間（`range`） | なし |  ユーザー定義アノテーション種別では、[組織プラグイン](#operation/putOrganizationPlugin)の [UserDefinedAnnotationTypeDefinition](#tag/x-data-types/UserDefinedAnnotationTypeDefinition) の `field_definitions` で定義されたフィールドIDをキーに指定します。値オブジェクトの `_type` には、設定値の構造を示す名前を指定します。指定する名前は、[フィールド定義と設定値の対応表](#tag/x-data-types/UserDefinedAnnotationTypeDefinition)（`field_definitions` の `definition` の説明）を参照してください。 """

    additional_data_definitions: list[str]
    """ラベルに所属する属性のID"""

    color: Color
    """"""

    metadata: dict[str, str] | None
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """


@dataclass
class AnnotationSpecsV3(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    labels: list[LabelV3]
    """ラベル"""

    additionals: list[AdditionalDataDefinitionV2]
    """属性"""

    restrictions: list[AdditionalDataRestriction]
    """属性の制約"""

    inspection_phrases: list[InspectionPhrase]
    """定型指摘"""

    annotation_type_version: str | None
    """アノテーション種別のバージョン。  拡張仕様プラグインで定義した値が転写されます。プロジェクトに拡張仕様プラグインが設定されていない場合は未指定です。 """

    format_version: str
    """アノテーション仕様のフォーマットのバージョン"""

    updated_datetime: str | None
    """更新日時 """

    option: AnnotationSpecsOption | None
    """"""

    metadata: dict[str, str]
    """ユーザーが自由に登録できるkey-value型のメタデータです。 """
