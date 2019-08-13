# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace
"""
annofabapiのmodelをDataClassで定義したクラス。(swagger.yamlの ``components.schemes`` )

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照.

    oneOf, allOfなどは正しく表現できない可能性がある。

"""

import warnings  # pylint: disable=unused-import
from dataclasses import dataclass
from typing import Any, Dict, List, NewType, Optional, Tuple, Union  # pylint: disable=unused-import

from dataclasses_json import dataclass_json

from annofabapi.models import (AccountAuthority, AdditionalDataDefinitionType, AnnotationDataHoldingType,
                               AnnotationType, AssigneeRuleOfResubmittedTask, InputDataOrder, InputDataType,
                               InspectionStatus, OrganizationMemberRole, OrganizationMemberStatus, PricePlan,
                               ProjectMemberRole, ProjectMemberStatus, ProjectStatus, TaskPhase, TaskStatus)

### 以下は自動生成の部分



@dataclass_json
@dataclass
class AggregationResult:
    """
    
    """
    type: str
    """他と区別するために `CountResult` を指定します """

    name: str
    """"""

    field: str
    """"""

    items: List[Count]
    """"""
@dataclass_json
@dataclass
class AnnotationEditorFeature:
    """
    
    """
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
@dataclass_json
@dataclass
class AnnotationQuery:
    """
    
    """
    task_id: str
    """"""

    exact_match_task_id: bool
    """タスクIDの検索方法を指定します。 trueの場合は完全一致検索、falseの場合は中間一致検索です。 """

    input_data_id: str
    """"""

    exact_match_input_data_id: bool
    """入力データIDの検索方法を指定します。 trueの場合は完全一致検索、falseの場合は中間一致検索です。 """

    label_id: str
    """"""

    attributes: List[AdditionalData]
    """"""
@dataclass_json
@dataclass
class BatchAnnotation:
    """
    
    """
    project_id: str
    """"""

    task_id: str
    """"""

    input_data_id: str
    """"""

    annotation_id: str
    """annotation_type が classification の場合は label_id と同じ値が格納されます。 """

    label_id: str
    """"""

    additional_data_list: List[FullAnnotationAdditionalData]
    """"""

    updated_datetime: str
    """"""
@dataclass_json
@dataclass
class Count:
    """
    
    """
    key: str
    """"""

    count: int
    """"""

    aggregations: List[AggregationResult]
    """"""
@dataclass_json
@dataclass
class CountResult:
    """
    
    """
    type: str
    """他と区別するために `CountResult` を指定します """

    name: str
    """"""

    field: str
    """"""

    items: List[Count]
    """"""
@dataclass_json
@dataclass
class DataPath:
    """
    
    """
    url: str
    """ファイルアップロード用の一時URLです。このURLにファイルをアップロードします。"""

    path: str
    """アップロードしたファイルをAFの [入力データ](#tag/af-input) や [補助情報](#tag/af-supplementary) に登録するとき、この`path`を指定します。"""
@dataclass_json
@dataclass
class Duplicated:
    """
    値の重複が許可されていない属性の重複エラー
    """
    label_id: str
    """"""

    annotation_id: str
    """"""

    additional_data: AdditionalData
    """"""

    type: str
    """Duplicated"""
@dataclass_json
@dataclass
class DuplicatedSegmentationV2:
    """
    塗りつぶしv2のラベルに対する1ラベルにつき1アノテーションまでの制約違反エラー
    """
    label_id: str
    """"""

    annotation_ids: List[str]
    """"""

    type: str
    """DuplicatedSegmentationV2"""
@dataclass_json
@dataclass
class EmptyAttribute:
    """
    属性が未入力であるエラー
    """
    label_id: str
    """"""

    annotation_id: str
    """"""

    additional_data_definition_id: str
    """"""

    type: str
    """EmptyAttribute"""

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
class FullAnnotationDataClassification:
    """
    
    """
    type: str
    """Classification"""
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
class FullAnnotationDataUnknown:
    """
    annotation_typeにデータ構造が一致していない場合に、元のdata文字列をそのまま記述したもの。
    """
    data: str
    """"""

    type: str
    """Unknown"""
@dataclass_json
@dataclass
class HistogramItem:
    """
    
    """
    begin: float
    """"""

    end: float
    """"""

    count: int
    """"""

@dataclass_json
@dataclass
class InspectionDataPoint:
    """
    問題のある部分を示す座標 
    """
    x: int
    """"""

    y: int
    """"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """
