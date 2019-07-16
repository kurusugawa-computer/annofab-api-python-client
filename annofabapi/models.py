# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace
"""
annofabapiのmodel(swagger.yamlの`components.schemes`)
enumならば列挙体として定義する。
それ以外は型ヒントしてして宣言する。

Notes:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照
"""

import warnings  # pylint: disable=unused-import
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import

AcceptOrganizationInvitationRequest = Dict[str, Any]
"""

Kyes of Dict

* token: str
    

"""

Account = Dict[str, Any]
"""

Kyes of Dict

* account_id: str
    
* user_id: str
    
* username: str
    
* email: str
    
* lang: str
    
* keylayout: str
    
* authority: AccountAuthority
    
* updated_datetime: datetime
    

"""


class AccountAuthority(Enum):
    """
    """

    USER = "user"
    ADMIN = "admin"


AccountWorktimeStatistics = Dict[str, Any]
"""

Kyes of Dict

* account_id: str
    
* by_tasks: List[WorktimeStatisticsItem]
    
* by_inputs: List[WorktimeStatisticsItem]
    

"""

AdditionalData = Dict[str, Any]
"""

Kyes of Dict

* additional_data_definition_id: str
    
* flag: bool
    
* interger: int
    
* comment: str
    
* choice: str
    

"""

AdditionalDataDefinition = Dict[str, Any]
"""

Kyes of Dict

* additional_data_definition_id: str
    
* read_only: bool
    
* name: InternationalizationMessage
    
* keybind: List[Keybind]
    
* type: AdditionalDataDefinitionType
    
* choices: List[AdditionalDataDefinitionChoices]
    
* regex: str
    
* label_ids: List[str]
    リンク属性において、リンク先として指定可能なラベルID（空の場合制限なし） # noqa: E501
* required: bool
    リンク属性において、入力を必須とするかどうか # noqa: E501

"""

AdditionalDataDefinitionChoices = Dict[str, Any]
"""

Kyes of Dict

* choice_id: str
    
* name: InternationalizationMessage
    
* keybind: List[Keybind]
    

"""


class AdditionalDataDefinitionType(Enum):
    """
    * `flag` - 真偽値 * `integer` - 整数値 * `comment` - 自由記述 * `choice` - 選択肢（ラジオボタン式） * `select` - 選択肢（ドロップダウン式） * `tracking` - 自由記述 (トラッキングID自動挿入) * `link` - アノテーションリンク   # noqa: E501
    """

    FLAG = "flag"
    INTEGER = "integer"
    COMMENT = "comment"
    CHOICE = "choice"
    SELECT = "select"
    TRACKING = "tracking"
    LINK = "link"


AggregationResult = Dict[str, Any]
"""

Kyes of Dict

* type: str
    他と区別するために `CountResult` を指定します  # noqa: E501
* name: str
    
* field: str
    
* items: List[Count]
    

"""

Annotation = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* task_id: str
    
* input_data_id: str
    
* details: List[AnnotationDetail]
    
* comment: str
    
* updated_datetime: datetime
    新規作成時は未指定、更新時は必須（更新前の日時）  # noqa: E501

"""


class AnnotationDataHoldingType(Enum):
    """
    * `inner` - アノテーションのデータ部をJSON内部に保持します。 * `outer` - アノテーションのデータ部を外部ファイルの形式（画像など）で保持します   # noqa: E501
    """

    INNER = "inner"
    OUTER = "outer"


AnnotationDetail = Dict[str, Any]
"""

Kyes of Dict

* annotation_id: str
    
* account_id: str
    
* label_id: str
    
* is_protected: bool
    
* data_holding_type: AnnotationDataHoldingType
    
* data: OneOfstringFullAnnotationData
    data_holding_type が inner の場合のみ存在し、annotation_type に応じたデータの値が格納されます。 `string`もしくは`object`の値を指定することができ、`string`の形式は次の通りです。   * annotation_type が bounding_box の場合: 左上x,左上y,右下x,右下y のCSV文字列形式。   * annotation_type が polygon/polyline の場合: x1,y1,x2,y2, ... のCSV文字列形式。   * annotation_type が segmentation または segmentation_v2 の場合: 塗っていないところは rgba(0,0,0,0)、塗ったところは rgba(255,255,255,1) の PNGデータをBase64エンコードしたもの。   * annotation_type が classification の場合: data 属性は存在しない。   * annotation_type が range の場合: 開始時間,終了時間 のCSV文字列形式。  # noqa: E501
* path: str
    data_holding_typeがouterの場合のみ存在し、データのパスが格納される (現在はアノテーションIDと等しい) # noqa: E501
* etag: str
    data_holding_typeがouterの場合のみ存在し、データのETagが格納される # noqa: E501
* url: str
    data_holding_typeがouterの場合のみ存在し、データへの一時URLが格納される # noqa: E501
* additional_data_list: List[AdditionalData]
    各要素は、 [アノテーション仕様](#operation/getAnnotationSpecs)で定義された属性（`additional_data_definitions`内）のいずれかの要素と対応づけます。 各要素は、どの属性なのかを表す`additional_data_definition_id`、値が必要です。値は、属性の種類に対応するキーに格納します（下表）。  <table> <tr><th>アノテーション属性の種類<br>（`additional_data_definition`の`type`）</th><th>属性の値を格納するキー</th><th>データ型</th></tr> <tr><td>`comment` または `tracking`</td><td>`comment`</td><td>string</td></tr> <tr><td>`flag`</td><td>`flag`</td><td>boolean</td></tr> <tr><td>`integer`</td><td>`integer`</td><td>integer</td></tr> <tr><td>`choice` または `select`</td><td>`choice`</td><td>string（選択肢ID）</td></tr> <tr><td>`link`</td><td>`comment`</td><td>string（アノテーションID）</td></tr> </table>  # noqa: E501
* comment: str
    

"""

AnnotationEditorFeature = Dict[str, Any]
"""

Kyes of Dict

* append: bool
    
* erase: bool
    
* freehand: bool
    
* rectangle_fill: bool
    
* polygon_fill: bool
    
* fill_near: bool
    

"""

AnnotationQuery = Dict[str, Any]
"""

Kyes of Dict

* task_id: str
    
* exact_match_task_id: bool
    タスクIDの検索方法を指定します。 trueの場合は完全一致検索、falseの場合は中間一致検索です。  # noqa: E501
* input_data_id: str
    
* exact_match_input_data_id: bool
    入力データIDの検索方法を指定します。 trueの場合は完全一致検索、falseの場合は中間一致検索です。  # noqa: E501
* label_id: str
    
* attributes: List[AdditionalData]
    

"""

AnnotationSpecs = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* labels: List[Label]
    
* inspection_phrases: List[InspectionPhrase]
    
* updated_datetime: datetime
    

"""

AnnotationSpecsRequest = Dict[str, Any]
"""

Kyes of Dict

* labels: List[Label]
    ラベル  # noqa: E501
* inspection_phrases: List[InspectionPhrase]
    定型指摘  # noqa: E501
* updated_datetime: datetime
    

"""


class AnnotationType(Enum):
    """
    * `bounding_box` - 矩形を表します。 * `segmentation` - ピクセルレベルでの塗りつぶし（ラスター）を表します。 * `segmentation_v2` - 塗りつぶしv2を表します。v2はSemantic Segmentationに特化しています。 * `polygon` - ポリゴン（閉じた頂点集合）を表します。 * `polyline` - ポリライン（開いた頂点集合）を表します。 * `classification` - 入力データ全体に対するアノテーションを表します。 * `range` - 動画の区間を表します。   # noqa: E501
    """

    BOUNDING_BOX = "bounding_box"
    SEGMENTATION = "segmentation"
    SEGMENTATION_V2 = "segmentation_v2"
    POLYGON = "polygon"
    POLYLINE = "polyline"
    CLASSIFICATION = "classification"
    RANGE = "range"


class AssigneeRuleOfResubmittedTask(Enum):
    """
    * `no_assignee` - 以前の担当者で固定せず、未割当てにします。 * `fixed` - 以前の担当者が再度担当します。以前の担当者がいない(1回目の検査/受入)場合は未割当てになります。   # noqa: E501
    """

    NO_ASSIGNEE = "no_assignee"
    FIXED = "fixed"


BatchAnnotation = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* task_id: str
    
* input_data_id: str
    
* annotation_id: str
    
* label_id: str
    
* additional_data_list: List[FullAnnotationAdditionalData]
    
* updated_datetime: datetime
    

"""

BatchAnnotationRequestItemDelete = Dict[str, Any]
"""
アノテーション削除
Kyes of Dict

* project_id: str
    
* task_id: str
    
* input_data_id: str
    
* annotation_id: str
    
* updated_datetime: datetime
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type)  # noqa: E501

