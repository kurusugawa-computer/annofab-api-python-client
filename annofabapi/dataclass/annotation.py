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
from annofabapi.models import (AnnotationDataHoldingType, InternationalizationMessage, AdditionalDataDefinitionType,
                               AnnotationType, TaskPhase, TaskStatus)

OneOfstringFullAnnotationData = Dict[str, Any]



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
class AnnotationDetail:
    """
    
    """
    annotation_id: str
    """annotation_type が classification の場合は label_id と同じ値が格納されます。 """



    account_id: str
    """"""



    label_id: str
    """"""



    is_protected: bool
    """"""



    data_holding_type: AnnotationDataHoldingType
    """"""



    data: Optional[OneOfstringFullAnnotationData]
    """data_holding_type が inner の場合のみ存在し、annotation_type に応じたデータの値が格納されます。 `string`もしくは`object`の値を指定することができ、`string`の形式は次の通りです。   * annotation_type が bounding_box の場合: 左上x,左上y,右下x,右下y のCSV文字列形式。   * annotation_type が polygon/polyline の場合: x1,y1,x2,y2, ... のCSV文字列形式。   * annotation_type が segmentation または segmentation_v2 の場合: 塗っていないところは rgba(0,0,0,0)、塗ったところは rgba(255,255,255,1) の PNGデータをBase64エンコードしたもの。   * annotation_type が classification の場合: data 属性は存在しない。   * annotation_type が range の場合: 開始時間,終了時間 のCSV文字列形式。 """



    path: Optional[str]
    """data_holding_typeがouterの場合のみ存在し、データのパスが格納される (現在はアノテーションIDと等しい)"""



    etag: Optional[str]
    """data_holding_typeがouterの場合のみ存在し、データのETagが格納される"""



    url: Optional[str]
    """data_holding_typeがouterの場合のみ存在し、データへの一時URLが格納される"""



    additional_data_list: List[AdditionalData]
    """各要素は、 [アノテーション仕様](#operation/getAnnotationSpecs)で定義された属性（`additional_data_definitions`内）のいずれかの要素と対応づけます。 各要素は、どの属性なのかを表す`additional_data_definition_id`、値が必要です。値は、属性の種類に対応するキーに格納します（下表）。  <table> <tr><th>アノテーション属性の種類<br>（`additional_data_definition`の`type`）</th><th>属性の値を格納するキー</th><th>データ型</th></tr> <tr><td>`comment` または `tracking`</td><td>`comment`</td><td>string</td></tr> <tr><td>`flag`</td><td>`flag`</td><td>boolean</td></tr> <tr><td>`integer`</td><td>`integer`</td><td>integer</td></tr> <tr><td>`choice` または `select`</td><td>`choice`</td><td>string（選択肢ID）</td></tr> <tr><td>`link`</td><td>`comment`</td><td>string（アノテーションID）</td></tr> </table> """



    comment: str
    """"""










@dataclass_json
@dataclass
class Annotation:
    """
    
    """
    project_id: str
    """"""



    task_id: str
    """"""



    input_data_id: str
    """"""



    details: List[AnnotationDetail]
    """"""



    comment: Optional[str]
    """"""



    updated_datetime: Optional[str]
    """新規作成時は未指定、更新時は必須（更新前の日時） """










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
class FullAnnotationData:
    """
    
    """
    type: str
    """Unknown"""



    data_uri: str
    """"""



    left_top: Point
    """"""



    right_bottom: Point
    """"""



    points: List[Point]
    """"""



    point: Point
    """"""



    begin: float
    """開始時間（ミリ秒）。小数点以下はミリ秒以下を表します。"""



    end: float
    """終了時間（ミリ秒）。小数点以下はミリ秒以下を表します。"""



    data: str
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



    path: Optional[str]
    """data_holding_typeがouterの場合のみ存在し、データへのパスが格納される"""



    additional_data_list: Optional[List[FullAnnotationAdditionalData]]
    """"""



    comment: Optional[str]
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



    details: Optional[List[FullAnnotationDetail]]
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



    attributes: Optional[object]
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







