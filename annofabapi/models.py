"""
annofabapiのmodel(swagger.yamlの ``components.schemes`` )
enumならば列挙体として定義する。
それ以外は型ヒントしてして宣言する。

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照
"""

from enum import Enum
from typing import Any, NewType  # pylint: disable=unused-import

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
AcceptOrganizationInvitationRequest = dict[str, Any]
"""


Kyes of dict

* token: str
    [inviteOrganizationMember](#operation/inviteOrganizationMember) APIで送信された招待メールに記載されているトークンです。 メールに記載されているURLの`invitation-token`クエリパラメータの値が、トークンになります。 

"""

Account = dict[str, Any]
"""


Kyes of dict

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

AccountWorktimeStatistics = dict[str, Any]
"""


Kyes of dict

* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* by_tasks: list[WorktimeStatisticsItem]
    タスクごとに計算した「画像1枚あたりの作業時間平均」の統計（動画プロジェクトの場合は空リスト）
* by_inputs: list[WorktimeStatisticsItem]
    画像1枚あたりの作業時間情報（動画プロジェクトの場合は空リスト）
* by_minutes: list[WorktimeStatisticsItem]
    動画1分あたりの作業時間情報（画像プロジェクトの場合は空リスト）

"""

ActionRequired = dict[str, Any]
"""
対応が必要な検査コメントが残っている時のエラー

Kyes of dict

* inspection: Inspection
    
* type: str
    ActionRequired

"""

AdditionalDataDefaultType = dict[str, Any]
"""
属性の初期値です。  初期値を設定する場合、属性の種類に応じて次の値を指定してください。 属性の種類に対して有効でない初期値を指定した場合、その初期値は無視されます。  |属性の種類（`type`）                 | 指定できる初期値| |-----------------|----------| | flag    | 真偽値(`true` or `false`)| | integer    | 整数値         | | text | 文字列         | | comment         | 文字列| | choice        | 選択肢(`choices`)の `choice_id` | | select           | 選択肢(`choices`)の`choice_id`|  属性の種類が`tracking`または`link`の場合、初期値を設定できません。  初期値を設定しない場合は、nullまたは空文字を指定してください。 

Kyes of dict


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


AdditionalDataDefinitionV1 = dict[str, Any]
"""


Kyes of dict

* additional_data_definition_id: str
    属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* read_only: bool
    読み込み専用
* name: InternationalizationMessage
    
* default: AdditionalDataDefaultType
    
* keybind: list[Keybind]
    ショートカットキー
* type: AdditionalDataDefinitionType
    
* choices: list[AdditionalDataDefinitionV1Choices]
    ドロップダウンまたはラジオボタンの選択肢
* regex: str
    属性の値が、指定した正規表現に一致している必要があります。
* label_ids: list[str]
    リンク属性において、リンク先として指定可能なラベルID（空の場合制限なし）
* required: bool
    リンク属性において、入力を必須とするかどうか
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AdditionalDataDefinitionV1Choices = dict[str, Any]
"""


Kyes of dict

* choice_id: str
    選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* name: InternationalizationMessage
    
* keybind: list[Keybind]
    ショートカットキー

"""

AdditionalDataDefinitionV2 = dict[str, Any]
"""


Kyes of dict

* additional_data_definition_id: str
    属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* read_only: bool
    読み込み専用
* name: InternationalizationMessage
    
* default: AdditionalDataDefaultType
    
* keybind: list[Keybind]
    ショートカットキー
* type: AdditionalDataDefinitionType
    
* choices: list[AdditionalDataDefinitionV1Choices]
    ドロップダウンまたはラジオボタンの選択肢
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AdditionalDataRestriction = dict[str, Any]
"""


Kyes of dict

* additional_data_definition_id: str
    属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* condition: AdditionalDataRestrictionCondition
    

"""

AdditionalDataRestrictionCondition = dict[str, Any]
"""
属性の制約    * `AdditionalDataRestrictionConditionCanInput`: 属性値の入力を許可するかどうか   * `AdditionalDataRestrictionConditionEquals`: 指定した値に等しい   * `AdditionalDataRestrictionConditionNotEquals`: 指定した値に等しくない   * `AdditionalDataRestrictionConditionMatches`: 指定した正規表現に一致する   * `AdditionalDataRestrictionConditionNotMatches`: 指定した正規表現に一致しない   * `AdditionalDataRestrictionConditionHasLabel`: 指定したラベルIDに一致する（アノテーションリンク属性限定）   * `AdditionalDataRestrictionConditionImply`: 指定した前提条件を満たすときのみ、制約を満たすかどうか  以下のJSONは、「属性IDが`attr2`の属性値が`true`ならば、属性IDが`attr1`の属性値は`choice1`である」という制約を表しています。  ``` {     \"additional_data_definition_id\": \"attr1\",     \"condition\": {         \"_type\": \"Imply\",         \"premise\": {             \"additional_data_definition_id\": \"attr2\",             \"condition\": {                 \"_type\": \"Equals\",                 \"value\": \"true\"             }         },         \"condition\": {             \"_type\": \"Equals\",             \"value\": \"choice1\"         }     } } ``` 

Kyes of dict

* type: str
    `Imply` [詳しくはこちら](#section/API-Convention/API-_type) 
* enable: bool
    `false`を指定することで、属性値の入力を許可しないようにできます。 `AdditionalDataRestrictionConditionImply`との組み合わせで、特定条件下のみ入力を許すといった制限ができます。 
* value: str
    指定された正規表現に一致しないことを要求します。
* labels: list[str]
    アノテーションリンク属性において、アノテーションリンク先として指定可能なラベルIDを制限します。
* premise: AdditionalDataRestriction
    
* condition: AdditionalDataRestrictionCondition
    

"""

AdditionalDataRestrictionConditionCanInput = dict[str, Any]
"""


Kyes of dict

* type: str
    `CanInput` [詳しくはこちら](#section/API-Convention/API-_type) 
* enable: bool
    `false`を指定することで、属性値の入力を許可しないようにできます。 `AdditionalDataRestrictionConditionImply`との組み合わせで、特定条件下のみ入力を許すといった制限ができます。 

"""

AdditionalDataRestrictionConditionEquals = dict[str, Any]
"""


Kyes of dict

* type: str
    `Equals` [詳しくはこちら](#section/API-Convention/API-_type) 
* value: str
    指定された値と等しいことを要求します。

"""

AdditionalDataRestrictionConditionHasLabel = dict[str, Any]
"""


Kyes of dict

* type: str
    `HasLabel` [詳しくはこちら](#section/API-Convention/API-_type) 
* labels: list[str]
    アノテーションリンク属性において、アノテーションリンク先として指定可能なラベルIDを制限します。

"""

AdditionalDataRestrictionConditionImply = dict[str, Any]
"""


Kyes of dict

* type: str
    `Imply` [詳しくはこちら](#section/API-Convention/API-_type) 
* premise: AdditionalDataRestriction
    
* condition: AdditionalDataRestrictionCondition
    

"""

AdditionalDataRestrictionConditionMatches = dict[str, Any]
"""


Kyes of dict

* type: str
    `Matches` [詳しくはこちら](#section/API-Convention/API-_type) 
* value: str
    指定された正規表現に一致することを要求します。

"""

AdditionalDataRestrictionConditionNotEquals = dict[str, Any]
"""


Kyes of dict

* type: str
    `NotEquals` [詳しくはこちら](#section/API-Convention/API-_type) 
* value: str
    指定された値と異なることを要求します。 `value`に`\"\"`を指定することで、入力を必須とすることができます。 

"""

AdditionalDataRestrictionConditionNotMatches = dict[str, Any]
"""


Kyes of dict

* type: str
    `NotMatches` [詳しくはこちら](#section/API-Convention/API-_type) 
* value: str
    指定された正規表現に一致しないことを要求します。

"""

AdditionalDataV1 = dict[str, Any]
"""


Kyes of dict

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

AdditionalDataV2 = dict[str, Any]
"""


Kyes of dict

* definition_id: str
    属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* value: AdditionalDataValue
    

"""

AdditionalDataValue = dict[str, Any]
"""
属性値 

Kyes of dict

* type: str
    
* value: str
    トラッキングID属性の属性値
* choice_id: str
    選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 

"""

AdditionalDataValueChoice = dict[str, Any]
"""


Kyes of dict

* type: str
    
* choice_id: str
    選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 

"""

AdditionalDataValueComment = dict[str, Any]
"""


Kyes of dict

* type: str
    
* value: str
    自由記述（1行）の属性値

"""

AdditionalDataValueFlag = dict[str, Any]
"""


Kyes of dict

* type: str
    
* value: bool
    ON/OFF属性の属性値。 ONの時trueとなります

"""

AdditionalDataValueInteger = dict[str, Any]
"""


Kyes of dict

* type: str
    
* value: int
    整数属性の属性値

"""

AdditionalDataValueLink = dict[str, Any]
"""


Kyes of dict

* type: str
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 

"""

AdditionalDataValueSelect = dict[str, Any]
"""


Kyes of dict

* type: str
    
* choice_id: str
    選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 

"""

AdditionalDataValueText = dict[str, Any]
"""


Kyes of dict

* type: str
    
* value: str
    自由記述（複数行）の属性値

"""

AdditionalDataValueTracking = dict[str, Any]
"""


Kyes of dict

* type: str
    
* value: str
    トラッキングID属性の属性値

"""

AggregationResult = dict[str, Any]
"""


Kyes of dict


"""

AllOidcEndpoints = dict[str, Any]
"""
OIDCエンドポイント

Kyes of dict

* type: str
    
* issuer: str
    RFC 8414で定義されるissuerの値。 `.well-known/openid-configuration`のissuer。
* authorize_url: str
    RFC 8414（及びRFC6749）で定義される、authorization_endpointのURL
* token_url: str
    RFC 8414（及びRFC6749）で定義される、token_endpointのURL
* userinfo_url: str
    OpenID Connect Core 1.0で定義される、UserInfo EndpointのURL
* jwks_url: str
    RFC 8414で定義される、jwks_uriの値