"""

BatchAnnotationRequestItemPut = Dict[str, Any]
"""
アノテーション更新
Kyes of Dict

* data: BatchAnnotation
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type)  # noqa: E501

"""

BatchInputDataRequestItemDelete = Dict[str, Any]
"""
入力データ削除
Kyes of Dict

* project_id: str
    
* input_data_id: str
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type)  # noqa: E501

"""

BatchInspectionRequestItemDelete = Dict[str, Any]
"""
検査コメント削除
Kyes of Dict

* project_id: str
    
* task_id: str
    
* input_data_id: str
    
* inspection_id: str
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type)  # noqa: E501

"""

BatchInspectionRequestItemPut = Dict[str, Any]
"""
検査コメント更新
Kyes of Dict

* data: Inspection
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type)  # noqa: E501

"""

BatchTaskRequestItemDelete = Dict[str, Any]
"""
タスク削除
Kyes of Dict

* project_id: str
    
* task_id: str
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type)  # noqa: E501

"""

CacheRecord = Dict[str, Any]
"""

Kyes of Dict

* input: str
    
* members: str
    
* project: str
    
* specs: str
    
* statistics: str
    
* organization: str
    

"""

ChangePasswordRequest = Dict[str, Any]
"""

Kyes of Dict

* user_id: str
    
* old_password: str
    
* new_password: str
    

"""

Color = Dict[str, Any]
"""

Kyes of Dict

* red: int
    
* green: int
    
* blue: int
    

"""

ConfirmAccountDeleteRequest = Dict[str, Any]
"""

Kyes of Dict

* token: str
    

"""

ConfirmResetEmailRequest = Dict[str, Any]
"""

Kyes of Dict

* token: str
    

"""

ConfirmResetPasswordRequest = Dict[str, Any]
"""

Kyes of Dict

* user_id: str
    
* confirmation_code: str
    
* new_password: str
    

"""

ConfirmSignUpRequest = Dict[str, Any]
"""

Kyes of Dict

* account_id: str
    
* user_id: str
    
* password: str
    
* username: str
    
* lang: str
    
* keylayout: str
    
* confirmation_code: str
    

"""

ConfirmVerifyEmailRequest = Dict[str, Any]
"""

Kyes of Dict

* token: Token
    
* confirmation_code: str
    

"""

Count = Dict[str, Any]
"""

Kyes of Dict

* key: str
    
* count: int
    
* aggregations: List[AggregationResult]
    

"""

CountResult = Dict[str, Any]
"""

Kyes of Dict

* type: str
    他と区別するために `CountResult` を指定します  # noqa: E501
* name: str
    
* field: str
    
* items: List[Count]
    

"""

DataPath = Dict[str, Any]
"""

Kyes of Dict

* url: str
    ファイルアップロード用の一時URLです。このURLにファイルをアップロードします。 # noqa: E501
