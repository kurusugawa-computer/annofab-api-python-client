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

from annofabapi.models import (
    AdditionalDataDefinitionType,
    AnnotationDataHoldingType,
    InternationalizationMessage,
    TaskPhase,
    TaskStatus,
)

AnnotationDataV1 = Union[str, Dict[str, Any]]
FullAnnotationData = Any
AdditionalDataValue = Dict[str, Any]
FullAnnotationAdditionalDataValue = Dict[str, Any]
AnnotationDetailV2Input = Dict[str, Any]
AnnotationDetailContentOutput = Dict[str, Any]
AnnotationType = str
AnnotationDetailContentInput = Dict[str, Any]
AnnotationDetailV2Output = Dict[str, Any]


@dataclass
class Point(DataClassJsonMixin):
    """
    点の座標値
    """

    x: int
    """X座標の値[ピクセル]"""

    y: int
    """Y座標の値[ピクセル]"""


@dataclass
class FullAnnotationDataClassification(DataClassJsonMixin):
    """ """

    type: str
    """`Classification` """


@dataclass
class FullAnnotationDataSegmentation(DataClassJsonMixin):
    """ """

    data_uri: str
    """塗りつぶし画像のパス。 塗りつぶし画像のファイル形式はPNGです。塗りつぶされた部分の色は`rgba(255, 255, 255, 1)`、塗りつぶされていない部分の色は`rgba(0, 0, 0, 0)`です。 """

    type: str
    """`Segmentation` """


@dataclass
class FullAnnotationDataSegmentationV2(DataClassJsonMixin):
    """ """

    data_uri: str
    """塗りつぶし画像のパス。 塗りつぶし画像のファイル形式はPNGです。塗りつぶされた部分の色は`rgba(255, 255, 255, 1)`、塗りつぶされていない部分の色は`rgba(0, 0, 0, 0)`です。 """

    type: str
    """`SegmentationV2` """


@dataclass
class FullAnnotationDataBoundingBox(DataClassJsonMixin):
    """ """

    left_top: Point
    """"""

    right_bottom: Point
    """"""

    type: str
    """`BoundingBox` """


@dataclass
class FullAnnotationDataPoints(DataClassJsonMixin):
    """ """

    points: List[Point]
    """頂点の座標値"""

    type: str
    """`Points` """


@dataclass
class FullAnnotationDataSinglePoint(DataClassJsonMixin):
    """ """

    point: Point
    """"""

    type: str
    """`SinglePoint` """


@dataclass
class FullAnnotationDataRange(DataClassJsonMixin):
    """ """

    begin: float
    """開始時間（ミリ秒）"""

    end: float
    """終了時間（ミリ秒）"""

    type: str
    """`Range` """


@dataclass
class AdditionalDataV1(DataClassJsonMixin):
    """ """

    additional_data_definition_id: str
    """属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    flag: Optional[bool]
    """`additional_data_definition`の`type`が`flag`のときの属性値。 """

    integer: Optional[int]
    """`additional_data_definition`の`type`が`integer`のときの属性値。 """

    comment: Optional[str]
    """`additional_data_definition`の`type`が`text`,`comment`,`link` または `tracking`のときの属性値。 """

    choice: Optional[str]
    """選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """


@dataclass
class FullAnnotationAdditionalData(DataClassJsonMixin):
    """
    属性情報
    """

    additional_data_definition_id: str
    """属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    additional_data_definition_name: InternationalizationMessage
    """"""

    type: AdditionalDataDefinitionType
    """"""

    value: FullAnnotationAdditionalDataValue
    """"""


@dataclass
class FullAnnotationDetail(DataClassJsonMixin):
    """ """

    annotation_id: str
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 """

    user_id: str
    """ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    label_name: InternationalizationMessage
    """"""

    annotation_type: AnnotationType
    """"""

    data_holding_type: AnnotationDataHoldingType
    """"""

    data: FullAnnotationData
    """"""

    additional_data_list: List[FullAnnotationAdditionalData]
    """属性情報。 """


