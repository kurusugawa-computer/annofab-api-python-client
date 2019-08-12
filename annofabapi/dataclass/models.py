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
class AcceptOrganizationInvitationRequest:
    """
    
    """
    token: str
    """"""
@dataclass_json
@dataclass
class Account:
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
@dataclass_json
@dataclass
class AccountWorktimeStatistics:
    """
    
    """
    account_id: str
    """"""

    by_tasks: List[WorktimeStatisticsItem]
    """"""

    by_inputs: List[WorktimeStatisticsItem]
    """"""
@dataclass_json
@dataclass
class AdditionalData:
    """
    
    """
    additional_data_definition_id: str
    """"""

    flag: bool
    """"""

    interger: int
    """"""

    comment: str
    """"""

    choice: str
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

    comment: str
    """"""

    updated_datetime: str
    """新規作成時は未指定、更新時は必須（更新前の日時） """
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

    data: OneOfstringFullAnnotationData
    """data_holding_type が inner の場合のみ存在し、annotation_type に応じたデータの値が格納されます。 `string`もしくは`object`の値を指定することができ、`string`の形式は次の通りです。   * annotation_type が bounding_box の場合: 左上x,左上y,右下x,右下y のCSV文字列形式。   * annotation_type が polygon/polyline の場合: x1,y1,x2,y2, ... のCSV文字列形式。   * annotation_type が segmentation または segmentation_v2 の場合: 塗っていないところは rgba(0,0,0,0)、塗ったところは rgba(255,255,255,1) の PNGデータをBase64エンコードしたもの。   * annotation_type が classification の場合: data 属性は存在しない。   * annotation_type が range の場合: 開始時間,終了時間 のCSV文字列形式。 """

    path: str
    """data_holding_typeがouterの場合のみ存在し、データのパスが格納される (現在はアノテーションIDと等しい)"""

    etag: str
    """data_holding_typeがouterの場合のみ存在し、データのETagが格納される"""

    url: str
    """data_holding_typeがouterの場合のみ存在し、データへの一時URLが格納される"""

    additional_data_list: List[AdditionalData]
    """各要素は、 [アノテーション仕様](#operation/getAnnotationSpecs)で定義された属性（`additional_data_definitions`内）のいずれかの要素と対応づけます。 各要素は、どの属性なのかを表す`additional_data_definition_id`、値が必要です。値は、属性の種類に対応するキーに格納します（下表）。  <table> <tr><th>アノテーション属性の種類<br>（`additional_data_definition`の`type`）</th><th>属性の値を格納するキー</th><th>データ型</th></tr> <tr><td>`comment` または `tracking`</td><td>`comment`</td><td>string</td></tr> <tr><td>`flag`</td><td>`flag`</td><td>boolean</td></tr> <tr><td>`integer`</td><td>`integer`</td><td>integer</td></tr> <tr><td>`choice` または `select`</td><td>`choice`</td><td>string（選択肢ID）</td></tr> <tr><td>`link`</td><td>`comment`</td><td>string（アノテーションID）</td></tr> </table> """

    comment: str
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
class AnnotationSpecs:
    """
    
    """
    project_id: str
    """"""

    labels: List[Label]
    """"""

    inspection_phrases: List[InspectionPhrase]
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
class AnnotationSpecsRequest:
    """
    
    """
    labels: List[Label]
    """ラベル """

    inspection_phrases: List[InspectionPhrase]
    """定型指摘 """

    comment: str
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
class BatchAnnotationRequestItemDelete:
    """
    アノテーション削除
    """
    project_id: str
    """"""

    task_id: str
    """"""

    input_data_id: str
    """"""

    annotation_id: str
    """annotation_type が classification の場合は label_id と同じ値が格納されます。 """

    updated_datetime: str
    """"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """
@dataclass_json
@dataclass
class BatchAnnotationRequestItemPut:
    """
    アノテーション更新
    """
    data: BatchAnnotation
    """"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """
@dataclass_json
@dataclass
class BatchInputDataRequestItemDelete:
    """
    入力データ削除
    """
    project_id: str
    """"""

    input_data_id: str
    """"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """
@dataclass_json
@dataclass
class BatchInspectionRequestItemDelete:
    """
    検査コメント削除
    """
    project_id: str
    """"""

    task_id: str
    """"""

    input_data_id: str
    """"""

    inspection_id: str
    """"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """
@dataclass_json
@dataclass
class BatchInspectionRequestItemPut:
    """
    検査コメント更新
    """
    data: Inspection
    """"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """
@dataclass_json
@dataclass
class BatchTaskRequestItemDelete:
    """
    タスク削除
    """
    project_id: str
    """"""

    task_id: str
    """"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """
@dataclass_json
@dataclass
class CacheRecord:
    """
    
    """
    input: str
    """"""

    members: str
    """"""

    project: str
    """"""

    instruction: str
    """"""

    specs: str
    """"""

    statistics: str
    """"""

    organization: str
    """"""

    supplementary: str
    """"""