* path: str
    アップロードしたファイルをAFの [入力データ](#tag/af-input) や [補助情報](#tag/af-supplementary) に登録するとき、この`path`を指定します。 # noqa: E501

"""

Duplicated = Dict[str, Any]
"""
値の重複が許可されていない属性の重複エラー
Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data: AdditionalData
    
* type: str
    Duplicated # noqa: E501

"""

DuplicatedSegmentationV2 = Dict[str, Any]
"""
塗りつぶしv2のラベルに対する1ラベルにつき1アノテーションまでの制約違反エラー
Kyes of Dict

* label_id: str
    
* annotation_ids: List[str]
    
* type: str
    DuplicatedSegmentationV2 # noqa: E501

"""

EmptyAttribute = Dict[str, Any]
"""
属性が未入力であるエラー
Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    EmptyAttribute # noqa: E501

"""

Error = Dict[str, Any]
"""

Kyes of Dict

* error_code: str
    
* message: str
    エラーの概要 # noqa: E501
* ext: object
    補足情報 # noqa: E501

"""

ErrorAlreadyUpdated = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorExpiredToken = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorForbiddenResource = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorInternalServerError = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorInvalidBody = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorInvalidPath = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorInvalidQueryParam = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorLoginFailed = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorMissingNecessaryQueryParam = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorMissingResource = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorPasswordResetRequired = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorRefreshTokenExpired = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorStateMismatch = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorTimeout = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorUnauthorizedApi = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

ErrorUnderMaintenance = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

Errors = Dict[str, Any]
"""

Kyes of Dict

* errors: List[Error]
    
* context: object
    内部補足情報 # noqa: E501

"""

FullAnnotation = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* task_id: str
    
* input_data_id: str
    
* input_data_name: str
    
* details: List[FullAnnotationDetail]
    
* comment: str
    
* updated_datetime: datetime
    

"""

FullAnnotationAdditionalData = Dict[str, Any]
"""

Kyes of Dict

* additional_data_definition_id: str
    
* additional_data_definition_name: InternationalizationMessage
    
* type: AdditionalDataDefinitionType
    
* flag: bool
    typeがflagの場合に、フラグのON(true)またはOFF(false)が格納される # noqa: E501
* integer: int
    typeがintegerの場合に、整数値が格納される # noqa: E501
* comment: str
    * typeがcommentの場合、コメントの値 * typeがtrackingの場合、トラッキングID * typeがlinkの場合、リンク先のアノテーションID  # noqa: E501
* choice: str
    
* choice_name: InternationalizationMessage
    

"""

FullAnnotationData = Dict[str, Any]
"""

Kyes of Dict

* type: str
    Unknown # noqa: E501
* data_uri: str
    
* left_top: Point
    
* right_bottom: Point
    
* points: List[Point]
    
* point: Point
    
* begin: float
    開始時間（ミリ秒）。小数点以下はミリ秒以下を表します。 # noqa: E501
* end: float
    終了時間（ミリ秒）。小数点以下はミリ秒以下を表します。 # noqa: E501
* data: str
    

"""

FullAnnotationDataBoundingBox = Dict[str, Any]
"""
annotation_type が bounding_boxの場合に、[左上頂点座標, 右下頂点座標]を {\"x\":int, \"y\":int} の形式で記述したもの。
Kyes of Dict

* left_top: Point
    
* right_bottom: Point
    
* type: str
    BoundingBox # noqa: E501

"""

FullAnnotationDataClassification = Dict[str, Any]
"""

Kyes of Dict

* type: str
    Classification # noqa: E501

"""

FullAnnotationDataPoints = Dict[str, Any]
"""
頂点座標 {\"x\":int, \"y\":int} の配列。  * annotation_type が polygon/polyline の場合: ポリゴン/ポリラインを構成する頂点の配列。 
Kyes of Dict

* points: List[Point]
    
* type: str
    Points # noqa: E501

"""

FullAnnotationDataRange = Dict[str, Any]
"""
annotation_type が rangeの場合に、[開始時間, 終了時間]を {\"begin\":number, \"end\":number} の形式で記述したもの。開始時間・終了時間の単位は秒で、精度はミリ秒まで。
Kyes of Dict

* begin: float
    開始時間（ミリ秒）。小数点以下はミリ秒以下を表します。 # noqa: E501
* end: float
    終了時間（ミリ秒）。小数点以下はミリ秒以下を表します。 # noqa: E501
* type: str
    Range # noqa: E501

"""

FullAnnotationDataSegmentation = Dict[str, Any]
"""
塗っていないところは rgba(0,0,0,0)、塗ったところは rgba(255,255,255,1) の PNGデータをBase64エンコードしたもの。
Kyes of Dict

* data_uri: str
    
* type: str
    Segmentation # noqa: E501

"""

FullAnnotationDataSegmentationV2 = Dict[str, Any]
"""

Kyes of Dict

* data_uri: str
    
* type: str
    SegmentationV2 # noqa: E501

"""

FullAnnotationDataSinglePoint = Dict[str, Any]
"""
annotation_type が pointの場合。
Kyes of Dict

* point: Point
    
* type: str
    SinglePoint。 # noqa: E501

"""

FullAnnotationDataUnknown = Dict[str, Any]
"""
annotation_typeにデータ構造が一致していない場合に、元のdata文字列をそのまま記述したもの。
Kyes of Dict

* data: str
    
* type: str
    Unknown # noqa: E501

"""

FullAnnotationDetail = Dict[str, Any]
"""

Kyes of Dict

* annotation_id: str
    
* user_id: str
    
* label_id: str
    
* label_name: InternationalizationMessage
    
* annotation_type: AnnotationType
    
* data_holding_type: AnnotationDataHoldingType
    
* data: FullAnnotationData
    
* path: str
    data_holding_typeがouterの場合のみ存在し、データへのパスが格納される # noqa: E501
* additional_data_list: List[FullAnnotationAdditionalData]
    
* comment: str
    

"""

HistogramItem = Dict[str, Any]
"""

Kyes of Dict

* begin: float
    
* end: float
    
* count: int
    

"""

InlineResponse200 = Dict[str, Any]
"""

Kyes of Dict

* list: List[MyOrganization]
    現在のページ番号に含まれる0件以上の所属組織です。 # noqa: E501
* page_no: float
    現在のページ番号です。 # noqa: E501
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる所属組織が0件であっても、総ページ数は1となります。 # noqa: E501
* total_count: float
    検索結果の総件数。 # noqa: E501
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。 # noqa: E501
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。 # noqa: E501

"""

InlineResponse2001 = Dict[str, Any]
"""

Kyes of Dict

* list: List[Project]
    現在のページ番号に含まれる0件以上のプロジェクトです。 # noqa: E501
* page_no: float
    現在のページ番号です。 # noqa: E501
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるプロジェクトが0件であっても、総ページ数は1となります。 # noqa: E501
* total_count: float
    検索結果の総件数。 # noqa: E501
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。 # noqa: E501
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。 # noqa: E501

"""

InlineResponse2002 = Dict[str, Any]
"""

Kyes of Dict

* list: List[OrganizationMember]
    
* page_no: float
    現在のページ番号です。 # noqa: E501
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる組織メンバーが0件であっても、総ページ数は1となります。 # noqa: E501
* total_count: float
    検索結果の総件数。 # noqa: E501
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。 # noqa: E501
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。 # noqa: E501

"""

InlineResponse2003 = Dict[str, Any]
"""

Kyes of Dict

* list: List[Project]
    
* has_next: bool
    

"""

InlineResponse2004 = Dict[str, Any]
"""

Kyes of Dict

* url: str
    

"""

InlineResponse2005 = Dict[str, Any]
"""

Kyes of Dict

* list: List[ProjectMember]
    
* page_no: float
    現在のページ番号です。 # noqa: E501
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるプロジェクトメンバーが0件であっても、総ページ数は1となります。 # noqa: E501
* total_count: float
    検索結果の総件数。 # noqa: E501
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。 # noqa: E501
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。 # noqa: E501

"""

InlineResponse2006 = Dict[str, Any]
"""

Kyes of Dict

* list: List[Task]
    現在のページ番号に含まれる0件以上のタスクです。 # noqa: E501
* page_no: float
    現在のページ番号です。 # noqa: E501
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるタスク0件であっても、総ページ数は1となります。 # noqa: E501
* total_count: float
    検索結果の総件数。 # noqa: E501
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。 # noqa: E501
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。 # noqa: E501

"""

InlineResponse2007 = Dict[str, Any]
"""

Kyes of Dict

* list: List[SingleAnnotation]
    現在のページ番号に含まれる0件以上のアノテーションです。 # noqa: E501
* page_no: float
    現在のページ番号です。 # noqa: E501
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるアノテーションが0件であっても、総ページ数は1となります。 # noqa: E501
* total_count: float
    検索結果の総件数。 # noqa: E501
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。 # noqa: E501
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。 # noqa: E501

"""

InlineResponse2008 = Dict[str, Any]
"""

Kyes of Dict

* list: List[InputData]
    現在のページ番号に含まれる0件以上の入力データです。 # noqa: E501
* page_no: float
    現在のページ番号です。 # noqa: E501
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる入力データが0件であっても、総ページ数は1となります。 # noqa: E501
* total_count: float
    検索結果の総件数。 # noqa: E501
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。 # noqa: E501
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。 # noqa: E501

"""

InputData = Dict[str, Any]
"""

Kyes of Dict

* input_data_id: str
    
* project_id: str
    
* input_data_name: str
    表示用の名前です。 # noqa: E501
* input_data_path: str
    入力データの実体が保存されたパスです。 s3スキーマまたはhttpsスキーマのみサポートしています。  # noqa: E501
* url: str
    入力データを取得するためのhttpsスキーマのURLです。  このURLはセキュリティのために認証認可が必要となっており、URLだけでは入力データを参照できません。 このURLは内部用であり、常に変更になる可能性があります。そのため、アクセスは保証外となります。 また、このURLのレスポンスは最低1時間キャッシュされます。 キャッシュを無効にしたい場合は、クエリパラメータにアクセス毎にランダムなUUIDなどを付与してください。  設定の不備等でデータが取得できない場合、この属性は設定されません。  # noqa: E501
* etag: str
    
* original_input_data_path: str
    AF外部のストレージから登録された場合、その外部ストレージ中のパス。 それ以外の場合は値なし  # noqa: E501
* original_resolution: Resolution
    
* resized_resolution: Resolution
    
* updated_datetime: datetime
    
* sign_required: bool
    データがSigned Cookieによるクロスオリジン配信に対応しているか否かです。  # noqa: E501

"""


class InputDataOrder(Enum):
    """
    タスクに割り当てる入力データの順序  * `name_asc` - 入力データ名 昇順（a, b, c, ...）。日付や番号などの連続するデータ名を扱う場合に推奨 * `name_asc` - 入力データ名 降順（z, y, x, ...） * `random` - ランダム   # noqa: E501
    """

    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"
    RANDOM = "random"


InputDataRequest = Dict[str, Any]
"""

Kyes of Dict

* input_data_name: str
    表示用の名前 # noqa: E501
* input_data_path: str
    AnnoFabに登録する入力データの実体が保存されたパスです。  対応スキーマ： * s3 * https * data（廃止予定）  場面別の使い分け： * [一時データ保存先取得API](#operation/createTempPath)を使ってAFにアップロードした場合: `s3://ANNOFAB-BUCKET/PATH/TO/INPUT_DATA` * [プライベートストレージ](/docs/faq/#prst9c)の場合     * `https://YOUR-DOMAIN/PATH/TO/INPUT_DATA`     * `s3://YOUR-BUCKET-FOR-PRIVATE-STORAGE/PATH/TO/INPUT_DATA`         * S3プライベートストレージのパスを登録する場合、[事前に認可の設定が必要](/docs/faq/#m0b240)です。 * dataスキーマでアップロードする場合: `data://....`     * dataスキーマは、4MB以内の画像であれば[一時データ保存先取得API](#operation/createTempPath)を使わずに直接アップロードできるので便利です。  # noqa: E501
* last_updated_datetime: datetime
    新規作成時は未指定、更新時は必須（更新前の日時）  # noqa: E501
* sign_required: bool
    データがSigned Cookieによるクロスオリジン配信に対応しているか否かです。<br> このオプションを有効にする場合は、`input_data_path`として、AnnoFabのAWS IDをTrusted Signerとして登録したCloudFrontのURLを指定してください。  # noqa: E501

"""

InputDataSummary = Dict[str, Any]
"""
ある入力データのバリデーション結果です。入力データIDをキーに引けるようにMap[入力データID, バリデーション結果]となっています
Kyes of Dict

* input_data_id: str
    
* inspection_summary: str
    
* annotation_summaries: List[ValidationError]
    

"""


class InputDataType(Enum):
    """
    プロジェクトの作成時のみ指定可能（未指定の場合は image）です。更新時は無視されます  # noqa: E501
    """

    IMAGE = "image"
    MOVIE = "movie"


Inspection = Dict[str, Any]
"""
検査コメント
Kyes of Dict

* project_id: str
    
* task_id: str
    
* input_data_id: str
    
* inspection_id: str
    
* phase: TaskPhase
    
* commenter_account_id: str
    
* annotation_id: str
    
* data: OneOfInspectionDataPointInspectionDataPolylineInspectionDataTime
    
* parent_inspection_id: str
    
* phrases: List[str]
    選択された定型指摘ID. 未選択時は空 # noqa: E501
* comment: str
    
* status: InspectionStatus
    
* created_datetime: datetime
    
* updated_datetime: datetime
    新規作成時は未指定、更新時は必須（更新前の日時）  # noqa: E501

"""

InspectionDataPoint = Dict[str, Any]
"""
問題のある部分を示す座標 
Kyes of Dict

* x: int
    
* y: int
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type)  # noqa: E501

"""

InspectionDataPolyline = Dict[str, Any]
"""
問題のある部分を示すポリライン 
Kyes of Dict

* coordinates: List[InspectionDataPolylineCoordinates]
    ポリラインを構成する頂点の配列  # noqa: E501
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type)  # noqa: E501

"""

InspectionDataPolylineCoordinates = Dict[str, Any]
"""

Kyes of Dict

* x: int
    
* y: int
    

"""

InspectionDataTime = Dict[str, Any]
"""
問題のある時間帯を表す区間 
Kyes of Dict

* start: float
    
* end: float
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type)  # noqa: E501

"""

InspectionPhrase = Dict[str, Any]
"""

Kyes of Dict

* id: str
    
* text: InternationalizationMessage
    

"""

InspectionStatistics = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* date: date
    集計日 # noqa: E501
* breakdown: InspectionStatisticsBreakdown
    

"""

InspectionStatisticsBreakdown = Dict[str, Any]
"""

Kyes of Dict

* labels: dict(str, InspectionStatisticsPhrases)
    ラベルごとの指摘集計結果 # noqa: E501
* no_label: InspectionStatisticsPhrases
    

"""

InspectionStatisticsPhrases = Dict[str, Any]
"""

Kyes of Dict

* phrases: dict(str, int)
    定型指摘ごとの合計数 # noqa: E501
* no_phrase: int
    非定型指摘の合計数 # noqa: E501

"""


class InspectionStatus(Enum):
    """
    * `annotator_action_required` - 未処置。`annotation`フェーズ担当者が何らかの回答をする必要あり * `no_correction_required` - 処置不要。`annotation`フェーズ担当者が、検査コメントによる修正は不要、と回答した * `error_corrected` - 修正済み。`annotation`フェーズ担当者が、検査コメントの指示どおり修正した * `no_comment_inspection` - 作成途中。検査コメントの中身が未入力   # noqa: E501
    """

    ANNOTATOR_ACTION_REQUIRED = "annotator_action_required"
    NO_CORRECTION_REQUIRED = "no_correction_required"
    ERROR_CORRECTED = "error_corrected"
    NO_COMMENT_INSPECTION = "no_comment_inspection"


InstructionHistory = Dict[str, Any]
"""

Kyes of Dict

* history_id: str
    
* account_id: str
    
* updated_datetime: datetime
    

"""

InstructionImage = Dict[str, Any]
"""

Kyes of Dict

* image_id: str
    
* path: str
    
* url: str
    
* etag: str
    

"""

InternationalizationMessage = Dict[str, Any]
"""

Kyes of Dict

* messages: List[InternationalizationMessageMessages]
    
* default_lang: str
    

"""

InternationalizationMessageMessages = Dict[str, Any]
"""

Kyes of Dict

* lang: str
    
* message: str
    

"""

InvalidAnnotationData = Dict[str, Any]
"""
アノテーションデータ不正エラー
Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* message: str
    
* type: str
    InvalidAnnotationData # noqa: E501

"""

InvalidCommentFormat = Dict[str, Any]
"""
コメントが正規表現に合致しないエラー
Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    InvalidCommentFormat # noqa: E501

"""

InvalidLinkTarget = Dict[str, Any]
"""
リンク先アノテーションが許可されているラベルでないエラー
Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    InvalidLinkTarget # noqa: E501

"""

InviteOrganizationMemberRequest = Dict[str, Any]
"""

Kyes of Dict

* role: OrganizationMemberRole
    

"""

JobInfo = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* job_type: str
    
* job_id: str
    
* job_status: str
    
* job_execution: object
    ジョブの内部情報 # noqa: E501
* job_detail: object
    ジョブ結果の内部情報 # noqa: E501
* created_datetime: datetime
    
* updated_datetime: datetime
    

"""

Keybind = Dict[str, Any]
"""

Kyes of Dict

* code: str
    
* shift: bool
    
* ctrl: bool
    
* alt: bool
    

"""

Label = Dict[str, Any]
"""

Kyes of Dict

* label_id: str
    
* label_name: InternationalizationMessage
    
* keybind: List[Keybind]
    
* annotation_type: AnnotationType
    
* bounding_box_metadata: LabelBoundingBoxMetadata
    
* segmentation_metadata: LabelSegmentationMetadata
    
* additional_data_definitions: List[AdditionalDataDefinition]
    
* color: Color
    
* annotation_editor_feature: AnnotationEditorFeature
    
* allow_out_of_image_bounds: bool
    

"""

LabelBoundingBoxMetadata = Dict[str, Any]
"""

Kyes of Dict

* min_width: int
    
* min_height: int
    
* min_warn_rule: str
    
* min_area: int
    
* max_vertices: int
    
* min_vertices: int
    
* tolerance: int
    

"""

LabelSegmentationMetadata = Dict[str, Any]
"""

Kyes of Dict

* min_width: int
    
* min_height: int
    
* min_warn_rule: str
    
* tolerance: int
    

"""

LabelStatistics = Dict[str, Any]
"""

Kyes of Dict

* label_id: str
    
* completed_labels: int
    ラベルごとの受入が完了したアノテーション数 # noqa: E501
* wip_labels: int
    ラベルごとの受入が完了していないアノテーション数 # noqa: E501

"""

LoginRequest = Dict[str, Any]
"""

Kyes of Dict

* user_id: str
    
* password: str
    

"""

LoginResponse = Dict[str, Any]
"""

Kyes of Dict

* token: Token
    

"""

Message = Dict[str, Any]
"""

Kyes of Dict

* message: str
    多言語対応 # noqa: E501

"""

MyAccount = Dict[str, Any]
"""

Kyes of Dict

* account_id: str
    
* user_id: str
    
* username: str
    
* email: str
    
* lang: str
    
* keylayout: str
    
* authority: AccountAuthority
    
* updated_datetime: datetime
    
* reset_requested_email: str
    
* errors: List[str]
    

"""

MyOrganization = Dict[str, Any]
"""

Kyes of Dict

* organization_id: str
    
* name: str
    
* email: str
    
* price_plan: PricePlan
    
* summary: OrganizationSummary
    
* created_datetime: datetime
    
* updated_datetime: datetime
    
* my_role: OrganizationMemberRole
    
* my_status: OrganizationMemberStatus
    

"""

Organization = Dict[str, Any]
"""

Kyes of Dict

* organization_id: str
    
* organization_name: str
    
* email: str
    
* price_plan: PricePlan
    
* summary: OrganizationSummary
    
* created_datetime: datetime
    
* updated_datetime: datetime
    

"""

OrganizationActivity = Dict[str, Any]
"""

Kyes of Dict

* organization_id: str
    
* created_datetime: datetime
    
* storage_usage_bytes: float
    

"""

OrganizationMember = Dict[str, Any]
"""

Kyes of Dict

* organization_id: str
    
* account_id: str
    
* user_id: str
    
* username: str
    
* role: OrganizationMemberRole
    
* status: OrganizationMemberStatus
    
* created_datetime: datetime
    
* updated_datetime: datetime
    

"""


class OrganizationMemberRole(Enum):
    """
    """

    OWNER = "owner"
    ADMINISTRATOR = "administrator"
    CONTRIBUTOR = "contributor"


class OrganizationMemberStatus(Enum):
    """
    * `active` - 組織メンバーとして有効で、組織を閲覧したり、権限があれば編集できます。 * `waiting_response` - 組織に招待され、まだ加入/脱退を返答していません。組織の一部を閲覧のみできます。 * `inactive` - 脱退したメンバーを表します。組織を閲覧できません。   # noqa: E501
    """

    ACTIVE = "active"
    WAITING_RESPONSE = "waiting_response"
    INACTIVE = "inactive"


OrganizationRegistrationRequest = Dict[str, Any]
"""

Kyes of Dict

* organization_name: str
    
* organization_email: str
    
* price_plan: PricePlan
    

"""

OrganizationSummary = Dict[str, Any]
"""

Kyes of Dict

* last_tasks_updated_datetime: datetime
    

"""

OutOfImageBounds = Dict[str, Any]
"""
画像範囲外にアノテーションがはみ出しているエラー
Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* type: str
    OutOfImageBounds # noqa: E501

"""

PasswordResetRequest = Dict[str, Any]
"""

Kyes of Dict

* email: str
    

"""

PhaseStatistics = Dict[str, Any]
"""

Kyes of Dict

* phase: str
    
* worktime: str
    

"""

Point = Dict[str, Any]
"""
座標
Kyes of Dict

* x: int
    
* y: int
    

"""


class PricePlan(Enum):
    """
    """

    FREE = "free"
    BUSINESS = "business"


Project = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* organization_id: str
    
* title: str
    
* overview: str
    
* status: ProjectStatus
    
* input_data_type: InputDataType
    
* configuration: ProjectConfiguration
    
* created_datetime: datetime
    
* updated_datetime: datetime
    
* summary: ProjectSummary
    

"""

ProjectAccountStatistics = Dict[str, Any]
"""

Kyes of Dict

* account_id: str
    
* histories: List[ProjectAccountStatisticsHistory]
    

"""

ProjectAccountStatisticsHistory = Dict[str, Any]
"""

Kyes of Dict

* date: date
    
* tasks_completed: int
    
* tasks_rejected: int
    
* worktime: str
    

"""

ProjectConfiguration = Dict[str, Any]
"""

Kyes of Dict

* project_rule: str
    
* project_workflow: ProjectWorkflow
    
* assignee_rule_of_resubmitted_task: AssigneeRuleOfResubmittedTask
    
* max_tasks_per_member: int
    保留中のタスクを除き、1人（オーナー以外）に割り当てられるタスク数上限。未指定の場合は10件として扱う。 # noqa: E501
* max_tasks_per_member_including_hold: int
    保留中のタスクを含めて、1人（オーナー以外）に割り当てられるタスク数上限。未指定の場合は20件として扱う。 # noqa: E501
* input_data_max_long_side_length: int
    入力データ画像の長辺の最大値（未指定時は4096px）。  画像をアップロードすると、長辺がこの値になるように画像が自動で圧縮されます。 アノテーションの座標は、もとの解像度の画像でつけたものに復元されます。  大きな数値を設定すると入力データ画像のサイズが大きくなり、生産性低下やブラウザで画像を表示できない懸念があります。注意して設定してください。  # noqa: E501
* sampling_inspection_rate: int
    抜取検査率。0-100のパーセント値で指定し、未指定の場合は100%として扱う。 # noqa: E501
* sampling_acceptance_rate: int
    抜取受入率。0-100のパーセント値で指定し、未指定の場合は100%として扱う。 # noqa: E501
* private_storage_aws_iam_role_arn: str
    AWS IAMロール。ビジネスプランでのS3プライベートストレージの認可で使います。 [S3プライベートストレージの認可の設定についてはこちら](/docs/faq/#m0b240)をご覧ください。  # noqa: E501

"""

ProjectCopyRequest = Dict[str, Any]
"""

Kyes of Dict

* dest_project_id: str
    
* dest_title: str
    
* dest_overview: str
    
* copy_inputs: bool
    true の場合は「プロジェクト」「プロジェクトメンバー」「アノテーション仕様」「入力データ」をコピーします。 false の場合は「プロジェクト」「プロジェクトメンバー」「アノテーション仕様」のみコピーします。 copyTasksWithAnnotations が true に設定されている場合、そちらが優先されます。  # noqa: E501
* copy_tasks_with_annotations: bool
    true の場合は「プロジェクト」「プロジェクトメンバー」「アノテーション仕様」「入力データ」「タスク」「アノテーション」をコピーします。 false の場合は copyInputs の設定に従います。  # noqa: E501
* copy_webhooks: bool
    true の場合はcopyInputs、copyTasksWithAnnotations によるコピー対象に加えて「Webhook」のコピーも行います。 false の場合はcopyInputs、copyTasksWithAnnotations によるコピー対象のコピーのみを行います。  # noqa: E501
* copy_supplementaly_data: bool
    copyInputs、copyTasksWithAnnotations のいずれかが true の時のみ、設定できます。いずれも false の場合、「補助情報」のコピーは行われません。 true の場合はcopyInputs、copyTasksWithAnnotations によるコピー対象に加えて「補助情報」のコピーも行います。 false の場合はcopyInputs、copyTasksWithAnnotations によるコピー対象のコピーのみを行います。  # noqa: E501
* copy_instructions: bool
    true の場合はcopyInputs、copyTasksWithAnnotations によるコピー対象に加えて「作業ガイド」のコピーも行います。 false の場合はcopyInputs、copyTasksWithAnnotations によるコピー対象のコピーのみを行います。  # noqa: E501

"""

ProjectMember = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* account_id: str
    
* user_id: str
    
* username: str
    
* member_status: ProjectMemberStatus
    
* member_role: ProjectMemberRole
    
* updated_datetime: datetime
    
* created_datetime: datetime
    
* sampling_inspection_rate: int
    メンバー固有の抜取検査率。0-100のパーセント値で指定する。値が指定された場合、プロジェクトの抜取検査率を指定の値で上書きする。 # noqa: E501

"""

ProjectMemberRequest = Dict[str, Any]
"""

Kyes of Dict

* member_status: ProjectMemberStatus
    
* member_role: ProjectMemberRole
    
* last_updated_datetime: datetime
    新規作成時は未指定、更新時は必須（更新前の日時）  # noqa: E501

"""


class ProjectMemberRole(Enum):
    """
    """

    OWNER = "owner"
    WORKER = "worker"
    ACCEPTER = "accepter"
    TRAINING_DATA_USER = "training_data_user"


class ProjectMemberStatus(Enum):
    """
    * `active` - プロジェクトメンバーとして有効で、プロジェクトを閲覧したり、権限があれば編集できます。 * `inactive` - 脱退したプロジェクトメンバーを表します。プロジェクトを閲覧できません。   # noqa: E501
    """

    ACTIVE = "active"
    INACTIVE = "inactive"


class ProjectStatus(Enum):
    """
    """

    ACTIVE = "active"
    SUSPENDED = "suspended"


ProjectSummary = Dict[str, Any]
"""

Kyes of Dict

* last_tasks_updated_datetime: datetime
    

"""

ProjectTaskStatistics = Dict[str, Any]
"""

Kyes of Dict

* phase: TaskPhase
    
* status: TaskStatus
    
* count: int
    
* work_timespan: int
    

"""

ProjectTaskStatisticsHistory = Dict[str, Any]
"""

Kyes of Dict

* date: date
    
* tasks: List[ProjectTaskStatistics]
    

"""


class ProjectWorkflow(Enum):
    """
    """

    _2PHASE = "2phase"
    _3PHASE = "3phase"


PutMyAccountRequest = Dict[str, Any]
"""

Kyes of Dict

* user_id: str
    
* username: str
    
* lang: str
    
* keylayout: str
    
* token: Token
    
* last_updated_datetime: datetime
    新規作成時は未指定、更新時は必須（更新前の日時）  # noqa: E501

"""

PutOrganizationMemberRoleRequest = Dict[str, Any]
"""

Kyes of Dict

* role: OrganizationMemberRole
    
* last_updated_datetime: datetime
    新規作成時は未指定、更新時は必須（更新前の日時）  # noqa: E501

"""

PutOrganizationNameRequest = Dict[str, Any]
"""

Kyes of Dict

* organization_id: str
    
* organization_name: str
    
* last_updated_datetime: datetime
    

"""

PutProjectRequest = Dict[str, Any]
"""

Kyes of Dict

* title: str
    
* overview: str
    
* status: str
    
* input_data_type: InputDataType
    
* organization_name: str
    プロジェクトの所属組織を変更する場合は、ここに変更先の組織名を指定します。  * 所属組織を変更する前にプロジェクトを停止する必要があります。 * APIを呼び出すアカウントは、変更先組織の管理者またはオーナーである必要があります。 * 変更後の組織に所属していないプロジェクトメンバーも残りますが、作業はできません。あらためて組織に招待してください。  # noqa: E501
* configuration: ProjectConfiguration
    
* last_updated_datetime: datetime
    新規作成時は未指定、更新時は必須（更新前の日時）  # noqa: E501
* force_suspend: bool
    作業中タスクがあるプロジェクトを停止する時trueにして下さい # noqa: E501

"""

RefreshTokenRequest = Dict[str, Any]
"""

Kyes of Dict

* refresh_token: str
    

"""

ResetEmailRequest = Dict[str, Any]
"""

Kyes of Dict

* email: str
    

"""

ResetPasswordRequest = Dict[str, Any]
"""

Kyes of Dict

* token: str
    

"""

Resolution = Dict[str, Any]
"""
画像などの解像度 
Kyes of Dict

* width: float
    
* height: float
    

"""

SignUpRequest = Dict[str, Any]
"""

Kyes of Dict

* email: str
    

"""

SimpleAnnotation = Dict[str, Any]
"""

Kyes of Dict

* annotation_format_version: str
    アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、AnnoFabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。  # noqa: E501
* project_id: str
    
* task_id: str
    
* input_data_id: str
    
* input_data_name: str
    
* details: List[SimpleAnnotationDetail]
    
* comment: str
    

"""

SimpleAnnotationDetail = Dict[str, Any]
"""

Kyes of Dict

* label: str
    アノテーション仕様のラベル名です。  # noqa: E501
* annotation_id: str
    個々のアノテーションにつけられたIDです。  # noqa: E501
* data: FullAnnotationData
    
* attributes: object
    キーに属性の名前、値に各属性の値が入った辞書構造です。  # noqa: E501

"""

SingleAnnotation = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* task_id: str
    
* input_data_id: str
    
* detail: SingleAnnotationDetail
    
* updated_datetime: datetime
    

"""

SingleAnnotationDetail = Dict[str, Any]
"""

Kyes of Dict

* annotation_id: str
    
* account_id: str
    
* label_id: str
    
* data_holding_type: AnnotationDataHoldingType
    
* data: FullAnnotationData
    
* etag: str
    data_holding_typeがouterの場合のみ存在し、データのETagが格納される # noqa: E501
* url: str
    data_holding_typeがouterの場合のみ存在し、データへの一時URLが格納される # noqa: E501
* additional_data_list: List[FullAnnotationAdditionalData]
    
* created_datetime: datetime
    
* updated_datetime: datetime
    

"""

SupplementaryData = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* input_data_id: str
    
* supplementary_data_id: str
    
* supplementary_data_name: str
    表示用の名前 # noqa: E501
* supplementary_data_path: str
    補助情報の実体が保存されたパスです。 s3スキーマまたはhttpsスキーマのみサポートしています。  # noqa: E501
* url: str
    このフィールドはAF内部での利用のみを想定しており、依存しないでください。 # noqa: E501
* etag: str
    
* supplementary_data_type: str
    
* supplementary_data_number: int
    表示順を表す数値（昇順）。同じ入力データに対して複数の補助情報で表示順が重複する場合、順序不定になります。 # noqa: E501
* updated_datetime: datetime
    

"""

SupplementaryDataRequest = Dict[str, Any]
"""

Kyes of Dict

* supplementary_data_name: str
    表示用の名前 # noqa: E501
* supplementary_data_path: str
    AnnoFabに登録する補助情報の実体が保存されたパスです。  対応スキーマ：s3, https  * [一時データ保存先取得API](#operation/createTempPath)を使ってAFにアップロードした場合: `s3://ANNOFAB-BUCKET/PATH/TO/INPUT_DATA` * [プライベートストレージ](/docs/faq/#prst9c)の場合     * `https://YOUR-DOMAIN/PATH/TO/INPUT_DATA`     * `s3://YOUR-BUCKET-FOR-PRIVATE-STORAGE/PATH/TO/INPUT_DATA`         * S3プライベートストレージのパスを登録する場合、[事前に認可の設定が必要](/docs/faq/#m0b240)です。  # noqa: E501
* supplementary_data_type: str
    
* supplementary_data_number: int
    表示順を表す数値（昇順）。同じ入力データに対して複数の補助情報で表示順が重複する場合、順序不定になります。 # noqa: E501
* last_updated_datetime: datetime
    

"""

Task = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* task_id: str
    
* phase: TaskPhase
    
* status: TaskStatus
    
* input_data_id_list: List[str]
    
* account_id: str
    
* histories_by_phase: List[TaskHistoryShort]
    
* work_timespan: int
    
* number_of_rejections: int
    このタスクが差戻しされた回数（すべてのフェーズでの差戻し回数の合計  このフィールドは、どのフェーズで何回差戻されたかを区別できないため、廃止予定です。 `histories_by_phase` で各フェーズの回数を計算することで、差戻し回数が分かります。  例）`acceptance`フェーズが3回ある場合、`acceptance`フェーズで2回差し戻しされたことになります。  # noqa: E501
* started_datetime: datetime
    
* updated_datetime: datetime
    
* sampling: str
    * `acceptance_skipped` - このタスクが抜取検査の対象外となり、受入フェーズをスキップしたことを表す。 * `inspection_and_acceptance_skipped` - このタスクが抜取検査の対象外となり、検査・受入フェーズをスキップしたことを表す  未指定時はこのタスクが抜取検査の対処となったことを表す。(通常のワークフローを通過する)  # noqa: E501

"""

TaskGenerateRequest = Dict[str, Any]
"""

Kyes of Dict

* task_generate_rule: OneOfTaskGenerateRuleByCountTaskGenerateRuleByDirectoryTaskGenerateRuleByInputDataCsv
    * `TaskGenerateRuleByCount`: 1つのタスクに割りあてる入力データの個数を指定してタスクを生成します。 * `TaskGenerateRuleByDirectory`: 入力データ名をファイルパスに見立て、ディレクトリ単位でタスクを生成します。  # noqa: E501
* task_id_prefix: str
    生成するタスクIDのプレフィックス # noqa: E501
* project_last_updated_datetime: datetime
    プロジェクトの最終更新日時。タスク生成の排他制御に使用。 # noqa: E501

"""

TaskGenerateRuleByCount = Dict[str, Any]
"""
1つのタスクに割りあてる入力データの個数を指定してタスクを生成します。
Kyes of Dict

* allow_duplicate_input_data: bool
    falseのときは、既にタスクに使われている入力データを除外し、まだタスクに使われていない入力データだけを新しいタスクに割り当てます。trueのときは、既にタスクに使われている入力データを除外しません。 # noqa: E501
* input_data_count: int
    1つのタスクに割り当てる入力データの個数 # noqa: E501
* input_data_order: InputDataOrder
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type)  # noqa: E501

"""

TaskGenerateRuleByDirectory = Dict[str, Any]
"""
入力データ名をファイルパスに見立て、ディレクトリ単位でタスクを生成します。<br>
Kyes of Dict

* input_data_name_prefix: str
    タスク生成対象の入力データ名プレフィックス # noqa: E501
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type)  # noqa: E501

