# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace

"""
annofabapiのmodel(swagger.yamlの`components.schemes`)
enumならば列挙体として定義する。
それ以外は型ヒントしてして宣言する。

Notes:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照
"""

import warnings # pylint: disable=unused-import
from typing import Any, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import
from enum import Enum

AcceptOrganizationInvitationRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * token: str

"""

Account = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
    * account_id: str
    * by_tasks: List[WorktimeStatisticsItem]
    * by_inputs: List[WorktimeStatisticsItem]

"""

AdditionalData = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * additional_data_definition_id: str
    * flag: bool
    * interger: int
    * comment: str
    * choice: str

"""

AdditionalDataDefinition = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * additional_data_definition_id: str
    * read_only: bool
    * name: InternationalizationMessage
    * keybind: List[Keybind]
    * type: AdditionalDataDefinitionType
    * choices: List[AdditionalDataDefinitionChoices]
    * regex: str
    * label_ids: List[str]
    * required: bool

"""

AdditionalDataDefinitionChoices = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
    * type: str
    * name: str
    * field: str
    * items: List[Count]

"""

Annotation = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * project_id: str
    * task_id: str
    * input_data_id: str
    * details: List[AnnotationDetail]
    * comment: str
    * updated_datetime: datetime

"""

class AnnotationDataHoldingType(Enum):
    """
    * `inner` - アノテーションのデータ部をJSON内部に保持します。 * `outer` - アノテーションのデータ部を外部ファイルの形式（画像など）で保持します   # noqa: E501
    """

    INNER = "inner"
    OUTER = "outer"

AnnotationDetail = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * annotation_id: str
    * account_id: str
    * label_id: str
    * is_protected: bool
    * data_holding_type: AnnotationDataHoldingType
    * data: OneOfstringFullAnnotationData
    * path: str
    * etag: str
    * url: str
    * additional_data_list: List[AdditionalData]
    * comment: str

"""

AnnotationEditorFeature = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * append: bool
    * erase: bool
    * freehand: bool
    * rectangle_fill: bool
    * polygon_fill: bool
    * fill_near: bool

"""

AnnotationQuery = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * task_id: str
    * exact_match_task_id: bool
    * input_data_id: str
    * exact_match_input_data_id: bool
    * label_id: str
    * attributes: List[AdditionalData]

"""

AnnotationSpecs = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * project_id: str
    * labels: List[Label]
    * inspection_phrases: List[InspectionPhrase]
    * updated_datetime: datetime

"""

AnnotationSpecsRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * labels: List[Label]
    * inspection_phrases: List[InspectionPhrase]
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

Notes:
    Dictのkeyとその型
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
アノテーション削除  # noqa: E501

Notes:
    Dictのkeyとその型
    * project_id: str
    * task_id: str
    * input_data_id: str
    * annotation_id: str
    * updated_datetime: datetime
    * type: str

"""

BatchAnnotationRequestItemPut = Dict[str, Any]
"""
アノテーション更新  # noqa: E501

Notes:
    Dictのkeyとその型
    * data: BatchAnnotation
    * type: str

"""

BatchInputDataRequestItemDelete = Dict[str, Any]
"""
入力データ削除  # noqa: E501

Notes:
    Dictのkeyとその型
    * project_id: str
    * input_data_id: str
    * type: str

"""

BatchInspectionRequestItemDelete = Dict[str, Any]
"""
検査コメント削除  # noqa: E501

Notes:
    Dictのkeyとその型
    * project_id: str
    * task_id: str
    * input_data_id: str
    * inspection_id: str
    * type: str

"""

BatchInspectionRequestItemPut = Dict[str, Any]
"""
検査コメント更新  # noqa: E501

Notes:
    Dictのkeyとその型
    * data: Inspection
    * type: str

"""

BatchTaskRequestItemDelete = Dict[str, Any]
"""
タスク削除  # noqa: E501

Notes:
    Dictのkeyとその型
    * project_id: str
    * task_id: str
    * type: str

"""

ChangePasswordRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * user_id: str
    * old_password: str
    * new_password: str

"""