@dataclass_json
@dataclass
class ChangePasswordRequest:
    """
    
    """
    user_id: str
    """"""

    old_password: str
    """"""

    new_password: str
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
class ConfirmAccountDeleteRequest:
    """
    
    """
    token: str
    """"""
@dataclass_json
@dataclass
class ConfirmResetEmailRequest:
    """
    
    """
    token: str
    """"""
@dataclass_json
@dataclass
class ConfirmResetPasswordRequest:
    """
    
    """
    user_id: str
    """"""

    confirmation_code: str
    """"""

    new_password: str
    """"""
@dataclass_json
@dataclass
class ConfirmSignUpRequest:
    """
    
    """
    account_id: str
    """"""

    user_id: str
    """"""

    password: str
    """"""

    username: str
    """"""

    lang: str
    """"""

    keylayout: str
    """"""

    confirmation_code: str
    """"""
@dataclass_json
@dataclass
class ConfirmVerifyEmailRequest:
    """
    
    """
    token: Token
    """"""

    confirmation_code: str
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
class Error:
    """
    
    """
    error_code: str
    """"""

    message: str
    """エラーの概要"""

    ext: object
    """補足情報"""
@dataclass_json
@dataclass
class ErrorAlreadyUpdated:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorExpiredToken:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorForbiddenResource:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorInternalServerError:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorInvalidBody:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorInvalidPath:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorInvalidQueryParam:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorLoginFailed:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorMissingNecessaryQueryParam:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorMissingResource:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorPasswordResetRequired:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorRefreshTokenExpired:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorStateMismatch:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorTimeout:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorUnauthorizedApi:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class ErrorUnderMaintenance:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class Errors:
    """
    
    """
    errors: List[Error]
    """"""

    context: object
    """内部補足情報"""
@dataclass_json
@dataclass
class FullAnnotation:
    """
    
    """
    project_id: str
    """"""

    task_id: str
    """"""

    task_phase: TaskPhase
    """"""

    task_phase_stage: int
    """"""

    task_status: TaskStatus
    """"""

    input_data_id: str
    """"""

    input_data_name: str
    """"""

    details: List[FullAnnotationDetail]
    """"""

    updated_datetime: str
    """"""
@dataclass_json
@dataclass
class FullAnnotationAdditionalData:
    """
    
    """
    additional_data_definition_id: str
    """"""

    additional_data_definition_name: InternationalizationMessage
    """"""

    type: AdditionalDataDefinitionType
    """"""

    flag: bool
    """typeがflagの場合に、フラグのON(true)またはOFF(false)が格納される"""

    integer: int
    """typeがintegerの場合に、整数値が格納される"""

    comment: str
    """* typeがcommentの場合、コメントの値 * typeがtrackingの場合、トラッキングID * typeがlinkの場合、リンク先のアノテーションID """

    choice: str
    """"""

    choice_name: InternationalizationMessage
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
class FullAnnotationDetail:
    """
    
    """
    annotation_id: str
    """annotation_type が classification の場合は label_id と同じ値が格納されます。 """

    user_id: str
    """"""

    label_id: str
    """"""

    label_name: InternationalizationMessage
    """"""

    annotation_type: AnnotationType
    """"""

    data_holding_type: AnnotationDataHoldingType
    """"""

    data: FullAnnotationData
    """"""

    path: str
    """data_holding_typeがouterの場合のみ存在し、データへのパスが格納される"""

    additional_data_list: List[FullAnnotationAdditionalData]
    """"""

    comment: str
    """"""
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
class InlineResponse200:
    """
    
    """
    list: List[MyOrganization]
    """現在のページ番号に含まれる0件以上の所属組織です。"""

    page_no: float
    """現在のページ番号です。"""

    total_page_no: float
    """指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる所属組織が0件であっても、総ページ数は1となります。"""

    total_count: float
    """検索結果の総件数。"""

    over_limit: bool
    """検索結果が1万件を超えた場合にtrueとなる。"""

    aggregations: List[AggregationResult]
    """Aggregationによる集約結果。"""
@dataclass_json
@dataclass
class InlineResponse2001:
    """
    
    """
    list: List[Project]
    """現在のページ番号に含まれる0件以上のプロジェクトです。"""

    page_no: float
    """現在のページ番号です。"""

    total_page_no: float
    """指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるプロジェクトが0件であっても、総ページ数は1となります。"""

    total_count: float
    """検索結果の総件数。"""

    over_limit: bool
    """検索結果が1万件を超えた場合にtrueとなる。"""

    aggregations: List[AggregationResult]
    """Aggregationによる集約結果。"""
@dataclass_json
@dataclass
class InlineResponse2002:
    """
    
    """
    list: List[OrganizationMember]
    """"""

    page_no: float
    """現在のページ番号です。"""

    total_page_no: float
    """指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる組織メンバーが0件であっても、総ページ数は1となります。"""

    total_count: float
    """検索結果の総件数。"""

    over_limit: bool
    """検索結果が1万件を超えた場合にtrueとなる。"""

    aggregations: List[AggregationResult]
    """Aggregationによる集約結果。"""