"""

TaskGenerateRuleByInputDataCsv = Dict[str, Any]
"""
各タスクへの入力データへの割当を記入したCSVへのS3上のパスを指定してタスクを生成します。
Kyes of Dict

* csv_data_path: str
    各タスクへの入力データへの割当を記入したCSVへのS3上のパス # noqa: E501
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type)  # noqa: E501

"""

TaskHistory = Dict[str, Any]
"""
タスクのあるフェーズで、誰がいつどれくらいの作業時間を費やしたかを表すタスク履歴です。
Kyes of Dict

* project_id: str
    
* task_id: str
    
* task_history_id: str
    
* started_datetime: datetime
    
* ended_datetime: datetime
    
* accumulated_labor_time_milliseconds: str
    
* phase: TaskPhase
    
* account_id: str
    

"""

TaskHistoryEvent = Dict[str, Any]
"""
タスク履歴イベントは、タスクの状態が変化した１時点を表します。作業時間は、複数のこれらイベントを集約して計算するものなので、このオブジェクトには含まれません。
Kyes of Dict

* project_id: str
    
* task_id: str
    
* task_history_id: str
    
* created_datetime: datetime
    
* phase: TaskPhase
    
* status: TaskStatus
    
* account_id: str
    

"""

TaskHistoryShort = Dict[str, Any]
"""
タスクのあるフェーズを誰が担当したかを表します。
Kyes of Dict

