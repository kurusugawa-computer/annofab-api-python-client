# flake8: noqa: W291

"""
enum.pyのヘッダ部分
注意：このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照
"""

import warnings # pylint: disable=unused-import
from enum import Enum
class AccountAuthority(Enum):
    """
    """

    USER = "user"
    ADMIN = "admin"
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
class AnnotationDataHoldingType(Enum):
    """
    * `inner` - アノテーションのデータ部をJSON内部に保持します。 * `outer` - アノテーションのデータ部を外部ファイルの形式（画像など）で保持します   # noqa: E501
    """

    INNER = "inner"
    OUTER = "outer"
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
class InputDataOrder(Enum):
    """
    タスクに割り当てる入力データの順序  * `name_asc` - 入力データ名 昇順（a, b, c, ...）。日付や番号などの連続するデータ名を扱う場合に推奨 * `name_asc` - 入力データ名 降順（z, y, x, ...） * `random` - ランダム   # noqa: E501
    """

    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"
    RANDOM = "random"
class InputDataType(Enum):
    """
    プロジェクトの作成時のみ指定可能（未指定の場合は image）です。更新時は無視されます  # noqa: E501
    """

    IMAGE = "image"
    MOVIE = "movie"
class InspectionStatus(Enum):
    """
    * `annotator_action_required` - 未処置。`annotation`フェーズ担当者が何らかの回答をする必要あり * `no_correction_required` - 処置不要。`annotation`フェーズ担当者が、検査コメントによる修正は不要、と回答した * `error_corrected` - 修正済み。`annotation`フェーズ担当者が、検査コメントの指示どおり修正した * `no_comment_inspection` - 作成途中。検査コメントの中身が未入力   # noqa: E501
    """

    ANNOTATOR_ACTION_REQUIRED = "annotator_action_required"
    NO_CORRECTION_REQUIRED = "no_correction_required"
    ERROR_CORRECTED = "error_corrected"
    NO_COMMENT_INSPECTION = "no_comment_inspection"
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
class PricePlan(Enum):
    """
    """

    FREE = "free"
    BUSINESS = "business"
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
class ProjectWorkflow(Enum):
    """
    """

    _2PHASE = "2phase"
    _3PHASE = "3phase"
class TaskPhase(Enum):
    """
    * `annotation` - 教師付け。 * `inspection` - 中間検査。ワークフローが3フェーズのときのみ。 * `acceptance` - 受入。   # noqa: E501
    """

    ANNOTATION = "annotation"
    INSPECTION = "inspection"
    ACCEPTANCE = "acceptance"
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