@dataclass_json
@dataclass
class InlineResponse2003:
    """
    
    """
    list: List[Project]
    """"""

    has_next: bool
    """"""
@dataclass_json
@dataclass
class InlineResponse2004:
    """
    
    """
    url: str
    """"""
@dataclass_json
@dataclass
class InlineResponse2005:
    """
    
    """
    list: List[ProjectMember]
    """"""

    page_no: float
    """現在のページ番号です。"""

    total_page_no: float
    """指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるプロジェクトメンバーが0件であっても、総ページ数は1となります。"""

    total_count: float
    """検索結果の総件数。"""

    over_limit: bool
    """検索結果が1万件を超えた場合にtrueとなる。"""

    aggregations: List[AggregationResult]
    """Aggregationによる集約結果。"""
@dataclass_json
@dataclass
class InlineResponse2006:
    """
    
    """
    list: List[JobInfo]
    """"""

    has_next: bool
    """"""
@dataclass_json
@dataclass
class InlineResponse2007:
    """
    
    """
    list: List[Task]
    """現在のページ番号に含まれる0件以上のタスクです。"""

    page_no: float
    """現在のページ番号です。"""

    total_page_no: float
    """指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるタスク0件であっても、総ページ数は1となります。"""

    total_count: float
    """検索結果の総件数。"""

    over_limit: bool
    """検索結果が1万件を超えた場合にtrueとなる。"""

    aggregations: List[AggregationResult]
    """Aggregationによる集約結果。"""
@dataclass_json
@dataclass
class InlineResponse2008:
    """
    
    """
    list: List[SingleAnnotation]
    """現在のページ番号に含まれる0件以上のアノテーションです。"""

    page_no: float
    """現在のページ番号です。"""

    total_page_no: float
    """指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるアノテーションが0件であっても、総ページ数は1となります。"""

    total_count: float
    """検索結果の総件数。"""

    over_limit: bool
    """検索結果が1万件を超えた場合にtrueとなる。"""

    aggregations: List[AggregationResult]
    """Aggregationによる集約結果。"""
@dataclass_json
@dataclass
class InlineResponse2009:
    """
    
    """
    list: List[InputData]
    """現在のページ番号に含まれる0件以上の入力データです。"""

    page_no: float
    """現在のページ番号です。"""

    total_page_no: float
    """指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる入力データが0件であっても、総ページ数は1となります。"""

    total_count: float
    """検索結果の総件数。"""

    over_limit: bool
    """検索結果が1万件を超えた場合にtrueとなる。"""

    aggregations: List[AggregationResult]
    """Aggregationによる集約結果。"""
@dataclass_json
@dataclass
class InputData:
    """
    
    """
    input_data_id: str
    """"""

    project_id: str
    """"""

    input_data_name: str
    """表示用の名前です。"""

    input_data_path: str
    """入力データの実体が保存されたパスです。 s3スキーマまたはhttpsスキーマのみサポートしています。 """

    url: str
    """入力データを取得するためのhttpsスキーマのURLです。  このURLはセキュリティのために認証認可が必要となっており、URLだけでは入力データを参照できません。 このURLは内部用であり、常に変更になる可能性があります。そのため、アクセスは保証外となります。 また、このURLのレスポンスは最低1時間キャッシュされます。 キャッシュを無効にしたい場合は、クエリパラメータにアクセス毎にランダムなUUIDなどを付与してください。  設定の不備等でデータが取得できない場合、この属性は設定されません。 """

    etag: str
    """"""

    original_input_data_path: str
    """AF外部のストレージから登録された場合、その外部ストレージ中のパス。 それ以外の場合は値なし """

    original_resolution: Resolution
    """"""

    resized_resolution: Resolution
    """"""

    updated_datetime: str
    """"""

    sign_required: bool
    """データがSigned Cookieによるクロスオリジン配信に対応しているか否かです。 """
@dataclass_json
@dataclass
class InputDataRequest:
    """
    
    """
    input_data_name: str
    """表示用の名前"""

    input_data_path: str
    """AnnoFabに登録する入力データの実体が保存されたパスです。  対応スキーマ： * s3 * https * data（廃止予定）  場面別の使い分け： * [一時データ保存先取得API](#operation/createTempPath)を使ってAFにアップロードした場合: `s3://ANNOFAB-BUCKET/PATH/TO/INPUT_DATA` * [プライベートストレージ](/docs/faq/#prst9c)の場合     * `https://YOUR-DOMAIN/PATH/TO/INPUT_DATA`     * `s3://YOUR-BUCKET-FOR-PRIVATE-STORAGE/PATH/TO/INPUT_DATA`         * S3プライベートストレージのパスを登録する場合、[事前に認可の設定が必要](/docs/faq/#m0b240)です。 * dataスキーマでアップロードする場合: `data://....`     * dataスキーマは、4MB以内の画像であれば[一時データ保存先取得API](#operation/createTempPath)を使わずに直接アップロードできるので便利です。 """

    last_updated_datetime: str
    """新規作成時は未指定、更新時は必須（更新前の日時） """

    sign_required: bool
    """データがSigned Cookieによるクロスオリジン配信に対応しているか否かです。<br> このオプションを有効にする場合は、`input_data_path`として、AnnoFabのAWS IDをTrusted Signerとして登録したCloudFrontのURLを指定してください。 """