* phase: TaskPhase
    
* account_id: str
    

"""

TaskOperation = Dict[str, Any]
"""

Kyes of Dict

* status: TaskStatus
    
* last_updated_datetime: datetime
    新規作成時は未指定、更新時は必須（更新前の日時）  # noqa: E501
* account_id: str
    

"""


class TaskPhase(Enum):
    """
    * `annotation` - 教師付け。 * `inspection` - 中間検査。ワークフローが3フェーズのときのみ。 * `acceptance` - 受入。   # noqa: E501
    """

    ANNOTATION = "annotation"
    INSPECTION = "inspection"
    ACCEPTANCE = "acceptance"


TaskPhaseStatistics = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* date: date
    
* phases: List[PhaseStatistics]
    

"""

TaskRequest = Dict[str, Any]
"""

Kyes of Dict

* input_data_id_list: List[str]
    

"""

TaskStart = Dict[str, Any]
"""

Kyes of Dict

* phase: TaskPhase
    

"""


class TaskStatus(Enum):
    """
    * `not_started` - 未着手。 * `working` - 作業中。誰かが実際にエディタ上で作業している状態。 * `on_hold` - 保留。作業ルールの確認などで作業できない状態。 * `break` - 休憩中。 * `complete` - 完了。次のフェーズへ進む * `rejected` - 差戻し。修正のため、`annotation`フェーズへ戻る。 * `cancelled` - 提出取消し。修正のため、前フェーズへ戻る。   # noqa: E501
    """

    NOT_STARTED = "not_started"
    WORKING = "working"
    ON_HOLD = "on_hold"
    BREAK = "break"
    COMPLETE = "complete"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


