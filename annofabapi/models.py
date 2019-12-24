# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace
"""
annofabapiのmodel(swagger.yamlの ``components.schemes`` )
enumならば列挙体として定義する。
それ以外は型ヒントしてして宣言する。

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照
"""

import warnings  # pylint: disable=unused-import
from enum import Enum
from typing import Any, Dict, List, NewType, Optional, Tuple, Union  # pylint: disable=unused-import

### 手動の部分

AccountId = NewType('AccountId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``
    
"""

UserId = NewType('UserId', str)
"""

Example:
    ``john_doe``

"""

OrganizationId = NewType('OrganizationId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

ProjectId = NewType('ProjectId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

LabelId = NewType('LabelId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

AdditionalDataDefinitionId = NewType('AdditionalDataDefinitionId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

ChoiceId = NewType('ChoiceId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

PhraseId = NewType('PhraseId', str)
"""

Example:
    ``my_phrase_id``

"""

TaskId = NewType('TaskId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

InputDataId = NewType('InputDataId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

SupplementaryDataId = NewType('SupplementaryDataId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

TaskHistoryId = NewType('TaskHistoryId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

AnnotationId = NewType('AnnotationId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

InspectionId = NewType('InspectionId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

MakerId = NewType('MakerId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

JobId = NewType('JobId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

WebhookId = NewType('WebhookId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

Duration = NewType('Duration', str)
"""

Example:
    ``PT34H17M36.789S``

"""

### 以下は自動生成の部分
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
    
* biography: str
    人物紹介、略歴。  この属性は、AnnoFab外の所属先や肩書などを表すために用います。 AnnoFab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 
* keylayout: str
    
* authority: AccountAuthority
    
* updated_datetime: str
    

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
    ユーザごとのタスク1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）
* by_inputs: List[WorktimeStatisticsItem]
    ユーザごとの画像1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）
* by_minutes: List[WorktimeStatisticsItem]
    ユーザごとの動画1分当たりの作業時間情報（画像プロジェクトの場合は空リスト）

"""

AdditionalData = Dict[str, Any]
"""


Kyes of Dict

* additional_data_definition_id: str
    
* flag: bool
    
* integer: int
    
* comment: str
    
* choice: str
    

"""

AdditionalDataChoiceValue = Dict[str, Any]
"""


Kyes of Dict

* id: str
    
* name: InternationalizationMessage
    

"""

AdditionalDataDefinition = Dict[str, Any]
"""


Kyes of Dict

* additional_data_definition_id: str
    
* read_only: bool
    
* name: InternationalizationMessage
    
* default: OneOfbooleanintegerstring
    属性の初期値です。  初期値を指定する場合、属性の種類に応じて次の値を指定します。初期値を設定しない場合には空文字を指定します。  * type が flag の場合: 真偽値(`true` or `false`) * type が integer の場合: 整数値 * type が text の場合: 文字列 * type が comment の場合: 文字列 * type が choice の場合: 選択肢(`choices`)の `choice_id` * type が select の場合: 選択肢(`choices`)の `choice_id`  属性の種類に対して有効でない初期値を設定した場合、その設定は無視されます。  なお、トラッキングとリンクには初期値を設定できません。 
* keybind: List[Keybind]
    
* type: AdditionalDataDefinitionType
    
* choices: List[AdditionalDataDefinitionChoices]
    
* regex: str
    
* label_ids: List[str]
    リンク属性において、リンク先として指定可能なラベルID（空の場合制限なし）
* required: bool
    リンク属性において、入力を必須とするかどうか

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
    * `flag` - 真偽値 * `integer` - 整数値 * `text` - 自由記述（1行） * `comment` - 自由記述（複数行） * `choice` - 選択肢（ラジオボタン式） * `select` - 選択肢（ドロップダウン式） * `tracking` - 自由記述 (トラッキングID自動挿入) * `link` - アノテーションリンク 
    """

    FLAG = "flag"
    INTEGER = "integer"
    TEXT = "text"
    COMMENT = "comment"
    CHOICE = "choice"
    SELECT = "select"
    TRACKING = "tracking"
    LINK = "link"


AdditionalDataValue = Dict[str, Any]
"""


Kyes of Dict

* type: str
    Link
* value: str
    リンク先アノテーションID

"""

AdditionalDataValueChoice = Dict[str, Any]
"""


Kyes of Dict

* type: str
    Choice
* value: AdditionalDataChoiceValue
    

"""

AdditionalDataValueComment = Dict[str, Any]
"""


Kyes of Dict

* type: str
    Comment
* value: str
    自由記述

"""

AdditionalDataValueFlag = Dict[str, Any]
"""


Kyes of Dict

* type: str
    Flag
* value: bool
    フラグのON(true)またはOFF(false)

"""

AdditionalDataValueInteger = Dict[str, Any]
"""


Kyes of Dict

* type: str
    Integer
* value: int
    整数値

"""

AdditionalDataValueLink = Dict[str, Any]
"""


Kyes of Dict

* type: str
    Link
* value: str
    リンク先アノテーションID

"""

AdditionalDataValueTracking = Dict[str, Any]
"""


Kyes of Dict

* type: str
    Tracking
* value: str
    トラッキングID

"""

AggregationResult = Dict[str, Any]
"""


Kyes of Dict


"""

Annotation = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: List[AnnotationDetail]
    
* comment: str
    
* updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""


class AnnotationDataHoldingType(Enum):
    """
    * `inner` - アノテーションのデータ部をJSON内部に保持します。 * `outer` - アノテーションのデータ部を外部ファイルの形式（画像など）で保持します 
    """

    INNER = "inner"
    OUTER = "outer"


AnnotationDetail = Dict[str, Any]
"""


Kyes of Dict

* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 
* account_id: str
    
* label_id: str
    
* is_protected: bool
    
* data_holding_type: AnnotationDataHoldingType
    
* data: OneOfstringFullAnnotationData
    data_holding_type が inner の場合のみ存在し、annotation_type に応じたデータの値が格納されます。 `string`もしくは`object`の値を指定することができ、`string`の形式は次の通りです。   * annotation_type が bounding_box の場合: 左上x,左上y,右下x,右下y のCSV文字列形式。   * annotation_type が polygon/polyline の場合: x1,y1,x2,y2, ... のCSV文字列形式。   * annotation_type が segmentation または segmentation_v2 の場合: 塗っていないところは rgba(0,0,0,0)、塗ったところは rgba(255,255,255,1) の PNGデータをBase64エンコードしたもの。   * annotation_type が classification の場合: data 属性は存在しない。   * annotation_type が range の場合: 開始時間,終了時間 のCSV文字列形式。 
* path: str
    data_holding_typeがouterの場合のみ存在し、データのパスが格納される (現在はアノテーションIDと等しい)
* etag: str
    data_holding_typeがouterの場合のみ存在し、データのETagが格納される
* url: str
    data_holding_typeがouterの場合のみ存在し、データへの一時URLが格納される
* additional_data_list: List[AdditionalData]
    各要素は、 [アノテーション仕様](#operation/getAnnotationSpecs)で定義された属性（`additional_data_definitions`内）のいずれかの要素と対応づけます。 各要素は、どの属性なのかを表す`additional_data_definition_id`、値が必要です。値は、属性の種類に対応するキーに格納します（下表）。  <table> <tr><th>アノテーション属性の種類<br>（`additional_data_definition`の`type`）</th><th>属性の値を格納するキー</th><th>データ型</th></tr> <tr><td>`comment` または `tracking`</td><td>`comment`</td><td>string</td></tr> <tr><td>`flag`</td><td>`flag`</td><td>boolean</td></tr> <tr><td>`integer`</td><td>`integer`</td><td>integer</td></tr> <tr><td>`choice` または `select`</td><td>`choice`</td><td>string（選択肢ID）</td></tr> <tr><td>`link`</td><td>`comment`</td><td>string（アノテーションID）</td></tr> </table> 
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
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* exact_match_task_id: bool
    タスクIDの検索方法を指定します。 trueの場合は完全一致検索、falseの場合は中間一致検索です。 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* exact_match_input_data_id: bool
    入力データIDの検索方法を指定します。 trueの場合は完全一致検索、falseの場合は中間一致検索です。 
* label_id: str
    
* attributes: List[AdditionalData]
    

"""

AnnotationSpecs = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* labels: List[Label]
    
* inspection_phrases: List[InspectionPhrase]
    

"""

AnnotationSpecsHistory = Dict[str, Any]
"""


Kyes of Dict

* history_id: str
    
* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* updated_datetime: str
    
* url: str
    
* account_id: str
    
* comment: str
    

"""

AnnotationSpecsRequest = Dict[str, Any]
"""


Kyes of Dict

* labels: List[Label]
    ラベル 
* inspection_phrases: List[InspectionPhrase]
    定型指摘 
* comment: str
    
* auto_marking: bool
    trueが指定された場合、各統計グラフにマーカーを自動追加します。 マーカーのタイトルには `comment` に指定された文字列が設定されます。 `comment` が指定されていなかった場合は \"アノテーション仕様の変更\" という文字列が設定されます。 

"""


class AnnotationType(Enum):
    """
    * `bounding_box` - 矩形を表します。 * `segmentation` - ピクセルレベルでの塗りつぶし（ラスター）を表します。 * `segmentation_v2` - 塗りつぶしv2を表します。v2はSemantic Segmentationに特化しています。 * `polygon` - ポリゴン（閉じた頂点集合）を表します。 * `polyline` - ポリライン（開いた頂点集合）を表します。 * `point` - 点を表します。 * `classification` - 入力データ全体に対するアノテーションを表します。 * `range` - 動画の区間を表します。 
    """

    BOUNDING_BOX = "bounding_box"
    SEGMENTATION = "segmentation"
    SEGMENTATION_V2 = "segmentation_v2"
    POLYGON = "polygon"
    POLYLINE = "polyline"
    POINT = "point"
    CLASSIFICATION = "classification"
    RANGE = "range"


class AssigneeRuleOfResubmittedTask(Enum):
    """
    * `no_assignee` - 以前の担当者で固定せず、未割当てにします。 * `fixed` - 以前の担当者が再度担当します。以前の担当者がいない(1回目の検査/受入)場合は未割当てになります。 
    """

    NO_ASSIGNEE = "no_assignee"
    FIXED = "fixed"


BatchAnnotation = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 
* label_id: str
    
* additional_data_list: List[AdditionalData]
    
* updated_datetime: str
    

"""

BatchAnnotationRequestItemDelete = Dict[str, Any]
"""
アノテーション削除

Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 
* updated_datetime: str
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchAnnotationRequestItemPut = Dict[str, Any]
"""
アノテーション更新

Kyes of Dict

* data: BatchAnnotation
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchInputDataRequestItemDelete = Dict[str, Any]
"""
入力データ削除

Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchInspectionRequestItemDelete = Dict[str, Any]
"""
検査コメント削除

Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* inspection_id: str
    検査ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchInspectionRequestItemPut = Dict[str, Any]
"""
検査コメント更新

Kyes of Dict

* data: Inspection
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchTaskRequestItemDelete = Dict[str, Any]
"""
タスク削除

Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

CacheRecord = Dict[str, Any]
"""


Kyes of Dict

* input: str
    
* members: str
    
* project: str
    
* instruction: str
    
* specs: str
    
* statistics: str
    
* organization: str
    
* supplementary: str
    

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
    他と区別するために `CountResult` を指定します 
* name: str
    
* field: str
    
* items: List[Count]
    

"""

DataPath = Dict[str, Any]
"""


Kyes of Dict

* url: str
    ファイルアップロード用の一時URLです。このURLにファイルをアップロードします。
* path: str
    アップロードしたファイルをAFの [入力データ](#tag/af-input) や [補助情報](#tag/af-supplementary) に登録するとき、この`path`を指定します。

"""

Duplicated = Dict[str, Any]
"""
値の重複が許可されていない属性の重複エラー

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data: AdditionalData
    
* type: str
    Duplicated

"""

DuplicatedSegmentationV2 = Dict[str, Any]
"""
塗りつぶしv2のラベルに対する1ラベルにつき1アノテーションまでの制約違反エラー

Kyes of Dict

* label_id: str
    
* annotation_ids: List[str]
    
* type: str
    DuplicatedSegmentationV2

"""

EmptyAttribute = Dict[str, Any]
"""
属性が未入力であるエラー

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    EmptyAttribute

"""

Error = Dict[str, Any]
"""


Kyes of Dict

* error_code: str
    
* message: str
    エラーの概要
* ext: __DictStrKeyAnyValue__
    補足情報

"""

ErrorAlreadyUpdated = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorExpiredToken = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorForbiddenResource = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorInternalServerError = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorInvalidBody = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorInvalidPath = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorInvalidQueryParam = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorLoginFailed = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorMissingNecessaryQueryParam = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorMissingResource = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorPasswordResetRequired = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorRefreshTokenExpired = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorStateMismatch = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorTimeout = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorUnauthorizedApi = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ErrorUnderMaintenance = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

Errors = Dict[str, Any]
"""


Kyes of Dict

* errors: List[Error]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

FullAnnotation = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_phase: TaskPhase
    
* task_phase_stage: int
    
* task_status: TaskStatus
    
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_name: str
    
* details: List[FullAnnotationDetail]
    
* detail: List[FullAnnotationDetailOld]
    use details
* updated_datetime: str
    
* annotation_format_version: str
    アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、AnnoFabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 

"""

FullAnnotationAdditionalData = Dict[str, Any]
"""


Kyes of Dict

* additional_data_definition_id: str
    
* additional_data_definition_name: InternationalizationMessage
    
* type: AdditionalDataDefinitionType
    
* value: AdditionalDataValue
    

"""

FullAnnotationAdditionalDataOld = Dict[str, Any]
"""
for v1

Kyes of Dict

* additional_data_definition_id: str
    
* additional_data_definition_name: InternationalizationMessage
    
* type: AdditionalDataDefinitionType
    
* flag: bool
    typeがflagの場合に、フラグのON(true)またはOFF(false)が格納される
* integer: int
    typeがintegerの場合に、整数値が格納される
* comment: str
    * typeがcommentの場合、コメントの値 * typeがtrackingの場合、トラッキングID * typeがlinkの場合、リンク先のアノテーションID 
* choice: str
    
* choice_name: InternationalizationMessage
    

"""

FullAnnotationData = Dict[str, Any]
"""
アノテーションのデータが格納されます。   * `FullAnnotationDataClassification`: 入力データ全体に対するアノテーションデータです。   * `FullAnnotationDataSegmentation`: ピクセルレベルでの塗りつぶし（ラスター）のアノテーションデータです。   * `FullAnnotationDataSegmentationV2`: 塗りつぶしv2ののアノテーションデータです。塗りつぶしv2はSemantic Segmentationに特化しています。   * `FullAnnotationDataBoundingBox`: 矩形のアノテーションデータです。   * `FullAnnotationDataPoints`: ポリゴン（閉じた頂点集合）のアノテーションデータです。   * `FullAnnotationDataSegmentation`: 点のアノテーションデータです。   * `FullAnnotationDataRange`: 動画区間のアノテーションデータです。 

Kyes of Dict

* type: str
    Unknown
* data_uri: str
    
* left_top: Point
    
* right_bottom: Point
    
* points: List[Point]
    
* point: Point
    
* begin: float
    開始時間（ミリ秒）。小数点以下はミリ秒以下を表します。
* end: float
    終了時間（ミリ秒）。小数点以下はミリ秒以下を表します。
* data: str
    

"""

FullAnnotationDataBoundingBox = Dict[str, Any]
"""
annotation_type が bounding_boxの場合に、[左上頂点座標, 右下頂点座標]を {\"x\":int, \"y\":int} の形式で記述したもの。

Kyes of Dict

* left_top: Point
    
* right_bottom: Point
    
* type: str
    BoundingBox

"""

FullAnnotationDataClassification = Dict[str, Any]
"""


Kyes of Dict

* type: str
    Classification

"""

FullAnnotationDataPoints = Dict[str, Any]
"""
頂点座標 {\"x\":int, \"y\":int} の配列。  * annotation_type が polygon/polyline の場合: ポリゴン/ポリラインを構成する頂点の配列。 

Kyes of Dict

* points: List[Point]
    
* type: str
    Points

"""

FullAnnotationDataRange = Dict[str, Any]
"""
annotation_type が rangeの場合に、[開始時間, 終了時間]を {\"begin\":number, \"end\":number} の形式で記述したもの。開始時間・終了時間の単位は秒で、精度はミリ秒まで。

Kyes of Dict

* begin: float
    開始時間（ミリ秒）。小数点以下はミリ秒以下を表します。
* end: float
    終了時間（ミリ秒）。小数点以下はミリ秒以下を表します。
* type: str
    Range

"""

FullAnnotationDataSegmentation = Dict[str, Any]
"""
塗っていないところは rgba(0,0,0,0)、塗ったところは rgba(255,255,255,1) の PNGデータをBase64エンコードしたもの。

Kyes of Dict

* data_uri: str
    
* type: str
    Segmentation

"""

FullAnnotationDataSegmentationV2 = Dict[str, Any]
"""


Kyes of Dict

* data_uri: str
    
* type: str
    SegmentationV2

"""

FullAnnotationDataSinglePoint = Dict[str, Any]
"""
annotation_type が pointの場合。

Kyes of Dict

* point: Point
    
* type: str
    SinglePoint。

"""

FullAnnotationDataUnknown = Dict[str, Any]
"""
annotation_typeにデータ構造が一致していない場合に、元のdata文字列をそのまま記述したもの。

Kyes of Dict

* data: str
    
* type: str
    Unknown

"""

FullAnnotationDetail = Dict[str, Any]
"""


Kyes of Dict

* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 
* user_id: str
    
* label_id: str
    
* label_name: InternationalizationMessage
    
* annotation_type: AnnotationType
    
* data_holding_type: AnnotationDataHoldingType
    
* data: FullAnnotationData
    
* additional_data_list: List[FullAnnotationAdditionalData]
    

"""

FullAnnotationDetailOld = Dict[str, Any]
"""
for v1

Kyes of Dict

* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 
* user_id: str
    
* label_id: str
    
* label_name: InternationalizationMessage
    
* annotation_type: AnnotationType
    
* data_holding_type: AnnotationDataHoldingType
    
* data: FullAnnotationData
    
* additional_data_list: List[AdditionalData]
    

"""


class GraphType(Enum):
    """
    * `task_progress` - タスク進捗状況 * `cumulative_labor_time_by_task_phase` - タスクフェーズ別累積作業時間 * `number_of_inspections_per_inspection_phrase` - 検査コメント内容別指摘回数 * `number_of_task_rejections_by_member` - メンバー別タスクが差戻された回数 * `labor_time_per_member` - メンバー別作業時間 * `mean_labor_time_per_image` - 画像一枚当たりの作業時間平均 * `mean_labor_time_per_minute_of_movie` - 動画一分当たりの作業時間平均 * `mean_labor_time_per_image_by_member` - メンバー別画像一枚当たりの作業時間平均 * `mean_labor_time_per_minute_of_movie_by_member` - メンバー別動画一分当たりの作業時間平均 
    """

    TASK_PROGRESS = "task_progress"
    CUMULATIVE_LABOR_TIME_BY_TASK_PHASE = "cumulative_labor_time_By_task_phase"
    NUMBER_OF_INSPECTIONS_PER_INSPECTION_PHRASE = "number_of_inspections_per_inspection_phrase"
    NUMBER_OF_TASK_REJECTIONS_BY_MEMBER = "number_of_task_rejections_by_member"
    LABOR_TIME_PER_MEMBER = "labor_time_per_member"
    MEAN_LABOR_TIME_PER_IMAGE = "mean_labor_time_per_image"
    MEAN_LABOR_TIME_PER_MINUTE_OF_MOVIE = "mean_labor_time_per_minute_of_movie"
    MEAN_LABOR_TIME_PER_IMAGE_BY_MEMBER = "mean_labor_time_per_image_by_member"
    MEAN_LABOR_TIME_PER_MINUTE_OF_MOVIE_BY_MEMBER = "mean_labor_time_per_minute_of_movie_by_member"


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
    現在のページ番号に含まれる0件以上の所属組織です。
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる所属組織が0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。

"""

InlineResponse2001 = Dict[str, Any]
"""


Kyes of Dict

* list: List[Project]
    現在のページ番号に含まれる0件以上のプロジェクトです。
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるプロジェクトが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。

"""

InlineResponse2002 = Dict[str, Any]
"""


Kyes of Dict

* list: List[OrganizationMember]
    
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる組織メンバーが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。

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
    認証済み一時URL

"""

InlineResponse2005 = Dict[str, Any]
"""


Kyes of Dict

* list: List[ProjectMember]
    
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるプロジェクトメンバーが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。

"""

InlineResponse2006 = Dict[str, Any]
"""


Kyes of Dict

* list: List[JobInfo]
    
* has_next: bool
    

"""

InlineResponse2007 = Dict[str, Any]
"""


Kyes of Dict

* list: List[Task]
    現在のページ番号に含まれる0件以上のタスクです。
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるタスク0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。

"""

InlineResponse2008 = Dict[str, Any]
"""


Kyes of Dict

* list: List[SingleAnnotation]
    現在のページ番号に含まれる0件以上のアノテーションです。
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるアノテーションが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。

"""

InlineResponse2009 = Dict[str, Any]
"""


Kyes of Dict

* list: List[InputData]
    現在のページ番号に含まれる0件以上の入力データです。
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる入力データが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: List[AggregationResult]
    Aggregationによる集約結果。

"""

InputData = Dict[str, Any]
"""


Kyes of Dict

* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_name: str
    表示用の名前です。
* input_data_path: str
    入力データの実体が保存されたパスです。 s3スキーマまたはhttpsスキーマのみサポートしています。 
* url: str
    入力データを取得するためのhttpsスキーマのURLです。  このURLはセキュリティのために認証認可が必要となっており、URLだけでは入力データを参照できません。 このURLは内部用であり、常に変更になる可能性があります。そのため、アクセスは保証外となります。 また、このURLのレスポンスは最低1時間キャッシュされます。 キャッシュを無効にしたい場合は、クエリパラメータにアクセス毎にランダムなUUIDなどを付与してください。  設定の不備等でデータが取得できない場合、この属性は設定されません。 
* etag: str
    
* original_input_data_path: str
    AF外部のストレージから登録された場合、その外部ストレージ中のパス。 それ以外の場合は値なし 
* original_resolution: Resolution
    
* resized_resolution: Resolution
    
* updated_datetime: str
    
* sign_required: bool
    データがSigned Cookieによるクロスオリジン配信に対応しているか否かです。 

"""


class InputDataOrder(Enum):
    """
    タスクに割り当てる入力データの順序  * `name_asc` - 入力データ名 昇順（a, b, c, ...）。日付や番号などの連続するデータ名を扱う場合に推奨 * `name_asc` - 入力データ名 降順（z, y, x, ...） * `random` - ランダム 
    """

    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"
    RANDOM = "random"


InputDataRequest = Dict[str, Any]
"""


Kyes of Dict

* input_data_name: str
    表示用の名前
* input_data_path: str
    AnnoFabに登録する入力データの実体が保存されたパスです。  対応スキーマ： * s3 * https * data（廃止予定）  場面別の使い分け： * [一時データ保存先取得API](#operation/createTempPath)を使ってAFにアップロードした場合: `s3://ANNOFAB-BUCKET/PATH/TO/INPUT_DATA` * [プライベートストレージ](/docs/faq/#prst9c)の場合     * `https://YOUR-DOMAIN/PATH/TO/INPUT_DATA`     * `s3://YOUR-BUCKET-FOR-PRIVATE-STORAGE/PATH/TO/INPUT_DATA`         * S3プライベートストレージのパスを登録する場合、[事前に認可の設定が必要](/docs/faq/#m0b240)です。 * dataスキーマでアップロードする場合: `data://....`     * dataスキーマは、4MB以内の画像であれば[一時データ保存先取得API](#operation/createTempPath)を使わずに直接アップロードできるので便利です。 
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 
* sign_required: bool
    データがSigned Cookieによるクロスオリジン配信に対応しているか否かです。<br> このオプションを有効にする場合は、`input_data_path`として、AnnoFabのAWS IDをTrusted Signerとして登録したCloudFrontのURLを指定してください。 

"""

InputDataSummary = Dict[str, Any]
"""
ある入力データのバリデーション結果です。入力データIDをキーに引けるようにMap[入力データID, バリデーション結果]となっています

Kyes of Dict

* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* inspection_summary: InspectionSummary
    
* annotation_summaries: List[ValidationError]
    

"""


class InputDataType(Enum):
    """
    プロジェクトの作成時のみ指定可能（未指定の場合は image）です。更新時は無視されます
    """

    IMAGE = "image"
    MOVIE = "movie"


Inspection = Dict[str, Any]
"""
検査コメント

Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* inspection_id: str
    検査ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* phase: TaskPhase
    
* phase_stage: int
    
* commenter_account_id: str
    
* annotation_id: str
    
* data: OneOfInspectionDataPointInspectionDataPolylineInspectionDataTime
    
* parent_inspection_id: str
    検査ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* phrases: List[str]
    選択された定型指摘ID. 未選択時は空
* comment: str
    
* status: InspectionStatus
    
* created_datetime: str
    
* updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

InspectionDataPoint = Dict[str, Any]
"""
問題のある部分を示す座標 

Kyes of Dict

* x: int
    
* y: int
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

InspectionDataPolyline = Dict[str, Any]
"""
問題のある部分を示すポリライン 

Kyes of Dict

* coordinates: List[InspectionDataPolylineCoordinates]
    ポリラインを構成する頂点の配列 
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

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
    [詳しくはこちら](#section/API-Convention/API-_type) 

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
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* date: str
    集計日
* breakdown: InspectionStatisticsBreakdown
    

"""

InspectionStatisticsBreakdown = Dict[str, Any]
"""
検査コメント数の集計結果

Kyes of Dict

* labels: dict(str, InspectionStatisticsPhrases)
    ラベルごとの指摘集計結果。キーは`label_id`
* no_label: InspectionStatisticsPhrases
    

"""

InspectionStatisticsPhrases = Dict[str, Any]
"""
ラベル外指摘の集計結果

Kyes of Dict

* phrases: dict(str, int)
    定型指摘ごとの合計数。キーは定型指摘ID、値は指摘数
* no_phrase: int
    非定型指摘の合計数

"""


class InspectionStatus(Enum):
    """
    * `annotator_action_required` - 未処置。`annotation`フェーズ担当者が何らかの回答をする必要あり * `no_correction_required` - 処置不要。`annotation`フェーズ担当者が、検査コメントによる修正は不要、と回答した * `error_corrected` - 修正済み。`annotation`フェーズ担当者が、検査コメントの指示どおり修正した * `no_comment_inspection` - 作成途中。検査コメントの中身が未入力 
    """

    ANNOTATOR_ACTION_REQUIRED = "annotator_action_required"
    NO_CORRECTION_REQUIRED = "no_correction_required"
    ERROR_CORRECTED = "error_corrected"
    NO_COMMENT_INSPECTION = "no_comment_inspection"


class InspectionSummary(Enum):
    """
    - `no_inspection` - 入力データに検査コメントが付けられていない。 - `no_comment_inspection` - 入力データに空の検査コメントが付けられている。 - `new_reply_to_unprocessed` - 現在進行中の検査・受入フェーズで未処理の検査コメントに対して新たに返信が付けられている。 - `new_unprocessed_inspection` - 現在進行中の検査・受入フェーズでつけられた検査コメントのうち、未処理のものが1つ以上ある。 - `unprocessed` - 過去の検査・受入フェーズでつけられた検査コメントのうち、未処理のものが1つ以上ある。 - `complete` - 入力データにつけられた検査コメントで未処理のものがない。 
    """

    NO_INSPECTION = "no_inspection"
    NO_COMMENT_INSPECTION = "no_comment_inspection"
    NEW_REPLY_TO_UNPROCESSED = "new_reply_to_unprocessed"
    NEW_UNPROCESSED_INSPECTION = "new_unprocessed_inspection"
    UNPROCESSED = "unprocessed"
    COMPLETE = "complete"


Instruction = Dict[str, Any]
"""


Kyes of Dict

* html: str
    
* last_updated_datetime: str
    * `GetInstruction` の場合: 最後に作業ガイドを更新した日時。 * `PutInstruction` の場合: 最後に作業ガイドを更新した日時を指定する。まだ一度も保存した事がない場合は指定しない。 

"""

InstructionHistory = Dict[str, Any]
"""


Kyes of Dict

* history_id: str
    
* account_id: str
    
* updated_datetime: str
    

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
    InvalidAnnotationData

"""

InvalidCommentFormat = Dict[str, Any]
"""
コメントが正規表現に合致しないエラー

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    InvalidCommentFormat

"""

InvalidLinkTarget = Dict[str, Any]
"""
リンク先アノテーションが許可されているラベルでないエラー

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    InvalidLinkTarget

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
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* job_type: JobType
    
* job_id: str
    
* job_status: JobStatus
    
* job_execution: __DictStrKeyAnyValue__
    ジョブの内部情報
* job_detail: __DictStrKeyAnyValue__
    ジョブ結果の内部情報
* created_datetime: str
    
* updated_datetime: str
    

"""


class JobStatus(Enum):
    """
    """

    PROGRESS = "progress"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class JobType(Enum):
    """
    * `copy-project` - プロジェクトのコピー。[initiateProjectCopy](#operation/initiateProjectCopy) APIを実行したときに登録されるジョブ。 * `gen-inputs` - zipファイルから入力データの作成。[putInputData](#operation/putInputData) APIを実行して、zipファイルから入力データを作成したときに登録されるジョブ。 * `gen-tasks` - タスクの一括作成。[initiateTasksGeneration](#operation/initiateTasksGeneration) APIを実行したときに登録されるジョブ。 * `gen-annotation` - アノテーションZIPの更新。[postAnnotationArchiveUpdate](#operation/postAnnotationArchiveUpdate) APIを実行したときに登録されるジョブ。 * `gen-tasks-list` - タスク全件ファイルの更新。[postProjectTasksUpdate](#operation/postProjectTasksUpdate) APIを実行したときに登録されるジョブ。 * `invoke-hook` - Webhookの起動。 
    """

    COPY_PROJECT = "copy-project"
    GEN_INPUTS = "gen-inputs"
    GEN_TASKS = "gen-tasks"
    GEN_ANNOTATION = "gen-annotation"
    GEN_TASKS_LIST = "gen-tasks-list"
    INVOKE_HOOK = "invoke-hook"


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
    
* completed: int
    ラベルごとの受入が完了したアノテーション数
* wip: int
    ラベルごとの受入が完了していないアノテーション数

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

Marker = Dict[str, Any]
"""


Kyes of Dict

* marker_id: str
    マーカーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* title: str
    
* graph_type: GraphType
    
* marked_at: str
    グラフ上のマーカー位置(x軸)

"""

Markers = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* markers: List[Marker]
    
* updated_datetime: str
    

"""

Message = Dict[str, Any]
"""


Kyes of Dict

* message: str
    多言語対応

"""

MyAccount = Dict[str, Any]
"""


Kyes of Dict

* account_id: str
    
* user_id: str
    
* username: str
    
* email: str
    
* lang: str
    
* biography: str
    人物紹介、略歴。  この属性は、AnnoFab外の所属先や肩書などを表すために用います。 AnnoFab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 
* keylayout: str
    
* authority: AccountAuthority
    
* updated_datetime: str
    
* reset_requested_email: str
    
* errors: List[str]
    

"""

MyAccountAllOf = Dict[str, Any]
"""


Kyes of Dict

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
    
* created_datetime: str
    
* updated_datetime: str
    
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
    
* created_datetime: str
    
* updated_datetime: str
    

"""

OrganizationActivity = Dict[str, Any]
"""


Kyes of Dict

* organization_id: str
    
* created_datetime: str
    
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
    
* biography: str
    人物紹介、略歴。  この属性は、AnnoFab外の所属先や肩書などを表すために用います。 AnnoFab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 
* created_datetime: str
    
* updated_datetime: str
    

"""


class OrganizationMemberRole(Enum):
    """
    """

    OWNER = "owner"
    ADMINISTRATOR = "administrator"
    CONTRIBUTOR = "contributor"


class OrganizationMemberStatus(Enum):
    """
    * `active` - 組織メンバーとして有効で、組織を閲覧したり、権限があれば編集できます。 * `waiting_response` - 組織に招待され、まだ加入/脱退を返答していません。組織の一部を閲覧のみできます。 * `inactive` - 脱退したメンバーを表します。組織を閲覧できません。 
    """

    ACTIVE = "active"
    WAITING_RESPONSE = "waiting_response"
    INACTIVE = "inactive"


OrganizationRegistrationRequest = Dict[str, Any]
"""


Kyes of Dict

* organization_name: str
    組織名。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* organization_email: str
    
* price_plan: PricePlan
    

"""

OrganizationSummary = Dict[str, Any]
"""


Kyes of Dict

* last_tasks_updated_datetime: str
    

"""

OutOfImageBounds = Dict[str, Any]
"""
画像範囲外にアノテーションがはみ出しているエラー

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* type: str
    OutOfImageBounds

"""

PasswordResetRequest = Dict[str, Any]
"""


Kyes of Dict

* email: str
    

"""

PhaseStatistics = Dict[str, Any]
"""


Kyes of Dict

* phase: TaskPhase
    
* worktime: str
    累積作業時間（ISO 8601 duration）

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
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* organization_id: str
    
* title: str
    
* overview: str
    
* project_status: ProjectStatus
    
* input_data_type: InputDataType
    
* configuration: ProjectConfiguration
    
* created_datetime: str
    
* updated_datetime: str
    
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

* date: str
    
* tasks_completed: int
    教師付を担当したタスクが完了状態になった回数
* tasks_rejected: int
    教師付を担当したタスクが差し戻された回数
* worktime: str
    作業時間（ISO 8601 duration）

"""

ProjectConfiguration = Dict[str, Any]
"""


Kyes of Dict

* number_of_inspections: int
    検査回数。 * 0回：教師付け -> 受入 * 1回：教師付け -> 検査 -> 受入 * n回(n >= 2)：教師付け -> 検査1 -> ... -> 検査n -> 受入 
* assignee_rule_of_resubmitted_task: AssigneeRuleOfResubmittedTask
    
* max_tasks_per_member: int
    保留中のタスクを除き、1人（オーナー以外）に割り当てられるタスク数上限。未指定の場合は10件として扱う。
* max_tasks_per_member_including_hold: int
    保留中のタスクを含めて、1人（オーナー以外）に割り当てられるタスク数上限。未指定の場合は20件として扱う。
* input_data_set_id_list: List[str]
    このフィールドは内部用でまだ何も意味を成しません。今は空配列を指定してください。
* input_data_max_long_side_length: int
    入力データ画像の長辺の最大値（未指定時は4096px）。  画像をアップロードすると、長辺がこの値になるように画像が自動で圧縮されます。 アノテーションの座標は、もとの解像度の画像でつけたものに復元されます。  大きな数値を設定すると入力データ画像のサイズが大きくなり、生産性低下やブラウザで画像を表示できない懸念があります。注意して設定してください。 
* sampling_inspection_rate: int
    抜取検査率。0-100のパーセント値で指定し、未指定の場合は100%として扱う。
* sampling_acceptance_rate: int
    抜取受入率。0-100のパーセント値で指定し、未指定の場合は100%として扱う。
* private_storage_aws_iam_role_arn: str
    AWS IAMロール。ビジネスプランでのS3プライベートストレージの認可で使います。 [S3プライベートストレージの認可の設定についてはこちら](/docs/faq/#m0b240)をご覧ください。 

"""

ProjectCopyRequest = Dict[str, Any]
"""


Kyes of Dict

* dest_project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* dest_title: str
    
* dest_overview: str
    
* copy_inputs: bool
    「入力データ」をコピーするかどうかを指定します。 
* copy_tasks: bool
    「タスク」をコピーするかどうかを指定します。  この属性の値を true とする場合、他の属性の値を必ず次のように指定してください。  * copy_inputs の値を true とする 
* copy_annotations: bool
    「アノテーション」をコピーするかどうかを指定します。  この属性の値を true とする場合、他の属性の値を必ず次のように指定してください。  * copy_inputs の値を true とする * copy_tasks の値を true とする 
* copy_webhooks: bool
    「Webhook」をコピーするかどうかを指定します。 
* copy_tasks_with_annotations: bool
    「タスク」および「アノテーション」をコピーするかどうかを指定します。  廃止予定の属性のためこの属性は使用せず、「タスク」および「アノテーション」をコピーする場合には他の属性の値を必ず次のように指定してください。  * copy_tasks の値を true とする * copy_inputs の値を true とする * copy_annotations の値を true とする  やむを得ない理由でこの属性の値を true とする場合、他の属性の値を必ず次のように指定してください。  * copy_tasks の値を false とする * copy_inputs の値を true とする * copy_annotations の値を false とする 
* copy_supplementaly_data: bool
    「補助情報」をコピーするかどうかを指定します。  この属性の値を true とする場合、他の属性の値を必ず次のように指定してください。  * copy_inputs の値を true とする 
* copy_instructions: bool
    「作業ガイド」をコピーするかどうかを指定します。 

"""

ProjectMember = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* account_id: str
    
* user_id: str
    
* username: str
    
* member_status: ProjectMemberStatus
    
* member_role: ProjectMemberRole
    
* biography: str
    人物紹介、略歴。  この属性は、AnnoFab外の所属先や肩書などを表すために用います。 AnnoFab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 
* updated_datetime: str
    
* created_datetime: str
    
* sampling_inspection_rate: int
    メンバー固有の抜取検査率（0-100のパーセント値）。
* sampling_acceptance_rate: int
    メンバー固有の抜取受入率（0-100のパーセント値）。

"""

ProjectMemberRequest = Dict[str, Any]
"""


Kyes of Dict

* member_status: ProjectMemberStatus
    
* member_role: ProjectMemberRole
    
* sampling_inspection_rate: int
    メンバー固有の抜取検査率。0-100のパーセント値で指定する。値が指定された場合、プロジェクトの抜取検査率を指定の値で上書きする。
* sampling_acceptance_rate: int
    メンバー固有の抜取受入率。0-100のパーセント値で指定する。値が指定された場合、プロジェクトの抜取受入率を指定の値で上書きする。
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

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
    * `active` - プロジェクトメンバーとして有効で、プロジェクトを閲覧したり、権限があれば編集できます。 * `inactive` - 脱退したプロジェクトメンバーを表します。プロジェクトを閲覧できません。 
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

* last_tasks_updated_datetime: str
    

"""

ProjectTaskCounts = Dict[str, Any]
"""


Kyes of Dict

* task_counts: List[ProjectTaskCountsTaskCounts]
    

"""

ProjectTaskCountsTaskCounts = Dict[str, Any]
"""


Kyes of Dict

* phase: TaskPhase
    
* status: TaskStatus
    
* count: float
    該当するタスクの数

"""

ProjectTaskStatistics = Dict[str, Any]
"""


Kyes of Dict

* phase: TaskPhase
    
* status: TaskStatus
    
* count: int
    タスク数
* work_timespan: int
    累計実作業時間(ミリ秒)

"""

ProjectTaskStatisticsHistory = Dict[str, Any]
"""


Kyes of Dict

* date: str
    
* tasks: List[ProjectTaskStatistics]
    

"""

PutMarkersRequest = Dict[str, Any]
"""


Kyes of Dict

* markers: List[Marker]
    
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutMyAccountRequest = Dict[str, Any]
"""


Kyes of Dict

* user_id: str
    
* username: str
    
* lang: str
    
* keylayout: str
    
* biography: str
    人物紹介、略歴。  この属性は、AnnoFab外の所属先や肩書などを表すために用います。 AnnoFab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 
* token: Token
    
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutOrganizationMemberRoleRequest = Dict[str, Any]
"""


Kyes of Dict

* role: OrganizationMemberRole
    
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutOrganizationNameRequest = Dict[str, Any]
"""


Kyes of Dict

* organization_id: str
    
* organization_name: str
    組織名。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* last_updated_datetime: str
    

"""

PutProjectRequest = Dict[str, Any]
"""


Kyes of Dict

* title: str
    
* overview: str
    
* status: ProjectStatus
    
* input_data_type: InputDataType
    
* organization_name: str
    プロジェクトの所属組織を変更する場合は、ここに変更先の組織名を指定します。  * 所属組織を変更する前にプロジェクトを停止する必要があります。 * APIを呼び出すアカウントは、変更先組織の管理者またはオーナーである必要があります。 * 変更後の組織に所属していないプロジェクトメンバーも残りますが、作業はできません。あらためて組織に招待してください。 
* configuration: ProjectConfiguration
    
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 
* force_suspend: bool
    作業中タスクがあるプロジェクトを停止する時trueにして下さい

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

Resolution = Dict[str, Any]
"""


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
    アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、AnnoFabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 
* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_phase: TaskPhase
    
* task_phase_stage: int
    
* task_status: TaskStatus
    
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_name: str
    
* details: List[SimpleAnnotationDetail]
    
* updated_datetime: str
    

"""

SimpleAnnotationDetail = Dict[str, Any]
"""


Kyes of Dict

* label: str
    アノテーション仕様のラベル名です。 
* annotation_id: str
    個々のアノテーションにつけられたIDです。 
* data: FullAnnotationData
    
* attributes: __DictStrKeyAnyValue__
    キーに属性の名前、値に各属性の値が入った辞書構造です。 

"""

SingleAnnotation = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* detail: SingleAnnotationDetail
    
* updated_datetime: str
    

"""

SingleAnnotationDetail = Dict[str, Any]
"""


Kyes of Dict

* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 
* account_id: str
    
* label_id: str
    
* data_holding_type: AnnotationDataHoldingType
    
* data: FullAnnotationData
    
* etag: str
    data_holding_typeがouterの場合のみ存在し、データのETagが格納される
* url: str
    data_holding_typeがouterの場合のみ存在し、データへの一時URLが格納される
* additional_data_list: List[AdditionalData]
    
* created_datetime: str
    
* updated_datetime: str
    

"""

SupplementaryData = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* supplementary_data_id: str
    
* supplementary_data_name: str
    表示用の名前
* supplementary_data_path: str
    補助情報の実体が保存されたパスです。 s3スキーマまたはhttpsスキーマのみサポートしています。 
* url: str
    このフィールドはAF内部での利用のみを想定しており、依存しないでください。
* etag: str
    
* supplementary_data_type: SupplementaryDataType
    
* supplementary_data_number: int
    表示順を表す数値（昇順）。同じ入力データに対して複数の補助情報で表示順が重複する場合、順序不定になります。
* updated_datetime: str
    

"""

SupplementaryDataRequest = Dict[str, Any]
"""


Kyes of Dict

* supplementary_data_name: str
    表示用の名前
* supplementary_data_path: str
    AnnoFabに登録する補助情報の実体が保存されたパスです。  対応スキーマ：s3, https  * [一時データ保存先取得API](#operation/createTempPath)を使ってAFにアップロードしたファイルパスの場合     * `s3://ANNOFAB-BUCKET/PATH/TO/INPUT_DATA`     * 補助情報作成/更新API成功時、アップロードしたファイルが一時データ保存先からコピーされます。         * APIのレスポンスからアップロードしたファイルのコピー先パス（s3スキーマ）を取得できます。 * すでにAFに登録されている補助情報のパスの場合     * `s3://ANNOFAB-SUPPLEMENTARY-BUCKET/PATH/TO/INPUT_DATA`     * ファイルはコピーされません。 * [プライベートストレージ](/docs/faq/#prst9c)のパスの場合     * `https://YOUR-DOMAIN/PATH/TO/INPUT_DATA`     * `s3://YOUR-BUCKET-FOR-PRIVATE-STORAGE/PATH/TO/INPUT_DATA`         * S3プライベートストレージのパスを登録する場合、[事前に認可の設定が必要](/docs/faq/#m0b240)です。     * AFにファイルはコピーされません。 
* supplementary_data_type: SupplementaryDataType
    
* supplementary_data_number: int
    表示順を表す数値（昇順）。同じ入力データに対して複数の補助情報で表示順が重複する場合、順序不定になります。
* last_updated_datetime: str
    

"""


class SupplementaryDataType(Enum):
    """
    """

    IMAGE = "image"
    TEXT = "text"


Task = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* phase: TaskPhase
    
* phase_stage: int
    
* status: TaskStatus
    
* input_data_id_list: List[str]
    
* account_id: str
    
* histories_by_phase: List[TaskHistoryShort]
    
* work_time_span: int
    累計実作業時間(ミリ秒)
* number_of_rejections: int
    このタスクが差戻しされた回数（すべてのフェーズでの差戻し回数の合計  このフィールドは、どのフェーズで何回差戻されたかを区別できないため、廃止予定です。 `histories_by_phase` で各フェーズの回数を計算することで、差戻し回数が分かります。  例）`acceptance`フェーズが3回ある場合、`acceptance`フェーズで2回差し戻しされたことになります。 
* started_datetime: str
    
* updated_datetime: str
    
* sampling: str
    * `inspection_skipped` - このタスクが抜取検査の対象外となり、検査フェーズをスキップしたことを表す。 * `inspection_stages_skipped` - このタスクが抜取検査の対象外となり、検査フェーズのステージを一部スキップしたことを表す。 * `acceptance_skipped` - このタスクが抜取検査の対象外となり、受入フェーズをスキップしたことを表す。 * `inspection_and_acceptance_skipped` - このタスクが抜取検査の対象外となり、検査・受入フェーズをスキップしたことを表す  未指定時はこのタスクが抜取検査の対象となったことを表す。(通常のワークフローを通過する) 

"""

TaskGenerateRequest = Dict[str, Any]
"""


Kyes of Dict

* task_generate_rule: OneOfTaskGenerateRuleByCountTaskGenerateRuleByDirectoryTaskGenerateRuleByInputDataCsv
    * `TaskGenerateRuleByCount`: 1つのタスクに割りあてる入力データの個数を指定してタスクを生成します。 * `TaskGenerateRuleByDirectory`: 入力データ名をファイルパスに見立て、ディレクトリ単位でタスクを生成します。 * `TaskGenerateRuleByInputDataCsv`: 各タスクへの入力データへの割当を記入したCSVへのS3上のパスを指定してタスクを生成します。 
* project_last_updated_datetime: str
    プロジェクトの最終更新日時。タスク生成の排他制御に使用。

"""

TaskGenerateRuleByCount = Dict[str, Any]
"""
1つのタスクに割りあてる入力データの個数を指定してタスクを生成します。

Kyes of Dict

* task_id_prefix: str
    生成するタスクIDのプレフィックス。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* allow_duplicate_input_data: bool
    falseのときは、既にタスクに使われている入力データを除外し、まだタスクに使われていない入力データだけを新しいタスクに割り当てます。trueのときは、既にタスクに使われている入力データを除外しません。
* input_data_count: int
    1つのタスクに割り当てる入力データの個数
* input_data_order: InputDataOrder
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

TaskGenerateRuleByDirectory = Dict[str, Any]
"""
入力データ名をファイルパスに見立て、ディレクトリ単位でタスクを生成します。<br>

Kyes of Dict

* task_id_prefix: str
    生成するタスクIDのプレフィックス。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_name_prefix: str
    タスク生成対象の入力データ名プレフィックス
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

TaskGenerateRuleByInputDataCsv = Dict[str, Any]
"""
各タスクへの入力データへの割当を記入したCSVへのS3上のパスを指定してタスクを生成します。

Kyes of Dict

* csv_data_path: str
    各タスクへの入力データへの割当を記入したCSVへのS3上のパス
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

TaskHistory = Dict[str, Any]
"""
タスクのあるフェーズで、誰がいつどれくらいの作業時間を費やしたかを表すタスク履歴です。

Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_history_id: str
    
* started_datetime: str
    
* ended_datetime: str
    
* accumulated_labor_time_milliseconds: str
    累計実作業時間（ISO 8601 duration）
* phase: TaskPhase
    
* phase_stage: int
    
* account_id: str
    

"""

TaskHistoryEvent = Dict[str, Any]
"""
タスク履歴イベントは、タスクの状態が変化した１時点を表します。作業時間は、複数のこれらイベントを集約して計算するものなので、このオブジェクトには含まれません。

Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_history_id: str
    
* created_datetime: str
    
* phase: TaskPhase
    
* phase_stage: int
    
* status: TaskStatus
    
* account_id: str
    

"""

TaskHistoryShort = Dict[str, Any]
"""
タスクのあるフェーズを誰が担当したかを表します。

Kyes of Dict

* phase: TaskPhase
    
* phase_stage: int
    
* account_id: str
    

"""

TaskOperation = Dict[str, Any]
"""


Kyes of Dict

* status: TaskStatus
    
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 
* account_id: str
    

"""


class TaskPhase(Enum):
    """
    * `annotation` - 教師付け。 * `inspection` - 中間検査。ワークフローが3フェーズのときのみ。 * `acceptance` - 受入。 
    """

    ANNOTATION = "annotation"
    INSPECTION = "inspection"
    ACCEPTANCE = "acceptance"


TaskPhaseStatistics = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* date: str
    
* phases: List[PhaseStatistics]
    タスクのフェーズごとの集計結果

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
    * `not_started` - 未着手。 * `working` - 作業中。誰かが実際にエディタ上で作業している状態。 * `on_hold` - 保留。作業ルールの確認などで作業できない状態。 * `break` - 休憩中。 * `complete` - 完了。次のフェーズへ進む * `rejected` - 差戻し。修正のため、`annotation`フェーズへ戻る。 * `cancelled` - 提出取消し。修正のため、前フェーズへ戻る。 
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
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* inputs: List[InputDataSummary]
    

"""

Token = Dict[str, Any]
"""


Kyes of Dict

* id_token: str
    形式は[JWT](https://jwt.io/)。
* access_token: str
    形式は[JWT](https://jwt.io/)。
* refresh_token: str
    形式は[JWT](https://jwt.io/)。

"""

UnknownAdditionalData = Dict[str, Any]
"""
何らかの原因で、アノテーション仕様にない属性がついているエラー

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    UnknownAdditionalData

"""

UnknownLabel = Dict[str, Any]
"""
何らかの原因で、アノテーション仕様にないラベルがついているエラー

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* type: str
    UnknownLabel

"""

UnknownLinkTarget = Dict[str, Any]
"""
指定されたIDに該当するアノテーションが存在しないエラー

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    UnknownLinkTarget

"""

ValidationError = Dict[str, Any]
"""


Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* message: str
    
* type: str
    UnknownLabel
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
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* event_type: WebhookEventType
    
* webhook_id: str
    WebhookID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* webhook_status: WebhookStatus
    
* method: WebhookHttpMethod
    
* headers: List[WebhookHeader]
    
* body: str
    
* url: str
    
* created_datetime: str
    
* updated_datetime: str
    

"""


class WebhookEventType(Enum):
    """
    * `task-completed` - タスク受入完了 * `annotation-archive-updated` - アノテーションZIP作成完了 * `input-data-zip-registered` - 入力データZIP登録完了 * `project-copy-completed` - プロジェクトコピー完了 
    """

    TASK_COMPLETED = "task-completed"
    ANNOTATION_ARCHIVE_UPDATED = "annotation-archive-updated"
    INPUT_DATA_ZIP_REGISTERED = "input-data-zip-registered"
    PROJECT_COPY_COMPLETED = "project-copy-completed"


WebhookHeader = Dict[str, Any]
"""


Kyes of Dict

* name: str
    
* value: str
    

"""


class WebhookHttpMethod(Enum):
    """
    """

    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    GET = "GET"
    HEAD = "HEAD"


class WebhookStatus(Enum):
    """
    """

    ACTIVE = "active"
    INACTIVE = "inactive"


WebhookTestRequest = Dict[str, Any]
"""


Kyes of Dict

* placeholders: __DictStrKeyAnyValue__
    プレースホルダ名と置換する値

"""

WebhookTestResponse = Dict[str, Any]
"""


Kyes of Dict

* result: str
    * success: 通知先から正常なレスポンス（2xx系）を受け取った * failure: 通知先からエラーレスポンス（2xx系以外）を受け取った * error: リクエスト送信に失敗した、もしくはレスポンスを受信できなかった 
* request_body: str
    実際に送信されたリクエストボディ
* response_status: int
    通知先から返されたHTTPステータスコード
* response_body: str
    通知先から返されたレスポンスボディ
* message: str
    result=\"error\" 時のエラー内容等

"""

WorktimeStatistics = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* date: str
    
* by_tasks: List[WorktimeStatisticsItem]
    タスク1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）
* by_inputs: List[WorktimeStatisticsItem]
    画像1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）
* by_minutes: List[WorktimeStatisticsItem]
    動画1分当たりの作業時間情報（画像プロジェクトの場合は空リスト）
* accounts: List[AccountWorktimeStatistics]
    ユーザごとの作業時間情報

"""

WorktimeStatisticsItem = Dict[str, Any]
"""


Kyes of Dict

* phase: TaskPhase
    
* histogram: List[HistogramItem]
    
* average: str
    作業時間の平均（ISO 8601 duration）
* standard_deviation: str
    作業時間の標準偏差（ISO 8601 duration）

"""