@dataclass_json
@dataclass
class InputDataSummary:
    """
    ある入力データのバリデーション結果です。入力データIDをキーに引けるようにMap[入力データID, バリデーション結果]となっています
    """
    input_data_id: str
    """"""

    inspection_summary: str
    """"""

    annotation_summaries: List[ValidationError]
    """"""
@dataclass_json
@dataclass
class Inspection:
    """
    検査コメント
    """
    project_id: str
    """"""

    task_id: str
    """"""

    input_data_id: str
    """"""

    inspection_id: str
    """"""

    phase: TaskPhase
    """"""

    phase_stage: int
    """"""

    commenter_account_id: str
    """"""

    annotation_id: str
    """"""

    data: OneOfInspectionDataPointInspectionDataPolylineInspectionDataTime
    """"""

    parent_inspection_id: str
    """"""

    phrases: List[str]
    """選択された定型指摘ID. 未選択時は空"""

    comment: str
    """"""

    status: InspectionStatus
    """"""

    created_datetime: str
    """"""

    updated_datetime: str
    """新規作成時は未指定、更新時は必須（更新前の日時） """
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
class InspectionPhrase:
    """
    
    """
    id: str
    """"""

    text: InternationalizationMessage
    """"""
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
class InternationalizationMessage:
    """
    
    """
    messages: List[InternationalizationMessageMessages]
    """"""

    default_lang: str
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
class InviteOrganizationMemberRequest:
    """
    
    """
    role: OrganizationMemberRole
    """"""
@dataclass_json
@dataclass
class JobInfo:
    """
    
    """
    project_id: str
    """"""

    job_type: str
    """"""

    job_id: str
    """"""

    job_status: str
    """"""

    job_execution: object
    """ジョブの内部情報"""

    job_detail: object
    """ジョブ結果の内部情報"""

    created_datetime: str
    """"""

    updated_datetime: str
    """"""
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
class LabelStatistics:
    """
    
    """
    label_id: str
    """"""

    completed_labels: int
    """ラベルごとの受入が完了したアノテーション数"""

    wip_labels: int
    """ラベルごとの受入が完了していないアノテーション数"""
@dataclass_json
@dataclass
class LoginRequest:
    """
    
    """
    user_id: str
    """"""

    password: str
    """"""
@dataclass_json
@dataclass
class LoginResponse:
    """
    
    """
    token: Token
    """"""
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
class Organization:
    """
    
    """
    organization_id: str
    """"""

    organization_name: str
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
@dataclass_json
@dataclass
class OrganizationActivity:
    """
    
    """
    organization_id: str
    """"""

    created_datetime: str
    """"""

    storage_usage_bytes: float
    """"""
@dataclass_json
@dataclass
class OrganizationMember:
    """
    
    """
    organization_id: str
    """"""

    account_id: str
    """"""

    user_id: str
    """"""

    username: str
    """"""

    role: OrganizationMemberRole
    """"""

    status: OrganizationMemberStatus
    """"""

    created_datetime: str
    """"""

    updated_datetime: str
    """"""
@dataclass_json
@dataclass
class OrganizationRegistrationRequest:
    """
    
    """
    organization_name: str
    """"""

    organization_email: str
    """"""

    price_plan: PricePlan
    """"""
@dataclass_json
@dataclass
class OrganizationSummary:
    """
    
    """
    last_tasks_updated_datetime: str
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
class PasswordResetRequest:
    """
    
    """
    email: str
    """"""
@dataclass_json
@dataclass
class PhaseStatistics:
    """
    
    """
    phase: str
    """"""

    worktime: str
    """"""
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
class Project:
    """
    
    """
    project_id: str
    """"""

    organization_id: str
    """"""

    title: str
    """"""

    overview: str
    """"""

    status: ProjectStatus
    """"""

    input_data_type: InputDataType
    """"""

    configuration: ProjectConfiguration
    """"""

    created_datetime: str
    """"""

    updated_datetime: str
    """"""

    summary: ProjectSummary
    """"""
@dataclass_json
@dataclass
class ProjectAccountStatistics:
    """
    
    """
    account_id: str
    """"""

    histories: List[ProjectAccountStatisticsHistory]
    """"""
@dataclass_json
@dataclass
class ProjectAccountStatisticsHistory:
    """
    
    """
    date: str
    """"""

    tasks_completed: int
    """"""

    tasks_rejected: int
    """"""

    worktime: str
    """"""
