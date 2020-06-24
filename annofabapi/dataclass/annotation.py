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

from annofabapi.models import (
    AdditionalDataDefinitionType,
    AnnotationDataHoldingType,
    AnnotationType,
    InternationalizationMessage,
    TaskPhase,
    TaskStatus,
)

AnnotationData = Union[str, Dict[str, Any]]
FullAnnotationData = Dict[str, Any]
AdditionalDataValue = Dict[str, Any]


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
class FullAnnotationDataClassification:
    """
    
    """

    type: str
    """Classification"""


@dataclass_json
@dataclass
class FullAnnotationDataSegmentation:
    """
    塗っていないところは rgba(0,0,0,0)、塗ったところは rgba(255,255,255,1) の PNGデータをBase64エンコードしたもの。
    """

    data_uri: str
    """"""

    type: str
    """Segmentation"""


@dataclass_json
@dataclass
class FullAnnotationDataSegmentationV2:
    """
    
    """

    data_uri: str
    """"""

    type: str
    """SegmentationV2"""


@dataclass_json
@dataclass
class FullAnnotationDataBoundingBox:
    """
    annotation_type が bounding_boxの場合に、[左上頂点座標, 右下頂点座標]を {\"x\":int, \"y\":int} の形式で記述したもの。
    """

    left_top: Point
    """"""

    right_bottom: Point
    """"""

    type: str
    """BoundingBox"""


@dataclass_json
@dataclass
class FullAnnotationDataPoints:
    """
    頂点座標 {\"x\":int, \"y\":int} の配列。  * annotation_type が polygon/polyline の場合: ポリゴン/ポリラインを構成する頂点の配列。 
    """

    points: List[Point]
    """"""

    type: str
    """Points"""


@dataclass_json
@dataclass
class FullAnnotationDataSinglePoint:
    """
    annotation_type が pointの場合。
    """

    point: Point
    """"""

    type: str
    """SinglePoint。"""


@dataclass_json
@dataclass
class FullAnnotationDataRange:
    """
    annotation_type が rangeの場合に、[開始時間, 終了時間]を {\"begin\":number, \"end\":number} の形式で記述したもの。開始時間・終了時間の単位は秒で、精度はミリ秒まで。
    """

    begin: float
    """開始時間（ミリ秒）。小数点以下はミリ秒以下を表します。"""

    end: float
    """終了時間（ミリ秒）。小数点以下はミリ秒以下を表します。"""

    type: str
    """Range"""


@dataclass_json
@dataclass
class AdditionalData:
    """
    
    """

    additional_data_definition_id: str
    """"""

    flag: Optional[bool]
    """`additional_data_definition`の`type`が`flag`のときの属性値。 """

    integer: Optional[int]
    """`additional_data_definition`の`type`が`integer`のときの属性値。 """

    comment: Optional[str]
    """`additional_data_definition`の`type`が`text`,`comment`,`link` または `tracking`のときの属性値。 """

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

    value: Optional[AdditionalDataValue]
    """"""


@dataclass_json
@dataclass
class FullAnnotationDetail:
    """
    
    """

    annotation_id: Optional[str]
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 """

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
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: Optional[str]
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_phase: Optional[TaskPhase]
    """"""

    task_phase_stage: Optional[int]
    """"""

    task_status: Optional[TaskStatus]
    """"""

    input_data_id: Optional[str]
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_name: Optional[str]
    """"""

    details: Optional[List[FullAnnotationDetail]]
    """"""

    updated_datetime: Optional[str]
    """"""

    annotation_format_version: Optional[str]
    """アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、AnnoFabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 """


@dataclass_json
@dataclass
class SimpleAnnotationDetail:
    """
    
    """

    label: str
    """アノテーション仕様のラベル名です。 """

    annotation_id: str
    """個々のアノテーションにつけられたIDです。 """

    data: FullAnnotationData
    """"""

    attributes: Dict[str, Any]
    """キーに属性の名前、値に各属性の値が入った辞書構造です。 """


@dataclass_json
@dataclass
class SimpleAnnotation:
    """
    
    """

    annotation_format_version: str
    """アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、AnnoFabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_phase: TaskPhase
    """"""

    task_phase_stage: int
    """"""

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