@dataclass_json
@dataclass
class InspectionDataPolyline:
    """
    問題のある部分を示すポリライン 
    """
    coordinates: List[InspectionDataPolylineCoordinates]
    """ポリラインを構成する頂点の配列 """

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """
@dataclass_json
@dataclass
class InspectionDataPolylineCoordinates:
    """
    
    """
    x: int
    """"""

    y: int
    """"""
@dataclass_json
@dataclass
class InspectionDataTime:
    """
    問題のある時間帯を表す区間 
    """
    start: float
    """"""

    end: float
    """"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """

@dataclass_json
@dataclass
class InspectionStatistics:
    """
    
    """
    project_id: str
    """"""

    date: str
    """集計日"""

    breakdown: InspectionStatisticsBreakdown
    """"""
@dataclass_json
@dataclass
class InspectionStatisticsBreakdown:
    """
    
    """
    labels: dict(str, InspectionStatisticsPhrases)
    """ラベルごとの指摘集計結果"""

    no_label: InspectionStatisticsPhrases
    """"""
@dataclass_json
@dataclass
class InspectionStatisticsPhrases:
    """
    
    """
    phrases: dict(str, int)
    """定型指摘ごとの合計数"""

    no_phrase: int
    """非定型指摘の合計数"""
@dataclass_json
@dataclass
class InstructionHistory:
    """
    
    """
    history_id: str
    """"""

    account_id: str
    """"""

    updated_datetime: str
    """"""
@dataclass_json
@dataclass
class InstructionImage:
    """
    
    """
    image_id: str
    """"""

    path: str
    """"""

    url: str
    """"""

    etag: str
    """"""
@dataclass_json
@dataclass
class InvalidAnnotationData:
    """
    アノテーションデータ不正エラー
    """
    label_id: str
    """"""

    annotation_id: str
    """"""

    message: str
    """"""

    type: str
    """InvalidAnnotationData"""
@dataclass_json
@dataclass
class InvalidCommentFormat:
    """
    コメントが正規表現に合致しないエラー
    """
    label_id: str
    """"""

    annotation_id: str
    """"""

    additional_data_definition_id: str
    """"""

    type: str
    """InvalidCommentFormat"""
@dataclass_json
@dataclass
class InvalidLinkTarget:
    """
    リンク先アノテーションが許可されているラベルでないエラー
    """
    label_id: str
    """"""

    annotation_id: str
    """"""

    additional_data_definition_id: str
    """"""

    type: str
    """InvalidLinkTarget"""
@dataclass_json
@dataclass
class Message:
    """
    
    """
    message: str
    """多言語対応"""
@dataclass_json
@dataclass
class MyAccount:
    """
    
    """
    account_id: str
    """"""

    user_id: str
    """"""

    username: str
    """"""

    email: str
    """"""

    lang: str
    """"""

    keylayout: str
    """"""

    authority: AccountAuthority
    """"""

    updated_datetime: str
    """"""

    reset_requested_email: str
    """"""

    errors: List[str]
    """"""
@dataclass_json
@dataclass
class MyOrganization:
    """
    
    """
    organization_id: str
    """"""

    name: str
    """"""

    email: str
    """"""

    price_plan: PricePlan
    """"""

    summary: OrganizationSummary
    """"""

    created_datetime: str
    """"""

    updated_datetime: str
    """"""

    my_role: OrganizationMemberRole
    """"""

    my_status: OrganizationMemberStatus
    """"""

@dataclass_json
@dataclass
class OutOfImageBounds:
    """
    画像範囲外にアノテーションがはみ出しているエラー
    """
    label_id: str
    """"""

    annotation_id: str
    """"""

    type: str
    """OutOfImageBounds"""

@dataclass_json
@dataclass
class UnknownAdditionalData:
    """
    何らかの原因で、アノテーション仕様にない属性がついているエラー
    """
    label_id: str
    """"""

    annotation_id: str
    """"""

    additional_data_definition_id: str
    """"""

    type: str
    """UnknownAdditionalData"""
@dataclass_json
@dataclass
class UnknownLabel:
    """
    何らかの原因で、アノテーション仕様にないラベルがついているエラー
    """
    label_id: str
    """"""

    annotation_id: str
    """"""

    type: str
    """UnknownLabel"""
@dataclass_json
@dataclass
class UnknownLinkTarget:
    """
    指定されたIDに該当するアノテーションが存在しないエラー
    """
    label_id: str
    """"""

    annotation_id: str
    """"""

    additional_data_definition_id: str
    """"""

    type: str
    """UnknownLinkTarget"""