@dataclass_json
@dataclass
class ProjectConfiguration:
    """
    
    """
    project_rule: str
    """"""

    number_of_inspections: int
    """検査回数。 * 0回：教師付け -> 受入 * 1回：教師付け -> 検査 -> 受入 * n回(n >= 2)：教師付け -> 検査1 -> ... -> 検査n -> 受入 """

    assignee_rule_of_resubmitted_task: AssigneeRuleOfResubmittedTask
    """"""

    max_tasks_per_member: int
    """保留中のタスクを除き、1人（オーナー以外）に割り当てられるタスク数上限。未指定の場合は10件として扱う。"""

    max_tasks_per_member_including_hold: int
    """保留中のタスクを含めて、1人（オーナー以外）に割り当てられるタスク数上限。未指定の場合は20件として扱う。"""

    input_data_max_long_side_length: int
    """入力データ画像の長辺の最大値（未指定時は4096px）。  画像をアップロードすると、長辺がこの値になるように画像が自動で圧縮されます。 アノテーションの座標は、もとの解像度の画像でつけたものに復元されます。  大きな数値を設定すると入力データ画像のサイズが大きくなり、生産性低下やブラウザで画像を表示できない懸念があります。注意して設定してください。 """

    sampling_inspection_rate: int
    """抜取検査率。0-100のパーセント値で指定し、未指定の場合は100%として扱う。"""

    sampling_acceptance_rate: int
    """抜取受入率。0-100のパーセント値で指定し、未指定の場合は100%として扱う。"""

    private_storage_aws_iam_role_arn: str
    """AWS IAMロール。ビジネスプランでのS3プライベートストレージの認可で使います。 [S3プライベートストレージの認可の設定についてはこちら](/docs/faq/#m0b240)をご覧ください。 """
@dataclass_json
@dataclass
class ProjectCopyRequest:
    """
    
    """
    dest_project_id: str
    """"""

    dest_title: str
    """"""

    dest_overview: str
    """"""

    copy_inputs: bool
    """「入力データ」をコピーするかどうかを指定します。 """

    copy_tasks: bool
    """「タスク」をコピーするかどうかを指定します。  以下の場合、copy_tasks を true に設定するとエラーとなります。 * copy_tasks_with_annotations が true に設定されているとき * copy_inputs が false に設定されているとき """

    copy_annotations: bool
    """「アノテーション」をコピーするかどうかを指定します。  以下の場合、copy_annotations を true に設定するとエラーとなります。 * copy_tasks_with_annotations が true に設定されているとき * copy_inputs が false に設定されているとき * copy_tasks が false に設定されているとき """

    copy_webhooks: bool
    """「Webhook」をコピーするかどうかを指定します。 """

    copy_tasks_with_annotations: bool
    """「タスク」「アノテーション」をコピーするかどうかを指定します。  以下の場合、copy_tasks_with_annotations を true に設定するとエラーとなります。 * copy_inputs が false に設定されているとき * copy_tasks が true に設定されているとき """

    copy_supplementaly_data: bool
    """「補助情報」をコピーするかどうかを指定します。  以下の場合、copy_supplementaly_data を true に設定するとエラーとなります。 * copy_inputs が false に設定されているとき """

    copy_instructions: bool
    """「作業ガイド」をコピーするかどうかを指定します。 """
@dataclass_json
@dataclass
class ProjectMember:
    """
    
    """
    project_id: str
    """"""

    account_id: str
    """"""

    user_id: str
    """"""

    username: str
    """"""

    member_status: ProjectMemberStatus
    """"""

    member_role: ProjectMemberRole
    """"""

    updated_datetime: str
    """"""

    created_datetime: str
    """"""

    sampling_inspection_rate: int
    """メンバー固有の抜取検査率。0-100のパーセント値で指定する。値が指定された場合、プロジェクトの抜取検査率を指定の値で上書きする。"""
@dataclass_json
@dataclass
class ProjectMemberRequest:
    """
    
    """
    member_status: ProjectMemberStatus
    """"""

    member_role: ProjectMemberRole
    """"""

    last_updated_datetime: str
    """新規作成時は未指定、更新時は必須（更新前の日時） """
@dataclass_json
@dataclass
class ProjectSummary:
    """
    
    """
    last_tasks_updated_datetime: str
    """"""
@dataclass_json
@dataclass
class ProjectTaskStatistics:
    """
    
    """
    phase: TaskPhase
    """"""

    status: TaskStatus
    """"""

    count: int
    """"""

    work_timespan: int
    """累計実作業時間(ミリ秒)"""
@dataclass_json
@dataclass
class ProjectTaskStatisticsHistory:
    """
    
    """
    date: str
    """"""

    tasks: List[ProjectTaskStatistics]
    """"""
