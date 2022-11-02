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

from annofabapi._utils import deprecated_class  # pylint: disable=unused-import

### 手動の部分

AccountId = NewType("AccountId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``
    
"""

UserId = NewType("UserId", str)
"""

Example:
    ``john_doe``

"""

OrganizationId = NewType("OrganizationId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

ProjectId = NewType("ProjectId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

LabelId = NewType("LabelId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

AdditionalDataDefinitionId = NewType("AdditionalDataDefinitionId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

ChoiceId = NewType("ChoiceId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

PhraseId = NewType("PhraseId", str)
"""

Example:
    ``my_phrase_id``

"""

TaskId = NewType("TaskId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

InputDataId = NewType("InputDataId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

SupplementaryDataId = NewType("SupplementaryDataId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

TaskHistoryId = NewType("TaskHistoryId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

AnnotationId = NewType("AnnotationId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

InspectionId = NewType("InspectionId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

MakerId = NewType("MakerId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

JobId = NewType("JobId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

WebhookId = NewType("WebhookId", str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

Duration = NewType("Duration", str)
"""

Example:
    ``PT34H17M36.789S``

"""

### 以下は自動生成の部分
AcceptOrganizationInvitationRequest = Dict[str, Any]
"""


Kyes of Dict

* token: str
    [inviteOrganizationMember](#operation/inviteOrganizationMember) APIで送信された招待メールに記載されているトークンです。 メールに記載されているURLの`invitation-token`クエリパラメータの値が、トークンになります。 

"""

Account = Dict[str, Any]
"""


Kyes of Dict

* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* username: str
    ユーザー名
* email: str
    メールアドレス
* lang: Lang
    
* biography: str
    人物紹介、略歴。  この属性は、Annofab外の所属先や肩書などを表すために用います。 Annofab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 
* keylayout: KeyLayout
    
* authority: str
    システム内部用のプロパティ
* account_type: str
    アカウントの種別 * `annofab` - 通常の手順で登録されたアカウント。後から[外部アカウントとの紐付け](/docs/faq/#yyyub0)をしたアカウントの場合もこちらになります。 * `external` - [外部アカウントだけで作成したアカウント](/docs/faq/#v1u344) * `project_guest` - [issueProjectGuestUserToken](#operation/issueProjectGuestUserToken)によって作成されたされたアカウント 
* updated_datetime: str
    更新日時

"""

AccountWorktimeStatistics = Dict[str, Any]
"""


Kyes of Dict

* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* by_tasks: List[WorktimeStatisticsItem]
    タスクごとに計算した「画像1枚あたりの作業時間平均」の統計（動画プロジェクトの場合は空リスト）
* by_inputs: List[WorktimeStatisticsItem]
    画像1枚あたりの作業時間情報（動画プロジェクトの場合は空リスト）
* by_minutes: List[WorktimeStatisticsItem]
    動画1分あたりの作業時間情報（画像プロジェクトの場合は空リスト）

"""

ActionRequired = Dict[str, Any]
"""
対応が必要な検査コメントが残っている時のエラー

Kyes of Dict

* inspection: Inspection
    
* type: str
    ActionRequired

"""

AdditionalDataDefaultType = Dict[str, Any]
"""
属性の初期値です。  初期値を設定する場合、属性の種類に応じて次の値を指定してください。 属性の種類に対して有効でない初期値を指定した場合、その初期値は無視されます。  |属性の種類（`type`）                 | 指定できる初期値| |-----------------|----------| | flag    | 真偽値(`true` or `false`)| | integer    | 整数値         | | text | 文字列         | | comment         | 文字列| | choice        | 選択肢(`choices`)の `choice_id` | | select           | 選択肢(`choices`)の`choice_id`|  属性の種類が`tracking`または`link`の場合、初期値を設定できません。  初期値を設定しない場合は、nullまたは空文字を指定してください。 

Kyes of Dict


"""


class AdditionalDataDefinitionType(Enum):
    """
    属性の種類 * `flag` - 真偽値 * `integer` - 整数値 * `text` - 自由記述（1行） * `comment` - 自由記述（複数行） * `choice` - 選択肢（ラジオボタン式） * `select` - 選択肢（ドロップダウン式） * `tracking` - トラッキングID * `link` - アノテーションリンク
    """

    FLAG = "flag"
    INTEGER = "integer"
    TEXT = "text"
    COMMENT = "comment"
    CHOICE = "choice"
    SELECT = "select"
    TRACKING = "tracking"
    LINK = "link"


AdditionalDataDefinitionV1 = Dict[str, Any]
"""


Kyes of Dict

* additional_data_definition_id: str
    属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* read_only: bool
    読み込み専用
* name: InternationalizationMessage
    
* default: AdditionalDataDefaultType
    
* keybind: List[Keybind]
    ショートカットキー
* type: AdditionalDataDefinitionType
    
* choices: List[AdditionalDataDefinitionV1Choices]
    ドロップダウンまたはラジオボタンの選択肢
* regex: str
    属性の値が、指定した正規表現に一致している必要があります。
* label_ids: List[str]
    リンク属性において、リンク先として指定可能なラベルID（空の場合制限なし）
* required: bool
    リンク属性において、入力を必須とするかどうか
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AdditionalDataDefinitionV1Choices = Dict[str, Any]
"""


Kyes of Dict

* choice_id: str
    選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* name: InternationalizationMessage
    
* keybind: List[Keybind]
    ショートカットキー

"""

AdditionalDataDefinitionV2 = Dict[str, Any]
"""


Kyes of Dict

* additional_data_definition_id: str
    属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* read_only: bool
    読み込み専用
* name: InternationalizationMessage
    
* default: AdditionalDataDefaultType
    
* keybind: List[Keybind]
    ショートカットキー
* type: AdditionalDataDefinitionType
    
* choices: List[AdditionalDataDefinitionV1Choices]
    ドロップダウンまたはラジオボタンの選択肢
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AdditionalDataRestriction = Dict[str, Any]
"""


Kyes of Dict

* additional_data_definition_id: str
    属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* condition: AdditionalDataRestrictionCondition
    

"""

AdditionalDataRestrictionCondition = Dict[str, Any]
"""
属性の制約    * `AdditionalDataRestrictionConditionCanInput`: 属性値の入力を許可するかどうか   * `AdditionalDataRestrictionConditionEquals`: 指定した値に等しい   * `AdditionalDataRestrictionConditionNotEquals`: 指定した値に等しくない   * `AdditionalDataRestrictionConditionMatches`: 指定した正規表現に一致する   * `AdditionalDataRestrictionConditionNotMatches`: 指定した正規表現に一致しない   * `AdditionalDataRestrictionConditionHasLabel`: 指定したラベルIDに一致する（アノテーションリンク属性限定）   * `AdditionalDataRestrictionConditionImply`: 指定した前提条件を満たすときのみ、制約を満たすかどうか  以下のJSONは、「属性IDが`attr2`の属性値が`true`ならば、属性IDが`attr1`の属性値は`choice1`である」という制約を表しています。  ``` {     \"additional_data_definition_id\": \"attr1\",     \"condition\": {         \"_type\": \"Imply\",         \"premise\": {             \"additional_data_definition_id\": \"attr2\",             \"condition\": {                 \"_type\": \"Equals\",                 \"value\": \"true\"             }         },         \"condition\": {             \"_type\": \"Equals\",             \"value\": \"choice1\"         }     } } ``` 

Kyes of Dict

* type: str
    `Imply` [詳しくはこちら](#section/API-Convention/API-_type) 
* enable: bool
    `false`を指定することで、属性値の入力を許可しないようにできます。 `AdditionalDataRestrictionConditionImply`との組み合わせで、特定条件下のみ入力を許すといった制限ができます。 
* value: str
    指定された正規表現に一致しないことを要求します。
* labels: List[str]
    アノテーションリンク属性において、アノテーションリンク先として指定可能なラベルIDを制限します。
* premise: AdditionalDataRestriction
    
* condition: AdditionalDataRestrictionCondition
    

"""

AdditionalDataRestrictionConditionCanInput = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `CanInput` [詳しくはこちら](#section/API-Convention/API-_type) 
* enable: bool
    `false`を指定することで、属性値の入力を許可しないようにできます。 `AdditionalDataRestrictionConditionImply`との組み合わせで、特定条件下のみ入力を許すといった制限ができます。 

"""

AdditionalDataRestrictionConditionEquals = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `Equals` [詳しくはこちら](#section/API-Convention/API-_type) 
* value: str
    指定された値と等しいことを要求します。

"""

AdditionalDataRestrictionConditionHasLabel = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `HasLabel` [詳しくはこちら](#section/API-Convention/API-_type) 
* labels: List[str]
    アノテーションリンク属性において、アノテーションリンク先として指定可能なラベルIDを制限します。

"""

AdditionalDataRestrictionConditionImply = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `Imply` [詳しくはこちら](#section/API-Convention/API-_type) 
* premise: AdditionalDataRestriction
    
* condition: AdditionalDataRestrictionCondition
    

"""

AdditionalDataRestrictionConditionMatches = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `Matches` [詳しくはこちら](#section/API-Convention/API-_type) 
* value: str
    指定された正規表現に一致することを要求します。

"""

AdditionalDataRestrictionConditionNotEquals = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `NotEquals` [詳しくはこちら](#section/API-Convention/API-_type) 
* value: str
    指定された値と異なることを要求します。 `value`に`\"\"`を指定することで、入力を必須とすることができます。 

"""

AdditionalDataRestrictionConditionNotMatches = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `NotMatches` [詳しくはこちら](#section/API-Convention/API-_type) 
* value: str
    指定された正規表現に一致しないことを要求します。

"""

AdditionalDataV1 = Dict[str, Any]
"""


Kyes of Dict

* additional_data_definition_id: str
    属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* flag: bool
    `additional_data_definition`の`type`が`flag`のときの属性値。 
* integer: int
    `additional_data_definition`の`type`が`integer`のときの属性値。 
* comment: str
    `additional_data_definition`の`type`が`text`,`comment`,`link` または `tracking`のときの属性値。 
* choice: str
    選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 

"""

AdditionalDataV2 = Dict[str, Any]
"""


Kyes of Dict

* definition_id: str
    属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* value: AdditionalDataValue
    

"""

AdditionalDataValue = Dict[str, Any]
"""
属性値 

Kyes of Dict

* type: str
    
* value: str
    トラッキングID属性の属性値
* choice_id: str
    選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 

"""

AdditionalDataValueChoice = Dict[str, Any]
"""


Kyes of Dict

* type: str
    
* choice_id: str
    選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 

"""

AdditionalDataValueComment = Dict[str, Any]
"""


Kyes of Dict

* type: str
    
* value: str
    自由記述（1行）の属性値

"""

AdditionalDataValueFlag = Dict[str, Any]
"""


Kyes of Dict

* type: str
    
* value: bool
    ON/OFF属性の属性値。 ONの時trueとなります

"""

AdditionalDataValueInteger = Dict[str, Any]
"""


Kyes of Dict

* type: str
    
* value: int
    整数属性の属性値

"""

AdditionalDataValueLink = Dict[str, Any]
"""


Kyes of Dict

* type: str
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 

"""

AdditionalDataValueSelect = Dict[str, Any]
"""


Kyes of Dict

* type: str
    
* choice_id: str
    選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 

"""

AdditionalDataValueText = Dict[str, Any]
"""


Kyes of Dict

* type: str
    
* value: str
    自由記述（複数行）の属性値

"""

AdditionalDataValueTracking = Dict[str, Any]
"""


Kyes of Dict

* type: str
    
* value: str
    トラッキングID属性の属性値

"""

AggregationResult = Dict[str, Any]
"""


Kyes of Dict


"""


class AnnotationDataHoldingType(Enum):
    """
    アノテーションのデータがどこに保持されるか * `inner` - アノテーションのデータ部をJSON内部に保持します。 * `outer` - アノテーションのデータ部を外部ファイルの形式（画像など）で保持します
    """

    INNER = "inner"
    OUTER = "outer"


AnnotationDataV1 = Dict[str, Any]
"""
アノテーションの座標値や区間などのデータ。  APIのレスポンスから参照される場合は、`FullAnnotationDataString`形式です。 [putAnnotation](#operation/putAnnotation) APIのリクエストボディは、`FullAnnotationDataString`形式または`FullAnnotationData`形式に対応しています。 

Kyes of Dict


"""

AnnotationDetailContentInput = Dict[str, Any]
"""
- **AnnotationDetailContentInputInner**   - アノテーションのデータ部をJSON内部に保持する場合、この型を利用します - **AnnotationDetailContentInputOuter**   - アノテーションのデータ部を外部ファイルの形式（画像など）で保持する場合、この型を利用します 

Kyes of Dict

* type: str
    
* data: FullAnnotationData
    
* path: str
    外部ファイルの位置を示す文字列。 [createTempPath](#operation/createTempPath) APIによって取得したpathを指定します。

"""

AnnotationDetailContentInputInner = Dict[str, Any]
"""
アノテーションのデータ部をJSON内部に保持します

Kyes of Dict

* type: str
    
* data: FullAnnotationData
    

"""

AnnotationDetailContentInputOuter = Dict[str, Any]
"""
アノテーションのデータ部を外部ファイルの形式（画像など）で保持します

Kyes of Dict

* type: str
    
* path: str
    外部ファイルの位置を示す文字列。 [createTempPath](#operation/createTempPath) APIによって取得したpathを指定します。

"""

AnnotationDetailContentOutput = Dict[str, Any]
"""
- **AnnotationDetailContentOutputInner**   - アノテーションのデータ部をJSON内部に保持している場合、通常はこの型の値となります - **AnnotationDetailContentOutputInnerUnknown**   - アノテーションのデータ部をJSON内部に保持しており、且つ、AnnotationDetailV1の形式で保存されていたデータのAnnotationTypeが特定できない場合にこの値となります   - 典型的な例では、アノテーションの保存後にアノテーション仕様が書き換わっていた場合が該当します - **AnnotationDetailContentOutputOuter**   - アノテーションのデータ部を外部ファイルの形式（画像など）で保持している場合、通常はこの型の値となります - **AnnotationDetailContentOutputOuterUnresolved**   - アノテーションのデータ部を外部ファイルの形式（画像など）で保持しており、且つ、Outerのurl / etagを解決しなかった場合（過去のアノテーションを取得した場合等）にこの値となります 

Kyes of Dict

* type: str
    
* data: str
    アノテーション座標値や区間などの文字列表現です。 アノテーション種類（`annotation_type`）とデータ格納形式（`data_holding_type`）に応じて、以下のとおり表現が変わります。  <table> <tr><th>annotation_type</th><th>data_holding_type</th><th>文字列表現</th></tr> <tr><td>bounding_box</td><td>inner</td><td><code>\"左上x,左上y,右下x,右下y\"</code></td></tr> <tr><td>point</td><td>inner</td><td><code>\"x1,y1\"</code></td></tr> <tr><td>polygon / polyline</td><td>inner</td><td><code>\"x1,y1,x2,y2, ... \"</code></td></tr> <tr><td>range </td><td>inner</td><td><code>\"開始時間(ミリ秒),終了時間(ミリ秒) \"</code></td></tr> <tr><td>classification</td><td>inner</td><td><code>null</code></td></tr> <tr><td>segmentation</td><td>outer</td><td><code>null</code></td></tr> <tr><td>segmentation_v2</td><td>outer</td><td><code>null</code></td></tr> </table> 
* url: str
    外部ファイルに保存されたアノテーションの認証済み一時URL
* etag: str
    外部ファイルに保存されたアノテーションのETag

"""

AnnotationDetailContentOutputInner = Dict[str, Any]
"""
アノテーションのデータ部をJSON内部に保持します

Kyes of Dict

* type: str
    
* data: FullAnnotationData
    

"""

AnnotationDetailContentOutputInnerUnknown = Dict[str, Any]
"""
アノテーションのデータ部をJSON内部に保持します。 AnnotationDetailV1の形式で保存されていたデータのAnnotationTypeが特定できない場合にこの値となります。 典型的な例では、アノテーションの保存後にアノテーション仕様が書き換わっていた場合が該当します。 

Kyes of Dict

* type: str
    
* data: str
    アノテーション座標値や区間などの文字列表現です。 アノテーション種類（`annotation_type`）とデータ格納形式（`data_holding_type`）に応じて、以下のとおり表現が変わります。  <table> <tr><th>annotation_type</th><th>data_holding_type</th><th>文字列表現</th></tr> <tr><td>bounding_box</td><td>inner</td><td><code>\"左上x,左上y,右下x,右下y\"</code></td></tr> <tr><td>point</td><td>inner</td><td><code>\"x1,y1\"</code></td></tr> <tr><td>polygon / polyline</td><td>inner</td><td><code>\"x1,y1,x2,y2, ... \"</code></td></tr> <tr><td>range </td><td>inner</td><td><code>\"開始時間(ミリ秒),終了時間(ミリ秒) \"</code></td></tr> <tr><td>classification</td><td>inner</td><td><code>null</code></td></tr> <tr><td>segmentation</td><td>outer</td><td><code>null</code></td></tr> <tr><td>segmentation_v2</td><td>outer</td><td><code>null</code></td></tr> </table> 

"""

AnnotationDetailContentOutputOuter = Dict[str, Any]
"""
アノテーションのデータ部を外部ファイルの形式（画像など）で保持します

Kyes of Dict

* type: str
    
* url: str
    外部ファイルに保存されたアノテーションの認証済み一時URL
* etag: str
    外部ファイルに保存されたアノテーションのETag

"""

AnnotationDetailContentOutputOuterUnresolved = Dict[str, Any]
"""
アノテーションのデータ部を外部ファイルの形式（画像など）で保持します。 Outerのurl / etagを解決しなかった場合（過去のアノテーションを取得した場合等）にこの値となります。 

Kyes of Dict

* type: str
    

"""

AnnotationDetailV1 = Dict[str, Any]
"""


Kyes of Dict

* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* is_protected: bool
    `true`の場合、アノテーションをアノテーションエディタ上での削除から保護できます。 外部から取り込んだアノテーションに属性を追加するときなどに指定すると、データの削除を防げます。 
* data_holding_type: AnnotationDataHoldingType
    
* data: AnnotationDataV1
    
* path: str
    外部ファイルに保存されたアノテーションのパス。`data_holding_type`が`inner`の場合は未指定です。 レスポンスの場合は`annotation_id`と同じ値が格納されます。  [putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は、[createTempPath](#operation/createTempPath) APIで取得できる一時データ保存先S3パスを格納してください。 更新しない場合は、[getEditorAnnotation](#operation/getEditorAnnotation) APIで取得した`path`をそのまま渡せます。  外部ファイルのフォーマットは下表の通りです。  <table> <tr><th>annotation_type</th><th>形式</th></tr> <tr><td>segmentation / segmentation_v2   </td><td>PNG画像。塗りつぶした部分は<code>rgba(255, 255, 255, 1) </code>、塗りつぶしていない部分は<code>rgba(0, 0, 0, 0) </code>。</td></tr> </table> 
* etag: str
    外部ファイルに保存されたアノテーションのETag。`data_holding_type`が`inner`の場合、または[putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は未指定です。
* url: str
    外部ファイルに保存されたアノテーションの認証済み一時URL。`data_holding_type`が`inner`の場合、または[putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は未指定です。
* additional_data_list: List[AdditionalDataV1]
    属性情報。  アノテーション属性の種類（`additional_data_definition`の`type`）によって、属性値を格納するプロパティは変わります。  | 属性の種類 | `additional_data_definition`の`type` | 属性値を格納するプロパティ                    | |------------|-------------------------|----------------------| | ON/OFF | flag       | flag                                          | | 整数 | integer    | integer                                       | | 自由記述（1行）| text       | comment                                       | | 自由記述（複数行）| comment    | comment                                       | | トラッキングID  | tracking | comment                                       | | アノテーションリンク    | link   | comment                                       | | 排他選択（ラジオボタン）  |choice   | choice                                        | | 排他選択（ドロップダウン） | select    | choice                                        | 
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

AnnotationDetailV2Create = Dict[str, Any]
"""
新規にアノテーションを作成する場合にこの型を利用します。

Kyes of Dict

* type: str
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* body: AnnotationDetailContentInput
    
* additional_data_list: List[AdditionalDataV2]
    
* editor_props: AnnotationPropsForEditor
    

"""

AnnotationDetailV2Get = Dict[str, Any]
"""


Kyes of Dict

* type: str
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* body: AnnotationDetailContentOutput
    
* additional_data_list: List[AdditionalDataV2]
    
* editor_props: AnnotationPropsForEditor
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

AnnotationDetailV2Import = Dict[str, Any]
"""
過去にAnnofab内外で作成したアノテーションをそのままインポートする場合にこの型を利用します。

Kyes of Dict

* type: str
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* body: AnnotationDetailContentInput
    
* additional_data_list: List[AdditionalDataV2]
    
* editor_props: AnnotationPropsForEditor
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

AnnotationDetailV2Input = Dict[str, Any]
"""
- **AnnotationDetailV2Create**   - 新規にアノテーションを作成する場合にこの型を利用します。 - **AnnotationDetailV2Import**   - 過去にAnnofab内外で作成したアノテーションをそのままインポートする場合にこの型を利用します。 - **AnnotationDetailV2Update**   - 既に存在するアノテーションを更新する場合にこの型を利用します 

Kyes of Dict

* type: str
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* body: AnnotationDetailContentInput
    
* additional_data_list: List[AdditionalDataV2]
    
* editor_props: AnnotationPropsForEditor
    
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

AnnotationDetailV2Output = Dict[str, Any]
"""


Kyes of Dict


"""

AnnotationDetailV2Update = Dict[str, Any]
"""
既に存在するアノテーションを更新する場合にこの型を利用します

Kyes of Dict

* type: str
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* body: AnnotationDetailContentInput
    
* additional_data_list: List[AdditionalDataV2]
    
* editor_props: AnnotationPropsForEditor
    

"""

AnnotationEditorFeature = Dict[str, Any]
"""
塗りつぶしの作図機能に関する情報 

Kyes of Dict

* append: bool
    塗りつぶしの「追記」機能が使えるか否か
* erase: bool
    塗りつぶしの「消しゴム」機能が使えるか否か
* freehand: bool
    塗りつぶしの「フリーハンド」機能が使えるか否か
* rectangle_fill: bool
    塗りつぶしの「矩形」機能が使えるか否か
* polygon_fill: bool
    塗りつぶしの「ポリゴン」機能が使えるか否か
* fill_near: bool
    「近似色塗りつぶし」機能を有効にするかどうか

"""

AnnotationInput = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: List[AnnotationDetailV2Input]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    対象タスク・対象入力データへの最初の保存時は未指定にしてください。 更新の場合はアノテーション取得時のupdated_datetimeをそのまま指定してください。 
* format_version: str
    

"""

AnnotationList = Dict[str, Any]
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
    [Aggregationによる集約結果](#section/API-Convention/AggregationResult)。 

"""

AnnotationOutput = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: List[AnnotationDetailV2Output]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    対象タスク・対象入力データへ一度もアノテーションの保存が行われていない場合、未指定となります。 そうで無い場合、対象タスク・対象入力データのアノテーション最終更新時刻です。 
* format_version: str
    

"""

AnnotationPropsForEditor = Dict[str, Any]
"""
アノテーションエディタ用のアノテーション毎のプロパティです。<br /> ここに含まれているデータはアノテーション結果に反映されず、エディタが利用するために存在します。  エディタ用のデータであるため、たとえば`can_delete`や`can_edit_data`が`false`でも、APIによる編集は妨げません。<br /> ここで定義されているデータを利用して動作を変えるかどうかは、エディタによって異なります。 

Kyes of Dict

* can_delete: bool
    アノテーションがエディタ上で削除できるかどうか。 trueの場合削除可能。
* can_edit_data: bool
    アノテーションの本体のデータを編集できるかどうか。 trueの場合編集可能。 2022/09現在、この値を利用しているエディタは存在しません。
* can_edit_additional: bool
    アノテーションの付加情報を編集できるかどうか。  trueの場合編集可能。 2022/09現在、この値を利用しているエディタは存在しません。
* description: str
    アノテーションについての人間可読な説明。 2022/09現在、この値を利用しているエディタは存在しません。
* tags: List[str]
    アノテーションに付与されている機械可読・人間可読なタグの列。  2022/09現在、この値を利用しているエディタは存在しません
* etc: __DictStrKeyAnyValue__
    上記以外の任意のJson構造

"""

AnnotationQuery = Dict[str, Any]
"""
アノテーションの絞り込み条件 

Kyes of Dict

* task_id: str
    タスクIDで絞り込みます。 
* exact_match_task_id: bool
    タスクIDの検索方法を指定します。 `true`の場合は完全一致検索、`false`の場合は部分一致検索です。 
* input_data_id: str
    入力データID絞り込みます。 
* exact_match_input_data_id: bool
    入力データIDの検索方法を指定します。 `true`の場合は完全一致検索、`false`の場合は部分一致検索です。 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* attributes: List[AdditionalDataV1]
    属性情報。  アノテーション属性の種類（`additional_data_definition`の`type`）によって、属性値を格納するプロパティは変わります。  | 属性の種類 | `additional_data_definition`の`type` | 属性値を格納するプロパティ                    | |------------|-------------------------|----------------------| | ON/OFF | flag       | flag                                          | | 整数 | integer    | integer                                       | | 自由記述（1行）| text       | comment                                       | | 自由記述（複数行）| comment    | comment                                       | | トラッキングID  | tracking | comment                                       | | アノテーションリンク    | link   | comment                                       | | 排他選択（ラジオボタン）  |choice   | choice                                        | | 排他選択（ドロップダウン） | select    | choice                                        | 
* updated_from: str
    開始日・終了日を含む区間[updated_from, updated_to]でアノテーションの更新日を絞り込むときに使用する、開始日（ISO 8601 拡張形式または基本形式）。  `updated_to` より後の日付が指定された場合、期間指定は開始日・終了日を含む区間[updated_to, updated_from]となる。未指定の場合、API実行日(JST)の日付が指定されたものとして扱われる。 
* updated_to: str
    開始日・終了日を含む区間[updated_from, updated_to]でアノテーションの更新日を絞り込むときに使用する、終了日（ISO 8601 拡張形式または基本形式）。  未指定の場合、API実行日(JST)の日付が指定されたものとして扱われる。 

"""

AnnotationSpecs = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* labels: List[LabelV3]
    ラベル
* inspection_phrases: List[InspectionPhrase]
    定型指摘
* updated_datetime: str
    更新日時 
* option: AnnotationSpecsOption
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 
* additionals: List[AdditionalDataDefinitionV2]
    属性
* restrictions: List[AdditionalDataRestriction]
    属性の制約
* format_version: str
    アノテーション仕様のフォーマットのバージョン
* annotation_type_version: str
    アノテーション種別のバージョン。  拡張仕様プラグインで定義した値が転写されます。プロジェクトに拡張仕様プラグインが設定されていない場合は未指定です。 

"""

AnnotationSpecsHistory = Dict[str, Any]
"""


Kyes of Dict

* history_id: str
    アノテーション仕様の履歴ID
* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* updated_datetime: str
    更新日時
* url: str
    アノテーション仕様が格納されたJSONのURL。URLにアクセスするには認証認可が必要です。
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* comment: str
    変更内容のコメント

"""

AnnotationSpecsMovieOption = Dict[str, Any]
"""


Kyes of Dict

* can_overwrap: bool
    動画プロジェクトのアノテーションに重複配置を許すか否か。 

"""

AnnotationSpecsOption = Dict[str, Any]
"""
アノテーション仕様のオプション設定。  現時点では動画プロジェクトでのみ利用・指定可能。動画以外のプロジェクトでは値なし。  動画プロジェクトで値が未指定の場合、AnnotationSpecsOption内の値はすべてデフォルト値が指定されたものとして扱われる。 

Kyes of Dict


"""

AnnotationSpecsRequest = Dict[str, Any]
"""


Kyes of Dict

* labels: List[LabelV3]
    ラベル
* inspection_phrases: List[InspectionPhrase]
    定型指摘
* comment: str
    変更内容のコメント
* auto_marking: bool
    trueが指定された場合、各統計グラフにマーカーを自動追加します。 マーカーのタイトルには `comment` に指定された文字列が設定されます。 `comment` が指定されていなかった場合は \"アノテーション仕様の変更\" という文字列が設定されます。 
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 
* option: AnnotationSpecsOption
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 
* additionals: List[AdditionalDataDefinitionV2]
    属性
* restrictions: List[AdditionalDataRestriction]
    属性の制約
* format_version: str
    アノテーション仕様のフォーマットのバージョン

"""

AnnotationSpecsRequestV1 = Dict[str, Any]
"""


Kyes of Dict

* labels: List[LabelV1]
    ラベル
* inspection_phrases: List[InspectionPhrase]
    定型指摘
* comment: str
    変更内容のコメント
* auto_marking: bool
    trueが指定された場合、各統計グラフにマーカーを自動追加します。 マーカーのタイトルには `comment` に指定された文字列が設定されます。 `comment` が指定されていなかった場合は \"アノテーション仕様の変更\" という文字列が設定されます。 
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 
* option: AnnotationSpecsOption
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AnnotationSpecsRequestV2 = Dict[str, Any]
"""


Kyes of Dict

* labels: List[LabelV2]
    ラベル
* additionals: List[AdditionalDataDefinitionV2]
    属性
* restrictions: List[AdditionalDataRestriction]
    属性の制約
* inspection_phrases: List[InspectionPhrase]
    定型指摘
* comment: str
    変更内容のコメント
* auto_marking: bool
    trueが指定された場合、各統計グラフにマーカーを自動追加します。 マーカーのタイトルには `comment` に指定された文字列が設定されます。 `comment` が指定されていなかった場合は \"アノテーション仕様の変更\" という文字列が設定されます。 
* format_version: str
    アノテーション仕様のフォーマットのバージョン
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 
* option: AnnotationSpecsOption
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AnnotationSpecsRequestV3 = Dict[str, Any]
"""


Kyes of Dict

* labels: List[LabelV3]
    ラベル
* additionals: List[AdditionalDataDefinitionV2]
    属性
* restrictions: List[AdditionalDataRestriction]
    属性の制約
* inspection_phrases: List[InspectionPhrase]
    定型指摘
* comment: str
    変更内容のコメント
* auto_marking: bool
    trueが指定された場合、各統計グラフにマーカーを自動追加します。 マーカーのタイトルには `comment` に指定された文字列が設定されます。 `comment` が指定されていなかった場合は \"アノテーション仕様の変更\" という文字列が設定されます。 
* format_version: str
    アノテーション仕様のフォーマットのバージョン
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 
* option: AnnotationSpecsOption
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AnnotationSpecsV1 = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* labels: List[LabelV1]
    ラベル
* inspection_phrases: List[InspectionPhrase]
    定型指摘
* updated_datetime: str
    更新日時 
* option: AnnotationSpecsOption
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AnnotationSpecsV2 = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* labels: List[LabelV2]
    ラベル
* additionals: List[AdditionalDataDefinitionV2]
    属性
* restrictions: List[AdditionalDataRestriction]
    属性の制約
* inspection_phrases: List[InspectionPhrase]
    定型指摘
* format_version: str
    アノテーション仕様のフォーマットのバージョン
* updated_datetime: str
    更新日時 
* option: AnnotationSpecsOption
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AnnotationSpecsV3 = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* labels: List[LabelV3]
    ラベル
* additionals: List[AdditionalDataDefinitionV2]
    属性
* restrictions: List[AdditionalDataRestriction]
    属性の制約
* inspection_phrases: List[InspectionPhrase]
    定型指摘
* annotation_type_version: str
    アノテーション種別のバージョン。  拡張仕様プラグインで定義した値が転写されます。プロジェクトに拡張仕様プラグインが設定されていない場合は未指定です。 
* format_version: str
    アノテーション仕様のフォーマットのバージョン
* updated_datetime: str
    更新日時 
* option: AnnotationSpecsOption
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AnnotationType = Dict[str, Any]
"""


Kyes of Dict


"""


class AnnotationTypeFieldMinWarnRule(Enum):
    """
    最小の幅(min_width)と最小の高さ(min_height)がどのような状態になったときにエラーとするかを指定します。  * `and` - min_width、min_heightの両方が最小値未満の場合にエラーとなります。 * `or` - min_width、min_heightのいずれかが最小値未満の場合にエラーとなります。
    """

    AND = "and"
    OR = "or"


AnnotationTypeFieldValue = Dict[str, Any]
"""
ユーザー定義アノテーション種別のフィールドに設定される値です。 アノテーション種別のフィールド定義と対応するフィールド値のみ登録を許可されます。 

Kyes of Dict

* type: str
    
* min_warn_rule: AnnotationTypeFieldMinWarnRule
    
* min_width: int
    
* min_height: int
    
* position_for_minimum_bounding_box_insertion: List[int]
    最小矩形の挿入位置を、要素が2の配列で指定します。 
* max_pixel: int
    
* min: int
    
* max: int
    
* min_area: int
    
* has_direction: bool
    
* append: bool
    
* erase: bool
    
* freehand: bool
    
* rectangle_fill: bool
    
* polygon_fill: bool
    
* fill_near: bool
    
* value: bool
    

"""

AnnotationTypeFieldValueAnnotationEditorFeature = Dict[str, Any]
"""
作図ツール・作図モード 

Kyes of Dict

* type: str
    
* append: bool
    
* erase: bool
    
* freehand: bool
    
* rectangle_fill: bool
    
* polygon_fill: bool
    
* fill_near: bool
    

"""

AnnotationTypeFieldValueDisplayLineDirection = Dict[str, Any]
"""
線の向き表示/非表示の設定 

Kyes of Dict

* type: str
    
* has_direction: bool
    

"""

AnnotationTypeFieldValueEmptyFieldValue = Dict[str, Any]
"""
値を持たないフィールド。　アノテーション仕様上に定義が存在すること自体に意味がある場合のフィールド値に利用します。

Kyes of Dict

* type: str
    

"""

AnnotationTypeFieldValueMarginOfErrorTolerance = Dict[str, Any]
"""
誤差許容範囲

Kyes of Dict

* type: str
    
* max_pixel: int
    

"""

AnnotationTypeFieldValueMinimumArea2d = Dict[str, Any]
"""
最小の面積 

Kyes of Dict

* type: str
    
* min_area: int
    

"""

AnnotationTypeFieldValueMinimumSize = Dict[str, Any]
"""
アノテーションの最小サイズに関する設定

Kyes of Dict

* type: str
    
* min_warn_rule: AnnotationTypeFieldMinWarnRule
    
* min_width: int
    
* min_height: int
    

"""

AnnotationTypeFieldValueMinimumSize2dWithDefaultInsertPosition = Dict[str, Any]
"""


Kyes of Dict

* type: str
    
* min_warn_rule: AnnotationTypeFieldMinWarnRule
    
* min_width: int
    
* min_height: int
    
* position_for_minimum_bounding_box_insertion: List[int]
    最小矩形の挿入位置を、要素が2の配列で指定します。 

"""

AnnotationTypeFieldValueOneBooleanFieldValue = Dict[str, Any]
"""
真偽値をひとつだけ持つフィールド

Kyes of Dict

* type: str
    
* value: bool
    

"""

AnnotationTypeFieldValueOneIntegerFieldValue = Dict[str, Any]
"""
数値をひとつだけ持つフィールド

Kyes of Dict

* type: str
    
* value: int
    

"""

AnnotationTypeFieldValueOneStringFieldValue = Dict[str, Any]
"""
文字列を一つだけ持つフィールド

Kyes of Dict

* type: str
    
* value: str
    

"""

AnnotationTypeFieldValueVertexCountMinMax = Dict[str, Any]
"""
頂点数の最大・最小 

Kyes of Dict

* type: str
    
* min: int
    
* max: int
    

"""

AnnotationV1 = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: List[AnnotationDetailV1]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    更新日時

"""

AnnotationV2Input = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: List[AnnotationDetailV2Input]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    対象タスク・対象入力データへの最初の保存時は未指定にしてください。 更新の場合はアノテーション取得時のupdated_datetimeをそのまま指定してください。 
* format_version: str
    

"""

AnnotationV2Output = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: List[AnnotationDetailV2Output]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    対象タスク・対象入力データへ一度もアノテーションの保存が行われていない場合、未指定となります。 そうで無い場合、対象タスク・対象入力データのアノテーション最終更新時刻です。 
* format_version: str
    

"""


class AssigneeRuleOfResubmittedTask(Enum):
    """
    再提出されたタスクの検査/受入担当者の割当方法 * `no_assignee` - 以前の担当者で固定せず、未割当てにします。 * `fixed` - 以前の担当者が再度担当します。以前の担当者がいない(1回目の検査/受入)場合は未割当てになります。
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
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* additional_data_list: List[AdditionalDataV1]
    属性情報。  アノテーション属性の種類（`additional_data_definition`の`type`）によって、属性値を格納するプロパティは変わります。  | 属性の種類 | `additional_data_definition`の`type` | 属性値を格納するプロパティ                    | |------------|-------------------------|----------------------| | ON/OFF | flag       | flag                                          | | 整数 | integer    | integer                                       | | 自由記述（1行）| text       | comment                                       | | 自由記述（複数行）| comment    | comment                                       | | トラッキングID  | tracking | comment                                       | | アノテーションリンク    | link   | comment                                       | | 排他選択（ラジオボタン）  |choice   | choice                                        | | 排他選択（ドロップダウン） | select    | choice                                        | 
* updated_datetime: str
    更新日時

"""

BatchAnnotationRequestItem = Dict[str, Any]
"""


Kyes of Dict

* data: BatchAnnotation
    
* type: str
    `Delete` [詳しくはこちら](#section/API-Convention/API-_type) 
* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* updated_datetime: str
    更新日時

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
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* updated_datetime: str
    更新日時
* type: str
    `Delete` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchAnnotationRequestItemPut = Dict[str, Any]
"""
アノテーション更新

Kyes of Dict

* data: BatchAnnotation
    
* type: str
    `Put` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchCommentRequestItem = Dict[str, Any]
"""


Kyes of Dict

* comment_id: str
    コメントのID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* phase: TaskPhase
    
* phase_stage: int
    コメントを作成したときのフェーズのステージ。
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* comment_type: str
    コメントの種別。次の値が指定できます。  * `onhold` - 保留コメントとして扱われます。 * `inspection` - 検査コメントとして扱われます。  返信コメント作成時は返信先コメントの `comment_type` と同じ値を指定してください。  コメント更新時は更新前コメントと同じ値を指定してください（変更はできません）。 
* phrases: List[str]
    `comment_type` の値によって指定可能な値が異なります。  * `onhold` の場合   * 使用しません（空配列 or 指定なし） 
* comment: str
    コメント本文。 
* comment_node: CommentNode
    
* datetime_for_sorting: str
    コメントのソート順を決める日時。コメント作成時のみ指定可能です。  Annofab標準エディタでは、コメントはここで指定した日時にしたがってスレッドごとに昇順で表示されます。  コメント作成時に未指定とした場合は、作成操作オブジェクトの順序に応じてコメント作成日時からずれた時刻が自動設定されます（ソート順を一意とするため）。  なお、この値は後から更新することはできません（値を指定しても無視されます）。 
* type: str
    `Delete`  [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchCommentRequestItemDelete = Dict[str, Any]
"""
コメント削除

Kyes of Dict

* comment_id: str
    コメントのID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* type: str
    `Delete`  [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchCommentRequestItemPut = Dict[str, Any]
"""
コメント更新

Kyes of Dict

* comment_id: str
    コメントのID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* phase: TaskPhase
    
* phase_stage: int
    コメントを作成したときのフェーズのステージ。
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* comment_type: str
    コメントの種別。次の値が指定できます。  * `onhold` - 保留コメントとして扱われます。 * `inspection` - 検査コメントとして扱われます。  返信コメント作成時は返信先コメントの `comment_type` と同じ値を指定してください。  コメント更新時は更新前コメントと同じ値を指定してください（変更はできません）。 
* phrases: List[str]
    `comment_type` の値によって指定可能な値が異なります。  * `onhold` の場合   * 使用しません（空配列 or 指定なし） 
* comment: str
    コメント本文。 
* comment_node: CommentNode
    
* datetime_for_sorting: str
    コメントのソート順を決める日時。コメント作成時のみ指定可能です。  Annofab標準エディタでは、コメントはここで指定した日時にしたがってスレッドごとに昇順で表示されます。  コメント作成時に未指定とした場合は、作成操作オブジェクトの順序に応じてコメント作成日時からずれた時刻が自動設定されます（ソート順を一意とするため）。  なお、この値は後から更新することはできません（値を指定しても無視されます）。 
* type: str
    `Put`  [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchInputDataRequestItem = Dict[str, Any]
"""


Kyes of Dict


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
    `Delete` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchInspectionRequestItem = Dict[str, Any]
"""


Kyes of Dict

* data: Inspection
    
* type: str
    `Delete` [詳しくはこちら](#section/API-Convention/API-_type) 
* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* inspection_id: str
    検査ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 

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
    `Delete` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchInspectionRequestItemPut = Dict[str, Any]
"""
検査コメント更新

Kyes of Dict

* data: Inspection
    
* type: str
    `Put` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchTaskRequestItem = Dict[str, Any]
"""


Kyes of Dict


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
    `Delete` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BoundingBoxMetadata = Dict[str, Any]
"""
ベクター形式のアノテーション（矩形、ポリゴン、ポリライン、点）のメタデータ

Kyes of Dict

* min_width: int
    幅の最小値[ピクセル]
* min_height: int
    高さの最小値[ピクセル]
* min_warn_rule: str
    サイズの制約に関する情報 * `none` - 制約なし * `or` - 幅と高さの両方が最小値以上 * `and` - 幅と高さのどちらか一方が最小値以上 
* min_area: int
    面積の最小値[平方ピクセル]
* max_vertices: int
    頂点数の最大値
* min_vertices: int
    頂点数の最小値
* position_for_minimum_bounding_box_insertion: PositionForMinimumBoundingBoxInsertion
    
* tolerance: int
    許容誤差[ピクセル]
* has_direction: bool
    `annotation_type` が `polyline` の場合、アノテーションに向きを持たせるかどうかを指定できます。 この値が `true` の場合、Annofabの標準画像エディタ上ではポリラインの向きを示す矢印が描画されるようになります。  `annotationType` が `polyline` 以外の場合は必ず `false` となります。 

"""

ChangePasswordRequest = Dict[str, Any]
"""


Kyes of Dict

* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* old_password: str
    
* new_password: str
    

"""

Color = Dict[str, Any]
"""
RGBで表現される色情報

Kyes of Dict

* red: int
    
* green: int
    
* blue: int
    

"""

Comment = Dict[str, Any]
"""
コメント

Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* comment_id: str
    コメントのID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* phase: TaskPhase
    
* phase_stage: int
    コメントを作成したときのフェーズのステージ。
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* comment_type: CommentType
    
* phrases: List[str]
    `comment_type` の値によって扱いが異なります。  * `onhold` の場合   * 使用しません（空配列） * `inspection` の場合   * 参照している定型指摘のIDリスト 
* comment: str
    コメント本文。 
* comment_node: CommentNode
    
* datetime_for_sorting: str
    コメントのソート順を決める日時。  Annofab標準エディタでは、コメントはここで指定した日時にしたがってスレッドごとに昇順で表示されます。 
* created_datetime: str
    コメントの作成日時。
* updated_datetime: str
    コメントの更新日時。

"""

CommentNode = Dict[str, Any]
"""
コメントのノード固有のデータ。  * `RootComment` - スレッドの先頭のコメント（ルートコメント）。 * `ReplyComment` - あるコメントへの返信コメント。 

Kyes of Dict

* data: InspectionData
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* status: CommentStatus
    
* type: str
    `Reply` [詳しくはこちら](#section/API-Convention/API-_type) 
* root_comment_id: str
    コメントのID。[値の制約についてはこちら。](#section/API-Convention/APIID) 

"""


class CommentStatus(Enum):
    """
    `comment_type` の値によってコメントのステータスに格納される値とステータスの意味が変わります。  * `onhold` の場合   * `open`（未対応）、`resolved`（対応完了）を指定可能 * `inspection` の場合   * `open`（未対応）、`resolved`（対応完了）、`closed`（対応不要）を指定可能
    """

    OPEN = "open"
    RESOLVED = "resolved"
    CLOSED = "closed"


class CommentType(Enum):
    """
    コメントの種別。  * `onhold` - 保留コメント * `inspection` - 検査コメント
    """

    ONHOLD = "onhold"
    INSPECTION = "inspection"


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
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* confirmation_code: str
    
* new_password: str
    

"""

ConfirmSignUpRequest = Dict[str, Any]
"""


Kyes of Dict

* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
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
    集約対象の `field` の値です。 
* count: int
    集約対象 `field` の値が `key` の値と等しかったリソースの件数です。 
* aggregations: List[AggregationResult]
    この集約のサブ集約です。サブ集約がないときは空の配列になります。 

"""

CountResult = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `CountResult` [詳しくはこちら](#section/API-Convention/API-_type) 
* name: str
    複数の集約を区別するための名前です。  `(フィールド名)_(集約内容)` のように命名されます。例えば `account_id` フィールドを `count` する場合、`account_id_count` となります。 
* field: str
    集約に使われたリソースのフィールド名です。  リソースの属性のさらに属性を参照するときは、`foo.bar.buz` のようにドット区切りになります。 
* doc_count: int
    集約の件数です。 
* items: List[Count]
    集約結果の値です。 

"""

DataPath = Dict[str, Any]
"""


Kyes of Dict

* url: str
    ファイルアップロード用の一時URLです。このURLにファイルをアップロードします。
* path: str
    [putInputData](#operation/putInputData) APIや[putSupplementaryData](#operation/putSupplementaryData) APIのリクエストボディに指定するパスです。 

"""

DateRange = Dict[str, Any]
"""
日付の期間

Kyes of Dict

* _from: str
    期間の開始日（ISO 8601 拡張形式）
* to: str
    期間の終了日（ISO 8601 拡張形式）

"""


class DefaultAnnotationType(Enum):
    """
    アノテーションの種類 * `bounding_box` - 矩形 * `segmentation` - 塗りつぶし（インスタンスセグメンテーション用） * `segmentation_v2` - 塗りつぶしv2（セマンティックセグメンテーション用） * `polygon` - ポリゴン（閉じた頂点集合） * `polyline` - ポリライン（開いた頂点集合） * `point` - 点 * `classification` - 全体 * `range` - 動画の区間 * `custom` - カスタム  プロジェクトの種類によって、使用できるアノテーションの種類は決まっています。アノテーションの種類が使用できるかどうかを、以下の表に記載しました。  * `○`：使用できる  * `×`：使用できない   |アノテーションの種類                 | 画像プロジェクト        | 動画プロジェクト | カスタムプロジェクト | |-----------------|:----------:|:----:|:------:| | bounding_box    | 〇         | ×  | ×    | | segmentation    | 〇         | ×  | ×    | | segmentation_v2 | 〇         | ×  | ×    | | polygon         | 〇         | ×  | ×    | | polyline        | 〇         | ×  | ×    | | point           | 〇         | ×  | ×    | | classification  | 〇         | 〇  | ×    | | range           | ×         | 〇  | ×    | | custom          | ×         | ×  | 〇    |
    """

    BOUNDING_BOX = "bounding_box"
    SEGMENTATION = "segmentation"
    SEGMENTATION_V2 = "segmentation_v2"
    POLYGON = "polygon"
    POLYLINE = "polyline"
    POINT = "point"
    CLASSIFICATION = "classification"
    RANGE = "range"
    CUSTOM = "custom"


DeleteProjectResponse = Dict[str, Any]
"""


Kyes of Dict

* job: ProjectJobInfo
    
* project: Project
    

"""

Duplicated = Dict[str, Any]
"""
値の重複が許可されていない属性の重複エラー

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data: AdditionalDataV1
    
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

EditorUsageTimespan = Dict[str, Any]
"""
エディタごとの利用時間

Kyes of Dict

* editor_name: str
    エディタ名です。  | editor_nameの値 | エディタ名   | |-----------------|--------------| | image_editor    | 画像エディタ | | video_editor    | 動画エディタ | | 3d_editor       | 3Dエディタ   | 
* value: float
    エディタ利用時間。単位は時

"""

ErrorItem = Dict[str, Any]
"""


Kyes of Dict

* error_code: str
    
* message: str
    エラーの概要
* ext: __DictStrKeyAnyValue__
    補足情報

"""

Errors = Dict[str, Any]
"""


Kyes of Dict

* errors: List[ErrorItem]
    
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
    タスクのフェーズのステージ番号
* task_status: TaskStatus
    
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_name: str
    入力データ名
* details: List[FullAnnotationDetail]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列
* updated_datetime: str
    更新日時。アノテーションが一つもない場合（教師付作業が未着手のときなど）は、未指定。
* annotation_format_version: str
    アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、Annofabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 

"""

FullAnnotationAdditionalData = Dict[str, Any]
"""
属性情報 

Kyes of Dict

* additional_data_definition_id: str
    属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* additional_data_definition_name: InternationalizationMessage
    
* type: AdditionalDataDefinitionType
    
* value: FullAnnotationAdditionalDataValue
    

"""

FullAnnotationAdditionalDataChoiceValue = Dict[str, Any]
"""


Kyes of Dict

* id: str
    選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* name: InternationalizationMessage
    

"""

FullAnnotationAdditionalDataValue = Dict[str, Any]
"""
属性値 

Kyes of Dict

* type: str
    Link
* value: str
    リンク先アノテーションID

"""

FullAnnotationAdditionalDataValueChoice = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `Choice` 
* value: AdditionalDataChoiceValue
    

"""

FullAnnotationAdditionalDataValueComment = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `Comment` 
* value: str
    自由記述

"""

FullAnnotationAdditionalDataValueFlag = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `Flag` 
* value: bool
    フラグのON(true)またはOFF(false)

"""

FullAnnotationAdditionalDataValueInteger = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `Integer` 
* value: int
    整数値

"""

FullAnnotationAdditionalDataValueLink = Dict[str, Any]
"""


Kyes of Dict

* type: str
    Link
* value: str
    リンク先アノテーションID

"""

FullAnnotationAdditionalDataValueTracking = Dict[str, Any]
"""


Kyes of Dict

* type: str
    Tracking
* value: str
    トラッキングID

"""

FullAnnotationData = Dict[str, Any]
"""
アノテーションのデータが格納されます。   * `FullAnnotationDataClassification`: 入力データ全体アノテーション   * `FullAnnotationDataSegmentation`: 塗りつぶしアノテーション   * `FullAnnotationDataSegmentationV2`: 塗りつぶしv2アノテーション   * `FullAnnotationDataBoundingBox`: 矩形アノテーション   * `FullAnnotationDataPoints`: ポリゴンまたはポリラインアノテーション   * `FullAnnotationDataSinglePoint`: 点アノテーション   * `FullAnnotationDataRange`: 動画区間アノテーション   * `FullAnnotationDataUnknown`: カスタムアノテーション 

Kyes of Dict

* type: str
    `Unknown` 
* data_uri: str
    塗りつぶし画像のパス。 塗りつぶし画像のファイル形式はPNGです。塗りつぶされた部分の色は`rgba(255, 255, 255, 1)`、塗りつぶされていない部分の色は`rgba(0, 0, 0, 0)`です。 
* left_top: Point
    
* right_bottom: Point
    
* points: List[Point]
    頂点の座標値
* point: Point
    
* begin: float
    開始時間（ミリ秒）
* end: float
    終了時間（ミリ秒）
* data: str
    アノテーションデータを文字列で表現した値

"""

FullAnnotationDataBoundingBox = Dict[str, Any]
"""


Kyes of Dict

* left_top: Point
    
* right_bottom: Point
    
* type: str
    `BoundingBox` 

"""

FullAnnotationDataClassification = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `Classification` 

"""

FullAnnotationDataPoints = Dict[str, Any]
"""


Kyes of Dict

* points: List[Point]
    頂点の座標値
* type: str
    `Points` 

"""

FullAnnotationDataRange = Dict[str, Any]
"""


Kyes of Dict

* begin: float
    開始時間（ミリ秒）
* end: float
    終了時間（ミリ秒）
* type: str
    `Range` 

"""

FullAnnotationDataSegmentation = Dict[str, Any]
"""


Kyes of Dict

* data_uri: str
    塗りつぶし画像のパス。 塗りつぶし画像のファイル形式はPNGです。塗りつぶされた部分の色は`rgba(255, 255, 255, 1)`、塗りつぶされていない部分の色は`rgba(0, 0, 0, 0)`です。 
* type: str
    `Segmentation` 

"""

FullAnnotationDataSegmentationV2 = Dict[str, Any]
"""


Kyes of Dict

* data_uri: str
    塗りつぶし画像のパス。 塗りつぶし画像のファイル形式はPNGです。塗りつぶされた部分の色は`rgba(255, 255, 255, 1)`、塗りつぶされていない部分の色は`rgba(0, 0, 0, 0)`です。 
* type: str
    `SegmentationV2` 

"""

FullAnnotationDataSinglePoint = Dict[str, Any]
"""


Kyes of Dict

* point: Point
    
* type: str
    `SinglePoint` 

"""

FullAnnotationDataUnknown = Dict[str, Any]
"""


Kyes of Dict

* data: str
    アノテーションデータを文字列で表現した値
* type: str
    `Unknown` 

"""

FullAnnotationDetail = Dict[str, Any]
"""


Kyes of Dict

* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_name: InternationalizationMessage
    
* annotation_type: AnnotationType
    
* data_holding_type: AnnotationDataHoldingType
    
* data: FullAnnotationData
    
* additional_data_list: List[FullAnnotationAdditionalData]
    属性情報。 

"""


class GraphType(Enum):
    """
    グラフの種類 * `task_progress` - タスク進捗状況 * `cumulative_labor_time_by_task_phase` - タスクフェーズ別累積作業時間 * `number_of_inspections_per_inspection_phrase` - 検査コメント内容別指摘回数 * `number_of_task_rejections_by_member` - メンバー別タスクが差戻された回数 * `labor_time_per_member` - メンバー別作業時間 * `mean_labor_time_per_image` - 画像一枚当たりの作業時間平均 * `mean_labor_time_per_minute_of_movie` - 動画一分当たりの作業時間平均 * `mean_labor_time_per_image_by_member` - メンバー別画像一枚当たりの作業時間平均 * `mean_labor_time_per_minute_of_movie_by_member` - メンバー別動画一分当たりの作業時間平均
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

IllegalState = Dict[str, Any]
"""
作業が開始されていない、担当が割り当たっていない等のエラー

Kyes of Dict

* type: str
    IllegalState

"""

InputData = Dict[str, Any]
"""
入力データの情報を表すデータ構造です。

Kyes of Dict

* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_set_id: str
    入力データセットID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_name: str
    入力データ名
* input_data_path: str
    入力データの実体が保存されたパスです。 s3スキーマまたはhttpsスキーマのみサポートしています。 
* url: str
    システム内部用のプロパティ
* etag: str
    [HTTPレスポンスヘッダー ETag](https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/ETag)に相当する値です。 
* original_input_data_path: str
    システム内部用のプロパティ 
* updated_datetime: str
    更新日時
* sign_required: bool
    CloudFrontのSignedCookieを使ったプライベートストレージを利用するかどうか 
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 
* system_metadata: SystemMetadata
    

"""

InputDataList = Dict[str, Any]
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
    検索結果の件数が1万件を超えた場合は`true`になります。
* aggregations: List[AggregationResult]
    システム内部用のプロパティ。 

"""


class InputDataOrder(Enum):
    """
    タスクに割り当てる入力データの順序  * `name_asc` - 入力データ名の昇順 * `name_desc` - 入力データ名の降順 * `random` - ランダム
    """

    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"
    RANDOM = "random"


InputDataRequest = Dict[str, Any]
"""


Kyes of Dict

* input_data_name: str
    入力データ名。ZIPファイルをアップロードする際は、入力データ名のプレフィックスを指定してください。
* input_data_path: str
    入力データの実体が存在するURLです。 Annofabにファイルをアップロードして入力データを作成する場合は、[createTempPath](#operation/createTempPath) APIで取得した`path`を指定してください。  入力データの実体が[プライベートストレージ](/docs/faq/#prst9c)に存在する場合は、S3スキーマまたはHTTPSスキーマのURLを指定してください。 S3プライベートストレージに存在するファイルを入力データとして登録する場合は、事前に[認可の設定](/docs/faq/#m0b240)が必要です。 
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 
* sign_required: bool
    CloudFrontのSignedCookieを使ったプライベートストレージを利用するかどうか。  `true`を指定する場合は，`input_data_path`にAnnofabのAWS IDをTrusted Signerとして登録したCloudFrontのURLを指定してください。 
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

InputDataSet = Dict[str, Any]
"""
入力データセットの情報を表すデータ構造です。

Kyes of Dict

* input_data_set_id: str
    入力データセットID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_set_name: str
    入力データセットの名前
* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_type: InputDataType
    
* private_storage_arn: str
    AWS IAMロール。ビジネスプランでのS3プライベートストレージの認可で使います。 [S3プライベートストレージの認可の設定についてはこちら](/docs/faq/#m0b240)をご覧ください。 
* updated_datetime: str
    入力データセットの最終更新日時

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
    アノテーションする入力データの種類。 * `image` - 画像 * `movie` - 動画 * `custom` - カスタム
    """

    IMAGE = "image"
    MOVIE = "movie"
    CUSTOM = "custom"


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
    検査コメントを付与したときのフェーズのステージ
* commenter_account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* data: InspectionData
    
* parent_inspection_id: str
    検査ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* phrases: List[str]
    参照している定型指摘のID。
* comment: str
    検査コメントの中身 
* status: InspectionStatus
    
* created_datetime: str
    
* updated_datetime: str
    

"""

InspectionData = Dict[str, Any]
"""
##### スレッドの先頭のコメントである（`parent_inspection_id` に値がない）場合  検査コメントの座標値や区間。  * `InspectionDataPoint`：点で検査コメントを付与したときの座標値 * `InspectionDataPolyline`：ポリラインで検査コメントを付与したときの座標値 * `InspectionDataTime`：検査コメントを付与した区間（動画プロジェクトの場合） * `InspectionDataCustom`：カスタム  ##### 返信コメントである（`parent_inspection_id` に値がある）場合  現在は使用しておらず、レスポンスに含まれる値は不定です。APIのレスポンスにこの値を含む場合でも、「スレッドの先頭のコメント」の値を利用してください。  リクエストボディに指定する場合は、スレッドの先頭のコメントと同じ値を指定します。 

Kyes of Dict

* x: int
    
* y: int
    
* type: str
    `Custom` [詳しくはこちら](#section/API-Convention/API-_type) 
* coordinates: List[InspectionDataPolylineCoordinates]
    ポリラインを構成する頂点の配列 
* start: float
    開始時間（ミリ秒）。小数点以下はミリ秒以下を表します。
* end: float
    終了時間（ミリ秒）。小数点以下はミリ秒以下を表します。
* data: str
    

"""

InspectionDataCustom = Dict[str, Any]
"""


Kyes of Dict

* data: str
    
* type: str
    `Custom` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

InspectionDataPoint = Dict[str, Any]
"""
問題のある部分を示す座標 

Kyes of Dict

* x: int
    
* y: int
    
* type: str
    `Point` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

InspectionDataPolyline = Dict[str, Any]
"""
問題のある部分を示すポリライン 

Kyes of Dict

* coordinates: List[InspectionDataPolylineCoordinates]
    ポリラインを構成する頂点の配列 
* type: str
    `Polyline` [詳しくはこちら](#section/API-Convention/API-_type) 

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
    開始時間（ミリ秒）。小数点以下はミリ秒以下を表します。
* end: float
    終了時間（ミリ秒）。小数点以下はミリ秒以下を表します。
* type: str
    `Time` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

InspectionOrReplyRequired = Dict[str, Any]
"""
新規検査コメントまたは未対応検査コメントへの返信が必要である時のエラー

Kyes of Dict

* type: str
    InspectionOrReplyRequired

"""

InspectionPhrase = Dict[str, Any]
"""


Kyes of Dict

* id: str
    定型指摘ID
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
    ラベルに紐付いている検査コメントの集計結果。キーは`label_id`です。
* no_label: InspectionStatisticsPhrases
    

"""

InspectionStatisticsPhrases = Dict[str, Any]
"""


Kyes of Dict

* phrases: dict(str, int)
    定型指摘ごとの検査コメントの個数。キーは定型指摘ID、値は検査コメント数です。
* no_phrase: int
    定型指摘を使っていない検査コメントの個数

"""


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


InspectionValidationError = Dict[str, Any]
"""


Kyes of Dict

* inspection: Inspection
    
* type: str
    IllegalState

"""

Instruction = Dict[str, Any]
"""


Kyes of Dict

* html: str
    作業ガイドのHTML
* last_updated_datetime: str
    更新日時

"""

InstructionHistory = Dict[str, Any]
"""


Kyes of Dict

* history_id: str
    作業ガイドの履歴ID
* account_id: str
    作業ガイドを更新したユーザーのアカウントID
* updated_datetime: str
    作業ガイドの最終更新日時

"""

InstructionImage = Dict[str, Any]
"""


Kyes of Dict

* image_id: str
    作業ガイド画像ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* path: str
    作業ガイド画像の実体が保存されたパスです。 
* url: str
    作業ガイド画像を取得するためのシステム内部用のURLです。
* etag: str
    [HTTPレスポンスヘッダー ETag](https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/ETag)に相当する値です。 

"""

InstructionImagePath = Dict[str, Any]
"""


Kyes of Dict

* url: str
    ファイルアップロード用の一時URLです。このURLにファイルをアップロードします。
* path: str
    作業ガイド画像のURL

"""

InternationalizationMessage = Dict[str, Any]
"""


Kyes of Dict

* messages: List[InternationalizationMessageMessages]
    言語コードとメッセージ（テキスト）のリスト。  * アノテーションエディタなどでは、Annofabの表示言語（各ユーザーが個人設定で選んだ言語）のメッセージが使われます * 以下の名前は、[Simple Annotation](#section/Simple-Annotation-ZIP) では `en-US` のメッセージが使われます     * ラベル名     * 属性名     * 選択肢名 * いずれの場合でも、表示しようとした言語が `messages` に含まれない場合、 `default_lang` に指定した言語のメッセージが使われます 
* default_lang: str
    希望された言語のメッセージが存在しない場合に、フォールバック先として使われる言語コード

"""

InternationalizationMessageMessages = Dict[str, Any]
"""


Kyes of Dict

* lang: str
    言語コード。`en-US` (英語) または `ja-JP` (日本語) のみサポートしています。
* message: str
    lang で指定された言語でのメッセージ

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

InvalidChoice = Dict[str, Any]
"""
選択肢不正エラー

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    InvalidChoice

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

InvalidValue = Dict[str, Any]
"""
値制約に合致しないエラー

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    InvalidValue

"""

InviteOrganizationMemberRequest = Dict[str, Any]
"""


Kyes of Dict

* role: OrganizationMemberRole
    

"""

IssueProjectGuestUserTokenRequest = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    ゲストユーザーがアクセスするプロジェクトのID
* app_token: str
    ゲストユーザートークンを要求するアプリケーションに提供されているトークン
* project_token: str
    [issueProjectToken](#operation/issueProjectToken)で発行されたトークン文字列
* role: str
    ゲストユーザーのプロジェクト上でのロール * `worker` - アノテーター * `accepter` - チェッカー 
* profile: ProjectGuestUserProfile
    

"""

IssueProjectTokenRequest = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトトークンの発行対象プロジェクトID
* description: str
    発行するトークンについての人間可読な説明

"""


class JobStatus(Enum):
    """
    ジョブのステータス
    """

    PROGRESS = "progress"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class KeyLayout(Enum):
    """
    キーボードレイアウト * `ja-JP` - 日本語(106/109)配列 * `en-US` - 英語(101/104)配列 * `other` - その他
    """

    JA_JP = "ja-JP"
    EN_US = "en-US"
    OTHER = "other"


Keybind = Dict[str, Any]
"""


Kyes of Dict

* code: str
    [KeyboardEvent.code](https://developer.mozilla.org/ja/docs/Web/API/KeyboardEvent/code)に相当する値です。 
* shift: bool
    Shiftキーを押しているかどうか
* ctrl: bool
    Ctrlキーを押しているかどうか
* alt: bool
    Altキーを押しているかどうか

"""

LabelStatistics = Dict[str, Any]
"""


Kyes of Dict

* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* completed: int
    ラベルごとの受入が完了したアノテーション数
* wip: int
    ラベルごとの受入が完了していないアノテーション数

"""

LabelV1 = Dict[str, Any]
"""


Kyes of Dict

* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_name: InternationalizationMessage
    
* keybind: List[Keybind]
    ショートカットキー
* annotation_type: AnnotationType
    
* bounding_box_metadata: BoundingBoxMetadata
    
* segmentation_metadata: SegmentationMetadata
    
* additional_data_definitions: List[AdditionalDataDefinitionV1]
    属性
* color: Color
    
* annotation_editor_feature: AnnotationEditorFeature
    
* allow_out_of_image_bounds: bool
    枠内制御がなくなったため値の設定は出来ません。値の取得では、必ず`true`が入ります。[廃止](/docs/releases/deprecation-announcements.html#notice25)までは互換性のため残されています。 
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

LabelV2 = Dict[str, Any]
"""


Kyes of Dict

* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_name: InternationalizationMessage
    
* keybind: List[Keybind]
    ショートカットキー
* annotation_type: AnnotationType
    
* bounding_box_metadata: BoundingBoxMetadata
    
* segmentation_metadata: SegmentationMetadata
    
* additional_data_definitions: List[str]
    ラベルに所属する属性のID
* color: Color
    
* annotation_editor_feature: AnnotationEditorFeature
    
* allow_out_of_image_bounds: bool
    枠内制御がなくなったため値の設定は出来ません。値の取得では、必ず`true`が入ります。[廃止](/docs/releases/deprecation-announcements.html#notice25)までは互換性のため残されています。 
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

LabelV3 = Dict[str, Any]
"""


Kyes of Dict

* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_name: InternationalizationMessage
    
* keybind: List[Keybind]
    ショートカットキー
* annotation_type: AnnotationType
    
* field_values: dict(str, AnnotationTypeFieldValue)
    KeyがフィールドIdであるDictionaryです。  カスタムの[組織プラグイン](#operation/putOrganizationPlugin)で利用される[UserDefinedAnnotationTypeDefinition](#section/UserDefinedAnnotationTypeDefinition).`field_definitions`で定義されます。 
* additional_data_definitions: List[str]
    ラベルに所属する属性のID
* color: Color
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""


class Lang(Enum):
    """
    表示言語 * `ja-JP` - 日本語 * `en-US` - 英語
    """

    EN_US = "en-US"
    JA_JP = "ja-JP"


LoginRequest = Dict[str, Any]
"""


Kyes of Dict

* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* password: str
    パスワード

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
    マーカーのタイトル
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
    マーカー一覧
* updated_datetime: str
    更新日時

"""

Message = Dict[str, Any]
"""


Kyes of Dict

* message: str
    メッセージ
* message_id: str
    システム内部用のプロパティ

"""

MessageOrJobInfo = Dict[str, Any]
"""


Kyes of Dict

* message: str
    メッセージ
* message_id: str
    システム内部用のプロパティ
* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* job_type: ProjectJobType
    
* job_id: str
    ジョブID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* job_status: JobStatus
    
* job_execution: __DictStrKeyAnyValue__
    ジョブの内部情報
* job_detail: __DictStrKeyAnyValue__
    ジョブ結果の内部情報
* errors: Errors
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

MyAccount = Dict[str, Any]
"""


Kyes of Dict

* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* username: str
    ユーザー名
* email: str
    メールアドレス
* lang: Lang
    
* biography: str
    人物紹介、略歴。  この属性は、Annofab外の所属先や肩書などを表すために用います。 Annofab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 
* keylayout: KeyLayout
    
* authority: str
    システム内部用のプロパティ
* account_type: str
    アカウントの種別 * `annofab` - 通常の手順で登録されたアカウント。後から[外部アカウントとの紐付け](/docs/faq/#yyyub0)をしたアカウントの場合もこちらになります。 * `external` - [外部アカウントだけで作成したアカウント](/docs/faq/#v1u344) * `project_guest` - [issueProjectGuestUserToken](#operation/issueProjectGuestUserToken)によって作成されたされたアカウント 
* updated_datetime: str
    更新日時
* reset_requested_email: str
    システム内部用のプロパティ
* errors: List[str]
    システム内部用のプロパティ

"""

MyAccountAllOf = Dict[str, Any]
"""


Kyes of Dict

* reset_requested_email: str
    システム内部用のプロパティ
* errors: List[str]
    システム内部用のプロパティ

"""

MyOrganization = Dict[str, Any]
"""


Kyes of Dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* name: str
    
* email: str
    
* price_plan: PricePlan
    
* summary: __DictStrKeyAnyValue__
    廃止予定のプロパティです。常に中身は空です。 
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時
* my_role: OrganizationMemberRole
    
* my_status: OrganizationMemberStatus
    

"""

MyOrganizationList = Dict[str, Any]
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
    システム内部用のプロパティ。 

"""

NoCommentInspection = Dict[str, Any]
"""
空の検査コメントがある時のエラー

Kyes of Dict

* inspection: Inspection
    
* type: str
    NoCommentInspection

"""

Organization = Dict[str, Any]
"""


Kyes of Dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* organization_name: str
    組織名。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* email: str
    メールアドレス
* price_plan: PricePlan
    
* summary: __DictStrKeyAnyValue__
    廃止予定のプロパティです。常に中身は空です。 
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

OrganizationActivity = Dict[str, Any]
"""


Kyes of Dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* created_datetime: str
    作成日時
* storage_usage_bytes: int
    Annofabストレージの使用量[バイト]

"""

OrganizationCacheRecord = Dict[str, Any]
"""


Kyes of Dict

* input: str
    
* members: str
    
* statistics: str
    
* organization: str
    

"""

OrganizationJobInfo = Dict[str, Any]
"""


Kyes of Dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* job_type: str
    ジョブの同時実行制御のために用いる、ジョブの種別。 (現在はまだ、この種別に該当するものはありません) 
* job_id: str
    ジョブID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* job_status: JobStatus
    
* job_execution: __DictStrKeyAnyValue__
    ジョブの内部情報
* job_detail: __DictStrKeyAnyValue__
    ジョブ結果の内部情報
* errors: Errors
    
* created_datetime: str
    
* updated_datetime: str
    

"""

OrganizationJobInfoContainer = Dict[str, Any]
"""


Kyes of Dict

* list: List[OrganizationJobInfo]
    バックグラウンドジョブの一覧。作成日時の降順でソートされています。
* has_next: bool
    さらに古いジョブが存在する場合は`true`です。取得したジョブ一覧の中で`created_datetime`が最も古い値を、クエリパラメータ`exclusive_start_created_datetime`に指定することで、さらに古いジョブを取得することができます。

"""

OrganizationMember = Dict[str, Any]
"""


Kyes of Dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* username: str
    ユーザー名
* role: OrganizationMemberRole
    
* status: OrganizationMemberStatus
    
* biography: str
    人物紹介、略歴。  この属性は、Annofab外の所属先や肩書などを表すために用います。 Annofab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

OrganizationMemberList = Dict[str, Any]
"""


Kyes of Dict

* list: List[OrganizationMember]
    組織メンバーの一覧
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる組織メンバーが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: List[AggregationResult]
    システム内部用のプロパティ 

"""


class OrganizationMemberRole(Enum):
    """
    組織メンバーのロール。 * `owner` - 組織オーナー * `administrator` - 組織管理者 * `contributor` - 組織貢献者
    """

    OWNER = "owner"
    ADMINISTRATOR = "administrator"
    CONTRIBUTOR = "contributor"


class OrganizationMemberStatus(Enum):
    """
    組織メンバーのステータス。 * `active` - 組織メンバーとして有効で、組織を閲覧したり、権限があれば編集できます。 * `waiting_response` - 組織に招待され、まだ加入/脱退を返答していません。組織の一部を閲覧のみできます。 * `inactive` - 脱退したメンバーを表します。組織を閲覧できません。
    """

    ACTIVE = "active"
    WAITING_RESPONSE = "waiting_response"
    INACTIVE = "inactive"


OrganizationPlugin = Dict[str, Any]
"""


Kyes of Dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* plugin_id: str
    プラグインID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* plugin_name: str
    プラグインの名前です。 プラグイン一覧や、プロジェクトで使うプラグインを選ぶときなどに表示されます。 
* description: str
    プラグインの説明です。 プラグイン一覧や、プロジェクトで使うプラグインを選ぶときなどに表示されます。 
* detail: PluginDetail
    
* is_builtin: bool
    trueの場合、プラグインはAnnofab組み込みのプラグインであり、更新や削除を行うことはできません。
* created_datetime: str
    
* updated_datetime: str
    

"""

OrganizationPluginCompatibility = Dict[str, Any]
"""
プラグイン間の互換性を表します。未指定の場合はinput、outputともに`Top`の`OrganizationPluginCompatibilityType`が設定されます。

Kyes of Dict

* input: OrganizationPluginCompatibilityType
    
* output: OrganizationPluginCompatibilityType
    

"""

OrganizationPluginCompatibilityType = Dict[str, Any]
"""
プラグインの入力/出力を表す型です。 

Kyes of Dict

* type: str
    Constant型で、かつidの値が一致している場合に互換性があることを示します。 
* id: str
    

"""

OrganizationPluginCompatibilityTypeBottom = Dict[str, Any]
"""


Kyes of Dict

* type: str
    inputに指定した場合、いずれのプラグインも前段になれないことを示します。 outputに指定した場合、いずれのプラグインも後段になれないことを示します。 

"""

OrganizationPluginCompatibilityTypeConstant = Dict[str, Any]
"""


Kyes of Dict

* type: str
    Constant型で、かつidの値が一致している場合に互換性があることを示します。 
* id: str
    

"""

OrganizationPluginCompatibilityTypeTop = Dict[str, Any]
"""


Kyes of Dict

* type: str
    inputに指定した場合、あらゆるプラグインの後段になれることを示します。 outputに指定した場合、入力がTopであるプラグインだけが後段になれることを示します。 

"""

OrganizationPluginList = Dict[str, Any]
"""


Kyes of Dict

* list: List[OrganizationPlugin]
    プラグイン一覧
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるプロジェクトが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: List[__DictStrKeyAnyValue__]
    システム内部用のプロパティ。 

"""

OrganizationRegistrationRequest = Dict[str, Any]
"""


Kyes of Dict

* organization_name: str
    組織名。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* organization_email: str
    メールアドレス
* price_plan: PricePlan
    

"""

OverlappedRangeAnnotation = Dict[str, Any]
"""
区間が重複しているアノテーションが存在している場合に発生するエラー

Kyes of Dict

* label_id: str
    
* annotation_id: str
    
* type: str
    OverlappedRangeAnnotation

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

PluginDetail = Dict[str, Any]
"""
* `PluginDetailAnnotationEditor` - カスタムアノテーションエディタ用のプラグインを表します。 * `PluginDetailTaskAssignment` - カスタムタスク割当用のプラグインを表します。 * `PluginDetailAnnotationSpecs` - カスタムアノテーション仕様用のプラグインを表します。 * `PluginDetailExtendedAnnotationSpecs` - カスタムのアノテーション種別を作成するプラグインを表します。 

Kyes of Dict

* url: str
    カスタムアノテーション仕様画面の URL です。 プラグイン種別がカスタムアノテーション仕様の場合のみ有効です。  この URL には、プロジェクトを特定するための以下のパラメータを必ず埋め込んでください。  * `{projectId}` 
* auth_redirect_url: str
    認証後のリダイレクト先 
* compatible_input_data_types: List[InputDataType]
    プラグインが対応している入力データです。 プラグイン種別がカスタムアノテーションエディタ、またはカスタムアノテーション仕様の場合のみ有効です。 
* type: str
    `ExtendedAnnotationSpecs` [詳しくはこちら](#section/API-Convention/API-_type) 
* plugin_compatibility: OrganizationPluginCompatibility
    
* annotation_types: List[AnnotationType]
    プラグインを使用したプロジェクトで選択可能なアノテーション種別のリストです。 同じ種別を重複して設定することはできません。 
* user_defined_annotation_type_definitions: PluginDetailExtendedAnnotationSpecsUserDefinedAnnotationTypeDefinitions
    

"""

PluginDetailAnnotationEditor = Dict[str, Any]
"""
カスタムアノテーションエディタ用のプラグインを表します。 

Kyes of Dict

* url: str
    カスタムアノテーションエディタでタスクを開くための URL です。 プラグインを使用するプロジェクトのタスク一覧などで使用されます。 プラグイン種別がカスタムアノテーションエディタの場合のみ有効です。  この URL には、タスクを特定するための以下のパラメータを必ず埋め込んでください。  * `{projectId}` * `{taskId}`  以下のパラメーターは任意で指定します。  * `{inputDataId}`: アノテーション一覧などから、特定の入力データにフォーカスした状態でタスクを開くときなどに指定します。 * `{annotationId}`: アノテーション一覧などから、特定のアノテーションにフォーカスした状態でタスクを開くときなどに指定します。 
* auth_redirect_url: str
    認証後のリダイレクト先。このURLに `?code=xxx` をつけてリダイレクトされます。 url プロパティとは異なり、 `{projectId}` や `{taskId}` といったパラメータの置換は行われません。  詳しくは [requestPluginToken API](#operation/requestPluginToken) を参照してください。 
* compatible_input_data_types: List[InputDataType]
    プラグインが対応している入力データです。 プラグイン種別がカスタムアノテーションエディタ、またはカスタムアノテーション仕様の場合のみ有効です。 
* type: str
    `AnnotationEditor` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

PluginDetailAnnotationSpecs = Dict[str, Any]
"""
カスタムアノテーション仕様用のプラグインを表します。 

Kyes of Dict

* url: str
    カスタムアノテーション仕様画面の URL です。 プラグイン種別がカスタムアノテーション仕様の場合のみ有効です。  この URL には、プロジェクトを特定するための以下のパラメータを必ず埋め込んでください。  * `{projectId}` 
* auth_redirect_url: str
    認証後のリダイレクト先 
* compatible_input_data_types: List[InputDataType]
    プラグインが対応している入力データです。 プラグイン種別がカスタムアノテーションエディタ、またはカスタムアノテーション仕様の場合のみ有効です。 
* type: str
    `AnnotationSpecs` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

PluginDetailExtendedAnnotationSpecs = Dict[str, Any]
"""
カスタムのアノテーション種別を作成するプラグインを表します。 なお、このプラグインが設定されているプロジェクトでは、ここで指定したアノテーション種別以外は使用できなくなります。 

Kyes of Dict

* plugin_compatibility: OrganizationPluginCompatibility
    
* annotation_types: List[AnnotationType]
    プラグインを使用したプロジェクトで選択可能なアノテーション種別のリストです。 同じ種別を重複して設定することはできません。 
* user_defined_annotation_type_definitions: PluginDetailExtendedAnnotationSpecsUserDefinedAnnotationTypeDefinitions
    
* compatible_input_data_types: List[InputDataType]
    プラグインが対応している入力データです。 プラグイン種別がカスタムアノテーションエディタ、またはカスタムアノテーション仕様の場合のみ有効です。 
* type: str
    `ExtendedAnnotationSpecs` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

PluginDetailExtendedAnnotationSpecsUserDefinedAnnotationTypeDefinitions = Dict[str, Any]
"""


Kyes of Dict

* annotation_type_definitions: UserDefinedAnnotationTypeDefinition
    

"""

PluginDetailTaskAssignment = Dict[str, Any]
"""
カスタムタスク割当用のプラグインを表します。 

Kyes of Dict

* url: str
    「カスタムタスク割当API」のURLです。 プラグイン種別がカスタムタスク割当の場合のみ有効です。  #### カスタムタスク割当APIについて。  * 独自のアルゴリズムで作業者にタスクを割当するAPIです。 * Annofabから提供されるものではなく、第三者 (ユーザー様) が用意します。 * 作業者がタスク一覧やアノテーションエディタのタスク取得ボタンを押すと、指定したURLに複数の情報 (※1) と共にHTTPリクエスト (POST) が送られます。 * カスタムタスク割当APIでは、Annofabで提供しているAPI (※2) を使用して作業者にタスクを割当してください。 * タスクの割当に成功した場合は以下のHTTPレスポンスを返却してください。   * レスポンスヘッダ: `Access-Control-Allow-Origin: https://annofab.com`   * レスポンスボディ: 割当した単一のタスク   * ステータスコード: 200 * 作業者に割当できるタスクがない場合は以下のHTTPレスポンスを返却してください。   * レスポンスヘッダ: `Access-Control-Allow-Origin: https://annofab.com`   * レスポンスボディ: `{\"errors\": [{\"error_code\": \"MISSING_RESOURCE\"}]}`   * ステータスコード: 404 * 作業者の認証トークンの期限が切れている場合があります。その場合は以下のHTTPレスポンスを返却してください。   * レスポンスヘッダ: `Access-Control-Allow-Origin: https://annofab.com`   * レスポンスボディ: `{\"errors\": [{\"error_code\": \"EXPIRED_TOKEN\"}]}`   * ステータスコード: 401  #### Preflightリクエストについて。  * Annofabからカスタムタスク割当APIへCross-OriginなHTTPリクエストを送信するより前に、ブラウザの仕様により「Preflightリクエスト」と呼ばれるHTTPリクエストが送られます。 * カスタムタスク割当を利用するためには、カスタムタスク割当APIとは別に「Preflightリクエスト対応API」を用意する必要があります。 * 以下の要件を満たす「Preflightリクエスト対応API」を用意してください。   * URL: カスタムタスク割当APIと同じURL   * HTTPメソッド: OPTIONS   * レスポンスヘッダ:     * `Access-Control-Allow-Origin: https://annofab.com`     * `Access-Control-Allow-Headers: Content-Type`   * レスポンスボディ: 空(から)   * ステータスコード: 200  ※1 以下の情報が送られます。  * HTTPボディ (JSON形式)   * `authorization_token` : タスク割当専用の認証トークン。AnnofabのAPIを利用する際に使用します。   * `project_id` : タスクの割当リクエストが行われたプロジェクトのID。   * `phase` : 作業者が割当を要求したタスクフェーズ。このフェーズのタスクを割当してください。  ※2 例えば以下のAPIがあります。(詳しい情報はAPIドキュメントを参照してください)  * `getMyAccount` : 作業者のアカウント情報を取得できます。 * `getTasks` : プロジェクトのタスクを取得できます。 * `assignTasks` : 作業者にタスクを割当することができます。 
* type: str
    `TaskAssignment` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

PluginTokenRequest = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `RefreshToken` を指定します
* authorization_code: str
    リダイレクト時にクエリパラメータ `code` として受け取った文字列
* code_verifier: str
    認可リクエスト時に渡した `code_challenge` に対応するverifier文字列
* refresh_token: str
    前回のトークン発行で得られた `refresh_token`

"""

PluginTokenRequestAuthorizationCode = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `AuthorizationCode` を指定します
* authorization_code: str
    リダイレクト時にクエリパラメータ `code` として受け取った文字列
* code_verifier: str
    認可リクエスト時に渡した `code_challenge` に対応するverifier文字列

"""

PluginTokenRequestRefreshToken = Dict[str, Any]
"""


Kyes of Dict

* type: str
    `RefreshToken` を指定します
* refresh_token: str
    前回のトークン発行で得られた `refresh_token`

"""

PluginTokenResponse = Dict[str, Any]
"""


Kyes of Dict

* access_token: str
    APIアクセスに用いるトークン。 リクエストヘッダにおいて `Authorization: Bearer {access_token}` の形で指定します。 
* refresh_token: str
    トークンの更新に用いるトークン

"""

Point = Dict[str, Any]
"""
点の座標値

Kyes of Dict

* x: int
    X座標の値[ピクセル]
* y: int
    Y座標の値[ピクセル]

"""

PositionForMinimumBoundingBoxInsertion = Dict[str, Any]
"""
`annotation_type` が `bounding_box` かつ `min_warn_rule` が `and` または `or` の場合のみ、挿入する最小矩形アノテーションの原点を指定できます。 画像左上の座標が「x=0, y=0」です。 未指定、もしくは「画像外に飛び出たアノテーション」を許可していないにも関わらず飛び出してしまう場合は、表示範囲の中央に挿入されます。 「スキャンした帳票の記入欄」や「定点カメラで撮影した製品ラベル」など、アノテーションしたい位置やサイズが多くの画像で共通している場合に便利です。  `annotation_type` が `bounding_box` 以外の場合は必ず未指定となります。 

Kyes of Dict

* x: int
    
* y: int
    

"""

PostAnnotationArchiveUpdateResponse = Dict[str, Any]
"""


Kyes of Dict

* job: ProjectJobInfo
    

"""

PostAnnotationArchiveUpdateResponseWrapper = Dict[str, Any]
"""


Kyes of Dict

* message: str
    メッセージ
* message_id: str
    システム内部用のプロパティ
* job: ProjectJobInfo
    

"""

PostProjectTasksUpdateResponse = Dict[str, Any]
"""


Kyes of Dict

* job: ProjectJobInfo
    

"""


class PricePlan(Enum):
    """
    料金プラン * `free` - フリープラン * `business` - ビジネスプラン
    """

    FREE = "free"
    BUSINESS = "business"


Project = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* title: str
    プロジェクトのタイトル
* overview: str
    プロジェクトの概要
* project_status: ProjectStatus
    
* input_data_type: InputDataType
    
* configuration: ProjectConfiguration
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時
* summary: ProjectSummary
    

"""

ProjectAccountStatistics = Dict[str, Any]
"""


Kyes of Dict

* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* histories: List[ProjectAccountStatisticsHistory]
    

"""

ProjectAccountStatisticsHistory = Dict[str, Any]
"""


Kyes of Dict

* date: str
    
* tasks_completed: int
    教師付フェーズのタスクを提出した回数、または検査/受入フェーズのタスクを合格/差戻にした回数。  たとえば、あるタスクのタスク履歴が下表の状態だった場合、2020-04-01の`tasks_completed`は以下の通りになります。  * Alice: 1 * Bob: 1 * Chris: 2   <table>   <tr>     <th>担当者</th>     <th>フェーズ</th>     <th>作業内容</th>     <th>完了日時</th>   </tr>   <tr>     <td>Alice</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 09:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>差し戻す</td>     <td>2020-04-01 10:00</td>   </tr>   <tr>     <td>Bob</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 11:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>合格にする</td>     <td>2020-04-01 12:00</td>   </tr> </table> 
* tasks_rejected: int
    教師付フェーズを担当したタスクが差し戻された回数、または受入フェーズを担当したタスクが受入完了を取り消された回数。  たとえば、あるタスクのタスク履歴が下表の状態だった場合、2020-04-01の`tasks_rejected`は以下の通りになります。  * Alice: 1 * Bob: 1 * Chris: 1   <table>   <tr>     <th>担当者</th>     <th>フェーズ</th>     <th>作業内容</th>     <th>完了日時</th>   </tr>   <tr>     <td>Alice</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 09:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>差し戻す</td>     <td>2020-04-01 10:00</td>   </tr>   <tr>     <td>Bob</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 11:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>差し戻す</td>     <td>2020-04-01 12:00</td>   </tr>   <tr>     <td>Bob</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 13:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>合格にする</td>     <td>2020-04-01 14:00</td>   </tr>   <tr>     <td>Dave</td>     <td>受入</td>     <td>受入完了状態を取り消して、再度合格にする</td>     <td>2020-04-01 15:00</td>   </tr> </table> 
* worktime: str
    作業時間（ISO 8601 duration）

"""

ProjectCacheRecord = Dict[str, Any]
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

ProjectConfiguration = Dict[str, Any]
"""
プロジェクトの設定情報

Kyes of Dict

* number_of_inspections: int
    検査回数。 * 0回：教師付け -> 受入 * 1回：教師付け -> 検査 -> 受入 * n回(n >= 2)：教師付け -> 検査1 -> ... -> 検査n -> 受入 
* assignee_rule_of_resubmitted_task: AssigneeRuleOfResubmittedTask
    
* task_assignment_type: TaskAssignmentType
    
* task_assignment_property: TaskAssignmentProperty
    
* max_tasks_per_member: int
    保留中のタスクを除き、1人（オーナー以外）に割り当てられるタスク数の上限。 
* max_tasks_per_member_including_hold: int
    保留中のタスクを含めて、1人（オーナー以外）に割り当てられるタスク数上限の保留分。 割り当て時の上限チェックは、max_tasks_per_memberとこの数字の合計で行われます。  例えばmax_tasks_per_memberが10、max_tasks_per_member_including_holdが20の場合、保留中を含むタスク数の割り当て上限は30になります。 
* input_data_set_id_list: List[str]
    システム内部用のプロパティ。 [putProject](#operation/putProject) APIでプロジェクトを更新する際は、[getProject](#operation/getProject) APIで取得した値を指定してください。 
* input_data_max_long_side_length: int
    入力データ画像の長辺の最大値（未指定時は4096px）。  画像をアップロードすると、長辺がこの値になるように画像が自動で圧縮されます。 アノテーションの座標は、もとの解像度の画像でつけたものに復元されます。  大きな数値を設定すると入力データ画像のサイズが大きくなり、生産性低下やブラウザで画像を表示できない懸念があります。注意して設定してください。 
* sampling_inspection_rate: int
    抜取検査率[%]。未指定の場合は100%として扱う。
* sampling_acceptance_rate: int
    抜取受入率[%]。未指定の場合は100%として扱う。
* private_storage_aws_iam_role_arn: str
    AWS IAMロール。ビジネスプランでのS3プライベートストレージの認可で使います。 [S3プライベートストレージの認可の設定についてはこちら](/docs/faq/#m0b240)をご覧ください。 
* plugin_id: str
    プラグインID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* custom_task_assignment_plugin_id: str
    プラグインID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* custom_specs_plugin_id: str
    プラグインID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* editor_version: str
    標準アノテーションエディタのバージョン。  * `stable`     * 安定版。通常はこちらを利用してください。 * `preview`     * 最新版。新機能やUI変更の先行リリース版。  プロジェクト更新時に未指定の場合は `stable` が指定されたものとみなします。 
* use_beginner_navigation: bool
    true の場合、プロジェクトの画面でナビゲーションUIを表示します（ログインユーザーがプロジェクトオーナーの場合のみ）。 

"""

ProjectContainer = Dict[str, Any]
"""


Kyes of Dict

* list: List[Project]
    
* has_next: bool
    

"""

ProjectCopyRequest = Dict[str, Any]
"""


Kyes of Dict

* dest_project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* dest_title: str
    コピー先プロジェクトのタイトル
* dest_overview: str
    コピー先プロジェクトの概要
* copy_inputs: bool
    「入力データ」をコピーするかどうかを指定します。 
* copy_tasks: bool
    「タスク」をコピーするかどうかを指定します。  この属性の値を`true`にする場合、他の属性の値を必ず次のように指定してください。  * `copy_inputs`の値を`true`とする 
* copy_annotations: bool
    「アノテーション」をコピーするかどうかを指定します。  この属性の値を`true`にする場合、他の属性の値を必ず次のように指定してください。  * `copy_inputs`の値を`true`とする * `copy_tasks`の値を`true`とする 
* copy_webhooks: bool
    「Webhook」をコピーするかどうかを指定します。 
* copy_supplementary_data: bool
    「補助情報」をコピーするかどうかを指定します。  この属性の値を`true`にする場合、他の属性の値を必ず次のように指定してください。  * `copy_inputs`の値を`true`とする 
* copy_instructions: bool
    「作業ガイド」をコピーするかどうかを指定します。 

"""

ProjectCopyResponse = Dict[str, Any]
"""


Kyes of Dict

* job: ProjectJobInfo
    
* dest_project: Project
    

"""

ProjectGuestUserProfile = Dict[str, Any]
"""
ゲストユーザーのプロフィール情報

Kyes of Dict

* user_id: str
    ゲストユーザーのIDです。 同じ文字列の場合、同じゲストユーザーとして認識されます。 [値の制約についてはこちら。](#section/API-Convention/APIID)
* user_name: str
    ユーザー名
* lang: str
    ゲストユーザーのUIの表示言語です
* key_layout: KeyLayout
    

"""

ProjectInputsUpdateResponse = Dict[str, Any]
"""


Kyes of Dict

* job: ProjectJobInfo
    

"""

ProjectJobInfo = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* job_type: ProjectJobType
    
* job_id: str
    ジョブID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* job_status: JobStatus
    
* job_execution: __DictStrKeyAnyValue__
    ジョブの内部情報
* job_detail: __DictStrKeyAnyValue__
    ジョブ結果の内部情報
* errors: Errors
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

ProjectJobInfoContainer = Dict[str, Any]
"""


Kyes of Dict

* list: List[ProjectJobInfo]
    バックグラウンドジョブの一覧。作成日時の降順でソートされています。
* has_next: bool
    さらに古いジョブが存在する場合は`true`です。取得したジョブ一覧の中で`created_datetime`が最も古い値を、クエリパラメータ`exclusive_start_created_datetime`に指定することで、さらに古いジョブを取得することができます。

"""


class ProjectJobType(Enum):
    """
    プロジェクトのジョブの種別 * `copy-project` - プロジェクトのコピー。[initiateProjectCopy](#operation/initiateProjectCopy) APIを実行したときに登録されるジョブ。 * `gen-inputs` - zipファイルから入力データの作成。[putInputData](#operation/putInputData) APIを実行して、zipファイルから入力データを作成したときに登録されるジョブ。 * `gen-tasks` - タスクの一括作成。[initiateTasksGeneration](#operation/initiateTasksGeneration) APIを実行したときに登録されるジョブ。 * `gen-annotation` - アノテーションZIPの更新。[postAnnotationArchiveUpdate](#operation/postAnnotationArchiveUpdate) APIを実行したときに登録されるジョブ。 * `gen-tasks-list` - タスク全件ファイルの更新。[postProjectTasksUpdate](#operation/postProjectTasksUpdate) APIを実行したときに登録されるジョブ。 * `gen-inputs-list` - 入力データ情報全件ファイルの更新。[postProjectInputsUpdate](#operation/postProjectInputsUpdate) APIを実行したときに登録されるジョブ。 * `delete-project` - プロジェクトの削除。[deleteProject](#operation/deleteProject) APIを実行したときに登録されるジョブ。 * `invoke-hook` - Webhookの起動。 * `move-project` - プロジェクトの組織移動。[putProject](#operation/putProject) API で組織を変更したときに登録されるジョブ。  ## ジョブの同時実行制限  Annofab上に登録されているデータの整合性を保つため、プロジェクト内で特定のジョブが実行中の間は他のジョブが実行できないよう制限をかけています。  ジョブの同時実行可否はジョブの種別によって異なります。  なお、ジョブを実行するプロジェクトが初期化中 (`project_status = \"initializing\"`) の場合は、どのジョブも実行できません。  ### copy-project 次のジョブが実行されている場合、このジョブを実行することはできません。  * `gen-inputs` * `gen-tasks` * `delete-project` * `move-project`  ### gen-inputs 次のジョブが実行されている場合、このジョブを実行することはできません。  * `copy-project` * `gen-inputs` * `gen-tasks` * `gen-inputs-list` * `delete-project` * `move-project`  ### gen-tasks 次のジョブが実行されている場合、このジョブを実行することはできません。  * `copy-project` * `gen-inputs` * `gen-tasks` * `gen-annotation` * `gen-tasks-list` * `delete-project` * `move-project`  ### gen-annotation 次のジョブが実行されている場合、このジョブを実行することはできません。  * `gen-tasks` * `gen-annotation` * `delete-project` * `move-project`  ### gen-tasks-list 次のジョブが実行されている場合、このジョブを実行することはできません。  * `gen-tasks` * `gen-tasks-list` * `delete-project` * `move-project`  ### gen-inputs-list 次のジョブが実行されている場合、このジョブを実行することはできません。  * `gen-inputs` * `gen-inputs-list` * `delete-project` * `move-project`  ### delete-project 他のジョブが実行されていない場合**のみ**実行できます。  ### invoke-hook 次のジョブが実行されている場合、このジョブを実行することはできません。  * `delete-project` * `move-project`  ### move-project 他のジョブが実行されていない場合**のみ**実行できます。
    """

    COPY_PROJECT = "copy-project"
    GEN_INPUTS = "gen-inputs"
    GEN_TASKS = "gen-tasks"
    GEN_ANNOTATION = "gen-annotation"
    GEN_TASKS_LIST = "gen-tasks-list"
    GEN_INPUTS_LIST = "gen-inputs-list"
    DELETE_PROJECT = "delete-project"
    INVOKE_HOOK = "invoke-hook"
    MOVE_PROJECT = "move-project"


ProjectList = Dict[str, Any]
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
    システム内部用のプロパティ 

"""

ProjectMember = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* username: str
    ユーザー名
* member_status: ProjectMemberStatus
    
* member_role: ProjectMemberRole
    
* biography: str
    人物紹介、略歴。  この属性は、Annofab外の所属先や肩書などを表すために用います。 Annofab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 
* updated_datetime: str
    更新日時
* created_datetime: str
    作成日時
* sampling_inspection_rate: int
    抜取検査率（パーセント）
* sampling_acceptance_rate: int
    抜取受入率（パーセント）

"""

ProjectMemberList = Dict[str, Any]
"""


Kyes of Dict

* list: List[ProjectMember]
    プロジェクトメンバーの一覧
* page_no: float
    現在のページ番号。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるプロジェクトメンバーが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: List[AggregationResult]
    システム内部用のプロパティ 

"""

ProjectMemberRequest = Dict[str, Any]
"""


Kyes of Dict

* member_status: ProjectMemberStatus
    
* member_role: ProjectMemberRole
    
* sampling_inspection_rate: int
    抜取検査率（パーセント）
* sampling_acceptance_rate: int
    抜取受入率（パーセント）
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""


class ProjectMemberRole(Enum):
    """
    プロジェクトメンバーのロール * `owner` - オーナー * `worker` - アノテーター * `accepter` - チェッカー * `training_data_user` - アノテーションユーザー
    """

    OWNER = "owner"
    WORKER = "worker"
    ACCEPTER = "accepter"
    TRAINING_DATA_USER = "training_data_user"


class ProjectMemberStatus(Enum):
    """
    プロジェクトメンバーの状態 * `active` - プロジェクトメンバーとして有効で、プロジェクトを閲覧したり、権限があれば編集できます。 * `inactive` - 脱退したプロジェクトメンバーを表します。プロジェクトを閲覧できません。
    """

    ACTIVE = "active"
    INACTIVE = "inactive"


class ProjectStatus(Enum):
    """
    プロジェクトの状態 * `active` - プロジェクトが進行中 * `suspended` - プロジェクトが停止中 * `initializing` - プロジェクトが初期化中
    """

    ACTIVE = "active"
    SUSPENDED = "suspended"
    INITIALIZING = "initializing"


ProjectSummary = Dict[str, Any]
"""
プロジェクトのサマリー情報

Kyes of Dict

* last_tasks_updated_datetime: str
    タスクの最終更新日時

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
    日付
* tasks: List[ProjectTaskStatistics]
    タスクのフェーズごと、ステータスごとの情報

"""

ProjectToken = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトトークンの発行対象プロジェクトID
* token: str
    プロジェクトトークン文字列。 [issueProjectGuestUserToken](#operation/issueProjectGuestUserToken)への入力となります。
* info: ProjectTokenInfo
    

"""

ProjectTokenInfo = Dict[str, Any]
"""
プロジェクトトークンについての付加情報

Kyes of Dict

* created_date_time: str
    トークンの作成日時
* last_used_date_time: str
    トークンが最後に利用された日時
* description: str
    トークンについての人間可読な説明

"""

PutAnnotationRequest = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: List[AnnotationDetailV1]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutInputDataSetRequest = Dict[str, Any]
"""
入力データセット新規作成/更新

Kyes of Dict

* input_data_set_name: str
    入力データセットの名前
* input_data_type: InputDataType
    
* private_storage_arn: str
    AWS IAMロール。ビジネスプランでのS3プライベートストレージの認可で使います。 [S3プライベートストレージの認可の設定についてはこちら](/docs/faq/#m0b240)をご覧ください。 
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutInstructionRequest = Dict[str, Any]
"""


Kyes of Dict

* html: str
    作業ガイドのHTML
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutMarkersRequest = Dict[str, Any]
"""


Kyes of Dict

* markers: List[Marker]
    マーカー一覧
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutMyAccountRequest = Dict[str, Any]
"""


Kyes of Dict

* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* username: str
    ユーザー名
* lang: Lang
    
* keylayout: KeyLayout
    
* biography: str
    人物紹介、略歴。  この属性は、Annofab外の所属先や肩書などを表すために用います。 Annofab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 
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

PutOrganizationPluginRequest = Dict[str, Any]
"""


Kyes of Dict

* plugin_name: str
    プラグインの名前です。 プラグイン一覧や、プロジェクトで使うプラグインを選ぶときなどに表示されます。 
* description: str
    プラグインの説明です。 プラグイン一覧や、プロジェクトで使うプラグインを選ぶときなどに表示されます。 
* detail: PluginDetail
    
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutOrganizationRequest = Dict[str, Any]
"""


Kyes of Dict

* organization_name: str
    組織名。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutProjectRequest = Dict[str, Any]
"""


Kyes of Dict

* title: str
    プロジェクトのタイトル
* overview: str
    プロジェクトの概要
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

PutProjectResponse = Dict[str, Any]
"""


Kyes of Dict

* job: ProjectJobInfo
    
* project: Project
    

"""

PutWebhookRequest = Dict[str, Any]
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
    Webhookが送信するHTTPリクエストのヘッダー
* body: str
    Webhookが送信するHTTPリクエストのボディ
* url: str
    Webhookの送信先URL
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

RefreshTokenRequest = Dict[str, Any]
"""


Kyes of Dict

* refresh_token: str
    リフレッシュトークン。[login](#operation/login) APIで取得します。 

"""

ReplyComment = Dict[str, Any]
"""


Kyes of Dict

* root_comment_id: str
    コメントのID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* type: str
    `Reply` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

ReplyRequired = Dict[str, Any]
"""
返信が必要な検査コメントが残っている時のエラー

Kyes of Dict

* inspection: Inspection
    
* type: str
    ReplyRequired

"""

ResetEmailRequest = Dict[str, Any]
"""


Kyes of Dict

* email: str
    

"""

Resolution = Dict[str, Any]
"""


Kyes of Dict

* width: int
    画像の幅[ピクセル]
* height: int
    画像の高さ[ピクセル]

"""

RevokeProjectTokenRequest = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    無効化するトークンが所属しているプロジェクトのID
* project_token: str
    [issueProjectToken](#operation/issueProjectToken)で発行されたトークン文字列

"""

RootComment = Dict[str, Any]
"""


Kyes of Dict

* data: InspectionData
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* status: CommentStatus
    
* type: str
    `Root` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

SegmentationMetadata = Dict[str, Any]
"""
塗りつぶしアノテーションのメタデータ

Kyes of Dict

* min_width: int
    幅の最小値[ピクセル]
* min_height: int
    高さの最小値[ピクセル]
* min_warn_rule: str
    サイズの制約に関する情報 * `none` - 制約なし * `or` - 幅と高さの両方が最小値以上 * `and` - 幅と高さのどちらか一方が最小値以上 
* tolerance: int
    許容誤差[ピクセル]

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
    アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、Annofabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 
* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_phase: TaskPhase
    
* task_phase_stage: int
    タスクのフェーズのステージ番号
* task_status: TaskStatus
    
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_name: str
    入力データ名
* details: List[SimpleAnnotationDetail]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    更新日時。アノテーションが一つもない場合（教師付作業が未着手のときなど）は、未指定。

"""

SimpleAnnotationDetail = Dict[str, Any]
"""


Kyes of Dict

* label: str
    アノテーション仕様で設定したラベル名 (英語) です。 
* annotation_id: str
    個々のアノテーションにつけられたIDです。 
* data: FullAnnotationData
    
* attributes: __DictStrKeyAnyValue__
    キーと値が以下のようになっている辞書構造です。  * キー: アノテーション仕様で設定した属性名 (英語) * 値: 各属性の値   * 選択肢を定義している場合、その選択肢の表示名 (英語)   * それ以外は属性値そのまま (文字列、数値、論理値) 

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
    更新日時

"""

SingleAnnotationDetail = Dict[str, Any]
"""
アノテーション情報 

Kyes of Dict

* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* data_holding_type: AnnotationDataHoldingType
    
* data: FullAnnotationData
    
* etag: str
    data_holding_typeがouterの場合のみ存在し、データのETagが格納される
* url: str
    data_holding_typeがouterの場合のみ存在し、データへの一時URLが格納される
* additional_data_list: List[AdditionalDataV1]
    属性情報。  アノテーション属性の種類（`additional_data_definition`の`type`）によって、属性値を格納するプロパティは変わります。  | 属性の種類 | `additional_data_definition`の`type` | 属性値を格納するプロパティ                    | |------------|-------------------------|----------------------| | ON/OFF | flag       | flag                                          | | 整数 | integer    | integer                                       | | 自由記述（1行）| text       | comment                                       | | 自由記述（複数行）| comment    | comment                                       | | トラッキングID  | tracking | comment                                       | | アノテーションリンク    | link   | comment                                       | | 排他選択（ラジオボタン）  |choice   | choice                                        | | 排他選択（ドロップダウン） | select    | choice                                        | 
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

SupplementaryData = Dict[str, Any]
"""


Kyes of Dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_set_id: str
    入力データセットID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* supplementary_data_id: str
    補助情報ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* supplementary_data_name: str
    補助情報の名前
* supplementary_data_path: str
    補助情報の実体が存在するパスです。 s3スキーマまたはhttpsスキーマのみサポートしています。 
* url: str
    システム内部用のプロパティ
* etag: str
    [HTTPレスポンスヘッダー ETag](https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/ETag)に相当する値です。 
* supplementary_data_type: SupplementaryDataType
    
* supplementary_data_number: int
    補助情報の表示順を表す数値。
* updated_datetime: str
    更新日時

"""

SupplementaryDataRequest = Dict[str, Any]
"""


Kyes of Dict

* supplementary_data_name: str
    補助情報の名前
* supplementary_data_path: str
    補助情報の実体が存在するURLです。 補助情報の実体をAnnofabにアップロードする場合は、[createTempPath](#operation/createTempPath) APIで取得した`path`を指定してください。  補助情報の実体が[プライベートストレージ](/docs/faq/#prst9c)に存在する場合は、S3スキーマまたはHTTPSスキーマのURLを指定してください。 補助情報の実体が、S3プライベートストレージに存在するファイルを補助情報として登録する場合は、[事前に認可の設定](/docs/faq/#m0b240)が必要です。 
* supplementary_data_type: SupplementaryDataType
    
* supplementary_data_number: int
    補助情報の表示順を表す数値。同じ入力データに対して複数の補助情報で表示順が重複する場合、順序不定になります。
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""


class SupplementaryDataType(Enum):
    """
    補助情報の種類 * `image` - 画像 * `text` - テキスト * `custom` - カスタム（カスタムプロジェクトでしか利用できません）
    """

    IMAGE = "image"
    TEXT = "text"
    CUSTOM = "custom"


SystemMetadata = Dict[str, Any]
"""
Annofabが設定したメタデータです。 `metadata`プロパティとは違い、ユーザー側では値を編集できません。  * `SystemMetadataImage`: 画像プロジェクト用のメタデータ * `SystemMetadataMovie`: 動画プロジェクト用のメタデータ * `SystemMetadataCustom`: カスタムプロジェクト用のメタデータ 

Kyes of Dict

* original_resolution: Resolution
    
* resized_resolution: Resolution
    
* type: str
    `Custom`
* input_duration: float
    動画の長さ[秒]。 動画の長さが取得できなかった場合は、設定されません。 

"""

SystemMetadataCustom = Dict[str, Any]
"""
カスタムデータ用システムメタデータ。 現行はプロパティがない形式的なオブジェクトです。 

Kyes of Dict

* type: str
    `Custom`

"""

SystemMetadataImage = Dict[str, Any]
"""
画像データ用システムメタデータ。 

Kyes of Dict

* original_resolution: Resolution
    
* resized_resolution: Resolution
    
* type: str
    `Image`

"""

SystemMetadataMovie = Dict[str, Any]
"""
動画データ用システムメタデータ。 

Kyes of Dict

* input_duration: float
    動画の長さ[秒]。 動画の長さが取得できなかった場合は、設定されません。 
* type: str
    `Movie`

"""

Task = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* phase: TaskPhase
    
* phase_stage: int
    タスクのフェーズのステージ番号
* status: TaskStatus
    
* input_data_id_list: List[str]
    タスクに含まれる入力データのID
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* histories_by_phase: List[TaskHistoryShort]
    簡易的なタスク履歴（あるフェーズを誰が担当したか）
* work_time_span: int
    累計実作業時間(ミリ秒)
* number_of_rejections: int
    このタスクが差戻しされた回数（すべてのフェーズでの差戻し回数の合計  このフィールドは、どのフェーズで何回差戻されたかを区別できないため、廃止予定です。 `histories_by_phase` で各フェーズの回数を計算することで、差戻し回数が分かります。  例）`acceptance`フェーズが3回ある場合、`acceptance`フェーズで2回差し戻しされたことになります。 
* started_datetime: str
    現在のフェーズが開始された日時
* updated_datetime: str
    更新日時
* operation_updated_datetime: str
    タスクのステータスやフェーズ、担当者などが更新されたときの日時
* sampling: str
    検査抜取検査/抜取受入によって、どのフェーズがスキップされたか  * `inspection_skipped` - 抜取検査の対象外となり、検査フェーズがスキップされた * `inspection_stages_skipped` - 抜取検査の対象外となり、検査フェーズのステージの一部がスキップされた * `acceptance_skipped` - 抜取受入の対象外となり、受入フェーズがスキップされた * `inspection_and_acceptance_skipped` - 抜取検査・抜取受入の対象外となり、検査・受入フェーズがスキップされた  未指定ならば、どのフェーズもスキップされていません。 
* metadata: dict(str, __DictStrKeyAnyValue__)
    ユーザーが自由に登録できるkey-value型のメタデータです。 keyにはメタデータ名、valueには値を指定してください。  keyに指定できる文字種は次の通りです。  * 半角英数字 * `_` (アンダースコア) * `-` (ハイフン)  valueに指定できる値は次の通りです。  * 文字列 * 数値 * 真偽値 

"""

TaskAssignRequest = Dict[str, Any]
"""


Kyes of Dict

* request_type: TaskAssignRequestType
    

"""

TaskAssignRequestType = Dict[str, Any]
"""
* `TaskAssignRequestTypeRandom`: 自分自身にランダムにタスクを割り当てます。プロジェクト設定でタスクのランダム割当を有効にした場合のみ利用できます。 * `TaskAssignRequestTypeSelection`: メンバーに指定したタスクを割り当てます。ただし、メンバーはプロジェクトオーナーもしくはチェッカーロールを持つ必要があります。プロジェクト設定でタスクの選択割当を有効にした場合のみ利用できます。 * `TaskAssignRequestTypeTaskProperty`: タスクプロパティ割当の設定に基づいて、タスクを自分自身に割り当てます。プロジェクト設定でタスクプロパティ割当を有効にした場合のみ利用できます。 

Kyes of Dict

* phase: TaskPhase
    
* type: str
    `TaskProperty` 
* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_ids: List[str]
    割り当てるタスクのID

"""

TaskAssignRequestTypeRandom = Dict[str, Any]
"""


Kyes of Dict

* phase: TaskPhase
    
* type: str
    `Random` 

"""

TaskAssignRequestTypeSelection = Dict[str, Any]
"""


Kyes of Dict

* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_ids: List[str]
    割り当てるタスクのID
* type: str
    `Selection` 

"""

TaskAssignRequestTypeTaskProperty = Dict[str, Any]
"""


Kyes of Dict

* phase: TaskPhase
    
* type: str
    `TaskProperty` 

"""


class TaskAssignmentOrder(Enum):
    """
    タスクの割当優先度を決定するための並び順。  * `asc` -  昇順 * `desc` - 降順
    """

    ASC = "asc"
    DESC = "desc"


TaskAssignmentProperty = Dict[str, Any]
"""
プロジェクト設定でタスクプロパティ割当を有効にしている場合のみ指定してください。 

Kyes of Dict

* name: str
    タスクの割当優先度を決定するためのタスクプロパティ。  指定できるプロパティは次のいずれかです。  * `task_id` * `updated_datetime` * `metadata` (`metadata.{メタデータ名}` の形式で指定してください) 
* order: TaskAssignmentOrder
    

"""


class TaskAssignmentType(Enum):
    """
    プロジェクトで使用するタスクの割当方式。  * `random` -  タスクフェーズのみを指定してランダムにタスクを自身に割当する方式です。 * `selection` - 担当者とタスクを明示的に指定してタスクを割当する方式です。プロジェクトオーナーもしくはチェッカーのみ、自身以外のプロジェクトメンバーを担当者に指定できます。 * `random_and_selection` - ランダム割当と選択割当の両機能を使用する方式です。 * `task_property` - タスクのプロパティ(タスクID/更新日時/メタデータ)と並び順(昇順/降順)を設定して、その順番通りにタスクを割当する方式です。順番が同じタスクが複数ある場合は、その中からランダムに1つのタスクを割当します。プロパティと並び順は`TaskAssignmentProperty` から設定します。 * `custom` - タスク割当アルゴリズム (API) を独自に定義してタスクを割当する方式です。
    """

    RANDOM = "random"
    SELECTION = "selection"
    RANDOM_AND_SELECTION = "random_and_selection"
    TASK_PROPERTY = "task_property"
    CUSTOM = "custom"


TaskGenerateRequest = Dict[str, Any]
"""


Kyes of Dict

* task_generate_rule: TaskGenerateRule
    
* project_last_updated_datetime: str
    プロジェクトの最終更新日時（[getProject](#operation/getProject) APIのレスポンス `updated_datetime`）。タスク生成の排他制御に使用。

"""

TaskGenerateResponse = Dict[str, Any]
"""


Kyes of Dict

* job: ProjectJobInfo
    
* project: Project
    

"""

TaskGenerateResponseWrapper = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* title: str
    プロジェクトのタイトル
* overview: str
    プロジェクトの概要
* project_status: ProjectStatus
    
* input_data_type: InputDataType
    
* configuration: ProjectConfiguration
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時
* summary: ProjectSummary
    
* job: ProjectJobInfo
    
* project: Project
    

"""

TaskGenerateRule = Dict[str, Any]
"""
タスク生成のルール * `TaskGenerateRuleByCount`: 1つのタスクに割り当てる入力データの個数を指定してタスクを生成します。 * `TaskGenerateRuleByDirectory`: 入力データ名をファイルパスに見立てて、ディレクトリ単位でタスクを生成します。 * `TaskGenerateRuleByInputDataCsv`: 各タスクへの入力データへの割り当てを記入したCSVへのS3上のパスを指定してタスクを生成します。 

Kyes of Dict

* task_id_prefix: str
    タスクIDのプレフィックス。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* allow_duplicate_input_data: bool
    `true`のときは、既にタスクに使われている入力データも、新しいタスクに割り当てます。`false`のときは、既にタスクに使われている入力データを除外します。まだタスクに使われていない入力データだけを、新しいタスクに割り当てます。 
* input_data_count: int
    1つのタスクに割り当てる入力データの個数。 動画プロジェクトでは必ず`1`を指定してください。 
* input_data_order: InputDataOrder
    
* type: str
    `ByInputDataCsv` [詳しくはこちら](#section/API-Convention/API-_type) 
* input_data_name_prefix: str
    タスク生成対象の入力データ名のプレフィックス
* csv_data_path: str
    各タスクへの入力データへの割り当てを記入したCSVへのS3上のパス。 

"""

TaskGenerateRuleByCount = Dict[str, Any]
"""
1つのタスクに割り当てる入力データの個数を指定してタスクを生成します。

Kyes of Dict

* task_id_prefix: str
    タスクIDのプレフィックス。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* allow_duplicate_input_data: bool
    `true`のときは、既にタスクに使われている入力データも、新しいタスクに割り当てます。`false`のときは、既にタスクに使われている入力データを除外します。まだタスクに使われていない入力データだけを、新しいタスクに割り当てます。 
* input_data_count: int
    1つのタスクに割り当てる入力データの個数。 動画プロジェクトでは必ず`1`を指定してください。 
* input_data_order: InputDataOrder
    
* type: str
    `ByCount` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

TaskGenerateRuleByDirectory = Dict[str, Any]
"""
入力データ名をファイルパスに見立て、ディレクトリ単位でタスクを生成します。

Kyes of Dict

* task_id_prefix: str
    タスクIDのプレフィックス。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_name_prefix: str
    タスク生成対象の入力データ名のプレフィックス
* type: str
    `ByDirectory` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

TaskGenerateRuleByInputDataCsv = Dict[str, Any]
"""
各タスクへの入力データへの割当を記入したCSVへのS3上のパスを指定してタスクを生成します。 1つのタスクに対する入力データの個数は最大200です。200を超えるタスクが1つでもある場合にはタスク生成に失敗します。 

Kyes of Dict

* csv_data_path: str
    各タスクへの入力データへの割り当てを記入したCSVへのS3上のパス。 
* type: str
    `ByInputDataCsv` [詳しくはこちら](#section/API-Convention/API-_type) 

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
    タスク履歴ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* started_datetime: str
    開始日時
* ended_datetime: str
    終了日時
* accumulated_labor_time_milliseconds: str
    累計実作業時間（ISO 8601 duration）
* phase: TaskPhase
    
* phase_stage: int
    タスクのフェーズのステージ番号
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 

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
    タスク履歴ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* created_datetime: str
    作成日時
* phase: TaskPhase
    
* phase_stage: int
    タスクのフェーズのステージ番号
* status: TaskStatus
    
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* request: TaskOperation
    

"""

TaskHistoryShort = Dict[str, Any]
"""
タスクのあるフェーズを誰が担当したかを表します。

Kyes of Dict

* phase: TaskPhase
    
* phase_stage: int
    
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* worked: bool
    そのフェーズでタスクの作業を行ったかどうか（行った場合はtrue）

"""

TaskInputValidation = Dict[str, Any]
"""
タスクの提出操作に対する入力データID別のバリデーション結果です。

Kyes of Dict

* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* annotation_errors: List[ValidationError]
    
* inspection_errors: List[InspectionValidationError]
    

"""

TaskList = Dict[str, Any]
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
    [Aggregationによる集約結果](#section/API-Convention/AggregationResult)。 

"""

TaskOperation = Dict[str, Any]
"""


Kyes of Dict

* status: TaskStatus
    
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* force: bool
    タスクの強制操作を行うかどうか。 `status`が`rejected`のときのみ、`true`を指定できます。 

"""


class TaskPhase(Enum):
    """
    タスクのフェーズ * `annotation` - 教師付け * `inspection` - 検査 * `acceptance` - 受入
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
    日付
* phases: List[PhaseStatistics]
    タスクのフェーズごとの集計結果

"""

TaskRequest = Dict[str, Any]
"""


Kyes of Dict

* input_data_id_list: List[str]
    タスクに割り当てる入力データのID。タスクに割り当てることができる入力データの個数は最大200です。
* metadata: dict(str, __DictStrKeyAnyValue__)
    ユーザーが自由に登録できるkey-value型のメタデータです。 keyにはメタデータ名、valueには値を指定してください。  keyに指定できる文字種は次の通りです。  * 半角英数字 * `_` (アンダースコア) * `-` (ハイフン)  valueに指定できる値は次の通りです。  * 文字列 * 数値 * 真偽値 

"""


class TaskStatus(Enum):
    """
    タスクのステータス * `not_started` - 未着手 * `working` - 作業中 * `on_hold` - 保留中 * `break` - 休憩中 * `complete` - 完了 * `rejected` - 差し戻し。[operateTask](#operation/operateTask) APIのリクエストボディに渡すときのみ利用する。その他のAPIのリクエストやレスポンスには使われない。 * `cancelled` - 提出の取り消し。[operateTask](#operation/operateTask) APIのリクエストボディに渡すときのみ利用する。その他のAPIのリクエストやレスポンスには使われない。
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

TemporaryUrl = Dict[str, Any]
"""
認証済み一時URL

Kyes of Dict

* url: str
    このURLは発行から1時間経過すると無効になります。 

"""

Token = Dict[str, Any]
"""
トークン情報

Kyes of Dict

* id_token: str
    IDトークン。HTTPリクエストの`Authorization`ヘッダーにIDトークンを指定することで、APIは認証されます。
* access_token: str
    アクセストークン
* refresh_token: str
    リフレッシュトークン

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

UpdateOrganizationNameRequest = Dict[str, Any]
"""


Kyes of Dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* organization_name: str
    組織名。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

UsageStatus = Dict[str, Any]
"""
利用状況

Kyes of Dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* year_month: str
    対象月。年月のフォーマットは YYYY-MM です。
* aggregation_period_from: str
    集計期間の開始日時。日時のフォーマットはISO 8601 拡張形式です。
* aggregation_period_to: str
    集計期間の終了日時。日時のフォーマットはISO 8601 拡張形式です。
* editor_usage: List[EditorUsageTimespan]
    エディタ利用時間のリスト
* storage_usage: float
    ストレージ利用量。単位はGB時

"""

UsageStatusByDay = Dict[str, Any]
"""
日ごとの利用状況

Kyes of Dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* date: str
    対象日。日付のフォーマットはISO 8601 拡張形式です。
* aggregation_period_from: str
    集計期間の開始日時。日時のフォーマットはISO 8601 拡張形式です。
* aggregation_period_to: str
    集計期間の終了日時。日時のフォーマットはISO 8601 拡張形式です。
* editor_usage: List[EditorUsageTimespan]
    エディタ利用時間のリスト
* storage_usage: float
    ストレージ利用量。単位はGB時

"""

UserCacheRecord = Dict[str, Any]
"""


Kyes of Dict

* account: str
    
* members: str
    
* projects: str
    
* organizations: str
    

"""

UserDefinedAnnotationDataType = Dict[str, Any]
"""


Kyes of Dict

* type: str
    ユーザー定義アノテーション種別の型を指定します。 指定可能な値と、その意味は下記の通りです。  * `BoundingBox2d` - 2次元の矩形 * `Polygon2d` - 2次元のポリゴン * `Polyline2d` - 2次元のポリライン * `SinglePoint2d` - 2次元の点 * `SemanticSegmentation2d` - 2次元のセマンティックセグメンテーション * `InstanceSegmentation2d` - 2次元のインスタンスセグメンテーション * `Range1d` - 1次元の範囲 * `Classification` - 全体アノテーション  ユーザー定義アノテーション種別の型によって、使用可能なフィールドが決まっています。 ユーザー定義アノテーション種別ごとの、各フィールドの使用可否を下記の表で示します。  |ユーザー定義アノテーション種別の型 | 使用可能なフィールド定義 | |-----------------|:----------:| | BoundingBox2d          | MinimumSize2d, MinimumSize2dWithDefaultInsertPosition, VertexCountMinMax, MinimumArea2d, MarginOfErrorTolerance | | Polygon2d              | MinimumSize2d, MinVertexSize, VertexCountMinMax, MinimumArea2d, MarginOfErrorTolerance | | Polyline2d             | VertexCountMinMax, DisplayLineDirection, MarginOfErrorTolerance | | SinglePoint2d          | MarginOfErrorTolerance | | SemanticSegmentation2d | AnnotationEditorFeature, MarginOfErrorTolerance | | InstanceSegmentation2d | AnnotationEditorFeature, MarginOfErrorTolerance | | Range1d                | MarginOfErrorTolerance | | Classification         | MarginOfErrorTolerance | 

"""

UserDefinedAnnotationTypeDefinition = Dict[str, Any]
"""


Kyes of Dict

* annotation_type_name: InternationalizationMessage
    
* field_definitions: List[UserDefinedAnnotationTypeDefinitionFieldDefinitions]
    ユーザーが定義するアノテーション種別のフィールド定義です。 フィールドIDをキー、フィールド定義を値とするオブジェクトを設定します。 
* metadata: dict(str, str)
    アノテーション種別を設定した際に、ラベルのメタデータとしてデフォルトで設定される値です。 
* annotation_data_type: UserDefinedAnnotationDataType
    

"""

UserDefinedAnnotationTypeDefinitionFieldDefinitions = Dict[str, Any]
"""


Kyes of Dict

* field_id: str
    フィールドID。任意の文字列を設定できます。
* definition: UserDefinedAnnotationTypeFieldDefinition
    

"""

UserDefinedAnnotationTypeFieldDefinition = Dict[str, Any]
"""


Kyes of Dict

* type: str
    ユーザー定義のアノテーション種別に設定可能なフィールドについての定義です。 設定可能な値とその意味は下記の通りです。 * `MinimumSize2d` - 2次元のデータに対する最小サイズ * `MinVertexSize` - 最小の頂点数 * `MinimumSize2dWithDefaultInsertPosition` - 2次元のデータに対する最小サイズ、および最小矩形の挿入位置 * `MarginOfErrorTolerance` - 誤差許容範囲 * `VertexCountMinMax` - 頂点制約 * `MinimumArea2d` - 2次元のデータに対する面積の制約 * `DisplayLineDirection` - 可視化オプション * `AnnotationEditorFeature` - 作図ツール・作図モード 

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
    
* additional_data: AdditionalDataV1
    

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
    Webhookが送信するHTTPリクエストのヘッダー
* body: str
    Webhookが送信するHTTPリクエストのボディ
* url: str
    Webhookの送信先URL
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""


class WebhookEventType(Enum):
    """
    Webhookイベントの種類 * `task-completed` - タスク受入完了 * `annotation-archive-updated` - アノテーションZIP作成完了 * `input-data-zip-registered` - 入力データZIP登録完了 * `project-copy-completed` - プロジェクトコピー完了
    """

    TASK_COMPLETED = "task-completed"
    ANNOTATION_ARCHIVE_UPDATED = "annotation-archive-updated"
    INPUT_DATA_ZIP_REGISTERED = "input-data-zip-registered"
    PROJECT_COPY_COMPLETED = "project-copy-completed"


WebhookHeader = Dict[str, Any]
"""


Kyes of Dict

* name: str
    HTTPヘッダーのフィールド名
* value: str
    HTTPヘッダーの値

"""


class WebhookHttpMethod(Enum):
    """
    Webhook通知するHTTPリクエストのメソッド
    """

    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    GET = "GET"


class WebhookStatus(Enum):
    """
    Webhookの状態
    """

    ACTIVE = "active"
    INACTIVE = "inactive"


WebhookTestRequest = Dict[str, Any]
"""


Kyes of Dict

* placeholders: dict(str, str)
    keyがプレースホルダーの名前、valueが置換後の値であるkey-valueペア

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
    タスクごとに計算した「画像1枚あたりの作業時間平均」の統計（動画プロジェクトの場合は空リスト）
* by_inputs: List[WorktimeStatisticsItem]
    画像1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）
* by_minutes: List[WorktimeStatisticsItem]
    動画1分当たりの作業時間情報（画像プロジェクトの場合は空リスト）
* accounts: List[AccountWorktimeStatistics]
    ユーザーごとの作業時間情報

"""

WorktimeStatisticsByAccount = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* data_series: List[WorktimeStatisticsData]
    プロジェクトメンバーの日毎の作業時間統計データ

"""

WorktimeStatisticsByProject = Dict[str, Any]
"""


Kyes of Dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* data_series: List[WorktimeStatisticsData]
    プロジェクトの日毎の作業時間統計データ

"""

WorktimeStatisticsData = Dict[str, Any]
"""


Kyes of Dict

* date: str
    日付
* grouped_by_input: List[WorktimeStatisticsItem]
    ユーザーごとの画像1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）
* grouped_by_task: List[WorktimeStatisticsItem]
    ユーザーごとのタスク1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）
* grouped_by_minute: List[WorktimeStatisticsItem]
    ユーザーごとの動画1分当たりの作業時間情報（画像プロジェクトの場合は空リスト）

"""

WorktimeStatisticsItem = Dict[str, Any]
"""


Kyes of Dict

* phase: TaskPhase
    
* histogram: List[HistogramItem]
    ヒストグラム情報
* average: str
    作業時間の平均（ISO 8601 duration）
* standard_deviation: str
    作業時間の標準偏差（ISO 8601 duration）

"""


@deprecated_class(deprecated_date="2022-08-23")
class InspectionStatus(Enum):
    """
    ##### スレッドの先頭のコメントである（`parent_inspection_id` に値がない）場合  * `annotator_action_required` - 未処置。`annotation`フェーズ担当者が何らかの回答をする必要あり * `no_correction_required` - 処置不要。`annotation`フェーズ担当者が、検査コメントによる修正は不要、と回答した * `error_corrected` - 修正済み。`annotation`フェーズ担当者が、検査コメントの指示どおり修正した  ##### 返信コメントである（`parent_inspection_id` に値がある）場合  現在は使用しておらず、レスポンスに含まれる値は不定です。APIのレスポンスにこの値を含む場合でも、「スレッドの先頭のコメント」の値を利用してください。  リクエストボディに指定する場合は、スレッドの先頭のコメントと同じ値を指定します。
    """

    ANNOTATOR_ACTION_REQUIRED = "annotator_action_required"
    NO_CORRECTION_REQUIRED = "no_correction_required"
    ERROR_CORRECTED = "error_corrected"