Color = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * red: int
    * green: int
    * blue: int

"""

ConfirmAccountDeleteRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * token: str

"""

ConfirmResetEmailRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * token: str

"""

ConfirmResetPasswordRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * user_id: str
    * confirmation_code: str
    * new_password: str

"""

ConfirmSignUpRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
    * token: Token
    * confirmation_code: str

"""

Count = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * key: str
    * count: int
    * aggregations: List[AggregationResult]

"""

CountResult = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * type: str
    * name: str
    * field: str
    * items: List[Count]

"""

DataPath = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * url: str
    * path: str

"""

Duplicated = Dict[str, Any]
"""
値の重複が許可されていない属性の重複エラー  # noqa: E501

Notes:
    Dictのkeyとその型
    * label_id: str
    * annotation_id: str
    * additional_data: AdditionalData
    * type: str

"""

DuplicatedSegmentationV2 = Dict[str, Any]
"""
塗りつぶしv2のラベルに対する1ラベルにつき1アノテーションまでの制約違反エラー  # noqa: E501

Notes:
    Dictのkeyとその型
    * label_id: str
    * annotation_ids: List[str]
    * type: str

"""

EmptyAttribute = Dict[str, Any]
"""
属性が未入力であるエラー  # noqa: E501

Notes:
    Dictのkeyとその型
    * label_id: str
    * annotation_id: str
    * additional_data_definition_id: str
    * type: str

"""

Error = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * error_code: str
    * message: str
    * ext: object

"""

ErrorAlreadyUpdated = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorExpiredToken = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorForbiddenResource = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorInternalServerError = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorInvalidBody = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorInvalidPath = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorInvalidQueryParam = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorLoginFailed = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorMissingNecessaryQueryParam = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorMissingResource = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorPasswordResetRequired = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorRefreshTokenExpired = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorStateMismatch = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorTimeout = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorUnauthorizedApi = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

ErrorUnderMaintenance = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

Errors = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * errors: List[Error]
    * context: object

"""

FullAnnotation = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
    * additional_data_definition_id: str
    * additional_data_definition_name: InternationalizationMessage
    * type: AdditionalDataDefinitionType
    * flag: bool
    * integer: int
    * comment: str
    * choice: str
    * choice_name: InternationalizationMessage

"""

FullAnnotationData = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * type: str
    * data_uri: str
    * left_top: Point
    * right_bottom: Point
    * points: List[Point]
    * point: Point
    * begin: float
    * end: float
    * data: str

"""

FullAnnotationDataBoundingBox = Dict[str, Any]
"""
annotation_type が bounding_boxの場合に、[左上頂点座標, 右下頂点座標]を {\"x\":int, \"y\":int} の形式で記述したもの。  # noqa: E501

Notes:
    Dictのkeyとその型
    * left_top: Point
    * right_bottom: Point
    * type: str

"""

FullAnnotationDataClassification = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * type: str