@dataclass_json
@dataclass
class PutMyAccountRequest:
    """
    
    """
    user_id: str
    """"""

    username: str
    """"""

    lang: str
    """"""

    keylayout: str
    """"""

    token: Token
    """"""

    last_updated_datetime: str
    """新規作成時は未指定、更新時は必須（更新前の日時） """
@dataclass_json
@dataclass
class PutOrganizationMemberRoleRequest:
    """
    
    """
    role: OrganizationMemberRole
    """"""

    last_updated_datetime: str
    """新規作成時は未指定、更新時は必須（更新前の日時） """
@dataclass_json
@dataclass
class PutOrganizationNameRequest:
    """
    
    """
    organization_id: str
    """"""

    organization_name: str
    """"""

    last_updated_datetime: str
    """"""
@dataclass_json
@dataclass
class PutProjectRequest:
    """
    
    """
    title: str
    """"""

    overview: str
    """"""

    status: str
    """"""

    input_data_type: InputDataType
    """"""

    organization_name: str
    """プロジェクトの所属組織を変更する場合は、ここに変更先の組織名を指定します。  * 所属組織を変更する前にプロジェクトを停止する必要があります。 * APIを呼び出すアカウントは、変更先組織の管理者またはオーナーである必要があります。 * 変更後の組織に所属していないプロジェクトメンバーも残りますが、作業はできません。あらためて組織に招待してください。 """

    configuration: ProjectConfiguration
    """"""

    last_updated_datetime: str
    """新規作成時は未指定、更新時は必須（更新前の日時） """

    force_suspend: bool
    """作業中タスクがあるプロジェクトを停止する時trueにして下さい"""
@dataclass_json
@dataclass
class RefreshTokenRequest:
    """
    
    """
    refresh_token: str
    """"""
@dataclass_json
@dataclass
class ResetEmailRequest:
    """
    
    """
    email: str
    """"""
@dataclass_json
@dataclass
class ResetPasswordRequest:
    """
    
    """
    token: str
    """"""
@dataclass_json
@dataclass
class Resolution:
    """
    画像などの解像度 
    """
    width: float
    """"""

    height: float
    """"""
@dataclass_json
@dataclass
class SignUpRequest:
    """
    
    """
    email: str
    """"""
@dataclass_json
@dataclass
class SimpleAnnotation:
    """
    
    """
    annotation_format_version: str
    """アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、AnnoFabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 """

    project_id: str
    """"""

    task_id: str
    """"""

    task_phase: TaskPhase
    """"""

    task_phase_stage: int
    """"""

    task_status: TaskStatus
    """"""

    input_data_id: str
    """"""

    input_data_name: str
    """"""

    details: List[SimpleAnnotationDetail]
    """"""
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

    attributes: object
    """キーに属性の名前、値に各属性の値が入った辞書構造です。 """
@dataclass_json
@dataclass
class SingleAnnotation:
    """
    
    """
    project_id: str
    """"""

    task_id: str
    """"""

    input_data_id: str
    """"""

    detail: SingleAnnotationDetail
    """"""

    updated_datetime: str
    """"""
@dataclass_json
@dataclass
class SingleAnnotationDetail:
    """
    
    """
    annotation_id: str
    """annotation_type が classification の場合は label_id と同じ値が格納されます。 """

    account_id: str
    """"""

    label_id: str
    """"""

    data_holding_type: AnnotationDataHoldingType
    """"""

    data: FullAnnotationData
    """"""

    etag: str
    """data_holding_typeがouterの場合のみ存在し、データのETagが格納される"""

    url: str
    """data_holding_typeがouterの場合のみ存在し、データへの一時URLが格納される"""

    additional_data_list: List[FullAnnotationAdditionalData]
    """"""

    created_datetime: str
    """"""

    updated_datetime: str
    """"""
@dataclass_json
@dataclass
class SupplementaryData:
    """
    
    """
    project_id: str
    """"""

    input_data_id: str
    """"""

    supplementary_data_id: str
    """"""

    supplementary_data_name: str
    """表示用の名前"""

    supplementary_data_path: str
    """補助情報の実体が保存されたパスです。 s3スキーマまたはhttpsスキーマのみサポートしています。 """

    url: str
    """このフィールドはAF内部での利用のみを想定しており、依存しないでください。"""

    etag: str
    """"""

    supplementary_data_type: str
    """"""

    supplementary_data_number: int
    """表示順を表す数値（昇順）。同じ入力データに対して複数の補助情報で表示順が重複する場合、順序不定になります。"""

    updated_datetime: str
    """"""