@dataclass
class FullAnnotation(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_phase: TaskPhase
    """"""

    task_phase_stage: int
    """タスクのフェーズのステージ番号"""

    task_status: TaskStatus
    """"""

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_name: str
    """入力データ名"""

    details: List[FullAnnotationDetail]
    """矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列"""

    updated_datetime: Optional[str]
    """更新日時。アノテーションが一つもない場合（教師付作業が未着手のときなど）は、未指定。"""

    annotation_format_version: str
    """アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、Annofabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 """


@dataclass
class SimpleAnnotationDetail(DataClassJsonMixin):
    """ """

    label: str
    """アノテーション仕様で設定したラベル名 (英語) です。 """

    annotation_id: str
    """個々のアノテーションにつけられたIDです。 """

    data: FullAnnotationData
    """"""

    attributes: Dict[str, Any]
    """キーと値が以下のようになっている辞書構造です。  * キー: アノテーション仕様で設定した属性名 (英語) * 値: 各属性の値   * 選択肢を定義している場合、その選択肢の表示名 (英語)   * それ以外は属性値そのまま (文字列、数値、論理値) """


@dataclass
class SimpleAnnotation(DataClassJsonMixin):
    """ """

    annotation_format_version: str
    """アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、Annofabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_phase: TaskPhase
    """"""

    task_phase_stage: int
    """タスクのフェーズのステージ番号"""

    task_status: TaskStatus
    """"""

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_name: str
    """入力データ名"""

    details: List[SimpleAnnotationDetail]
    """矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。"""

    updated_datetime: Optional[str]
    """更新日時。アノテーションが一つもない場合（教師付作業が未着手のときなど）は、未指定。"""


@dataclass
class SingleAnnotationDetail(DataClassJsonMixin):
    """
    アノテーション情報
    """

    annotation_id: str
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 """

    account_id: str
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    data_holding_type: AnnotationDataHoldingType
    """"""

    data: Optional[FullAnnotationData]
    """"""

    etag: Optional[str]
    """data_holding_typeがouterの場合のみ存在し、データのETagが格納される"""

    url: Optional[str]
    """data_holding_typeがouterの場合のみ存在し、データへの一時URLが格納される"""

    additional_data_list: List[AdditionalDataV1]
    """属性情報。  アノテーション属性の種類（`additional_data_definition`の`type`）によって、属性値を格納するプロパティは変わります。  | 属性の種類 | `additional_data_definition`の`type` | 属性値を格納するプロパティ                    | |------------|-------------------------|----------------------| | ON/OFF | flag       | flag                                          | | 整数 | integer    | integer                                       | | 自由記述（1行）| text       | comment                                       | | 自由記述（複数行）| comment    | comment                                       | | トラッキングID  | tracking | comment                                       | | アノテーションリンク    | link   | comment                                       | | 排他選択（ラジオボタン）  |choice   | choice                                        | | 排他選択（ドロップダウン） | select    | choice                                        | """

    created_datetime: str
    """作成日時"""

    updated_datetime: str
    """更新日時"""


@dataclass
class SingleAnnotation(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    detail: SingleAnnotationDetail
    """"""

    updated_datetime: str
    """更新日時"""


@dataclass
class AnnotationDetailV1(DataClassJsonMixin):
    """ """

    annotation_id: str
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 """

    account_id: str
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    is_protected: bool
    """`true`の場合、アノテーションをアノテーションエディタ上での削除から保護できます。 外部から取り込んだアノテーションに属性を追加するときなどに指定すると、データの削除を防げます。 """

    data_holding_type: AnnotationDataHoldingType
    """"""

    data: Optional[AnnotationDataV1]
    """"""

    path: Optional[str]
    """外部ファイルに保存されたアノテーションのパス。`data_holding_type`が`inner`の場合は未指定です。 レスポンスの場合は`annotation_id`と同じ値が格納されます。  [putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は、[createTempPath](#operation/createTempPath) APIで取得できる一時データ保存先S3パスを格納してください。 更新しない場合は、[getEditorAnnotation](#operation/getEditorAnnotation) APIで取得した`path`をそのまま渡せます。  外部ファイルのフォーマットは下表の通りです。  <table> <tr><th>annotation_type</th><th>形式</th></tr> <tr><td>segmentation / segmentation_v2   </td><td>PNG画像。塗りつぶした部分は<code>rgba(255, 255, 255, 1) </code>、塗りつぶしていない部分は<code>rgba(0, 0, 0, 0) </code>。</td></tr> </table> """

    etag: Optional[str]
    """外部ファイルに保存されたアノテーションのETag。`data_holding_type`が`inner`の場合、または[putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は未指定です。"""

    url: Optional[str]
    """外部ファイルに保存されたアノテーションの認証済み一時URL。`data_holding_type`が`inner`の場合、または[putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は未指定です。"""

    additional_data_list: List[AdditionalDataV1]
    """属性情報。  アノテーション属性の種類（`additional_data_definition`の`type`）によって、属性値を格納するプロパティは変わります。  | 属性の種類 | `additional_data_definition`の`type` | 属性値を格納するプロパティ                    | |------------|-------------------------|----------------------| | ON/OFF | flag       | flag                                          | | 整数 | integer    | integer                                       | | 自由記述（1行）| text       | comment                                       | | 自由記述（複数行）| comment    | comment                                       | | トラッキングID  | tracking | comment                                       | | アノテーションリンク    | link   | comment                                       | | 排他選択（ラジオボタン）  |choice   | choice                                        | | 排他選択（ドロップダウン） | select    | choice                                        | """

    created_datetime: Optional[str]
    """作成日時"""

    updated_datetime: Optional[str]
    """更新日時"""


@dataclass
class AnnotationV1(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    details: List[AnnotationDetailV1]
    """矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。"""

    updated_datetime: Optional[str]
    """更新日時"""


@dataclass
class AdditionalDataV2(DataClassJsonMixin):
    """ """

    definition_id: str
    """属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    value: Optional[AdditionalDataValue]
    """"""


@dataclass
class AnnotationPropsForEditor(DataClassJsonMixin):
    """
    アノテーションエディタ用のアノテーション毎のプロパティです。<br /> ここに含まれているデータはアノテーション結果に反映されず、エディタが利用するために存在します。  エディタ用のデータであるため、たとえば`can_delete`や`can_edit_data`が`false`でも、APIによる編集は妨げません。<br /> ここで定義されているデータを利用して動作を変えるかどうかは、エディタによって異なります。
    """

    can_delete: Optional[bool]
    """アノテーションがエディタ上で削除できるかどうか。 trueの場合削除可能。"""

    can_edit_data: Optional[bool]
    """アノテーションの本体のデータを編集できるかどうか。 trueの場合編集可能。 2022/09現在、この値を利用しているエディタは存在しません。"""

    can_edit_additional: Optional[bool]
    """アノテーションの付加情報を編集できるかどうか。  trueの場合編集可能。 2022/09現在、この値を利用しているエディタは存在しません。"""

    description: Optional[str]
    """アノテーションについての人間可読な説明。 2022/09現在、この値を利用しているエディタは存在しません。"""

    tags: Optional[List[str]]
    """アノテーションに付与されている機械可読・人間可読なタグの列。  2022/09現在、この値を利用しているエディタは存在しません"""

    etc: Optional[Dict[str, Any]]
    """上記以外の任意のJson構造"""


@dataclass
class AdditionalDataValueFlag(DataClassJsonMixin):
    """ """

    type: str
    """"""

    value: bool
    """ON/OFF属性の属性値。 ONの時trueとなります"""


@dataclass
class AdditionalDataValueInteger(DataClassJsonMixin):
    """ """

    type: str
    """"""

    value: int
    """整数属性の属性値"""


@dataclass
class AdditionalDataValueComment(DataClassJsonMixin):
    """ """

    type: str
    """"""

    value: str
    """自由記述（1行）の属性値"""


@dataclass
class AdditionalDataValueText(DataClassJsonMixin):
    """ """

    type: str
    """"""

    value: str
    """自由記述（複数行）の属性値"""


@dataclass
class AdditionalDataValueChoice(DataClassJsonMixin):
    """ """

    type: str
    """"""

    choice_id: str
    """選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """


@dataclass
class AdditionalDataValueSelect(DataClassJsonMixin):
    """ """

    type: str
    """"""

    choice_id: str
    """選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """


@dataclass
class AdditionalDataValueTracking(DataClassJsonMixin):
    """ """

    type: str
    """"""

    value: str
    """トラッキングID属性の属性値"""


@dataclass
class AdditionalDataValueLink(DataClassJsonMixin):
    """ """

    type: str
    """"""

    annotation_id: str
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 """


@dataclass
class AnnotationDetailContentInputInner(DataClassJsonMixin):
    """
    アノテーションのデータ部をJSON内部に保持します
    """

    type: str
    """"""

    data: FullAnnotationData
    """"""


@dataclass
class AnnotationDetailContentInputOuter(DataClassJsonMixin):
    """
    アノテーションのデータ部を外部ファイルの形式（画像など）で保持します
    """

    type: str
    """"""

    path: str
    """外部ファイルの位置を示す文字列。 [createTempPath](#operation/createTempPath) APIによって取得したpathを指定します。"""


@dataclass
class AnnotationDetailV2Create(DataClassJsonMixin):
    """
    新規にアノテーションを作成する場合にこの型を利用します。
    """

    type: str
    """"""

    annotation_id: str
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    body: AnnotationDetailContentInput
    """"""

    additional_data_list: List[AdditionalDataV2]
    """"""

    editor_props: AnnotationPropsForEditor
    """"""


@dataclass
class AnnotationDetailV2Import(DataClassJsonMixin):
    """
    過去にAnnofab内外で作成したアノテーションをそのままインポートする場合にこの型を利用します。
    """

    type: str
    """"""

    annotation_id: str
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 """

    account_id: str
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    body: AnnotationDetailContentInput
    """"""

    additional_data_list: List[AdditionalDataV2]
    """"""

    editor_props: AnnotationPropsForEditor
    """"""

    created_datetime: str
    """作成日時"""

    updated_datetime: str
    """更新日時"""


@dataclass
class AnnotationDetailV2Update(DataClassJsonMixin):
    """
    既に存在するアノテーションを更新する場合にこの型を利用します
    """

    type: str
    """"""

    annotation_id: str
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    body: Optional[AnnotationDetailContentInput]
    """"""

    additional_data_list: List[AdditionalDataV2]
    """"""

    editor_props: AnnotationPropsForEditor
    """"""


@dataclass
class AnnotationV2Input(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    details: List[AnnotationDetailV2Input]
    """矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。"""

    updated_datetime: Optional[str]
    """対象タスク・対象入力データへの最初の保存時は未指定にしてください。 更新の場合はアノテーション取得時のupdated_datetimeをそのまま指定してください。 """

    format_version: str
    """"""


@dataclass
class AnnotationDetailContentOutputInner(DataClassJsonMixin):
    """
    アノテーションのデータ部をJSON内部に保持します
    """

    type: str
    """"""

    data: FullAnnotationData
    """"""


@dataclass
class AnnotationDetailContentOutputInnerUnknown(DataClassJsonMixin):
    """
    アノテーションのデータ部をJSON内部に保持します。 AnnotationDetailV1の形式で保存されていたデータのAnnotationTypeが特定できない場合にこの値となります。 典型的な例では、アノテーションの保存後にアノテーション仕様が書き換わっていた場合が該当します。
    """

    type: str
    """"""

    data: str
    """アノテーション座標値や区間などの文字列表現です。 アノテーション種類（`annotation_type`）とデータ格納形式（`data_holding_type`）に応じて、以下のとおり表現が変わります。  <table> <tr><th>annotation_type</th><th>data_holding_type</th><th>文字列表現</th></tr> <tr><td>bounding_box</td><td>inner</td><td><code>\"左上x,左上y,右下x,右下y\"</code></td></tr> <tr><td>point</td><td>inner</td><td><code>\"x1,y1\"</code></td></tr> <tr><td>polygon / polyline</td><td>inner</td><td><code>\"x1,y1,x2,y2, ... \"</code></td></tr> <tr><td>range </td><td>inner</td><td><code>\"開始時間(ミリ秒),終了時間(ミリ秒) \"</code></td></tr> <tr><td>classification</td><td>inner</td><td><code>null</code></td></tr> <tr><td>segmentation</td><td>outer</td><td><code>null</code></td></tr> <tr><td>segmentation_v2</td><td>outer</td><td><code>null</code></td></tr> </table> """


@dataclass
class AnnotationDetailContentOutputOuter(DataClassJsonMixin):
    """
    アノテーションのデータ部を外部ファイルの形式（画像など）で保持します
    """

    type: str
    """"""

    url: str
    """外部ファイルに保存されたアノテーションの認証済み一時URL"""

    etag: str
    """外部ファイルに保存されたアノテーションのETag"""


@dataclass
class AnnotationDetailContentOutputOuterUnresolved(DataClassJsonMixin):
    """
    アノテーションのデータ部を外部ファイルの形式（画像など）で保持します。 Outerのurl / etagを解決しなかった場合（過去のアノテーションを取得した場合等）にこの値となります。
    """

    type: str
    """"""


@dataclass
class AnnotationDetailV2Get(DataClassJsonMixin):
    """ """

    type: str
    """"""

    annotation_id: str
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 """

    account_id: str
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    label_id: str
    """ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    body: AnnotationDetailContentOutput
    """"""

    additional_data_list: List[AdditionalDataV2]
    """"""

    editor_props: AnnotationPropsForEditor
    """"""

    created_datetime: str
    """作成日時"""

    updated_datetime: str
    """更新日時"""


@dataclass
class AnnotationV2Output(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    details: List[AnnotationDetailV2Output]
    """矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。"""

    updated_datetime: Optional[str]
    """対象タスク・対象入力データへ一度もアノテーションの保存が行われていない場合、未指定となります。 そうで無い場合、対象タスク・対象入力データのアノテーション最終更新時刻です。 """

    format_version: str
    """"""
