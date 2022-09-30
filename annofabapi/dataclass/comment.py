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

from dataclasses_json import DataClassJsonMixin

from annofabapi.models import CommentType, TaskPhase

CommentNode = Dict[str, Any]


@dataclass
class Comment(DataClassJsonMixin):
    """
    コメント
    """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    comment_id: str
    """コメントのID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    phase: TaskPhase
    """"""

    phase_stage: int
    """コメントを作成したときのフェーズのステージ。"""

    account_id: str
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    comment_type: CommentType
    """"""

    phrases: Optional[List[str]]
    """`comment_type` の値によって扱いが異なります。  * `onhold` の場合   * 使用しません（空配列） * `inspection` の場合   * 参照している定型指摘のIDリスト """

    comment: str
    """コメント本文。 """

    comment_node: CommentNode
    """"""

    datetime_for_sorting: str
    """コメントのソート順を決める日時。  Annofab標準エディタでは、コメントはここで指定した日時にしたがってスレッドごとに昇順で表示されます。 """

    created_datetime: str
    """コメントの作成日時。"""

    updated_datetime: str
    """コメントの更新日時。"""