@dataclass_json
@dataclass
class SupplementaryDataRequest:
    """
    
    """
    supplementary_data_name: str
    """表示用の名前"""

    supplementary_data_path: str
    """AnnoFabに登録する補助情報の実体が保存されたパスです。  対応スキーマ：s3, https  * [一時データ保存先取得API](#operation/createTempPath)を使ってAFにアップロードしたファイルパスの場合     * `s3://ANNOFAB-BUCKET/PATH/TO/INPUT_DATA`     * 補助情報作成/更新API成功時、アップロードしたファイルが一時データ保存先からコピーされます。         * APIのレスポンスからアップロードしたファイルのコピー先パス（s3スキーマ）を取得できます。 * すでにAFに登録されている補助情報のパスの場合     * `s3://ANNOFAB-SUPPLEMENTARY-BUCKET/PATH/TO/INPUT_DATA`     * ファイルはコピーされません。 * [プライベートストレージ](/docs/faq/#prst9c)のパスの場合     * `https://YOUR-DOMAIN/PATH/TO/INPUT_DATA`     * `s3://YOUR-BUCKET-FOR-PRIVATE-STORAGE/PATH/TO/INPUT_DATA`         * S3プライベートストレージのパスを登録する場合、[事前に認可の設定が必要](/docs/faq/#m0b240)です。     * AFにファイルはコピーされません。 """

    supplementary_data_type: str
    """"""

    supplementary_data_number: int
    """表示順を表す数値（昇順）。同じ入力データに対して複数の補助情報で表示順が重複する場合、順序不定になります。"""

    last_updated_datetime: str
    """"""
@dataclass_json
@dataclass
class Task:
    """
    
    """
    project_id: str
    """"""

    task_id: str
    """"""

    phase: TaskPhase
    """"""

    phase_stage: int
    """"""

    status: TaskStatus
    """"""

    input_data_id_list: List[str]
    """"""

    account_id: str
    """"""

    histories_by_phase: List[TaskHistoryShort]
    """"""

    work_timespan: int
    """累計実作業時間(ミリ秒)"""

    number_of_rejections: int
    """このタスクが差戻しされた回数（すべてのフェーズでの差戻し回数の合計  このフィールドは、どのフェーズで何回差戻されたかを区別できないため、廃止予定です。 `histories_by_phase` で各フェーズの回数を計算することで、差戻し回数が分かります。  例）`acceptance`フェーズが3回ある場合、`acceptance`フェーズで2回差し戻しされたことになります。 """

    started_datetime: str
    """"""

    updated_datetime: str
    """"""

    sampling: str
    """* 'inspection_skipped' - このタスクが抜取検査の対象外となり、検査フェーズをスキップしたことを表す。 * 'inspection_stages_skipped' - このタスクが抜取検査の対象外となり、検査フェーズのステージを一部スキップしたことを表す。 * `acceptance_skipped` - このタスクが抜取検査の対象外となり、受入フェーズをスキップしたことを表す。 * `inspection_and_acceptance_skipped` - このタスクが抜取検査の対象外となり、検査・受入フェーズをスキップしたことを表す  未指定時はこのタスクが抜取検査の対象となったことを表す。(通常のワークフローを通過する) """
@dataclass_json
@dataclass
class TaskGenerateRequest:
    """
    
    """
    task_generate_rule: OneOfTaskGenerateRuleByCountTaskGenerateRuleByDirectoryTaskGenerateRuleByInputDataCsv
    """* `TaskGenerateRuleByCount`: 1つのタスクに割りあてる入力データの個数を指定してタスクを生成します。 * `TaskGenerateRuleByDirectory`: 入力データ名をファイルパスに見立て、ディレクトリ単位でタスクを生成します。 """

    task_id_prefix: str
    """生成するタスクIDのプレフィックス"""

    project_last_updated_datetime: str
    """プロジェクトの最終更新日時。タスク生成の排他制御に使用。"""
@dataclass_json
@dataclass
class TaskGenerateRuleByCount:
    """
    1つのタスクに割りあてる入力データの個数を指定してタスクを生成します。
    """
    allow_duplicate_input_data: bool
    """falseのときは、既にタスクに使われている入力データを除外し、まだタスクに使われていない入力データだけを新しいタスクに割り当てます。trueのときは、既にタスクに使われている入力データを除外しません。"""

    input_data_count: int
    """1つのタスクに割り当てる入力データの個数"""

    input_data_order: InputDataOrder
    """"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """
@dataclass_json
@dataclass
class TaskGenerateRuleByDirectory:
    """
    入力データ名をファイルパスに見立て、ディレクトリ単位でタスクを生成します。<br>
    """
    input_data_name_prefix: str
    """タスク生成対象の入力データ名プレフィックス"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """
@dataclass_json
@dataclass
class TaskGenerateRuleByInputDataCsv:
    """
    各タスクへの入力データへの割当を記入したCSVへのS3上のパスを指定してタスクを生成します。
    """
    csv_data_path: str
    """各タスクへの入力データへの割当を記入したCSVへのS3上のパス"""

    type: str
    """[詳しくはこちら](#section/API-Convention/API-_type) """
@dataclass_json
@dataclass
class TaskHistory:
    """
    タスクのあるフェーズで、誰がいつどれくらいの作業時間を費やしたかを表すタスク履歴です。
    """
    project_id: str
    """"""

    task_id: str
    """"""

    task_history_id: str
    """"""

    started_datetime: str
    """"""

    ended_datetime: str
    """"""

    accumulated_labor_time_milliseconds: str
    """"""

    phase: TaskPhase
    """"""

    phase_stage: int
    """"""

    account_id: str
    """"""