TaskValidation = Dict[str, Any]
"""
タスクの全入力データに対するバリデーション結果です。
Kyes of Dict

* project_id: str
    
* task_id: str
    
* inputs: List[InputDataSummary]
    

"""

TasksInputs = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* tasks: List[TasksInputsTask]
    

"""

TasksInputsTask = Dict[str, Any]
"""

Kyes of Dict

* task_id: str
    
* phase: TaskPhase
    
* status: TaskStatus
    
* input_data_id_list: List[str]
    

"""

Token = Dict[str, Any]
"""

Kyes of Dict

* id_token: str
    形式は[JWT](https://jwt.io/)。 # noqa: E501
* access_token: str
    形式は[JWT](https://jwt.io/)。 # noqa: E501
* refresh_token: str
    形式は[JWT](https://jwt.io/)。 # noqa: E501

"""

UnknownAdditionalData = Dict[str, Any]
"""
何らかの原因で、アノテーション仕様にない属性がついているエラー
Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    UnknownAdditionalData # noqa: E501

"""

UnknownLabel = Dict[str, Any]
"""
何らかの原因で、アノテーション仕様にないラベルがついているエラー
Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* type: str
    UnknownLabel # noqa: E501

"""

UnknownLinkTarget = Dict[str, Any]
"""
指定されたIDに該当するアノテーションが存在しないエラー
Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    UnknownLinkTarget # noqa: E501

"""

ValidationError = Dict[str, Any]
"""

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* message: str
    
* type: str
    UnknownLabel # noqa: E501
* annotation_ids: List[str]
    
* additional_data_definition_id: str
    
* additional_data: AdditionalData
    

"""

VerifyEmailRequest = Dict[str, Any]
"""

Kyes of Dict

* token: Token
    

"""

Webhook = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* event_type: str
    
* webhook_id: str
    
* webhook_status: str
    
* method: str
    
* headers: List[WebhookHeader]
    
* body: str
    
* url: str
    
* created_datetime: datetime
    
* updated_datetime: datetime
    

"""

WebhookHeader = Dict[str, Any]
"""

Kyes of Dict

* name: str
    
* value: str
    

"""

WebhookTestRequest = Dict[str, Any]
"""

Kyes of Dict

* placeholders: object
    プレースホルダ名と置換する値 # noqa: E501

"""

WebhookTestResponse = Dict[str, Any]
"""

Kyes of Dict

* result: str
    * success: 通知先から正常なレスポンス（2xx系）を受け取った * failure: 通知先からエラーレスポンス（2xx系以外）を受け取った * error: リクエスト送信に失敗した、もしくはレスポンスを受信できなかった  # noqa: E501
* request_body: str
    実際に送信されたリクエストボディ # noqa: E501
* response_status: int
    通知先から返されたHTTPステータスコード # noqa: E501
* response_body: str
    通知先から返されたレスポンスボディ # noqa: E501
* message: str
    result=\"error\" 時のエラー内容等 # noqa: E501

"""

WorktimeStatistics = Dict[str, Any]
"""

Kyes of Dict

* project_id: str
    
* date: date
    
* by_tasks: List[WorktimeStatisticsItem]
    
* by_inputs: List[WorktimeStatisticsItem]
    
* accounts: List[AccountWorktimeStatistics]
    

"""

WorktimeStatisticsItem = Dict[str, Any]
"""

Kyes of Dict

* phase: TaskPhase
    
* histogram: List[HistogramItem]
    
* average: str
    
* standard_deviation: str
    

"""