"""


class AnnotationDataHoldingType(Enum):
    """
    アノテーションのデータがどこに保持されるか * `inner` - アノテーションのデータ部をJSON内部に保持します。 * `outer` - アノテーションのデータ部を外部ファイルの形式（画像など）で保持します
    """

    INNER = "inner"
    OUTER = "outer"


AnnotationDataV1 = dict[str, Any]
"""
アノテーションの座標値や区間などのデータ。  APIのレスポンスから参照される場合は、`FullAnnotationDataString`形式です。 [putAnnotation](#operation/putAnnotation) APIのリクエストボディは、`FullAnnotationDataString`形式または`FullAnnotationData`形式に対応しています。 

Kyes of dict


"""

AnnotationDetailContentInput = dict[str, Any]
"""
- **AnnotationDetailContentInputInner**   - アノテーションのデータ部をJSON内部に保持する場合、この型を利用します - **AnnotationDetailContentInputOuter**   - アノテーションのデータ部を外部ファイルの形式（画像など）で保持する場合、この型を利用します 

Kyes of dict

* type: str
    
* data: FullAnnotationData
    
* path: str
    外部ファイルの位置を示す文字列。 [createTempPath](#operation/createTempPath) APIによって取得したpathを指定します。

"""

AnnotationDetailContentInputInner = dict[str, Any]
"""
アノテーションのデータ部をJSON内部に保持します

Kyes of dict

* type: str
    
* data: FullAnnotationData
    

"""

AnnotationDetailContentInputOuter = dict[str, Any]
"""
アノテーションのデータ部を外部ファイルの形式（画像など）で保持します

Kyes of dict

* type: str
    
* path: str
    外部ファイルの位置を示す文字列。 [createTempPath](#operation/createTempPath) APIによって取得したpathを指定します。

"""

AnnotationDetailContentOutput = dict[str, Any]
"""
- **AnnotationDetailContentOutputInner**   - アノテーションのデータ部をJSON内部に保持している場合、通常はこの型の値となります - **AnnotationDetailContentOutputInnerUnknown**   - アノテーションのデータ部をJSON内部に保持しており、且つ、AnnotationDetailV1の形式で保存されていたデータのAnnotationTypeが特定できない場合にこの値となります   - 典型的な例では、アノテーションの保存後にアノテーション仕様が書き換わっていた場合が該当します - **AnnotationDetailContentOutputOuter**   - アノテーションのデータ部を外部ファイルの形式（画像など）で保持している場合、通常はこの型の値となります - **AnnotationDetailContentOutputOuterUnresolved**   - アノテーションのデータ部を外部ファイルの形式（画像など）で保持しており、且つ、Outerのurl / etagを解決しなかった場合（過去のアノテーションを取得した場合等）にこの値となります 

Kyes of dict

* type: str
    
* data: str
    アノテーション座標値や区間などの文字列表現です。 アノテーション種類（`annotation_type`）とデータ格納形式（`data_holding_type`）に応じて、以下のとおり表現が変わります。  <table> <tr><th>annotation_type</th><th>data_holding_type</th><th>文字列表現</th></tr> <tr><td>bounding_box</td><td>inner</td><td><code>\"左上x,左上y,右下x,右下y\"</code></td></tr> <tr><td>point</td><td>inner</td><td><code>\"x1,y1\"</code></td></tr> <tr><td>polygon / polyline</td><td>inner</td><td><code>\"x1,y1,x2,y2, ... \"</code></td></tr> <tr><td>range </td><td>inner</td><td><code>\"開始時間(ミリ秒),終了時間(ミリ秒) \"</code></td></tr> <tr><td>classification</td><td>inner</td><td><code>null</code></td></tr> <tr><td>segmentation</td><td>outer</td><td><code>null</code></td></tr> <tr><td>segmentation_v2</td><td>outer</td><td><code>null</code></td></tr> </table> 
* url: str
    外部ファイルに保存されたアノテーションの認証済み一時URL
* etag: str
    外部ファイルに保存されたアノテーションのETag

"""

AnnotationDetailContentOutputInner = dict[str, Any]
"""
アノテーションのデータ部をJSON内部に保持します

Kyes of dict

* type: str
    
* data: FullAnnotationData
    

"""

AnnotationDetailContentOutputInnerUnknown = dict[str, Any]
"""
アノテーションのデータ部をJSON内部に保持します。 AnnotationDetailV1の形式で保存されていたデータのAnnotationTypeが特定できない場合にこの値となります。 典型的な例では、アノテーションの保存後にアノテーション仕様が書き換わっていた場合が該当します。 

Kyes of dict

* type: str
    
* data: str
    アノテーション座標値や区間などの文字列表現です。 アノテーション種類（`annotation_type`）とデータ格納形式（`data_holding_type`）に応じて、以下のとおり表現が変わります。  <table> <tr><th>annotation_type</th><th>data_holding_type</th><th>文字列表現</th></tr> <tr><td>bounding_box</td><td>inner</td><td><code>\"左上x,左上y,右下x,右下y\"</code></td></tr> <tr><td>point</td><td>inner</td><td><code>\"x1,y1\"</code></td></tr> <tr><td>polygon / polyline</td><td>inner</td><td><code>\"x1,y1,x2,y2, ... \"</code></td></tr> <tr><td>range </td><td>inner</td><td><code>\"開始時間(ミリ秒),終了時間(ミリ秒) \"</code></td></tr> <tr><td>classification</td><td>inner</td><td><code>null</code></td></tr> <tr><td>segmentation</td><td>outer</td><td><code>null</code></td></tr> <tr><td>segmentation_v2</td><td>outer</td><td><code>null</code></td></tr> </table> 

"""

AnnotationDetailContentOutputOuter = dict[str, Any]
"""
アノテーションのデータ部を外部ファイルの形式（画像など）で保持します

Kyes of dict

* type: str
    
* url: str
    外部ファイルに保存されたアノテーションの認証済み一時URL
* etag: str
    外部ファイルに保存されたアノテーションのETag

"""

AnnotationDetailContentOutputOuterUnresolved = dict[str, Any]
"""
アノテーションのデータ部を外部ファイルの形式（画像など）で保持します。 Outerのurl / etagを解決しなかった場合（過去のアノテーションを取得した場合等）にこの値となります。 

Kyes of dict

* type: str
    

"""

AnnotationDetailV1 = dict[str, Any]
"""


Kyes of dict

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
    外部ファイルに保存されたアノテーションのパス。`data_holding_type`が`inner`の場合は未指定です。 レスポンスの場合は`annotation_id`と同じ値が格納されます。  [putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は、[createTempPath](#operation/createTempPath) APIで取得できる一時データ保存先パスを格納してください。 更新しない場合は、[getEditorAnnotation](#operation/getEditorAnnotation) APIで取得した`path`をそのまま渡せます。  外部ファイルのフォーマットは下表の通りです。  <table> <tr><th>annotation_type</th><th>形式</th></tr> <tr><td>segmentation / segmentation_v2   </td><td>PNG画像。塗りつぶした部分は<code>rgba(255, 255, 255, 1) </code>、塗りつぶしていない部分は<code>rgba(0, 0, 0, 0) </code>。</td></tr> </table> 
* etag: str
    外部ファイルに保存されたアノテーションのETag。`data_holding_type`が`inner`の場合、または[putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は未指定です。
* url: str
    外部ファイルに保存されたアノテーションの認証済み一時URL。`data_holding_type`が`inner`の場合、または[putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は未指定です。
* additional_data_list: list[AdditionalDataV1]
    属性情報。  アノテーション属性の種類（`additional_data_definition`の`type`）によって、属性値を格納するプロパティは変わります。  | 属性の種類 | `additional_data_definition`の`type` | 属性値を格納するプロパティ                    | |------------|-------------------------|----------------------| | ON/OFF | flag       | flag                                          | | 整数 | integer    | integer                                       | | 自由記述（1行）| text       | comment                                       | | 自由記述（複数行）| comment    | comment                                       | | トラッキングID  | tracking | comment                                       | | アノテーションリンク    | link   | comment                                       | | 排他選択（ラジオボタン）  |choice   | choice                                        | | 排他選択（ドロップダウン） | select    | choice                                        | 
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

AnnotationDetailV2Create = dict[str, Any]
"""
新規にアノテーションを作成する場合にこの型を利用します。

Kyes of dict

* type: str
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* body: AnnotationDetailContentInput
    
* additional_data_list: list[AdditionalDataV2]
    
* editor_props: AnnotationPropsForEditor
    

"""

AnnotationDetailV2Get = dict[str, Any]
"""


Kyes of dict

* type: str
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* body: AnnotationDetailContentOutput
    
* additional_data_list: list[AdditionalDataV2]
    
* editor_props: AnnotationPropsForEditor
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

AnnotationDetailV2Import = dict[str, Any]
"""
過去にAnnofab内外で作成したアノテーションをそのままインポートする場合にこの型を利用します。

Kyes of dict

* type: str
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* body: AnnotationDetailContentInput
    
* additional_data_list: list[AdditionalDataV2]
    
* editor_props: AnnotationPropsForEditor
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

AnnotationDetailV2Input = dict[str, Any]
"""
- **AnnotationDetailV2Create**   - 新規にアノテーションを作成する場合にこの型を利用します。 - **AnnotationDetailV2Import**   - 過去にAnnofab内外で作成したアノテーションをそのままインポートする場合にこの型を利用します。 - **AnnotationDetailV2Update**   - 既に存在するアノテーションを更新する場合にこの型を利用します 

Kyes of dict

* type: str
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* body: AnnotationDetailContentInput
    
* additional_data_list: list[AdditionalDataV2]
    
* editor_props: AnnotationPropsForEditor
    
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

AnnotationDetailV2Output = dict[str, Any]
"""


Kyes of dict


"""

AnnotationDetailV2Update = dict[str, Any]
"""
既に存在するアノテーションを更新する場合にこの型を利用します

Kyes of dict

* type: str
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* body: AnnotationDetailContentInput
    
* additional_data_list: list[AdditionalDataV2]
    
* editor_props: AnnotationPropsForEditor
    

"""

AnnotationEditorFeature = dict[str, Any]
"""
塗りつぶしの作図機能に関する情報 

Kyes of dict

* append: bool
    塗りつぶしの「追記」機能が使えるか否か
* erase: bool
    塗りつぶしの「消しゴム」機能が使えるか否か
* freehand: bool
    塗りつぶしの「フリーハンド」機能が使えるか否か
* rectangle_fill: bool
    塗りつぶしの「矩形」機能が使えるか否か
* polygon_fill: bool
    塗りつぶしの「自由形状」機能が使えるか否か
* fill_near: bool
    「近似色塗りつぶし」機能を有効にするかどうか

"""

AnnotationInput = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: list[AnnotationDetailV2Input]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    対象タスク・対象入力データへの最初の保存時は未指定にしてください。 更新の場合はアノテーション取得時のupdated_datetimeをそのまま指定してください。 
* format_version: str
    

"""

AnnotationList = dict[str, Any]
"""


Kyes of dict

* list: list[SingleAnnotation]
    現在のページ番号に含まれる0件以上のアノテーションです。
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるアノテーションが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: list[AggregationResult]
    [Aggregationによる集約結果](#section/API-Convention/AggregationResult)。 

"""

AnnotationOutput = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: list[AnnotationDetailV2Output]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    対象タスク・対象入力データへ一度もアノテーションの保存が行われていない場合、未指定となります。 そうで無い場合、対象タスク・対象入力データのアノテーション最終更新時刻です。 
* format_version: str
    

"""

AnnotationPropsForEditor = dict[str, Any]
"""
アノテーションエディタ用のアノテーション毎のプロパティです。<br /> ここに含まれているデータはアノテーション結果に反映されず、エディタが利用するために存在します。  エディタ用のデータであるため、たとえば`can_delete`や`can_edit_data`が`false`でも、APIによる編集は妨げません。<br /> ここで定義されているデータを利用して動作を変えるかどうかは、エディタによって異なります。 

Kyes of dict

* can_delete: bool
    アノテーションがエディタ上で削除できるかどうか。 trueの場合削除可能。
* can_edit_data: bool
    アノテーションの本体のデータを編集できるかどうか。 trueの場合編集可能。 2022/09現在、この値を利用しているエディタは存在しません。
* can_edit_additional: bool
    アノテーションの付加情報を編集できるかどうか。  trueの場合編集可能。 2022/09現在、この値を利用しているエディタは存在しません。
* description: str
    アノテーションについての人間可読な説明。 2022/09現在、この値を利用しているエディタは存在しません。
* tags: list[str]
    アノテーションに付与されている機械可読・人間可読なタグの列。  2022/09現在、この値を利用しているエディタは存在しません
* etc: __DictStrKeyAnyValue__
    上記以外の任意のJson構造

"""

AnnotationQuery = dict[str, Any]
"""
アノテーションの絞り込み条件 

Kyes of dict

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
* attributes: list[AdditionalDataV1]
    属性情報。  アノテーション属性の種類（`additional_data_definition`の`type`）によって、属性値を格納するプロパティは変わります。  | 属性の種類 | `additional_data_definition`の`type` | 属性値を格納するプロパティ                    | |------------|-------------------------|----------------------| | ON/OFF | flag       | flag                                          | | 整数 | integer    | integer                                       | | 自由記述（1行）| text       | comment                                       | | 自由記述（複数行）| comment    | comment                                       | | トラッキングID  | tracking | comment                                       | | アノテーションリンク    | link   | comment                                       | | 排他選択（ラジオボタン）  |choice   | choice                                        | | 排他選択（ドロップダウン） | select    | choice                                        | 
* updated_from: str
    開始日・終了日を含む区間[updated_from, updated_to]でアノテーションの更新日を絞り込むときに使用する、開始日（ISO 8601 拡張形式または基本形式）。  `updated_to` より後の日付が指定された場合、期間指定は開始日・終了日を含む区間[updated_to, updated_from]となる。未指定の場合、API実行日(JST)の日付が指定されたものとして扱われる。 
* updated_to: str
    開始日・終了日を含む区間[updated_from, updated_to]でアノテーションの更新日を絞り込むときに使用する、終了日（ISO 8601 拡張形式または基本形式）。  未指定の場合、API実行日(JST)の日付が指定されたものとして扱われる。 

"""

AnnotationSpecs = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* labels: list[LabelV3]
    ラベル
* inspection_phrases: list[InspectionPhrase]
    定型指摘
* updated_datetime: str
    更新日時 
* option: AnnotationSpecsOption
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 
* additionals: list[AdditionalDataDefinitionV2]
    属性
* restrictions: list[AdditionalDataRestriction]
    属性の制約
* format_version: str
    アノテーション仕様のフォーマットのバージョン
* annotation_type_version: str
    アノテーション種別のバージョン。  拡張仕様プラグインで定義した値が転写されます。プロジェクトに拡張仕様プラグインが設定されていない場合は未指定です。 

"""

AnnotationSpecsHistory = dict[str, Any]
"""


Kyes of dict

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

AnnotationSpecsMovieOption = dict[str, Any]
"""


Kyes of dict

* can_overwrap: bool
    動画プロジェクトのアノテーションに重複配置を許すか否か。 

"""

AnnotationSpecsOption = dict[str, Any]
"""
アノテーション仕様のオプション設定。  現時点では動画プロジェクトでのみ利用・指定可能。動画以外のプロジェクトでは値なし。  動画プロジェクトで値が未指定の場合、AnnotationSpecsOption内の値はすべてデフォルト値が指定されたものとして扱われる。 

Kyes of dict


"""

AnnotationSpecsRequest = dict[str, Any]
"""


Kyes of dict

* labels: list[LabelV3]
    ラベル
* inspection_phrases: list[InspectionPhrase]
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
* additionals: list[AdditionalDataDefinitionV2]
    属性
* restrictions: list[AdditionalDataRestriction]
    属性の制約
* format_version: str
    アノテーション仕様のフォーマットのバージョン
* annotation_type_version: str
    アノテーション種別のバージョン。拡張仕様プラグインを利用している場合に、プラグインに設定されている値が転写されます。 プロジェクトに拡張仕様プラグインが設定されていない場合は未指定です。

"""

AnnotationSpecsRequestV1 = dict[str, Any]
"""


Kyes of dict

* labels: list[LabelV1]
    ラベル
* inspection_phrases: list[InspectionPhrase]
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

AnnotationSpecsRequestV2 = dict[str, Any]
"""


Kyes of dict

* labels: list[LabelV2]
    ラベル
* additionals: list[AdditionalDataDefinitionV2]
    属性
* restrictions: list[AdditionalDataRestriction]
    属性の制約
* inspection_phrases: list[InspectionPhrase]
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

AnnotationSpecsRequestV3 = dict[str, Any]
"""


Kyes of dict

* labels: list[LabelV3]
    ラベル
* additionals: list[AdditionalDataDefinitionV2]
    属性
* restrictions: list[AdditionalDataRestriction]
    属性の制約
* inspection_phrases: list[InspectionPhrase]
    定型指摘
* comment: str
    変更内容のコメント
* auto_marking: bool
    trueが指定された場合、各統計グラフにマーカーを自動追加します。 マーカーのタイトルには `comment` に指定された文字列が設定されます。 `comment` が指定されていなかった場合は \"アノテーション仕様の変更\" という文字列が設定されます。 
* annotation_type_version: str
    アノテーション種別のバージョン。拡張仕様プラグインを利用している場合に、プラグインに設定されている値が転写されます。 プロジェクトに拡張仕様プラグインが設定されていない場合は未指定です。
* format_version: str
    アノテーション仕様のフォーマットのバージョン
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 
* option: AnnotationSpecsOption
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AnnotationSpecsV1 = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* labels: list[LabelV1]
    ラベル
* inspection_phrases: list[InspectionPhrase]
    定型指摘
* updated_datetime: str
    更新日時 
* option: AnnotationSpecsOption
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AnnotationSpecsV2 = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* labels: list[LabelV2]
    ラベル
* additionals: list[AdditionalDataDefinitionV2]
    属性
* restrictions: list[AdditionalDataRestriction]
    属性の制約
* inspection_phrases: list[InspectionPhrase]
    定型指摘
* format_version: str
    アノテーション仕様のフォーマットのバージョン
* updated_datetime: str
    更新日時 
* option: AnnotationSpecsOption
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

AnnotationSpecsV3 = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* labels: list[LabelV3]
    ラベル
* additionals: list[AdditionalDataDefinitionV2]
    属性
* restrictions: list[AdditionalDataRestriction]
    属性の制約
* inspection_phrases: list[InspectionPhrase]
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

AnnotationThumbnail = dict[str, Any]
"""
アノテーションのサムネイル情報

Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* images: list[AnnotationThumbnailImage]
    サムネイル画像情報の一覧
* annotations: dict(str, AnnotationThumbnailDetail)
    アノテーションIDをキーとしたサムネイル情報
* annotation_updated_datetime: str
    サムネイルの元になったアノテーションの更新日時。サムネイルが未作成の場合はnull。
* created_datetime: str
    サムネイル登録日時。サムネイルが未作成の場合はnull。

"""

AnnotationThumbnailDetail = dict[str, Any]
"""
- **AnnotationThumbnailDetailImageSlice**:<br>   画像の一部をサムネイルとして使用する - **AnnotationThumbnailDetailUnsupported**:<br>   サムネイル生成に対応していない - **AnnotationThumbnailDetailFailed**:<br>   サムネイル生成に失敗した 

Kyes of dict

* type: str
    
* image: int
    AnnotationThumbnail.imageのインデックス
* x: int
    x座標
* y: int
    y座標
* width: int
    幅
* height: int
    高さ
* reason: str
    失敗理由

"""

AnnotationThumbnailDetailFailed = dict[str, Any]
"""
サムネイル生成に失敗した

Kyes of dict

* type: str
    
* reason: str
    失敗理由

"""

AnnotationThumbnailDetailImageSlice = dict[str, Any]
"""
画像の一部をサムネイルとして使用する

Kyes of dict

* type: str
    
* image: int
    AnnotationThumbnail.imageのインデックス
* x: int
    x座標
* y: int
    y座標
* width: int
    幅
* height: int
    高さ

"""

AnnotationThumbnailDetailUnsupported = dict[str, Any]
"""
サムネイル生成に対応していない

Kyes of dict

* type: str
    

"""

AnnotationThumbnailImage = dict[str, Any]
"""


Kyes of dict

* type: str
    
* url: str
    サムネイル画像のURL
* width: int
    画像の幅
* height: int
    画像の高さ

"""

AnnotationThumbnailImageSource = dict[str, Any]
"""


Kyes of dict

* type: str
    
* temporary_path: str
    事前にアップロードしたサムネイル画像のパス。 [createTempPath](#operation/createTempPath) APIで取得した `path` の値を指定します。

"""

AnnotationType = dict[str, Any]
"""


Kyes of dict


"""

AnnotationTypeFieldDefinitionAnnotationEditorFeature = dict[str, Any]
"""
作図ツール・作図モードのフィールドの定義 

Kyes of dict

* type: str
    

"""

AnnotationTypeFieldDefinitionDisplayLineDirection = dict[str, Any]
"""
線の向き表示/非表示の設定のフィールド定義 

Kyes of dict

* type: str
    

"""

AnnotationTypeFieldDefinitionMarginOfErrorTolerance = dict[str, Any]
"""
誤差許容範囲のフィールド定義 

Kyes of dict

* type: str
    

"""

AnnotationTypeFieldDefinitionMinimumArea2d = dict[str, Any]
"""
最小の面積のフィールド定義 

Kyes of dict

* type: str
    

"""

AnnotationTypeFieldDefinitionMinimumSize2d = dict[str, Any]
"""
アノテーションの最小サイズに関する設定のフィールド定義 

Kyes of dict

* type: str
    

"""

AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition = dict[str, Any]
"""
アノテーションの最小サイズに関する設定、および最小矩形の挿入位置のフィールド定義 

Kyes of dict

* type: str
    

"""

AnnotationTypeFieldDefinitionOneBooleanField = dict[str, Any]
"""
真偽値の値をひとつだけ持つフィールドの定義 

Kyes of dict

* type: str
    
* title: InternationalizationMessage
    
* description: InternationalizationMessage
    
* initial_value: bool
    フィールドの初期値 
* label: InternationalizationMessage
    

"""

AnnotationTypeFieldDefinitionOneIntegerField = dict[str, Any]
"""
数値の値をひとつだけ持つフィールドの定義 

Kyes of dict

* type: str
    
* title: InternationalizationMessage
    
* prefix: str
    フィールドの前に付与する文字列。 
* postfix: str
    フィールドの後に付与する文字列 
* description: InternationalizationMessage
    
* initial_value: int
    フィールドの初期値 

"""

AnnotationTypeFieldDefinitionOneStringField = dict[str, Any]
"""
文字列の値をひとつだけ持つフィールドの定義 

Kyes of dict

* type: str
    
* title: InternationalizationMessage
    
* prefix: str
    フィールドの前に付与する文字列。 
* postfix: str
    フィールドの後に付与する文字列 
* description: InternationalizationMessage
    
* initial_value: str
    フィールドの初期値 

"""

AnnotationTypeFieldDefinitionVertexCountMinMax = dict[str, Any]
"""
頂点数の最大・最小のフィールド定義 

Kyes of dict

* type: str
    

"""


class AnnotationTypeFieldMinWarnRule(Enum):
    """
    最小の幅(min_width)と最小の高さ(min_height)がどのような状態になったときにエラーとするかを指定します。  * `and` - min_width、min_heightの両方が最小値未満の場合にエラーとなります。 * `or` - min_width、min_heightのいずれかが最小値未満の場合にエラーとなります。
    """

    AND = "and"
    OR = "or"


AnnotationTypeFieldValue = dict[str, Any]
"""
ユーザー定義アノテーション種別のフィールドに設定される値です。 アノテーション種別のフィールド定義と対応するフィールド値のみ登録を許可されます。 

Kyes of dict

* type: str
    
* min_warn_rule: AnnotationTypeFieldMinWarnRule
    
* min_width: int
    
* min_height: int
    
* position_for_minimum_bounding_box_insertion: list[int]
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

AnnotationTypeFieldValueAnnotationEditorFeature = dict[str, Any]
"""
作図ツール・作図モード 

Kyes of dict

* type: str
    
* append: bool
    
* erase: bool
    
* freehand: bool
    
* rectangle_fill: bool
    
* polygon_fill: bool
    
* fill_near: bool
    

"""

AnnotationTypeFieldValueDisplayLineDirection = dict[str, Any]
"""
線の向き表示/非表示の設定 

Kyes of dict

* type: str
    
* has_direction: bool
    

"""

AnnotationTypeFieldValueEmptyFieldValue = dict[str, Any]
"""
値を持たないフィールド。　アノテーション仕様上に定義が存在すること自体に意味がある場合のフィールド値に利用します。

Kyes of dict

* type: str
    

"""

AnnotationTypeFieldValueMarginOfErrorTolerance = dict[str, Any]
"""
誤差許容範囲

Kyes of dict

* type: str
    
* max_pixel: int
    

"""

AnnotationTypeFieldValueMinimumArea2d = dict[str, Any]
"""
最小の面積 

Kyes of dict

* type: str
    
* min_area: int
    

"""

AnnotationTypeFieldValueMinimumSize = dict[str, Any]
"""
アノテーションの最小サイズに関する設定

Kyes of dict

* type: str
    
* min_warn_rule: AnnotationTypeFieldMinWarnRule
    
* min_width: int
    
* min_height: int
    

"""

AnnotationTypeFieldValueMinimumSize2dWithDefaultInsertPosition = dict[str, Any]
"""


Kyes of dict

* type: str
    
* min_warn_rule: AnnotationTypeFieldMinWarnRule
    
* min_width: int
    
* min_height: int
    
* position_for_minimum_bounding_box_insertion: list[int]
    最小矩形の挿入位置を、要素が2の配列で指定します。 

"""

AnnotationTypeFieldValueOneBooleanFieldValue = dict[str, Any]
"""
真偽値をひとつだけ持つフィールド

Kyes of dict

* type: str
    
* value: bool
    

"""

AnnotationTypeFieldValueOneIntegerFieldValue = dict[str, Any]
"""
数値をひとつだけ持つフィールド

Kyes of dict

* type: str
    
* value: int
    

"""

AnnotationTypeFieldValueOneStringFieldValue = dict[str, Any]
"""
文字列を一つだけ持つフィールド

Kyes of dict

* type: str
    
* value: str
    

"""

AnnotationTypeFieldValueVertexCountMinMax = dict[str, Any]
"""
頂点数の最大・最小 

Kyes of dict

* type: str
    
* min: int
    
* max: int
    

"""

AnnotationV1 = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: list[AnnotationDetailV1]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    更新日時

"""

AnnotationV2Input = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: list[AnnotationDetailV2Input]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    対象タスク・対象入力データへの最初の保存時は未指定にしてください。 更新の場合はアノテーション取得時のupdated_datetimeをそのまま指定してください。 
* format_version: str
    

"""

AnnotationV2Output = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: list[AnnotationDetailV2Output]
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


BatchAnnotationRequestItem = dict[str, Any]
"""


Kyes of dict

* data: BatchAnnotationV2
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 
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

BatchAnnotationRequestItemDelete = dict[str, Any]
"""
アノテーション削除

Kyes of dict

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
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchAnnotationRequestItemPutV1 = dict[str, Any]
"""
アノテーション更新

Kyes of dict

* data: BatchAnnotationV1
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchAnnotationRequestItemPutV2 = dict[str, Any]
"""
アノテーション更新

Kyes of dict

* data: BatchAnnotationV2
    
* type: str
    [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchAnnotationV1 = dict[str, Any]
"""


Kyes of dict

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
* additional_data_list: list[AdditionalDataV1]
    属性情報。  アノテーション属性の種類（`additional_data_definition`の`type`）によって、属性値を格納するプロパティは変わります。  | 属性の種類 | `additional_data_definition`の`type` | 属性値を格納するプロパティ                    | |------------|-------------------------|----------------------| | ON/OFF | flag       | flag                                          | | 整数 | integer    | integer                                       | | 自由記述（1行）| text       | comment                                       | | 自由記述（複数行）| comment    | comment                                       | | トラッキングID  | tracking | comment                                       | | アノテーションリンク    | link   | comment                                       | | 排他選択（ラジオボタン）  |choice   | choice                                        | | 排他選択（ドロップダウン） | select    | choice                                        | 
* updated_datetime: str
    アノテーション取得時の更新日時。更新時の楽観ロックに利用されます。 AnnotationDetailのものではなく、それを格納するAnnotationV2Outputなどが保持する更新時刻であることに注意してください。 

"""

BatchAnnotationV2 = dict[str, Any]
"""


Kyes of dict

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
* additional_data_list: list[AdditionalDataV2]
    
* updated_datetime: str
    アノテーション取得時の更新日時。更新時の楽観ロックに利用されます。 AnnotationDetailのものではなく、それを格納するAnnotationV2Outputなどが保持する更新時刻であることに注意してください。 

"""

BatchCommentRequestItem = dict[str, Any]
"""


Kyes of dict

* comment_id: str
    コメントのID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* phase: TaskPhase
    
* phase_stage: int
    コメントを作成したときのフェーズのステージ。
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* comment_type: str
    コメントの種別。次の値が指定できます。  * `onhold` - 保留コメントとして扱われます。 * `inspection` - 検査コメントとして扱われます。  返信コメント作成時は返信先コメントの `comment_type` と同じ値を指定してください。  コメント更新時は更新前コメントと同じ値を指定してください（変更はできません）。 
* phrases: list[str]
    `comment_type` の値によって指定可能な値が異なります。  * `onhold` の場合   * 使用しません（空配列 or 指定なし） 
* comment: str
    コメント本文。 
* comment_node: CommentNode
    
* datetime_for_sorting: str
    コメントのソート順を決める日時。コメント作成時のみ指定可能です。  Annofab標準エディタでは、コメントはここで指定した日時にしたがってスレッドごとに昇順で表示されます。  コメント作成時に未指定とした場合は、作成操作オブジェクトの順序に応じてコメント作成日時からずれた時刻が自動設定されます（ソート順を一意とするため）。  なお、この値は後から更新することはできません（値を指定しても無視されます）。 
* type: str
    `Delete`  [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchCommentRequestItemDelete = dict[str, Any]
"""
コメント削除

Kyes of dict

* comment_id: str
    コメントのID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* type: str
    `Delete`  [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchCommentRequestItemPut = dict[str, Any]
"""
コメント更新

Kyes of dict

* comment_id: str
    コメントのID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* phase: TaskPhase
    
* phase_stage: int
    コメントを作成したときのフェーズのステージ。
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* comment_type: str
    コメントの種別。次の値が指定できます。  * `onhold` - 保留コメントとして扱われます。 * `inspection` - 検査コメントとして扱われます。  返信コメント作成時は返信先コメントの `comment_type` と同じ値を指定してください。  コメント更新時は更新前コメントと同じ値を指定してください（変更はできません）。 
* phrases: list[str]
    `comment_type` の値によって指定可能な値が異なります。  * `onhold` の場合   * 使用しません（空配列 or 指定なし） 
* comment: str
    コメント本文。 
* comment_node: CommentNode
    
* datetime_for_sorting: str
    コメントのソート順を決める日時。コメント作成時のみ指定可能です。  Annofab標準エディタでは、コメントはここで指定した日時にしたがってスレッドごとに昇順で表示されます。  コメント作成時に未指定とした場合は、作成操作オブジェクトの順序に応じてコメント作成日時からずれた時刻が自動設定されます（ソート順を一意とするため）。  なお、この値は後から更新することはできません（値を指定しても無視されます）。 
* type: str
    `Put`  [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchInputDataRequestItem = dict[str, Any]
"""


Kyes of dict


"""

BatchInputDataRequestItemDelete = dict[str, Any]
"""
入力データ削除

Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* type: str
    `Delete` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchInspectionRequestItem = dict[str, Any]
"""


Kyes of dict

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

BatchInspectionRequestItemDelete = dict[str, Any]
"""
検査コメント削除

Kyes of dict

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

BatchInspectionRequestItemPut = dict[str, Any]
"""
検査コメント更新

Kyes of dict

* data: Inspection
    
* type: str
    `Put` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BatchTaskRequestItem = dict[str, Any]
"""


Kyes of dict


"""

BatchTaskRequestItemDelete = dict[str, Any]
"""
タスク削除

Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* type: str
    `Delete` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

BoundingBoxMetadata = dict[str, Any]
"""
ベクター形式のアノテーション（矩形、ポリゴン、ポリライン、点）のメタデータ

Kyes of dict

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

ChangePasswordRequest = dict[str, Any]
"""


Kyes of dict

* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* old_password: str
    
* new_password: str
    

"""

Color = dict[str, Any]
"""
RGBで表現される色情報

Kyes of dict

* red: int
    
* green: int
    
* blue: int
    

"""

Comment = dict[str, Any]
"""
コメント

Kyes of dict

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
    
* phrases: list[str]
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

CommentNode = dict[str, Any]
"""
コメントのノード固有のデータ。  * `RootComment` - スレッドの先頭のコメント（ルートコメント）。 * `ReplyComment` - あるコメントへの返信コメント。 

Kyes of dict

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


ConfirmAccountDeleteRequest = dict[str, Any]
"""


Kyes of dict

* token: str
    

"""

ConfirmResetEmailRequest = dict[str, Any]
"""


Kyes of dict

* token: str
    

"""

ConfirmResetPasswordRequest = dict[str, Any]
"""


Kyes of dict

* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* confirmation_code: str
    
* new_password: str
    
* is_reset_mfa: bool
    MFA設定をリセットするか。trueの場合にリセットする。

"""

ConfirmSignUpRequest = dict[str, Any]
"""


Kyes of dict

* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* password: str
    
* username: str
    
* lang: Lang
    
* keylayout: KeyLayout
    
* confirmation_code: str
    

"""

ConfirmVerifyEmailRequest = dict[str, Any]
"""


Kyes of dict

* token: Token
    
* confirmation_code: str
    

"""

Count = dict[str, Any]
"""


Kyes of dict

* key: str
    集約対象の `field` の値です。 
* count: int
    集約対象 `field` の値が `key` の値と等しかったリソースの件数です。 
* aggregations: list[AggregationResult]
    この集約のサブ集約です。サブ集約がないときは空の配列になります。 

"""

CountResult = dict[str, Any]
"""


Kyes of dict

* type: str
    `CountResult` [詳しくはこちら](#section/API-Convention/API-_type) 
* name: str
    複数の集約を区別するための名前です。  `(フィールド名)_(集約内容)` のように命名されます。例えば `account_id` フィールドを `count` する場合、`account_id_count` となります。 
* field: str
    集約に使われたリソースのフィールド名です。  リソースの属性のさらに属性を参照するときは、`foo.bar.buz` のようにドット区切りになります。 
* doc_count: int
    集約の件数です。 
* items: list[Count]
    集約結果の値です。 

"""

DataPath = dict[str, Any]
"""


Kyes of dict

* url: str
    ファイルアップロード用の一時URLです。このURLにファイルをアップロードします。
* path: str
    [putInputData](#operation/putInputData) APIや[putSupplementaryData](#operation/putSupplementaryData) APIのリクエストボディに指定するパスです。 

"""

DateRange = dict[str, Any]
"""
日付の期間

Kyes of dict

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


DeleteProjectResponse = dict[str, Any]
"""


Kyes of dict

* job: ProjectJobInfo
    
* project: Project
    

"""

DuplicatedSegmentationV2 = dict[str, Any]
"""
塗りつぶしv2のラベルに対する1ラベルにつき1アノテーションまでの制約違反エラー

Kyes of dict

* label_id: str
    
* annotation_ids: list[str]
    
* type: str
    DuplicatedSegmentationV2

"""

DuplicatedV1 = dict[str, Any]
"""
値の重複が許可されていない属性の重複エラー

Kyes of dict

* label_id: str
    
* annotation_id: str
    
* additional_data: AdditionalDataV1
    
* type: str
    

"""

DuplicatedV2 = dict[str, Any]
"""
値の重複が許可されていない属性の重複エラー

Kyes of dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    

"""

EditorUsageTimespan = dict[str, Any]
"""
エディタごとの利用時間

Kyes of dict

* editor_name: str
    エディタ名です。  | editor_nameの値 | エディタ名   | |-----------------|--------------| | image_editor    | 画像エディタ | | video_editor    | 動画エディタ | | 3d_editor       | 3Dエディタ   | 
* value: float
    エディタ利用時間。単位は時

"""

ErrorItem = dict[str, Any]
"""


Kyes of dict

* error_code: str
    
* message: str
    エラーの概要
* ext: __DictStrKeyAnyValue__
    補足情報

"""

Errors = dict[str, Any]
"""


Kyes of dict

* errors: list[ErrorItem]
    
* context: __DictStrKeyAnyValue__
    内部補足情報

"""

ExternalIdpDeterminant = dict[str, Any]
"""


Kyes of dict

* type: str
    
* name: str
    
* organization_name: str
    組織名。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* provider_id: str
    組織IDプロバイダーのID。[値の制約についてはこちら。](#section/API-Convention/APIID)
* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 

"""

FullAnnotation = dict[str, Any]
"""


Kyes of dict

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
* details: list[FullAnnotationDetail]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列
* updated_datetime: str
    更新日時。アノテーションが一つもない場合（教師付作業が未着手のときなど）は、未指定。
* annotation_format_version: str
    アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、Annofabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 

"""

FullAnnotationAdditionalData = dict[str, Any]
"""
属性情報 

Kyes of dict

* additional_data_definition_id: str
    属性ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* additional_data_definition_name: InternationalizationMessage
    
* type: AdditionalDataDefinitionType
    
* value: FullAnnotationAdditionalDataValue
    

"""

FullAnnotationAdditionalDataChoiceValue = dict[str, Any]
"""


Kyes of dict

* id: str
    選択肢ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* name: InternationalizationMessage
    

"""

FullAnnotationAdditionalDataValue = dict[str, Any]
"""
属性値 

Kyes of dict

* type: str
    Link
* value: str
    リンク先アノテーションID

"""

FullAnnotationAdditionalDataValueChoice = dict[str, Any]
"""


Kyes of dict

* type: str
    `Choice` 
* value: FullAnnotationAdditionalDataChoiceValue
    

"""

FullAnnotationAdditionalDataValueComment = dict[str, Any]
"""


Kyes of dict

* type: str
    `Comment` 
* value: str
    自由記述

"""

FullAnnotationAdditionalDataValueFlag = dict[str, Any]
"""


Kyes of dict

* type: str
    `Flag` 
* value: bool
    フラグのON(true)またはOFF(false)

"""

FullAnnotationAdditionalDataValueInteger = dict[str, Any]
"""


Kyes of dict

* type: str
    `Integer` 
* value: int
    整数値

"""

FullAnnotationAdditionalDataValueLink = dict[str, Any]
"""


Kyes of dict

* type: str
    Link
* value: str
    リンク先アノテーションID

"""

FullAnnotationAdditionalDataValueTracking = dict[str, Any]
"""


Kyes of dict

* type: str
    Tracking
* value: str
    トラッキングID

"""

FullAnnotationData = dict[str, Any]
"""
アノテーションのデータが格納されます。   * `FullAnnotationDataClassification`: 入力データ全体アノテーション   * `FullAnnotationDataSegmentation`: 塗りつぶしアノテーション   * `FullAnnotationDataSegmentationV2`: 塗りつぶしv2アノテーション   * `FullAnnotationDataBoundingBox`: 矩形アノテーション   * `FullAnnotationDataPoints`: ポリゴンまたはポリラインアノテーション   * `FullAnnotationDataSinglePoint`: 点アノテーション   * `FullAnnotationDataRange`: 動画区間アノテーション   * `FullAnnotationDataUnknown`: カスタムアノテーション 

Kyes of dict

* type: str
    `Unknown` 
* data_uri: str
    塗りつぶし画像のパス。 塗りつぶし画像のファイル形式はPNGです。塗りつぶされた部分の色は`rgba(255, 255, 255, 1)`、塗りつぶされていない部分の色は`rgba(0, 0, 0, 0)`です。 
* left_top: Point
    
* right_bottom: Point
    
* points: list[Point]
    頂点の座標値
* point: Point
    
* begin: float
    開始時間（ミリ秒）
* end: float
    終了時間（ミリ秒）
* data: str
    アノテーションデータを文字列で表現した値

"""

FullAnnotationDataBoundingBox = dict[str, Any]
"""


Kyes of dict

* left_top: Point
    
* right_bottom: Point
    
* type: str
    `BoundingBox` 

"""

FullAnnotationDataClassification = dict[str, Any]
"""


Kyes of dict

* type: str
    `Classification` 

"""

FullAnnotationDataPoints = dict[str, Any]
"""


Kyes of dict

* points: list[Point]
    頂点の座標値
* type: str
    `Points` 

"""

FullAnnotationDataRange = dict[str, Any]
"""


Kyes of dict

* begin: float
    開始時間（ミリ秒）
* end: float
    終了時間（ミリ秒）
* type: str
    `Range` 

"""

FullAnnotationDataSegmentation = dict[str, Any]
"""


Kyes of dict

* data_uri: str
    塗りつぶし画像のパス。 塗りつぶし画像のファイル形式はPNGです。塗りつぶされた部分の色は`rgba(255, 255, 255, 1)`、塗りつぶされていない部分の色は`rgba(0, 0, 0, 0)`です。 
* type: str
    `Segmentation` 

"""

FullAnnotationDataSegmentationV2 = dict[str, Any]
"""


Kyes of dict

* data_uri: str
    塗りつぶし画像のパス。 塗りつぶし画像のファイル形式はPNGです。塗りつぶされた部分の色は`rgba(255, 255, 255, 1)`、塗りつぶされていない部分の色は`rgba(0, 0, 0, 0)`です。 
* type: str
    `SegmentationV2` 

"""

FullAnnotationDataSinglePoint = dict[str, Any]
"""


Kyes of dict

* point: Point
    
* type: str
    `SinglePoint` 

"""

FullAnnotationDataUnknown = dict[str, Any]
"""


Kyes of dict

* data: str
    アノテーションデータを文字列で表現した値
* type: str
    `Unknown` 

"""

FullAnnotationDetail = dict[str, Any]
"""


Kyes of dict

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
    
* additional_data_list: list[FullAnnotationAdditionalData]
    属性情報。 

"""

GlobalIdpNameDeterminant = dict[str, Any]
"""
Annofab全体で利用するIDプロバイダー名を元に外部IDプロバイダーを特定する決定因子

Kyes of dict

* type: str
    
* name: str
    

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


HistogramItem = dict[str, Any]
"""


Kyes of dict

* begin: float
    
* end: float
    
* count: int
    

"""

IllegalState = dict[str, Any]
"""
作業が開始されていない、担当が割り当たっていない等のエラー

Kyes of dict

* type: str
    IllegalState

"""

InitiateMfaSetupRequest = dict[str, Any]
"""


Kyes of dict

* access_token: str
    アクセストークン。[login](#operation/login) APIで取得します。 

"""

InitiateMfaSetupResponse = dict[str, Any]
"""


Kyes of dict

* secret_code: str
    TOTPアルゴリズムでワンタイムコードを生成するために使用される、一意に生成された共有秘密コードです。 
* qr_code_data: str
    MFAを有効化する際、認証アプリで読み込むQRコードに埋め込むデータです。Google AuthenticatorとIIJ SmartKeyに対応しています。 

"""

InputData = dict[str, Any]
"""
入力データの情報を表すデータ構造です。

Kyes of dict

* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_set_id: str
    入力データセットID(システム内部用のプロパティ)。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_name: str
    入力データ名
* input_data_path: str
    入力データの実体が保存されたURLです。 URLスキームが s3 もしくは https であるもののみをサポートしています。 
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

InputDataList = dict[str, Any]
"""


Kyes of dict

* list: list[InputData]
    現在のページ番号に含まれる0件以上の入力データです。
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる入力データが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果の件数が1万件を超えた場合は`true`になります。
* aggregations: list[AggregationResult]
    システム内部用のプロパティ。 

"""


class InputDataOrder(Enum):
    """
    タスクに割り当てる入力データの順序  * `name_asc` - 入力データ名の昇順 * `name_desc` - 入力データ名の降順 * `random` - ランダム
    """

    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"
    RANDOM = "random"


InputDataRequest = dict[str, Any]
"""


Kyes of dict

* input_data_name: str
    入力データ名。ZIPファイルをアップロードする際は、入力データ名のプレフィックスを指定してください。
* input_data_path: str
    入力データの実体が存在するURLです。 Annofabにファイルをアップロードして入力データを作成する場合は、[createTempPath](#operation/createTempPath) APIで取得した`path`を指定してください。  入力データの実体が[プライベートストレージ](/docs/faq/#prst9c)に存在する場合は、スキームが s3 または https であるURLを指定してください。 S3プライベートストレージに存在するファイルを入力データとして登録する場合は、事前に[認可の設定](/docs/faq/#m0b240)が必要です。 
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 
* sign_required: bool
    CloudFrontのSignedCookieを使ったプライベートストレージを利用するかどうか。  `true`を指定する場合は，`input_data_path`にAnnofabのAWS IDをTrusted Signerとして登録したCloudFrontのURLを指定してください。 
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

InputDataSummary = dict[str, Any]
"""
ある入力データのバリデーション結果です。入力データIDをキーに引けるようにMap[入力データID, バリデーション結果]となっています

Kyes of dict

* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* inspection_summary: InspectionSummary
    
* annotation_summaries: list[ValidationError]
    

"""


class InputDataType(Enum):
    """
    アノテーションする入力データの種類。 * `image` - 画像 * `movie` - 動画 * `custom` - カスタム
    """

    IMAGE = "image"
    MOVIE = "movie"
    CUSTOM = "custom"


Inspection = dict[str, Any]
"""
検査コメント

Kyes of dict

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
* phrases: list[str]
    参照している定型指摘のID。
* comment: str
    検査コメントの中身 
* status: InspectionStatus
    
* created_datetime: str
    
* updated_datetime: str
    

"""

InspectionData = dict[str, Any]
"""
##### スレッドの先頭のコメントである（`parent_inspection_id` に値がない）場合  検査コメントの座標値や区間。  * `InspectionDataPoint`：点で検査コメントを付与したときの座標値 * `InspectionDataPolyline`：ポリラインで検査コメントを付与したときの座標値 * `InspectionDataTime`：検査コメントを付与した区間（動画プロジェクトの場合） * `InspectionDataCustom`：カスタム  ##### 返信コメントである（`parent_inspection_id` に値がある）場合  現在は使用しておらず、レスポンスに含まれる値は不定です。APIのレスポンスにこの値を含む場合でも、「スレッドの先頭のコメント」の値を利用してください。  リクエストボディに指定する場合は、スレッドの先頭のコメントと同じ値を指定します。 

Kyes of dict

* x: int
    
* y: int
    
* type: str
    `Custom` [詳しくはこちら](#section/API-Convention/API-_type) 
* coordinates: list[InspectionDataPolylineCoordinates]
    ポリラインを構成する頂点の配列 
* start: float
    開始時間（ミリ秒）。小数点以下はミリ秒以下を表します。
* end: float
    終了時間（ミリ秒）。小数点以下はミリ秒以下を表します。
* data: str
    

"""

InspectionDataCustom = dict[str, Any]
"""


Kyes of dict

* data: str
    
* type: str
    `Custom` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

InspectionDataPoint = dict[str, Any]
"""
問題のある部分を示す座標 

Kyes of dict

* x: int
    
* y: int
    
* type: str
    `Point` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

InspectionDataPolyline = dict[str, Any]
"""
問題のある部分を示すポリライン 

Kyes of dict

* coordinates: list[InspectionDataPolylineCoordinates]
    ポリラインを構成する頂点の配列 
* type: str
    `Polyline` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

InspectionDataPolylineCoordinates = dict[str, Any]
"""


Kyes of dict

* x: int
    
* y: int
    

"""

InspectionDataTime = dict[str, Any]
"""
問題のある時間帯を表す区間 

Kyes of dict

* start: float
    開始時間（ミリ秒）。小数点以下はミリ秒以下を表します。
* end: float
    終了時間（ミリ秒）。小数点以下はミリ秒以下を表します。
* type: str
    `Time` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

InspectionOrReplyRequired = dict[str, Any]
"""
新規検査コメントまたは未対応検査コメントへの返信が必要である時のエラー

Kyes of dict

* type: str
    InspectionOrReplyRequired

"""

InspectionPhrase = dict[str, Any]
"""


Kyes of dict

* id: str
    定型指摘ID
* text: InternationalizationMessage
    

"""

InspectionStatistics = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* date: str
    集計日
* breakdown: InspectionStatisticsBreakdown
    

"""

InspectionStatisticsBreakdown = dict[str, Any]
"""
検査コメント数の集計結果

Kyes of dict

* labels: dict(str, InspectionStatisticsPhrases)
    ラベルに紐付いている検査コメントの集計結果。キーは`label_id`です。
* no_label: InspectionStatisticsPhrases
    

"""

InspectionStatisticsPhrases = dict[str, Any]
"""


Kyes of dict

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


InspectionValidationError = dict[str, Any]
"""


Kyes of dict

* inspection: Inspection
    
* type: str
    IllegalState

"""

Instruction = dict[str, Any]
"""


Kyes of dict

* html: str
    作業ガイドのHTML
* last_updated_datetime: str
    更新日時

"""

InstructionHistory = dict[str, Any]
"""


Kyes of dict

* history_id: str
    作業ガイドの履歴ID
* account_id: str
    作業ガイドを更新したユーザーのアカウントID
* updated_datetime: str
    作業ガイドの最終更新日時

"""

InstructionImage = dict[str, Any]
"""


Kyes of dict

* image_id: str
    作業ガイド画像ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* path: str
    作業ガイド画像の実体が保存されたパスです。 
* url: str
    作業ガイド画像を取得するためのシステム内部用のURLです。
* etag: str
    [HTTPレスポンスヘッダー ETag](https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/ETag)に相当する値です。 

"""

InstructionImagePath = dict[str, Any]
"""


Kyes of dict

* url: str
    ファイルアップロード用の一時URLです。このURLにファイルをアップロードします。
* path: str
    作業ガイド画像のURL

"""

InternationalizationMessage = dict[str, Any]
"""


Kyes of dict

* messages: list[InternationalizationMessageMessages]
    言語コードとメッセージ（テキスト）のリスト。  * アノテーションエディタなどでは、Annofabの表示言語（各ユーザーが個人設定で選んだ言語）のメッセージが使われます * 以下の名前は、[Simple Annotation](#section/Simple-Annotation-ZIP) では `en-US` のメッセージが使われます     * ラベル名     * 属性名     * 選択肢名 * いずれの場合でも、表示しようとした言語が `messages` に含まれない場合、 `default_lang` に指定した言語のメッセージが使われます 
* default_lang: str
    希望された言語のメッセージが存在しない場合に、フォールバック先として使われる言語コード

"""

InternationalizationMessageMessages = dict[str, Any]
"""


Kyes of dict

* lang: str
    言語コード。`en-US` (英語) 、`ja-JP` (日本語)、 `vi-VN`（ベトナム語）のみサポートしています。
* message: str
    lang で指定された言語でのメッセージ

"""

InvalidAnnotationData = dict[str, Any]
"""
アノテーションデータ不正エラー

Kyes of dict

* label_id: str
    
* annotation_id: str
    
* message: str
    
* type: str
    InvalidAnnotationData

"""

InvalidChoice = dict[str, Any]
"""
選択肢不正エラー

Kyes of dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    InvalidChoice

"""

InvalidLinkTarget = dict[str, Any]
"""
リンク先アノテーションが許可されているラベルでないエラー

Kyes of dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    InvalidLinkTarget

"""

InvalidValue = dict[str, Any]
"""
値制約に合致しないエラー

Kyes of dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    InvalidValue

"""

InviteOrganizationMemberRequest = dict[str, Any]
"""


Kyes of dict

* role: OrganizationMemberRole
    

"""

IssuePersonalAccessTokenRequest = dict[str, Any]
"""


Kyes of dict

* id: str
    パーソナルアクセストークンのID。ユーザごとに一意な文字列。 [値の制約についてはこちら。](#section/API-Convention/APIID) 
* note: str
    人間可読なトークンの説明
* expiration: float
    トークンの期間。 単位はミリ秒
* permissions: list[PersonalAccessTokenPermission]
    トークンに与える権限

"""

IssueProjectGuestUserTokenRequest = dict[str, Any]
"""


Kyes of dict

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

IssueProjectTokenRequest = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトトークンの発行対象プロジェクトID
* description: str
    発行するトークンについての人間可読な説明

"""

IssuerOnlyOidcEndpoints = dict[str, Any]
"""
OIDCエンドポイント

Kyes of dict

* type: str
    
* issuer: str
    RFC 8414で定義されるissuerの値。 `.well-known/openid-configuration`のissuer。

"""

JobDetail = dict[str, Any]
"""
ジョブ結果の内部情報

Kyes of dict

* request: ProjectCopyRequest
    
* generated_task_count: int
    
* src_organization_id: str
    
* dest_organization_id: str
    
* src_input_data_set_id: str
    
* dest_input_data_set_id: str
    
* webhook: Webhook
    
* message: str
    
* replaced_body: str
    

"""

JobDetailCopyProject = dict[str, Any]
"""


Kyes of dict

* request: ProjectCopyRequest
    

"""

JobDetailGenInputs = dict[str, Any]
"""


Kyes of dict

* request: InputDataRequest
    

"""

JobDetailGenTasks = dict[str, Any]
"""


Kyes of dict

* request: TaskGenerateRequest
    
* generated_task_count: int
    

"""

JobDetailInvokeHook = dict[str, Any]
"""


Kyes of dict

* webhook: Webhook
    
* message: str
    
* replaced_body: str
    

"""

JobDetailMoveProject = dict[str, Any]
"""


Kyes of dict

* src_organization_id: str
    
* dest_organization_id: str
    
* src_input_data_set_id: str
    
* dest_input_data_set_id: str
    

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


Keybind = dict[str, Any]
"""


Kyes of dict

* code: str
    [KeyboardEvent.code](https://developer.mozilla.org/ja/docs/Web/API/KeyboardEvent/code)に相当する値です。 
* shift: bool
    Shiftキーを押しているかどうか
* ctrl: bool
    Ctrlキーを押しているかどうか
* alt: bool
    Altキーを押しているかどうか

"""

LabelStatistics = dict[str, Any]
"""


Kyes of dict

* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* completed: int
    ラベルごとの受入が完了したアノテーション数
* wip: int
    ラベルごとの受入が完了していないアノテーション数

"""

LabelV1 = dict[str, Any]
"""


Kyes of dict

* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_name: InternationalizationMessage
    
* keybind: list[Keybind]
    ショートカットキー
* annotation_type: AnnotationType
    
* bounding_box_metadata: BoundingBoxMetadata
    
* segmentation_metadata: SegmentationMetadata
    
* additional_data_definitions: list[AdditionalDataDefinitionV1]
    属性
* color: Color
    
* annotation_editor_feature: AnnotationEditorFeature
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

LabelV2 = dict[str, Any]
"""


Kyes of dict

* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_name: InternationalizationMessage
    
* keybind: list[Keybind]
    ショートカットキー
* annotation_type: AnnotationType
    
* bounding_box_metadata: BoundingBoxMetadata
    
* segmentation_metadata: SegmentationMetadata
    
* additional_data_definitions: list[str]
    ラベルに所属する属性のID
* color: Color
    
* annotation_editor_feature: AnnotationEditorFeature
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""

LabelV3 = dict[str, Any]
"""


Kyes of dict

* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_name: InternationalizationMessage
    
* keybind: list[Keybind]
    ショートカットキー
* annotation_type: AnnotationType
    
* field_values: dict(str, AnnotationTypeFieldValue)
    KeyがフィールドIdであるDictionaryです。  カスタムの[組織プラグイン](#operation/putOrganizationPlugin)で利用される[UserDefinedAnnotationTypeDefinition](#section/UserDefinedAnnotationTypeDefinition).`field_definitions`で定義されます。 
* additional_data_definitions: list[str]
    ラベルに所属する属性のID
* color: Color
    
* metadata: dict(str, str)
    ユーザーが自由に登録できるkey-value型のメタデータです。 

"""


class Lang(Enum):
    """
    表示言語 * `ja-JP` - 日本語 * `en-US` - 英語 * `vi-VN` - ベトナム語
    """

    EN_US = "en-US"
    JA_JP = "ja-JP"
    VI_VN = "vi-VN"


LoginNeedChallengeResponse = dict[str, Any]
"""


Kyes of dict

* session: str
    セッション

"""

LoginRequest = dict[str, Any]
"""


Kyes of dict

* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* password: str
    パスワード

"""

LoginRespondToAuthChallengeRequest = dict[str, Any]
"""


Kyes of dict

* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* mfa_code: str
    MFAコード。Time-based One-time Password (TOTP) のみ対応している
* session: str
    [login API](#operation/login)が返したセッション 

"""

LoginResponse = dict[str, Any]
"""


Kyes of dict

* token: Token
    
* session: str
    セッション

"""

LoginSucceedResponse = dict[str, Any]
"""


Kyes of dict

* token: Token
    

"""

Marker = dict[str, Any]
"""


Kyes of dict

* marker_id: str
    マーカーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* title: str
    マーカーのタイトル
* graph_type: GraphType
    
* marked_at: str
    グラフ上のマーカー位置(x軸)

"""

Markers = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* markers: list[Marker]
    マーカー一覧
* updated_datetime: str
    更新日時

"""

Message = dict[str, Any]
"""


Kyes of dict

* message: str
    メッセージ
* message_id: str
    システム内部用のプロパティ

"""

MessageOrJobInfo = dict[str, Any]
"""


Kyes of dict

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
* job_detail: JobDetail
    
* errors: Errors
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

MfaSetting = dict[str, Any]
"""


Kyes of dict

* enabled: bool
    MFAが有効か (trueの場合に有効)
* is_updatable: bool
    MFA設定を更新可能か (falseの場合、MFA設定の更新不可)。「Sign in with Google」でログインしたユーザーがAPIを実行した場合falseとなる。 

"""

MyAccount = dict[str, Any]
"""


Kyes of dict

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
* errors: list[str]
    システム内部用のプロパティ

"""

MyAccountAllOf = dict[str, Any]
"""


Kyes of dict

* reset_requested_email: str
    システム内部用のプロパティ
* errors: list[str]
    システム内部用のプロパティ

"""

MyNotificationList = dict[str, Any]
"""
自分に届いているユーザー通知の取得結果です。

Kyes of dict

* messages: list[MyNotificationMessage]
    
* opened: int
    開封済みの通知メッセージの数。 over_limitがtrueの場合、メッセージのタイムスタンプが新しい順から10000件のメッセージをもとに集計される 
* total: int
    通知メッセージの総数 
* page: int
    messagesに含まれる通知メッセージが何ページ目のものか 
* page_total: int
    ページ数の総数 
* over_limit: bool
    通知メッセージの取得上限を超えているか 

"""

MyNotificationMessage = dict[str, Any]
"""
自分への通知メッセージの情報です。

Kyes of dict

* message_id: str
    通知メッセージID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* title: str
    メッセージ通知のタイトル 
* body: str
    メッセージ通知の本文 
* content_type: str
    メッセージのコンテンツタイプ。 メッセージを表示する際のマークアップのヒントとして使われることを想定しています。 
* opened: bool
    自身がメッセージを開封したか(開封済みの場合true) 
* timestamp: str
    最後に通知メッセージ内容を更新した日時。更新がない場合はメッセージ作成日時 
* created_datetime: str
    メッセージ作成日時 

"""

MyNotificationUnreadMessagesCount = dict[str, Any]
"""
通知メッセージの未読件数

Kyes of dict

* unread: int
    通知メッセージの未読件数

"""

MyOrganization = dict[str, Any]
"""


Kyes of dict

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

MyOrganizationList = dict[str, Any]
"""


Kyes of dict

* list: list[MyOrganization]
    現在のページ番号に含まれる0件以上の所属組織です。
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる所属組織が0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: list[AggregationResult]
    システム内部用のプロパティ。 

"""

NoCommentInspection = dict[str, Any]
"""
空の検査コメントがある時のエラー

Kyes of dict

* inspection: Inspection
    
* type: str
    NoCommentInspection

"""

OidcAttributeMapping = dict[str, Any]
"""
外部IDプロバイダー上の属性と、Annofabが認識する属性のマッピング

Kyes of dict

* email: str
    Eメールアドレスを表す外部IDプロバイダー上の属性名
* name: str
    ユーザーの表示名を表す外部IDプロバイダー上の属性名

"""

OidcEndpoints = dict[str, Any]
"""


Kyes of dict

* type: str
    
* issuer: str
    RFC 8414で定義されるissuerの値。 `.well-known/openid-configuration`のissuer。
* authorize_url: str
    RFC 8414（及びRFC6749）で定義される、authorization_endpointのURL
* token_url: str
    RFC 8414（及びRFC6749）で定義される、token_endpointのURL
* userinfo_url: str
    OpenID Connect Core 1.0で定義される、UserInfo EndpointのURL
* jwks_url: str
    RFC 8414で定義される、jwks_uriの値

"""

Organization = dict[str, Any]
"""


Kyes of dict

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

OrganizationActivity = dict[str, Any]
"""


Kyes of dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* created_datetime: str
    作成日時
* storage_usage_bytes: int
    Annofabストレージの使用量[バイト]

"""

OrganizationCacheRecord = dict[str, Any]
"""


Kyes of dict

* input: str
    
* members: str
    
* statistics: str
    
* organization: str
    

"""

OrganizationIdpIdDeterminant = dict[str, Any]
"""
組織名とIDプロバイダーIDを元に外部IDプロバイダーを特定する決定因子

Kyes of dict

* type: str
    
* organization_name: str
    組織名。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* provider_id: str
    組織IDプロバイダーのID。[値の制約についてはこちら。](#section/API-Convention/APIID)

"""

OrganizationJobInfo = dict[str, Any]
"""


Kyes of dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* job_type: str
    ジョブの同時実行制御のために用いる、ジョブの種別。 (現在はまだ、この種別に該当するものはありません) 
* job_id: str
    ジョブID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* job_status: JobStatus
    
* job_execution: __DictStrKeyAnyValue__
    ジョブの内部情報
* job_detail: JobDetail
    
* errors: Errors
    
* created_datetime: str
    
* updated_datetime: str
    

"""

OrganizationJobInfoContainer = dict[str, Any]
"""


Kyes of dict

* list: list[OrganizationJobInfo]
    バックグラウンドジョブの一覧。作成日時の降順でソートされています。
* has_next: bool
    さらに古いジョブが存在する場合は`true`です。取得したジョブ一覧の中で`created_datetime`が最も古い値を、クエリパラメータ`exclusive_start_created_datetime`に指定することで、さらに古いジョブを取得することができます。

"""

OrganizationMember = dict[str, Any]
"""


Kyes of dict

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

OrganizationMemberList = dict[str, Any]
"""


Kyes of dict

* list: list[OrganizationMember]
    組織メンバーの一覧
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまる組織メンバーが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: list[AggregationResult]
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


OrganizationOidcIdp = dict[str, Any]
"""
組織が利用する外部IDプロバイダー設定

Kyes of dict

* id: str
    組織IDプロバイダーのID。[値の制約についてはこちら。](#section/API-Convention/APIID)
* organization_name: str
    組織名。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* client_id: str
    外部IDプロバイダーで指定されたクライアントID
* client_secret: str
    外部IDプロバイダーで指定されたクライアントシークレット
* attributes_request_method: str
    ユーザー属性を取得する際に利用するリクエストメソッド 
* endpoints: OidcEndpoints
    
* attribute_mapping: OidcAttributeMapping
    
* sign_up_url: str
    組織IDプロバイダーを用いたユーザ登録時、ユーザがアクセスすべきURL 
* created_datetime: str
    IDプロバイダー設定の作成日時
* updated_datetime: str
    IDプロバイダー設定の更新日時

"""

OrganizationPlugin = dict[str, Any]
"""


Kyes of dict

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
* project_extra_data_kinds: list[str]
    このプラグインが適用されたプロジェクトで使用可能となるProjectExtraDataKindのId列。 
* created_datetime: str
    
* updated_datetime: str
    

"""

OrganizationPluginCompatibility = dict[str, Any]
"""
プラグイン間の互換性を表します。未指定の場合はinput、outputともに`Top`の`OrganizationPluginCompatibilityType`が設定されます。

Kyes of dict

* input: OrganizationPluginCompatibilityType
    
* output: OrganizationPluginCompatibilityType
    

"""

OrganizationPluginCompatibilityType = dict[str, Any]
"""
プラグインの入力/出力を表す型です。 

Kyes of dict

* type: str
    Constant型で、かつidの値が一致している場合に互換性があることを示します。 
* id: str
    

"""

OrganizationPluginCompatibilityTypeBottom = dict[str, Any]
"""


Kyes of dict

* type: str
    inputに指定した場合、いずれのプラグインも前段になれないことを示します。 outputに指定した場合、いずれのプラグインも後段になれないことを示します。 

"""

OrganizationPluginCompatibilityTypeConstant = dict[str, Any]
"""


Kyes of dict

* type: str
    Constant型で、かつidの値が一致している場合に互換性があることを示します。 
* id: str
    

"""

OrganizationPluginCompatibilityTypeTop = dict[str, Any]
"""


Kyes of dict

* type: str
    inputに指定した場合、あらゆるプラグインの後段になれることを示します。 outputに指定した場合、入力がTopであるプラグインだけが後段になれることを示します。 

"""

OrganizationPluginList = dict[str, Any]
"""


Kyes of dict

* list: list[OrganizationPlugin]
    プラグイン一覧
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるプロジェクトが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: list[__DictStrKeyAnyValue__]
    システム内部用のプロパティ。 

"""

OrganizationRegistrationRequest = dict[str, Any]
"""


Kyes of dict

* organization_name: str
    組織名。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* organization_email: str
    メールアドレス

"""

OverlappedRangeAnnotation = dict[str, Any]
"""
区間が重複しているアノテーションが存在している場合に発生するエラー

Kyes of dict

* label_id: str
    
* annotation_id: str
    
* type: str
    OverlappedRangeAnnotation

"""

PasswordResetRequest = dict[str, Any]
"""


Kyes of dict

* email: str
    

"""

PersonalAccessToken = dict[str, Any]
"""
パーソナルアクセストークン

Kyes of dict

* id: str
    パーソナルアクセストークンのID。ユーザごとに一意な文字列。 [値の制約についてはこちら。](#section/API-Convention/APIID) 
* token: str
    APIアクセスに用いるトークン文字列。 リクエストヘッダにおいて `Authorization: Bearer {token}` の形で指定します。 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* note: str
    人間可読なトークンの説明
* expired_datetime: str
    トークンの有効期限
* permissions: list[PersonalAccessTokenPermission]
    トークンが持つ権限
* created_datetime: str
    トークンの作成時刻
* last_used_datetime: str
    トークンの最終利用時刻

"""

PersonalAccessTokenInfo = dict[str, Any]
"""
パーソナルアクセストークンから実際のトークン文字列を取り除いたもの

Kyes of dict

* id: str
    パーソナルアクセストークンのID。ユーザごとに一意な文字列。 [値の制約についてはこちら。](#section/API-Convention/APIID) 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* note: str
    人間可読なトークンの説明
* expired_datetime: str
    トークンの有効期限
* permissions: list[PersonalAccessTokenPermission]
    トークンが持つ権限
* created_datetime: str
    トークンの作成時刻
* last_used_datetime: str
    トークンの最終利用時刻

"""

PersonalAccessTokenPermission = dict[str, Any]
"""


Kyes of dict


"""

PersonalAccessTokenPermissionAll = dict[str, Any]
"""
トークンにトークン発行者と完全に同等の権限を与える

Kyes of dict

* type: str
    

"""

PhaseStatistics = dict[str, Any]
"""


Kyes of dict

* phase: TaskPhase
    
* worktime: str
    累積作業時間（ISO 8601 duration）

"""

PluginDetail = dict[str, Any]
"""
* `PluginDetailAnnotationEditor` - カスタムアノテーションエディタ用のプラグインを表します。 * `PluginDetailTaskAssignment` - カスタムタスク割当用のプラグインを表します。 * `PluginDetailAnnotationSpecs` - カスタムアノテーション仕様用のプラグインを表します。 * `PluginDetailExtendedAnnotationSpecs` - カスタムのアノテーション種別を作成するプラグインを表します。 

Kyes of dict

* url: str
    カスタムアノテーション仕様画面の URL です。 プラグイン種別がカスタムアノテーション仕様の場合のみ有効です。  この URL には、プロジェクトを特定するための以下のパラメータを必ず埋め込んでください。  * `{projectId}` 
* auth_redirect_url: str
    認証後のリダイレクト先 
* compatible_input_data_types: list[InputDataType]
    プラグインが対応している入力データです。 プラグイン種別がカスタムアノテーションエディタ、またはカスタムアノテーション仕様の場合のみ有効です。 
* type: str
    `ExtendedAnnotationSpecs` [詳しくはこちら](#section/API-Convention/API-_type) 
* plugin_compatibility: OrganizationPluginCompatibility
    
* annotation_types: list[AnnotationType]
    プラグインを使用したプロジェクトで選択可能なアノテーション種別のリストです。 同じ種別を重複して設定することはできません。 
* user_defined_annotation_type_definitions: dict(str, UserDefinedAnnotationTypeDefinition)
    Keyが[アノテーションの種類(AnnotationType)](#section/AnnotationType)であるDictionaryです。 

"""

PluginDetailAnnotationEditor = dict[str, Any]
"""
カスタムアノテーションエディタ用のプラグインを表します。 

Kyes of dict

* url: str
    カスタムアノテーションエディタでタスクを開くための URL です。 プラグインを使用するプロジェクトのタスク一覧などで使用されます。 プラグイン種別がカスタムアノテーションエディタの場合のみ有効です。  この URL には、タスクを特定するための以下のパラメータを必ず埋め込んでください。  * `{projectId}` * `{taskId}`  以下のパラメーターは任意で指定します。  * `{inputDataId}`: アノテーション一覧などから、特定の入力データにフォーカスした状態でタスクを開くときなどに指定します。 * `{annotationId}`: アノテーション一覧などから、特定のアノテーションにフォーカスした状態でタスクを開くときなどに指定します。 
* auth_redirect_url: str
    認証後のリダイレクト先。このURLに `?code=xxx` をつけてリダイレクトされます。 url プロパティとは異なり、 `{projectId}` や `{taskId}` といったパラメータの置換は行われません。  詳しくは [requestPluginToken API](#operation/requestPluginToken) を参照してください。 
* compatible_input_data_types: list[InputDataType]
    プラグインが対応している入力データです。 プラグイン種別がカスタムアノテーションエディタ、またはカスタムアノテーション仕様の場合のみ有効です。 
* type: str
    `AnnotationEditor` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

PluginDetailAnnotationSpecs = dict[str, Any]
"""
カスタムアノテーション仕様用のプラグインを表します。 

Kyes of dict

* url: str
    カスタムアノテーション仕様画面の URL です。 プラグイン種別がカスタムアノテーション仕様の場合のみ有効です。  この URL には、プロジェクトを特定するための以下のパラメータを必ず埋め込んでください。  * `{projectId}` 
* auth_redirect_url: str
    認証後のリダイレクト先 
* compatible_input_data_types: list[InputDataType]
    プラグインが対応している入力データです。 プラグイン種別がカスタムアノテーションエディタ、またはカスタムアノテーション仕様の場合のみ有効です。 
* type: str
    `AnnotationSpecs` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

PluginDetailExtendedAnnotationSpecs = dict[str, Any]
"""
カスタムのアノテーション種別を作成するプラグインを表します。 なお、このプラグインが設定されているプロジェクトでは、ここで指定したアノテーション種別以外は使用できなくなります。 

Kyes of dict

* plugin_compatibility: OrganizationPluginCompatibility
    
* annotation_types: list[AnnotationType]
    プラグインを使用したプロジェクトで選択可能なアノテーション種別のリストです。 同じ種別を重複して設定することはできません。 
* user_defined_annotation_type_definitions: dict(str, UserDefinedAnnotationTypeDefinition)
    Keyが[アノテーションの種類(AnnotationType)](#section/AnnotationType)であるDictionaryです。 
* compatible_input_data_types: list[InputDataType]
    プラグインが対応している入力データです。 プラグイン種別がカスタムアノテーションエディタ、またはカスタムアノテーション仕様の場合のみ有効です。 
* type: str
    `ExtendedAnnotationSpecs` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

PluginDetailTaskAssignment = dict[str, Any]
"""
カスタムタスク割当用のプラグインを表します。 

Kyes of dict

* url: str
    「カスタムタスク割当API」のURLです。 プラグイン種別がカスタムタスク割当の場合のみ有効です。  #### カスタムタスク割当APIについて。  * 独自のアルゴリズムで作業者にタスクを割当するAPIです。 * Annofabから提供されるものではなく、第三者 (ユーザー様) が用意します。 * 作業者がタスク一覧やアノテーションエディタのタスク取得ボタンを押すと、指定したURLに複数の情報 (※1) と共にHTTPリクエスト (POST) が送られます。 * カスタムタスク割当APIでは、Annofabで提供しているAPI (※2) を使用して作業者にタスクを割当してください。 * タスクの割当に成功した場合は以下のHTTPレスポンスを返却してください。   * レスポンスヘッダ: `Access-Control-Allow-Origin: https://annofab.com`   * レスポンスボディ: 割当した単一の[タスク](https://annofab.com/docs/api/#section/Task)   * ステータスコード: 200 * 作業者に割当できるタスクがない場合は以下のHTTPレスポンスを返却してください。   * レスポンスヘッダ: `Access-Control-Allow-Origin: https://annofab.com`   * レスポンスボディ: `{\"errors\": [{\"error_code\": \"MISSING_RESOURCE\"}]}`   * ステータスコード: 404 * 作業者の認証トークンの期限が切れている場合があります。その場合は以下のHTTPレスポンスを返却してください。   * レスポンスヘッダ: `Access-Control-Allow-Origin: https://annofab.com`   * レスポンスボディ: `{\"errors\": [{\"error_code\": \"EXPIRED_TOKEN\"}]}`   * ステータスコード: 401  #### Preflightリクエストについて。  * Annofabからカスタムタスク割当APIへCross-OriginなHTTPリクエストを送信するより前に、ブラウザの仕様により「Preflightリクエスト」と呼ばれるHTTPリクエストが送られます。 * カスタムタスク割当を利用するためには、カスタムタスク割当APIとは別に「Preflightリクエスト対応API」を用意する必要があります。 * 以下の要件を満たす「Preflightリクエスト対応API」を用意してください。   * URL: カスタムタスク割当APIと同じURL   * HTTPメソッド: OPTIONS   * レスポンスヘッダ:     * `Access-Control-Allow-Origin: https://annofab.com`     * `Access-Control-Allow-Headers: Content-Type`   * レスポンスボディ: 空(から)   * ステータスコード: 200  ※1 以下の情報が送られます。  * HTTPボディ (JSON形式)   * `authorization_token` : タスク割当専用の認証トークン。AnnofabのAPIを利用する際に使用します。   * `project_id` : タスクの割当リクエストが行われたプロジェクトのID。   * `phase` : 作業者が割当を要求したタスクフェーズ。このフェーズのタスクを割当してください。  ※2 例えば以下のAPIがあります。(詳しい情報はAPIドキュメントを参照してください)  * `getMyAccount` : 作業者のアカウント情報を取得できます。 * `getTasks` : プロジェクトのタスクを取得できます。 * `assignTasks` : 作業者にタスクを割当することができます。 
* type: str
    `TaskAssignment` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

PluginTokenRequest = dict[str, Any]
"""


Kyes of dict

* type: str
    `RefreshToken` を指定します
* authorization_code: str
    リダイレクト時にクエリパラメータ `code` として受け取った文字列
* code_verifier: str
    認可リクエスト時に渡した `code_challenge` に対応するverifier文字列
* refresh_token: str
    前回のトークン発行で得られた `refresh_token`

"""

PluginTokenRequestAuthorizationCode = dict[str, Any]
"""


Kyes of dict

* type: str
    `AuthorizationCode` を指定します
* authorization_code: str
    リダイレクト時にクエリパラメータ `code` として受け取った文字列
* code_verifier: str
    認可リクエスト時に渡した `code_challenge` に対応するverifier文字列

"""

PluginTokenRequestRefreshToken = dict[str, Any]
"""


Kyes of dict

* type: str
    `RefreshToken` を指定します
* refresh_token: str
    前回のトークン発行で得られた `refresh_token`

"""

PluginTokenResponse = dict[str, Any]
"""


Kyes of dict

* access_token: str
    APIアクセスに用いるトークン。 リクエストヘッダにおいて `Authorization: Bearer {access_token}` の形で指定します。 
* refresh_token: str
    トークンの更新に用いるトークン

"""

Point = dict[str, Any]
"""
点の座標値

Kyes of dict

* x: int
    X座標の値[ピクセル]
* y: int
    Y座標の値[ピクセル]

"""

PositionForMinimumBoundingBoxInsertion = dict[str, Any]
"""
`annotation_type` が `bounding_box` かつ `min_warn_rule` が `and` または `or` の場合のみ、挿入する最小矩形アノテーションの原点を指定できます。 画像左上の座標が「x=0, y=0」です。 未指定、もしくは「画像外に飛び出たアノテーション」を許可していないにも関わらず飛び出してしまう場合は、表示範囲の中央に挿入されます。 「スキャンした帳票の記入欄」や「定点カメラで撮影した製品ラベル」など、アノテーションしたい位置やサイズが多くの画像で共通している場合に便利です。  `annotation_type` が `bounding_box` 以外の場合は必ず未指定となります。 

Kyes of dict

* x: int
    
* y: int
    

"""

PostAnnotationArchiveUpdateResponse = dict[str, Any]
"""


Kyes of dict

* job: ProjectJobInfo
    

"""

PostAnnotationArchiveUpdateResponseWrapper = dict[str, Any]
"""


Kyes of dict

* message: str
    メッセージ
* message_id: str
    システム内部用のプロパティ
* job: ProjectJobInfo
    

"""

PostExchangeCodeLoginResponse = dict[str, Any]
"""


Kyes of dict

* token: Token
    

"""

PostExchangeCodeResponse = dict[str, Any]
"""


Kyes of dict

* token: Token
    
* temporary_token: Token
    

"""

PostMfaSettingRequest = dict[str, Any]
"""


Kyes of dict

* enabled: bool
    MFAをONにするか
* mfa_code: str
    [initiateMfaSetup](#operation/initiateMfaSetup)が返したシークレットコードを元に生成したTOTP。enabledがtrueの場合に設定する 
* access_token: str
    アクセストークン。enabledがtrueの場合に設定する

"""

PostProjectTasksUpdateResponse = dict[str, Any]
"""


Kyes of dict

* job: ProjectJobInfo
    

"""


class PricePlan(Enum):
    """
    料金プラン * `free` - フリープラン * `business` - ビジネスプラン
    """

    FREE = "free"
    BUSINESS = "business"


Project = dict[str, Any]
"""


Kyes of dict

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
    
* configuration: ProjectConfigurationGet
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時
* summary: ProjectSummary
    

"""

ProjectAccountStatistics = dict[str, Any]
"""


Kyes of dict

* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* histories: list[ProjectAccountStatisticsHistory]
    

"""

ProjectAccountStatisticsHistory = dict[str, Any]
"""


Kyes of dict

* date: str
    
* tasks_completed: int
    教師付フェーズのタスクを提出した回数、または検査/受入フェーズのタスクを合格/差戻にした回数。  たとえば、あるタスクのタスク履歴が下表の状態だった場合、2020-04-01の`tasks_completed`は以下の通りになります。  * Alice: 1 * Bob: 1 * Chris: 2   <table>   <tr>     <th>担当者</th>     <th>フェーズ</th>     <th>作業内容</th>     <th>完了日時</th>   </tr>   <tr>     <td>Alice</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 09:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>差し戻す</td>     <td>2020-04-01 10:00</td>   </tr>   <tr>     <td>Bob</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 11:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>合格にする</td>     <td>2020-04-01 12:00</td>   </tr> </table> 
* tasks_rejected: int
    教師付フェーズを担当したタスクが差し戻された回数、または受入フェーズを担当したタスクが受入完了を取り消された回数。  たとえば、あるタスクのタスク履歴が下表の状態だった場合、2020-04-01の`tasks_rejected`は以下の通りになります。  * Alice: 1 * Bob: 1 * Chris: 1   <table>   <tr>     <th>担当者</th>     <th>フェーズ</th>     <th>作業内容</th>     <th>完了日時</th>   </tr>   <tr>     <td>Alice</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 09:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>差し戻す</td>     <td>2020-04-01 10:00</td>   </tr>   <tr>     <td>Bob</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 11:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>差し戻す</td>     <td>2020-04-01 12:00</td>   </tr>   <tr>     <td>Bob</td>     <td>教師付</td>     <td>提出する</td>     <td>2020-04-01 13:00</td>   </tr>   <tr>     <td>Chris</td>     <td>受入</td>     <td>合格にする</td>     <td>2020-04-01 14:00</td>   </tr>   <tr>     <td>Dave</td>     <td>受入</td>     <td>受入完了状態を取り消して、再度合格にする</td>     <td>2020-04-01 15:00</td>   </tr> </table> 
* worktime: str
    作業時間（ISO 8601 duration）

"""

ProjectCacheRecord = dict[str, Any]
"""


Kyes of dict

* input: str
    
* members: str
    
* project: str
    
* instruction: str
    
* specs: str
    
* statistics: str
    
* organization: str
    
* supplementary: str
    

"""

ProjectConfigurationGet = dict[str, Any]
"""


Kyes of dict


"""

ProjectConfigurationPut = dict[str, Any]
"""
プロジェクトの設定情報

Kyes of dict

* number_of_inspections: int
    検査回数。 * 0回：教師付け -> 受入 * 1回：教師付け -> 検査 -> 受入 * n回(n >= 2)：教師付け -> 検査1 -> ... -> 検査n -> 受入 
* assignee_rule_of_resubmitted_task: AssigneeRuleOfResubmittedTask
    
* task_assignment_type: TaskAssignmentType
    
* task_assignment_property: TaskAssignmentProperty
    
* max_tasks_per_member: int
    保留中のタスクを除き、1人（オーナー以外）に割り当てられるタスク数の上限。 
* max_tasks_per_member_including_hold: int
    保留中のタスクを含めて、1人（オーナー以外）に割り当てられるタスク数上限の保留分。 割り当て時の上限チェックは、max_tasks_per_memberとこの数字の合計で行われます。  例えばmax_tasks_per_memberが10、max_tasks_per_member_including_holdが20の場合、保留中を含むタスク数の割り当て上限は30になります。 
* input_data_set_id_list: list[str]
    システム内部用のプロパティ。 [putProject](#operation/putProject) APIでプロジェクトを更新する際は、[getProject](#operation/getProject) APIで取得した値を指定してください。 
* input_data_max_long_side_length: int
    入力データ画像の長辺の最大値（未指定時は4096px）。  画像をアップロードすると、長辺がこの値になるように画像が自動で圧縮されます。 アノテーションの座標は、もとの解像度の画像でつけたものに復元されます。  大きな数値を設定すると入力データ画像のサイズが大きくなり、生産性低下やブラウザで画像を表示できない懸念があります。注意して設定してください。 
* sampling_inspection_rate: int
    抜取検査率[%]。未指定の場合は100%として扱う。
* sampling_acceptance_rate: int
    抜取受入率[%]。未指定の場合は100%として扱う。
* private_storage_aws_iam_role_arn: str
    AWS IAMロール。S3プライベートストレージの認可で使います。 [S3プライベートストレージの認可の設定についてはこちら](/docs/faq/#m0b240)をご覧ください。 
* plugin_id: str
    プラグインID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* custom_task_assignment_plugin_id: str
    プラグインID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* custom_specs_plugin_id: str
    プラグインID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* extended_specs_plugin_id: str
    プラグインID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* editor_version: str
    標準アノテーションエディタのバージョン。  * `stable`     * 安定版。通常はこちらを利用してください。 * `preview`     * 最新版。新機能やUI変更の先行リリース版。  プロジェクト更新時に未指定の場合は `stable` が指定されたものとみなします。 
* use_beginner_navigation: bool
    true の場合、プロジェクトの画面でナビゲーションUIを表示します（ログインユーザーがプロジェクトオーナーの場合のみ）。 

"""

ProjectCopyRequest = dict[str, Any]
"""


Kyes of dict

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

ProjectCopyResponse = dict[str, Any]
"""


Kyes of dict

* job: ProjectJobInfo
    
* dest_project: Project
    

"""

ProjectExtraData = dict[str, Any]
"""
プロジェクトの追加データ。 追加のプロジェクトの設定や、プロジェクトに対するユーザ毎のデータを表す。 (project_id, account_id, kind_id)の組み合わせで一意になり、account_idが指定指定されていない場合はユーザに割りつかず、プロジェクト自体に割りついている値を表す。 

Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* kind_id: str
    プロジェクト追加データの種別ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* value: ProjectExtraDataValue
    

"""

ProjectExtraDataKind = dict[str, Any]
"""
プロジェクトの追加データの種別。 

Kyes of dict

* id: str
    プロジェクト追加データの種別ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* display_name: InternationalizationMessage
    
* schema: __DictStrKeyAnyValue__
    プロジェクト追加データのスキーマを表す構造。
* scope: ProjectExtraDataKindScope
    
* default_value: __DictStrKeyAnyValue__
    プロジェクト追加データの値。 nullを除く任意のJson

"""


class ProjectExtraDataKindScope(Enum):
    """
    プロジェクト追加データがユーザーとプロジェクトに割りつくかどうかを表す列挙値。  - `project` => プロジェクトにのみ割りつき、ユーザには割りつかない - `user` => ユーザにのみ割りつき、プロジェクトには割りつかない - `both` => プロジェクトとユーザの両方に割りつく
    """

    PROJECT = "project"
    USER = "user"
    BOTH = "both"


ProjectExtraDataValue = dict[str, Any]
"""


Kyes of dict

* type: str
    
* value: __DictStrKeyAnyValue__
    プロジェクト追加データの値。 nullを除く任意のJson
* updated_datetime: str
    データが最後に更新された日時

"""

ProjectExtraDataValueDefault = dict[str, Any]
"""
保存されているデータが無く、デフォルト値が設定されている場合

Kyes of dict

* type: str
    
* value: __DictStrKeyAnyValue__
    プロジェクト追加データの値。 nullを除く任意のJson

"""

ProjectExtraDataValueEmpty = dict[str, Any]
"""
保存されているデータが無く、デフォルト値も設定されていない場合

Kyes of dict

* type: str
    

"""

ProjectExtraDataValueSaved = dict[str, Any]
"""
保存されているデータがある場合

Kyes of dict

* type: str
    
* value: __DictStrKeyAnyValue__
    プロジェクト追加データの値。 nullを除く任意のJson
* updated_datetime: str
    データが最後に更新された日時

"""

ProjectGuestUserProfile = dict[str, Any]
"""
ゲストユーザーのプロフィール情報

Kyes of dict

* user_id: str
    ゲストユーザーのIDです。 同じ文字列の場合、同じゲストユーザーとして認識されます。 [値の制約についてはこちら。](#section/API-Convention/APIID)
* user_name: str
    ユーザー名
* lang: str
    ゲストユーザーのUIの表示言語です
* key_layout: KeyLayout
    

"""

ProjectInputsUpdateResponse = dict[str, Any]
"""


Kyes of dict

* job: ProjectJobInfo
    

"""

ProjectJobInfo = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* job_type: ProjectJobType
    
* job_id: str
    ジョブID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* job_status: JobStatus
    
* job_execution: __DictStrKeyAnyValue__
    ジョブの内部情報
* job_detail: JobDetail
    
* errors: Errors
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

ProjectJobInfoContainer = dict[str, Any]
"""


Kyes of dict

* list: list[ProjectJobInfo]
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


ProjectList = dict[str, Any]
"""


Kyes of dict

* list: list[Project]
    現在のページ番号に含まれる0件以上のプロジェクトです。
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるプロジェクトが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: list[AggregationResult]
    システム内部用のプロパティ 

"""

ProjectMember = dict[str, Any]
"""


Kyes of dict

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

ProjectMemberList = dict[str, Any]
"""


Kyes of dict

* list: list[ProjectMember]
    プロジェクトメンバーの一覧
* page_no: float
    現在のページ番号。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるプロジェクトメンバーが0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: list[AggregationResult]
    システム内部用のプロパティ 

"""

ProjectMemberRequest = dict[str, Any]
"""


Kyes of dict

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


ProjectSummary = dict[str, Any]
"""
プロジェクトのサマリー情報

Kyes of dict

* last_tasks_updated_datetime: str
    タスクの最終更新日時

"""

ProjectTaskCounts = dict[str, Any]
"""


Kyes of dict

* task_counts: list[ProjectTaskCountsTaskCounts]
    

"""

ProjectTaskCountsTaskCounts = dict[str, Any]
"""


Kyes of dict

* phase: TaskPhase
    
* status: TaskStatus
    
* count: float
    該当するタスクの数

"""

ProjectTaskStatistics = dict[str, Any]
"""


Kyes of dict

* phase: TaskPhase
    
* status: TaskStatus
    
* count: int
    タスク数
* work_timespan: int
    累計実作業時間(ミリ秒)

"""

ProjectTaskStatisticsHistory = dict[str, Any]
"""


Kyes of dict

* date: str
    日付
* tasks: list[ProjectTaskStatistics]
    タスクのフェーズごと、ステータスごとの情報

"""

ProjectToken = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトトークンの発行対象プロジェクトID
* token: str
    プロジェクトトークン文字列。 [issueProjectGuestUserToken](#operation/issueProjectGuestUserToken)への入力となります。
* info: ProjectTokenInfo
    

"""

ProjectTokenInfo = dict[str, Any]
"""
プロジェクトトークンについての付加情報

Kyes of dict

* created_date_time: str
    トークンの作成日時
* last_used_date_time: str
    トークンが最後に利用された日時
* description: str
    トークンについての人間可読な説明

"""

PutAnnotationRequest = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* details: list[AnnotationDetailV1]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutAnnotationThumbnailBody = dict[str, Any]
"""
アノテーションのサムネイル更新リクエスト

Kyes of dict

* images: list[AnnotationThumbnailImageSource]
    アップロードするサムネイル画像の一覧
* annotations: dict(str, AnnotationThumbnailDetail)
    アノテーションIDをキーとしたサムネイル情報
* annotation_updated_datetime: str
    サムネイルの元になったアノテーションの更新日時。 [putEditorAnnotation](#operation/putEditorAnnotation) API や [getEditorAnnotation](#operation/getEditorAnnotation) API のレスポンスに含まれる `updated_datetime` を指定します。

"""

PutInstructionRequest = dict[str, Any]
"""


Kyes of dict

* html: str
    作業ガイドのHTML
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutMarkersRequest = dict[str, Any]
"""


Kyes of dict

* markers: list[Marker]
    マーカー一覧
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutMyAccountRequest = dict[str, Any]
"""


Kyes of dict

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

PutMyNotificationMessageOpenedRequest = dict[str, Any]
"""


Kyes of dict

* opened: bool
    メッセージの開封状態に対するアクション。 trueが指定された場合は開封済みの状態、falseが指定された場合は未開封の状態にします。 

"""

PutOrganizationIdpBody = dict[str, Any]
"""
組織が利用するIDプロバイダー設定

Kyes of dict

* client_id: str
    外部IDプロバイダーで指定されたクライアントID
* client_secret: str
    外部IDプロバイダーで指定されたクライアントシークレット
* attributes_request_method: str
    ユーザー属性を取得する際に利用するリクエストメソッド 
* endpoints: OidcEndpoints
    
* attribute_mapping: OidcAttributeMapping
    

"""

PutOrganizationMemberRoleRequest = dict[str, Any]
"""


Kyes of dict

* role: OrganizationMemberRole
    
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutOrganizationPluginRequest = dict[str, Any]
"""


Kyes of dict

* plugin_name: str
    プラグインの名前です。 プラグイン一覧や、プロジェクトで使うプラグインを選ぶときなどに表示されます。 
* description: str
    プラグインの説明です。 プラグイン一覧や、プロジェクトで使うプラグインを選ぶときなどに表示されます。 
* project_extra_data_kinds: list[str]
    プラグインが適用されたプロジェクトで使用可能となるProjectExtraDataKindのId列。 
* detail: PluginDetail
    
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutOrganizationRequest = dict[str, Any]
"""


Kyes of dict

* organization_name: str
    組織名。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 

"""

PutProjectExtraDataBody = dict[str, Any]
"""
プロジェクトの追加データの更新時のリクエストボディ

Kyes of dict

* value: __DictStrKeyAnyValue__
    プロジェクト追加データの値。 nullを除く任意のJson
* last_updated_datetime: str
    データの最終更新時刻。新規作成時は未指定、更新時は必須（更新前の日時）

"""

PutProjectRequest = dict[str, Any]
"""


Kyes of dict

* title: str
    プロジェクトのタイトル
* overview: str
    プロジェクトの概要
* status: ProjectStatus
    
* input_data_type: InputDataType
    
* organization_name: str
    プロジェクトの所属組織を変更する場合は、ここに変更先の組織名を指定します。  * 所属組織を変更する前にプロジェクトを停止する必要があります。 * APIを呼び出すアカウントは、変更先組織の管理者またはオーナーである必要があります。 * 変更後の組織に所属していないプロジェクトメンバーも残りますが、作業はできません。あらためて組織に招待してください。 
* configuration: ProjectConfigurationPut
    
* last_updated_datetime: str
    新規作成時は未指定、更新時は必須（更新前の日時） 
* force_suspend: bool
    作業中タスクがあるプロジェクトを停止する時trueにして下さい

"""

PutProjectResponse = dict[str, Any]
"""


Kyes of dict

* job: ProjectJobInfo
    
* project: Project
    

"""

PutWebhookRequest = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* event_type: WebhookEventType
    
* webhook_id: str
    WebhookID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* webhook_status: WebhookStatus
    
* method: WebhookHttpMethod
    
* headers: list[WebhookHeader]
    Webhookが送信するHTTPリクエストのヘッダー
* body: str
    Webhookが送信するHTTPリクエストのボディ。methodがGETの場合は指定不可。
* url: str
    Webhookの送信先URL
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

RefreshTokenRequest = dict[str, Any]
"""


Kyes of dict

* refresh_token: str
    リフレッシュトークン。[login](#operation/login) APIで取得します。 

"""

ReplyComment = dict[str, Any]
"""


Kyes of dict

* root_comment_id: str
    コメントのID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* type: str
    `Reply` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

ReplyRequired = dict[str, Any]
"""
返信が必要な検査コメントが残っている時のエラー

Kyes of dict

* inspection: Inspection
    
* type: str
    ReplyRequired

"""

ResetEmailRequest = dict[str, Any]
"""


Kyes of dict

* email: str
    

"""

Resolution = dict[str, Any]
"""


Kyes of dict

* width: int
    画像の幅[ピクセル]
* height: int
    画像の高さ[ピクセル]

"""

RevokePersonalAccessTokenRequest = dict[str, Any]
"""


Kyes of dict

* id: str
    失効させる対象トークンのID

"""

RevokeProjectTokenRequest = dict[str, Any]
"""


Kyes of dict

* project_id: str
    無効化するトークンが所属しているプロジェクトのID
* project_token: str
    [issueProjectToken](#operation/issueProjectToken)で発行されたトークン文字列

"""

RootComment = dict[str, Any]
"""


Kyes of dict

* data: InspectionData
    
* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* status: CommentStatus
    
* type: str
    `Root` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

SegmentationMetadata = dict[str, Any]
"""
塗りつぶしアノテーションのメタデータ

Kyes of dict

* min_width: int
    幅の最小値[ピクセル]
* min_height: int
    高さの最小値[ピクセル]
* min_warn_rule: str
    サイズの制約に関する情報 * `none` - 制約なし * `or` - 幅と高さの両方が最小値以上 * `and` - 幅と高さのどちらか一方が最小値以上 
* tolerance: int
    許容誤差[ピクセル]

"""

SignUpRequest = dict[str, Any]
"""


Kyes of dict

* email: str
    

"""

SimpleAnnotation = dict[str, Any]
"""


Kyes of dict

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
* details: list[SimpleAnnotationDetail]
    矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。
* updated_datetime: str
    更新日時。アノテーションが一つもない場合（教師付作業が未着手のときなど）は、未指定。

"""

SimpleAnnotationDetail = dict[str, Any]
"""


Kyes of dict

* label: str
    アノテーション仕様で設定したラベル名 (英語) です。 
* annotation_id: str
    個々のアノテーションにつけられたIDです。 
* data: FullAnnotationData
    
* attributes: __DictStrKeyAnyValue__
    キーと値が以下のようになっている辞書構造です。  * キー: アノテーション仕様で設定した属性名 (英語) * 値: 各属性の値   * 選択肢を定義している場合、その選択肢の表示名 (英語)   * それ以外は属性値そのまま (文字列、数値、論理値) 

"""

SingleAnnotation = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* detail: SingleAnnotationDetailV2
    
* updated_datetime: str
    更新日時

"""

SingleAnnotationDetailV1 = dict[str, Any]
"""
アノテーション情報 

Kyes of dict

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
* additional_data_list: list[AdditionalDataV1]
    属性情報。  アノテーション属性の種類（`additional_data_definition`の`type`）によって、属性値を格納するプロパティは変わります。  | 属性の種類 | `additional_data_definition`の`type` | 属性値を格納するプロパティ                    | |------------|-------------------------|----------------------| | ON/OFF | flag       | flag                                          | | 整数 | integer    | integer                                       | | 自由記述（1行）| text       | comment                                       | | 自由記述（複数行）| comment    | comment                                       | | トラッキングID  | tracking | comment                                       | | アノテーションリンク    | link   | comment                                       | | 排他選択（ラジオボタン）  |choice   | choice                                        | | 排他選択（ドロップダウン） | select    | choice                                        | 
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

SingleAnnotationDetailV2 = dict[str, Any]
"""
アノテーション情報 

Kyes of dict

* annotation_id: str
    アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* label_id: str
    ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* body: AnnotationDetailContentOutput
    
* additional_data_list: list[AdditionalDataV2]
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時

"""

SingleAnnotationV1 = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* detail: SingleAnnotationDetailV1
    
* updated_datetime: str
    更新日時

"""

SingleAnnotationV2 = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* detail: SingleAnnotationDetailV2
    
* updated_datetime: str
    更新日時

"""

SupplementaryData = dict[str, Any]
"""


Kyes of dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_set_id: str
    入力データセットID(システム内部用のプロパティ)。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* supplementary_data_id: str
    補助情報ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* supplementary_data_name: str
    補助情報の名前
* supplementary_data_path: str
    補助情報の実体が存在するURLです。 URLスキームが s3 もしくは https であるもののみをサポートしています。 
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

SupplementaryDataRequest = dict[str, Any]
"""


Kyes of dict

* supplementary_data_name: str
    補助情報の名前
* supplementary_data_path: str
    補助情報の実体が存在するURLです。 補助情報の実体をAnnofabにアップロードする場合は、[createTempPath](#operation/createTempPath) APIで取得した`path`を指定してください。  補助情報の実体が[プライベートストレージ](/docs/faq/#prst9c)に存在する場合は、スキームが s3 または https であるURLを指定してください。 補助情報の実体が、S3プライベートストレージに存在するファイルを補助情報として登録する場合は、[事前に認可の設定](/docs/faq/#m0b240)が必要です。 
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


SystemMetadata = dict[str, Any]
"""
Annofabが設定したメタデータです。 `metadata`プロパティとは違い、ユーザー側では値を編集できません。  * `SystemMetadataImage`: 画像プロジェクト用のメタデータ * `SystemMetadataMovie`: 動画プロジェクト用のメタデータ * `SystemMetadataCustom`: カスタムプロジェクト用のメタデータ 

Kyes of dict

* original_resolution: Resolution
    
* resized_resolution: Resolution
    
* type: str
    `Custom`
* input_duration: float
    動画の長さ[秒]。 動画の長さが取得できなかった場合は、設定されません。 

"""

SystemMetadataCustom = dict[str, Any]
"""
カスタムデータ用システムメタデータ。 現行はプロパティがない形式的なオブジェクトです。 

Kyes of dict

* type: str
    `Custom`

"""

SystemMetadataImage = dict[str, Any]
"""
画像データ用システムメタデータ。 

Kyes of dict

* original_resolution: Resolution
    
* resized_resolution: Resolution
    
* type: str
    `Image`

"""

SystemMetadataMovie = dict[str, Any]
"""
動画データ用システムメタデータ。 

Kyes of dict

* input_duration: float
    動画の長さ[秒]。 動画の長さが取得できなかった場合は、設定されません。 
* type: str
    `Movie`

"""

Task = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* phase: TaskPhase
    
* phase_stage: int
    タスクのフェーズのステージ番号
* status: TaskStatus
    
* input_data_id_list: list[str]
    タスクに含まれる入力データのID
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* histories_by_phase: list[TaskHistoryShort]
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

TaskAssignRequest = dict[str, Any]
"""


Kyes of dict

* request_type: TaskAssignRequestType
    

"""

TaskAssignRequestType = dict[str, Any]
"""
* `TaskAssignRequestTypeRandom`: 自分自身にランダムにタスクを割り当てます。プロジェクト設定でタスクのランダム割当を有効にした場合のみ利用できます。 * `TaskAssignRequestTypeSelection`: メンバーに指定したタスクを割り当てます。ただし、メンバーはプロジェクトオーナーもしくはチェッカーロールを持つ必要があります。プロジェクト設定でタスクの選択割当を有効にした場合のみ利用できます。 * `TaskAssignRequestTypeTaskProperty`: タスクプロパティ割当の設定に基づいて、タスクを自分自身に割り当てます。プロジェクト設定でタスクプロパティ割当を有効にした場合のみ利用できます。 

Kyes of dict

* phase: TaskPhase
    
* type: str
    `TaskProperty` 
* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_ids: list[str]
    割り当てるタスクのID

"""

TaskAssignRequestTypeRandom = dict[str, Any]
"""


Kyes of dict

* phase: TaskPhase
    
* type: str
    `Random` 

"""

TaskAssignRequestTypeSelection = dict[str, Any]
"""


Kyes of dict

* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_ids: list[str]
    割り当てるタスクのID
* type: str
    `Selection` 

"""

TaskAssignRequestTypeTaskProperty = dict[str, Any]
"""


Kyes of dict

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


TaskAssignmentProperty = dict[str, Any]
"""
プロジェクト設定でタスクプロパティ割当を有効にしている場合のみ指定してください。 

Kyes of dict

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


TaskGenerateRequest = dict[str, Any]
"""


Kyes of dict

* task_generate_rule: TaskGenerateRule
    
* project_last_updated_datetime: str
    プロジェクトの最終更新日時（[getProject](#operation/getProject) APIのレスポンス `updated_datetime`）。タスク生成の排他制御に使用。

"""

TaskGenerateResponse = dict[str, Any]
"""


Kyes of dict

* job: ProjectJobInfo
    
* project: Project
    

"""

TaskGenerateResponseWrapper = dict[str, Any]
"""


Kyes of dict

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
    
* configuration: ProjectConfigurationGet
    
* created_datetime: str
    作成日時
* updated_datetime: str
    更新日時
* summary: ProjectSummary
    
* job: ProjectJobInfo
    
* project: Project
    

"""

TaskGenerateRule = dict[str, Any]
"""
タスク生成のルール * `TaskGenerateRuleByCount`: 1つのタスクに割り当てる入力データの個数を指定してタスクを生成します。 * `TaskGenerateRuleByDirectory`: 入力データ名をファイルパスに見立てて、ディレクトリ単位でタスクを生成します。 * `TaskGenerateRuleByInputDataCsv`: 各タスクへの入力データへの割り当てを記入したCSVをアップロードした、一時データ保存先パスを指定してタスクを生成します。 

Kyes of dict

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

TaskGenerateRuleByCount = dict[str, Any]
"""
1つのタスクに割り当てる入力データの個数を指定してタスクを生成します。

Kyes of dict

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

TaskGenerateRuleByDirectory = dict[str, Any]
"""
入力データ名をファイルパスに見立て、ディレクトリ単位でタスクを生成します。

Kyes of dict

* task_id_prefix: str
    タスクIDのプレフィックス。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* input_data_name_prefix: str
    タスク生成対象の入力データ名のプレフィックス
* type: str
    `ByDirectory` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

TaskGenerateRuleByInputDataCsv = dict[str, Any]
"""
各タスクへの入力データへの割当を記入したCSVへのS3上のパスを指定してタスクを生成します。 1つのタスクに対する入力データの個数は最大200です。200を超えるタスクが1つでもある場合にはタスク生成に失敗します。 

Kyes of dict

* csv_data_path: str
    各タスクへの入力データへの割り当てを記入したCSVへのS3上のパス。 
* type: str
    `ByInputDataCsv` [詳しくはこちら](#section/API-Convention/API-_type) 

"""

TaskHistory = dict[str, Any]
"""
タスクのあるフェーズで、誰がいつどれくらいの作業時間を費やしたかを表すタスク履歴です。

Kyes of dict

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

TaskHistoryEvent = dict[str, Any]
"""
タスク履歴イベントは、タスクの状態が変化した１時点を表します。作業時間は、複数のこれらイベントを集約して計算するものなので、このオブジェクトには含まれません。

Kyes of dict

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

TaskHistoryShort = dict[str, Any]
"""
タスクのあるフェーズを誰が担当したかを表します。

Kyes of dict

* phase: TaskPhase
    
* phase_stage: int
    
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* worked: bool
    そのフェーズでタスクの作業を行ったかどうか（行った場合はtrue）

"""

TaskInputValidation = dict[str, Any]
"""
タスクの提出操作に対する入力データID別のバリデーション結果です。

Kyes of dict

* input_data_id: str
    入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* annotation_errors: list[ValidationError]
    
* inspection_errors: list[InspectionValidationError]
    

"""

TaskList = dict[str, Any]
"""


Kyes of dict

* list: list[Task]
    現在のページ番号に含まれる0件以上のタスクです。
* page_no: float
    現在のページ番号です。
* total_page_no: float
    指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるタスク0件であっても、総ページ数は1となります。
* total_count: float
    検索結果の総件数。
* over_limit: bool
    検索結果が1万件を超えた場合にtrueとなる。
* aggregations: list[AggregationResult]
    [Aggregationによる集約結果](#section/API-Convention/AggregationResult)。 

"""

TaskOperation = dict[str, Any]
"""


Kyes of dict

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


TaskPhaseStatistics = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* date: str
    日付
* phases: list[PhaseStatistics]
    タスクのフェーズごとの集計結果

"""

TaskRequest = dict[str, Any]
"""


Kyes of dict

* input_data_id_list: list[str]
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


TaskValidation = dict[str, Any]
"""
タスクの全入力データに対するバリデーション結果です。

Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* task_id: str
    タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* inputs: list[InputDataSummary]
    

"""

TemporaryUrl = dict[str, Any]
"""
認証済み一時URL

Kyes of dict

* url: str
    このURLは発行から1時間経過すると無効になります。 

"""

Token = dict[str, Any]
"""
トークン情報

Kyes of dict

* id_token: str
    IDトークン。HTTPリクエストの`Authorization`ヘッダーにIDトークンを指定することで、APIは認証されます。
* access_token: str
    アクセストークン
* refresh_token: str
    リフレッシュトークン

"""

UnconfirmedUserResponse = dict[str, Any]
"""


Kyes of dict

* temporary_token: Token
    

"""

UnknownAdditionalData = dict[str, Any]
"""
何らかの原因で、アノテーション仕様にない属性がついているエラー

Kyes of dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    UnknownAdditionalData

"""

UnknownLabel = dict[str, Any]
"""
何らかの原因で、アノテーション仕様にないラベルがついているエラー

Kyes of dict

* label_id: str
    
* annotation_id: str
    
* type: str
    UnknownLabel

"""

UnknownLinkTarget = dict[str, Any]
"""
指定されたIDに該当するアノテーションが存在しないエラー

Kyes of dict

* label_id: str
    
* annotation_id: str
    
* additional_data_definition_id: str
    
* type: str
    UnknownLinkTarget

"""

UsageStatus = dict[str, Any]
"""
利用状況

Kyes of dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* year_month: str
    対象月。年月のフォーマットは YYYY-MM です。
* aggregation_period_from: str
    集計期間の開始日時。日時のフォーマットはISO 8601 拡張形式です。
* aggregation_period_to: str
    集計期間の終了日時。日時のフォーマットはISO 8601 拡張形式です。
* editor_usage: list[EditorUsageTimespan]
    エディタ利用時間のリスト
* storage_usage: float
    ストレージ利用量。単位はGB時

"""

UsageStatusByDay = dict[str, Any]
"""
日ごとの利用状況

Kyes of dict

* organization_id: str
    組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* date: str
    対象日。日付のフォーマットはISO 8601 拡張形式です。
* aggregation_period_from: str
    集計期間の開始日時。日時のフォーマットはISO 8601 拡張形式です。
* aggregation_period_to: str
    集計期間の終了日時。日時のフォーマットはISO 8601 拡張形式です。
* editor_usage: list[EditorUsageTimespan]
    エディタ利用時間のリスト
* storage_usage: float
    ストレージ利用量。単位はGB時

"""

UsageStatusCsvFileUrl = dict[str, Any]
"""
利用状況詳細のCSVファイルのURL

Kyes of dict

* url: str
    CSVファイルのURL

"""

UserCacheRecord = dict[str, Any]
"""


Kyes of dict

* account: str
    
* members: str
    
* projects: str
    
* organizations: str
    

"""

UserDefinedAnnotationDataType = dict[str, Any]
"""


Kyes of dict

* type: str
    ユーザー定義アノテーション種別の型を指定します。 指定可能な値と、その意味は下記の通りです。  * `BoundingBox2d` - 2次元の矩形 * `Polygon2d` - 2次元のポリゴン * `Polyline2d` - 2次元のポリライン * `SinglePoint2d` - 2次元の点 * `SemanticSegmentation2d` - 2次元のセマンティックセグメンテーション * `InstanceSegmentation2d` - 2次元のインスタンスセグメンテーション * `Range1d` - 1次元の範囲 * `Classification` - 全体アノテーション * `Unknown` - その他のアノテーション種別  下記のフィールド定義は、すべてのアノテーション種別の型に対して使用可能です。 * `OneIntegerField` * `OneStringField` * `OneBooleanField`  その他のフィールド定義は、使用可能なアノテーション種別の型に制限があります。 ユーザー定義アノテーション種別の型ごとの、使用可能なフィールド定義を下記の表で示します。  |ユーザー定義アノテーション種別の型 | 使用可能なフィールド定義 | |-----------------|:----------:| | BoundingBox2d          | MinimumSize2dWithDefaultInsertPosition, VertexCountMinMax, MinimumArea2d, MarginOfErrorTolerance | | Polygon2d              | MinimumSize2d, VertexCountMinMax, MinimumArea2d, MarginOfErrorTolerance | | Polyline2d             | VertexCountMinMax, DisplayLineDirection, MarginOfErrorTolerance | | SinglePoint2d          | MarginOfErrorTolerance | | SemanticSegmentation2d | AnnotationEditorFeature, MarginOfErrorTolerance | | InstanceSegmentation2d | AnnotationEditorFeature, MarginOfErrorTolerance | | Range1d                | MarginOfErrorTolerance | | Classification         | MarginOfErrorTolerance | | Unknown | - | 

"""

UserDefinedAnnotationTypeDefinition = dict[str, Any]
"""


Kyes of dict

* annotation_type_name: InternationalizationMessage
    
* field_definitions: list[UserDefinedAnnotationTypeDefinitionFieldDefinitions]
    ユーザーが定義するアノテーション種別のフィールド定義です。 フィールドIDをキー、フィールド定義を値とするオブジェクトを設定します。 
* metadata: dict(str, str)
    アノテーション種別を設定した際に、ラベルのメタデータとしてデフォルトで設定される値です。 
* annotation_data_type: UserDefinedAnnotationDataType
    

"""

UserDefinedAnnotationTypeDefinitionFieldDefinitions = dict[str, Any]
"""


Kyes of dict

* field_id: str
    フィールドID。任意の文字列を設定できます。
* definition: UserDefinedAnnotationTypeFieldDefinition
    

"""

UserDefinedAnnotationTypeFieldDefinition = dict[str, Any]
"""
ユーザー定義のアノテーション種別に設定可能なフィールドについての定義です。 

Kyes of dict

* type: str
    
* title: InternationalizationMessage
    
* prefix: str
    フィールドの前に付与する文字列。 
* postfix: str
    フィールドの後に付与する文字列 
* description: InternationalizationMessage
    
* initial_value: bool
    フィールドの初期値 
* label: InternationalizationMessage
    

"""

UserIdDeterminant = dict[str, Any]
"""
ユーザーIDを元に外部IDプロバイダーを特定する決定因子。 指定されたユーザが利用すべき外部IDプロバイダーが一つに定まる場合に、その一つを特定する。

Kyes of dict

* type: str
    
* user_id: str
    ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) 

"""

ValidationError = dict[str, Any]
"""


Kyes of dict

* label_id: str
    
* annotation_id: str
    
* message: str
    
* type: str
    UnknownLabel
* annotation_ids: list[str]
    
* additional_data_definition_id: str
    
* additional_data: AdditionalDataV1
    

"""

VerifyEmailRequest = dict[str, Any]
"""


Kyes of dict

* token: Token
    

"""

Webhook = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* event_type: WebhookEventType
    
* webhook_id: str
    WebhookID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* webhook_status: WebhookStatus
    
* method: WebhookHttpMethod
    
* headers: list[WebhookHeader]
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


WebhookHeader = dict[str, Any]
"""


Kyes of dict

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


WebhookTestRequest = dict[str, Any]
"""


Kyes of dict

* placeholders: dict(str, str)
    keyがプレースホルダーの名前、valueが置換後の値であるkey-valueペア

"""

WebhookTestResponse = dict[str, Any]
"""


Kyes of dict

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

WorktimeStatistics = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* date: str
    
* by_tasks: list[WorktimeStatisticsItem]
    タスクごとに計算した「画像1枚あたりの作業時間平均」の統計（動画プロジェクトの場合は空リスト）
* by_inputs: list[WorktimeStatisticsItem]
    画像1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）
* by_minutes: list[WorktimeStatisticsItem]
    動画1分当たりの作業時間情報（画像プロジェクトの場合は空リスト）
* accounts: list[AccountWorktimeStatistics]
    ユーザーごとの作業時間情報

"""

WorktimeStatisticsByAccount = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* account_id: str
    アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* data_series: list[WorktimeStatisticsData]
    プロジェクトメンバーの日毎の作業時間統計データ

"""

WorktimeStatisticsByProject = dict[str, Any]
"""


Kyes of dict

* project_id: str
    プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) 
* data_series: list[WorktimeStatisticsData]
    プロジェクトの日毎の作業時間統計データ

"""

WorktimeStatisticsData = dict[str, Any]
"""


Kyes of dict

* date: str
    日付
* grouped_by_input: list[WorktimeStatisticsItem]
    ユーザーごとの画像1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）
* grouped_by_task: list[WorktimeStatisticsItem]
    ユーザーごとのタスク1個当たりの作業時間情報（動画プロジェクトの場合は空リスト）
* grouped_by_minute: list[WorktimeStatisticsItem]
    ユーザーごとの動画1分当たりの作業時間情報（画像プロジェクトの場合は空リスト）

"""

WorktimeStatisticsItem = dict[str, Any]
"""


Kyes of dict

* phase: TaskPhase
    
* histogram: list[HistogramItem]
    ヒストグラム情報
* average: str
    作業時間の平均（ISO 8601 duration）
* standard_deviation: str
    作業時間の標準偏差（ISO 8601 duration）

"""


# `@deprecated_class`を指定した理由：
# InspectionStatusは非推奨のgetInspections APIとbatchUpdateComments APIからしか参照されていない。
# したがってInspectionStatusも非推奨にしている。
@deprecated_class(deprecated_date="2022-08-23")
class InspectionStatus(Enum):
    """
    ##### スレッドの先頭のコメントである（`parent_inspection_id` に値がない）場合  * `annotator_action_required` - 未処置。`annotation`フェーズ担当者が何らかの回答をする必要あり * `no_correction_required` - 処置不要。`annotation`フェーズ担当者が、検査コメントによる修正は不要、と回答した * `error_corrected` - 修正済み。`annotation`フェーズ担当者が、検査コメントの指示どおり修正した  ##### 返信コメントである（`parent_inspection_id` に値がある）場合  現在は使用しておらず、レスポンスに含まれる値は不定です。APIのレスポンスにこの値を含む場合でも、「スレッドの先頭のコメント」の値を利用してください。  リクエストボディに指定する場合は、スレッドの先頭のコメントと同じ値を指定します。
    """

    ANNOTATOR_ACTION_REQUIRED = "annotator_action_required"
    NO_CORRECTION_REQUIRED = "no_correction_required"
    ERROR_CORRECTED = "error_corrected"