@dataclass_json
@dataclass
class TaskHistoryEvent:
    """
    タスク履歴イベントは、タスクの状態が変化した１時点を表します。作業時間は、複数のこれらイベントを集約して計算するものなので、このオブジェクトには含まれません。
    """
    project_id: str
    """"""

    task_id: str
    """"""

    task_history_id: str
    """"""

    created_datetime: str
    """"""

    phase: TaskPhase
    """"""

    phase_stage: int
    """"""

    status: TaskStatus
    """"""

    account_id: str
    """"""
@dataclass_json
@dataclass
class TaskHistoryShort:
    """
    タスクのあるフェーズを誰が担当したかを表します。
    """
    phase: TaskPhase
    """"""

    phase_stage: int
    """"""

    account_id: str
    """"""
@dataclass_json
@dataclass
class TaskOperation:
    """
    
    """
    status: TaskStatus
    """"""

    last_updated_datetime: str
    """新規作成時は未指定、更新時は必須（更新前の日時） """

    account_id: str
    """"""
@dataclass_json
@dataclass
class TaskPhaseStatistics:
    """
    
    """
    project_id: str
    """"""

    date: str
    """"""

    phases: List[PhaseStatistics]
    """"""
@dataclass_json
@dataclass
class TaskRequest:
    """
    
    """
    input_data_id_list: List[str]
    """"""
@dataclass_json
@dataclass
class TaskStart:
    """
    
    """
    phase: TaskPhase
    """"""
@dataclass_json
@dataclass
class TaskValidation:
    """
    タスクの全入力データに対するバリデーション結果です。
    """
    project_id: str
    """"""

    task_id: str
    """"""

    inputs: List[InputDataSummary]
    """"""
@dataclass_json
@dataclass
class TasksInputs:
    """
    
    """
    project_id: str
    """"""

    tasks: List[TasksInputsTask]
    """"""
@dataclass_json
@dataclass
class TasksInputsTask:
    """
    
    """
    task_id: str
    """"""

    phase: TaskPhase
    """"""

    status: TaskStatus
    """"""

    input_data_id_list: List[str]
    """"""
@dataclass_json
@dataclass
class Token:
    """
    
    """
    id_token: str
    """形式は[JWT](https://jwt.io/)。"""

    access_token: str
    """形式は[JWT](https://jwt.io/)。"""

    refresh_token: str
    """形式は[JWT](https://jwt.io/)。"""
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
@dataclass_json
@dataclass
class ValidationError:
    """
    
    """
    label_id: str
    """"""

    annotation_id: str
    """"""

    message: str
    """"""

    type: str
    """UnknownLabel"""

    annotation_ids: List[str]
    """"""

    additional_data_definition_id: str
    """"""

    additional_data: AdditionalData
    """"""
@dataclass_json
@dataclass
class VerifyEmailRequest:
    """
    
    """
    token: Token
    """"""
@dataclass_json
@dataclass
class Webhook:
    """
    
    """
    project_id: str
    """"""

    event_type: str
    """"""

    webhook_id: str
    """"""

    webhook_status: str
    """"""

    method: str
    """"""

    headers: List[WebhookHeader]
    """"""

    body: str
    """"""

    url: str
    """"""

    created_datetime: str
    """"""

    updated_datetime: str
    """"""
@dataclass_json
@dataclass
class WebhookHeader:
    """
    
    """
    name: str
    """"""

    value: str
    """"""
@dataclass_json
@dataclass
class WebhookTestRequest:
    """
    
    """
    placeholders: object
    """プレースホルダ名と置換する値"""
@dataclass_json
@dataclass
class WebhookTestResponse:
    """
    
    """
    result: str
    """* success: 通知先から正常なレスポンス（2xx系）を受け取った * failure: 通知先からエラーレスポンス（2xx系以外）を受け取った * error: リクエスト送信に失敗した、もしくはレスポンスを受信できなかった """

    request_body: str
    """実際に送信されたリクエストボディ"""

    response_status: int
    """通知先から返されたHTTPステータスコード"""

    response_body: str
    """通知先から返されたレスポンスボディ"""

    message: str
    """result=\"error\" 時のエラー内容等"""
@dataclass_json
@dataclass
class WorktimeStatistics:
    """
    
    """
    project_id: str
    """"""

    date: str
    """"""

    by_tasks: List[WorktimeStatisticsItem]
    """"""

    by_inputs: List[WorktimeStatisticsItem]
    """"""

    accounts: List[AccountWorktimeStatistics]
    """"""
@dataclass_json
@dataclass
class WorktimeStatisticsItem:
    """

    """
    phase: TaskPhase
    """"""

    histogram: List[HistogramItem]
    """"""

    average: str
    """"""

    standard_deviation: str
    """"""