@dataclass_json
@dataclass
class SingleAnnotationDetail:
    """
    
    """

    annotation_id: str
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 """

    account_id: str
    """"""

    label_id: str
    """"""

    data_holding_type: AnnotationDataHoldingType
    """"""

    data: Optional[FullAnnotationData]
    """"""

    etag: Optional[str]
    """data_holding_typeがouterの場合のみ存在し、データのETagが格納される"""

    url: Optional[str]
    """data_holding_typeがouterの場合のみ存在し、データへの一時URLが格納される"""

    additional_data_list: List[AdditionalData]
    """"""

    created_datetime: str
    """"""

    updated_datetime: str
    """"""


@dataclass_json
@dataclass
class SingleAnnotation:
    """
    
    """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    detail: SingleAnnotationDetail
    """"""

    updated_datetime: str
    """"""


@dataclass_json
@dataclass
class AnnotationDetail:
    """
    
    """

    annotation_id: str
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 """

    account_id: str
    """"""

    label_id: str
    """"""

    is_protected: bool
    """`true`の場合、アノテーションをアノテーションエディタ上での削除から保護できます。 外部から取り込んだアノテーションに属性を追加するときなどに指定すると、データの削除を防げます。 """

    data_holding_type: AnnotationDataHoldingType
    """"""

    data: Optional[AnnotationData]
    """"""

    path: Optional[str]
    """外部ファイルに保存されたアノテーションのパス。`data_holding_type`が`inner`の場合は未指定です。 レスポンスの場合は`annotation_id`と同じ値が格納されます。  [putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は、[createTempPath](#operation/createTempPath) APIで取得できる一時データ保存先S3パスを格納してください。 更新しない場合は、[getEditorAnnotation](#operation/getEditorAnnotation) APIで取得した`path`をそのまま渡せます。  外部ファイルのフォーマットは下表の通りです。  <table> <tr><th>annotation_type</th><th>形式</th></tr> <tr><td>segmentation / segmentation_v2   </td><td>PNG画像。塗りつぶした部分は<code>rgba(255, 255, 255, 1) </code>、塗りつぶしていない部分は<code>rgba(0, 0, 0, 0) </code>。</td></tr> </table> """

    etag: Optional[str]
    """外部ファイルに保存されたアノテーションのETag。`data_holding_type`が`inner`の場合、または[putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は未指定です。"""

    url: Optional[str]
    """外部ファイルに保存されたアノテーションの認証済み一時URL。`data_holding_type`が`inner`の場合、または[putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は未指定です。"""

    additional_data_list: List[AdditionalData]
    """各要素は、 [アノテーション仕様](#operation/getAnnotationSpecs)で定義された属性（`additional_data_definitions`内）のいずれかの要素と対応づけます。 各要素は、どの属性なのかを表す`additional_data_definition_id`と値が必要です。値は、属性の種類に対応するキーに格納します（下表）。  <table> <tr><th>アノテーション属性の種類<br>（<code>additional_data_definition</code>の<code>type</code>）</th><th>属性の値を格納するキー</th><th>データ型</th></tr> <tr><td><code>text</code>, <code>comment</code> または <code>tracking</code></td><td><code>comment</code></td><td>string</td></tr> <tr><td><code>flag<c/ode></td><td><code>flag</code></td><td>boolean</td></tr> <tr><td><code>integer</code></td><td><code>integer</code></td><td>integer</td></tr> <tr><td><code>choice</code> または <code>select</code></td><td><code>choice</code></td><td>string（選択肢ID）</td></tr> <tr><td><code>link</code></td><td><code>comment</code></td><td>string（アノテーションID）</td></tr> </table> """

    created_datetime: Optional[str]
    """"""

    updated_datetime: Optional[str]
    """"""


@dataclass_json
@dataclass
class Annotation:
    """
    
    """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    details: List[AnnotationDetail]
    """矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。"""

    updated_datetime: Optional[str]
    """新規作成時は未指定、更新時は必須（更新前の日時） """