"""

FullAnnotationDataPoints = Dict[str, Any]
"""
頂点座標 {\"x\":int, \"y\":int} の配列。  * annotation_type が polygon/polyline の場合: ポリゴン/ポリラインを構成する頂点の配列。   # noqa: E501

Notes:
    Dictのkeyとその型
    * points: List[Point]
    * type: str

"""

FullAnnotationDataRange = Dict[str, Any]
"""
annotation_type が rangeの場合に、[開始時間, 終了時間]を {\"begin\":number, \"end\":number} の形式で記述したもの。開始時間・終了時間の単位は秒で、精度はミリ秒まで。  # noqa: E501

Notes:
    Dictのkeyとその型
    * begin: float
    * end: float
    * type: str

"""

FullAnnotationDataSegmentation = Dict[str, Any]
"""
塗っていないところは rgba(0,0,0,0)、塗ったところは rgba(255,255,255,1) の PNGデータをBase64エンコードしたもの。  # noqa: E501

Notes:
    Dictのkeyとその型
    * data_uri: str
    * type: str

"""

FullAnnotationDataSegmentationV2 = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * data_uri: str
    * type: str

"""

FullAnnotationDataSinglePoint = Dict[str, Any]
"""
annotation_type が pointの場合。  # noqa: E501

Notes:
    Dictのkeyとその型
    * point: Point
    * type: str

"""

FullAnnotationDataUnknown = Dict[str, Any]
"""
annotation_typeにデータ構造が一致していない場合に、元のdata文字列をそのまま記述したもの。  # noqa: E501

Notes:
    Dictのkeyとその型
    * data: str
    * type: str

"""

FullAnnotationDetail = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * annotation_id: str
    * user_id: str
    * label_id: str
    * label_name: InternationalizationMessage
    * annotation_type: AnnotationType
    * data_holding_type: AnnotationDataHoldingType
    * data: FullAnnotationData
    * path: str
    * additional_data_list: List[FullAnnotationAdditionalData]
    * comment: str

"""

HistogramItem = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * begin: float
    * end: float
    * count: int

"""

InlineResponse200 = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * list: List[MyOrganization]
    * page_no: float
    * total_page_no: float
    * total_count: float
    * over_limit: bool
    * aggregations: List[AggregationResult]

"""

InlineResponse2001 = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * list: List[Project]
    * page_no: float
    * total_page_no: float
    * total_count: float
    * over_limit: bool
    * aggregations: List[AggregationResult]

"""

InlineResponse2002 = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * list: List[OrganizationMember]
    * page_no: float
    * total_page_no: float
    * total_count: float
    * over_limit: bool
    * aggregations: List[AggregationResult]

"""

InlineResponse2003 = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * list: List[Project]
    * has_next: bool

"""

InlineResponse2004 = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * url: str

"""

InlineResponse2005 = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * list: List[ProjectMember]
    * page_no: float
    * total_page_no: float
    * total_count: float
    * over_limit: bool
    * aggregations: List[AggregationResult]

"""

InlineResponse2006 = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * list: List[Task]
    * page_no: float
    * total_page_no: float
    * total_count: float
    * over_limit: bool
    * aggregations: List[AggregationResult]

"""

InlineResponse2007 = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * list: List[SingleAnnotation]
    * page_no: float
    * total_page_no: float
    * total_count: float
    * over_limit: bool
    * aggregations: List[AggregationResult]

"""

InlineResponse2008 = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * list: List[InputData]
    * page_no: float
    * total_page_no: float
    * total_count: float
    * over_limit: bool
    * aggregations: List[AggregationResult]

"""

InputData = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * input_data_id: str
    * project_id: str
    * input_data_name: str
    * input_data_path: str
    * url: str
    * etag: str
    * original_input_data_path: str
    * original_resolution: Resolution
    * resized_resolution: Resolution
    * updated_datetime: datetime
    * sign_required: bool

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

Notes:
    Dictのkeyとその型
    * input_data_name: str
    * input_data_path: str
    * last_updated_datetime: datetime
    * sign_required: bool

"""

InputDataSummary = Dict[str, Any]
"""
ある入力データのバリデーション結果です。入力データIDをキーに引けるようにMap[入力データID, バリデーション結果]となっています  # noqa: E501

Notes:
    Dictのkeyとその型
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
検査コメント  # noqa: E501

Notes:
    Dictのkeyとその型
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
    * comment: str
    * status: InspectionStatus
    * created_datetime: datetime
    * updated_datetime: datetime

"""

InspectionDataPoint = Dict[str, Any]
"""
問題のある部分を示す座標   # noqa: E501

Notes:
    Dictのkeyとその型
    * x: int
    * y: int
    * type: str

"""

InspectionDataPolyline = Dict[str, Any]
"""
問題のある部分を示すポリライン   # noqa: E501

Notes:
    Dictのkeyとその型
    * coordinates: List[InspectionDataPolylineCoordinates]
    * type: str

"""

InspectionDataPolylineCoordinates = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * x: int
    * y: int

"""

InspectionDataTime = Dict[str, Any]
"""
問題のある時間帯を表す区間   # noqa: E501

Notes:
    Dictのkeyとその型
    * start: float
    * end: float
    * type: str

"""

InspectionPhrase = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * id: str
    * text: InternationalizationMessage

"""

InspectionStatistics = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * project_id: str
    * date: date
    * breakdown: InspectionStatisticsBreakdown

"""

InspectionStatisticsBreakdown = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * labels: dict(str, InspectionStatisticsPhrases)
    * no_label: InspectionStatisticsPhrases

"""

InspectionStatisticsPhrases = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * phrases: dict(str, int)
    * no_phrase: int

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

Notes:
    Dictのkeyとその型
    * history_id: str
    * account_id: str
    * updated_datetime: datetime

"""

InstructionImage = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * image_id: str
    * path: str
    * url: str
    * etag: str

"""

InternationalizationMessage = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * messages: List[InternationalizationMessageMessages]
    * default_lang: str

"""

InternationalizationMessageMessages = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * lang: str
    * message: str

"""

InvalidAnnotationData = Dict[str, Any]
"""
アノテーションデータ不正エラー  # noqa: E501

Notes:
    Dictのkeyとその型
    * label_id: str
    * annotation_id: str
    * message: str
    * type: str

"""

InvalidCommentFormat = Dict[str, Any]
"""
コメントが正規表現に合致しないエラー  # noqa: E501

Notes:
    Dictのkeyとその型
    * label_id: str
    * annotation_id: str
    * additional_data_definition_id: str
    * type: str

"""

InvalidLinkTarget = Dict[str, Any]
"""
リンク先アノテーションが許可されているラベルでないエラー  # noqa: E501

Notes:
    Dictのkeyとその型
    * label_id: str
    * annotation_id: str
    * additional_data_definition_id: str
    * type: str

"""

InviteOrganizationMemberRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * role: OrganizationMemberRole

"""

JobInfo = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * project_id: str
    * job_type: str
    * job_id: str
    * job_status: str
    * job_execution: object
    * job_detail: object
    * created_datetime: datetime
    * updated_datetime: datetime

"""

Keybind = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * code: str
    * shift: bool
    * ctrl: bool
    * alt: bool

"""

Label = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
    * min_width: int
    * min_height: int
    * min_warn_rule: str
    * tolerance: int

"""

LabelStatistics = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * label_id: str
    * completed_labels: int
    * wip_labels: int

"""

LoginRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * user_id: str
    * password: str

"""

LoginResponse = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * token: Token

"""

Message = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * message: str

"""

MyAccount = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
    * organization_id: str
    * created_datetime: datetime
    * storage_usage_bytes: float

"""

OrganizationMember = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
    * organization_name: str
    * organization_email: str
    * price_plan: PricePlan

"""

OrganizationSummary = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * last_tasks_updated_datetime: datetime

"""

OutOfImageBounds = Dict[str, Any]
"""
画像範囲外にアノテーションがはみ出しているエラー  # noqa: E501

Notes:
    Dictのkeyとその型
    * label_id: str
    * annotation_id: str
    * type: str

"""

PasswordResetRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * email: str

"""

PhaseStatistics = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * phase: str
    * worktime: str

"""

Point = Dict[str, Any]
"""
座標  # noqa: E501

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
    * account_id: str
    * histories: List[ProjectAccountStatisticsHistory]

"""

ProjectAccountStatisticsHistory = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * date: date
    * tasks_completed: int
    * tasks_rejected: int
    * worktime: str

"""

ProjectConfiguration = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * project_rule: str
    * project_workflow: ProjectWorkflow
    * assignee_rule_of_resubmitted_task: AssigneeRuleOfResubmittedTask
    * max_tasks_per_member: int
    * max_tasks_per_member_including_hold: int
    * input_data_max_long_side_length: int
    * sampling_inspection_rate: int
    * sampling_acceptance_rate: int
    * private_storage_aws_iam_role_arn: str

"""

ProjectCopyRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * dest_project_id: str
    * dest_title: str
    * dest_overview: str
    * copy_inputs: bool
    * copy_tasks_with_annotations: bool
    * copy_webhooks: bool
    * copy_supplementaly_data: bool
    * copy_instructions: bool

"""

ProjectMember = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * project_id: str
    * account_id: str
    * user_id: str
    * username: str
    * member_status: ProjectMemberStatus
    * member_role: ProjectMemberRole
    * updated_datetime: datetime
    * created_datetime: datetime
    * sampling_inspection_rate: int

"""

ProjectMemberRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * member_status: ProjectMemberStatus
    * member_role: ProjectMemberRole
    * last_updated_datetime: datetime

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

Notes:
    Dictのkeyとその型
    * last_tasks_updated_datetime: datetime

"""

ProjectTaskStatistics = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * phase: TaskPhase
    * status: TaskStatus
    * count: int
    * work_timespan: int

"""

ProjectTaskStatisticsHistory = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
    * user_id: str
    * username: str
    * lang: str
    * keylayout: str
    * token: Token
    * last_updated_datetime: datetime

"""

PutOrganizationMemberRoleRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * role: OrganizationMemberRole
    * last_updated_datetime: datetime

"""

PutOrganizationNameRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * organization_id: str
    * organization_name: str
    * last_updated_datetime: datetime

"""

PutProjectRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * title: str
    * overview: str
    * status: str
    * input_data_type: InputDataType
    * organization_name: str
    * configuration: ProjectConfiguration
    * last_updated_datetime: datetime
    * force_suspend: bool

"""

RefreshTokenRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * refresh_token: str

"""

ResetEmailRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * email: str

"""

ResetPasswordRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * token: str

"""

Resolution = Dict[str, Any]
"""
画像などの解像度   # noqa: E501

Notes:
    Dictのkeyとその型
    * width: float
    * height: float

"""

SignUpRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * email: str

"""

SimpleAnnotation = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * annotation_format_version: str
    * project_id: str
    * task_id: str
    * input_data_id: str
    * input_data_name: str
    * details: List[SimpleAnnotationDetail]
    * comment: str

"""

SimpleAnnotationDetail = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * label: str
    * annotation_id: str
    * data: FullAnnotationData
    * attributes: object

"""

SingleAnnotation = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * project_id: str
    * task_id: str
    * input_data_id: str
    * detail: SingleAnnotationDetail
    * updated_datetime: datetime

"""

SingleAnnotationDetail = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * annotation_id: str
    * account_id: str
    * label_id: str
    * data_holding_type: AnnotationDataHoldingType
    * data: FullAnnotationData
    * etag: str
    * url: str
    * additional_data_list: List[FullAnnotationAdditionalData]
    * created_datetime: datetime
    * updated_datetime: datetime

"""

SupplementaryData = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * project_id: str
    * input_data_id: str
    * supplementary_data_id: str
    * supplementary_data_name: str
    * supplementary_data_path: str
    * url: str
    * etag: str
    * supplementary_data_type: str
    * supplementary_data_number: int
    * updated_datetime: datetime

"""

SupplementaryDataRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * supplementary_data_name: str
    * supplementary_data_path: str
    * supplementary_data_type: str
    * supplementary_data_number: int
    * last_updated_datetime: datetime

"""

Task = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * project_id: str
    * task_id: str
    * phase: TaskPhase
    * status: TaskStatus
    * input_data_id_list: List[str]
    * account_id: str
    * histories_by_phase: List[TaskHistoryShort]
    * work_timespan: int
    * number_of_rejections: int
    * started_datetime: datetime
    * updated_datetime: datetime
    * sampling: str

"""

TaskGenerateRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * task_generate_rule: OneOfTaskGenerateRuleByCountTaskGenerateRuleByDirectoryTaskGenerateRuleByInputDataCsv
    * task_id_prefix: str
    * project_last_updated_datetime: datetime

"""

TaskGenerateRuleByCount = Dict[str, Any]
"""
1つのタスクに割りあてる入力データの個数を指定してタスクを生成します。  # noqa: E501

Notes:
    Dictのkeyとその型
    * allow_duplicate_input_data: bool
    * input_data_count: int
    * input_data_order: InputDataOrder
    * type: str

"""

TaskGenerateRuleByDirectory = Dict[str, Any]
"""
入力データ名をファイルパスに見立て、ディレクトリ単位でタスクを生成します。<br>  # noqa: E501

Notes:
    Dictのkeyとその型
    * input_data_name_prefix: str
    * type: str

"""

TaskGenerateRuleByInputDataCsv = Dict[str, Any]
"""
各タスクへの入力データへの割当を記入したCSVへのS3上のパスを指定してタスクを生成します。  # noqa: E501

Notes:
    Dictのkeyとその型
    * csv_data_path: str
    * type: str

"""

TaskHistory = Dict[str, Any]
"""
タスクのあるフェーズで、誰がいつどれくらいの作業時間を費やしたかを表すタスク履歴です。  # noqa: E501

Notes:
    Dictのkeyとその型
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
タスク履歴イベントは、タスクの状態が変化した１時点を表します。作業時間は、複数のこれらイベントを集約して計算するものなので、このオブジェクトには含まれません。  # noqa: E501

Notes:
    Dictのkeyとその型
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
タスクのあるフェーズを誰が担当したかを表します。  # noqa: E501

Notes:
    Dictのkeyとその型
    * phase: TaskPhase
    * account_id: str

"""

TaskOperation = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * status: TaskStatus
    * last_updated_datetime: datetime
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

Notes:
    Dictのkeyとその型
    * project_id: str
    * date: date
    * phases: List[PhaseStatistics]

"""

TaskRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * input_data_id_list: List[str]

"""

TaskStart = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
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
タスクの全入力データに対するバリデーション結果です。  # noqa: E501

Notes:
    Dictのkeyとその型
    * project_id: str
    * task_id: str
    * inputs: List[InputDataSummary]

"""

TasksInputs = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * project_id: str
    * tasks: List[TasksInputsTask]

"""

TasksInputsTask = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * task_id: str
    * phase: TaskPhase
    * status: TaskStatus
    * input_data_id_list: List[str]

"""

Token = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * id_token: str
    * access_token: str
    * refresh_token: str

"""

UnknownAdditionalData = Dict[str, Any]
"""
何らかの原因で、アノテーション仕様にない属性がついているエラー  # noqa: E501

Notes:
    Dictのkeyとその型
    * label_id: str
    * annotation_id: str
    * additional_data_definition_id: str
    * type: str

"""

UnknownLabel = Dict[str, Any]
"""
何らかの原因で、アノテーション仕様にないラベルがついているエラー  # noqa: E501

Notes:
    Dictのkeyとその型
    * label_id: str
    * annotation_id: str
    * type: str

"""

UnknownLinkTarget = Dict[str, Any]
"""
指定されたIDに該当するアノテーションが存在しないエラー  # noqa: E501

Notes:
    Dictのkeyとその型
    * label_id: str
    * annotation_id: str
    * additional_data_definition_id: str
    * type: str

"""

ValidationError = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * label_id: str
    * annotation_id: str
    * message: str
    * type: str
    * annotation_ids: List[str]
    * additional_data_definition_id: str
    * additional_data: AdditionalData

"""

VerifyEmailRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * token: Token

"""

Webhook = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
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

Notes:
    Dictのkeyとその型
    * name: str
    * value: str

"""

WebhookTestRequest = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * placeholders: object

"""

WebhookTestResponse = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * result: str
    * request_body: str
    * response_status: int
    * response_body: str
    * message: str

"""

WorktimeStatistics = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * project_id: str
    * date: date
    * by_tasks: List[WorktimeStatisticsItem]
    * by_inputs: List[WorktimeStatisticsItem]
    * accounts: List[AccountWorktimeStatistics]

"""

WorktimeStatisticsItem = Dict[str, Any]
"""

Notes:
    Dictのkeyとその型
    * phase: TaskPhase
    * histogram: List[HistogramItem]
    * average: str
    * standard_deviation: str

"""

