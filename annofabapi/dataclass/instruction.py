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


@dataclass_json
@dataclass
class Instruction:
    """
    
    """

    html: Optional[str]
    """作業ガイドのHTML"""

    last_updated_datetime: Optional[str]
    """* [getInstruction](#operation/getInstruction) APIのレスポンスの場合: 最後に作業ガイドを更新した日時。 * [putInstruction](#operation/putInstruction) APIのリクエストボディの場合: 最後に作業ガイドを更新した日時を指定する。まだ一度も保存した事がない場合は指定しない。 """


@dataclass_json
@dataclass
class InstructionHistory:
    """
    
    """

    history_id: str
    """作業ガイドの履歴ID"""

    account_id: str
    """作業ガイドを更新したユーザのアカウントID"""

    updated_datetime: str
    """作業ガイドの最終更新日時"""


@dataclass_json
@dataclass
class InstructionImage:
    """
    
    """

    image_id: str
    """作業ガイド画像ID"""

    path: str
    """作業ガイド画像の実体が保存されたパスです。 """

    url: str
    """作業ガイド画像を取得するための内部用URLです。"""

    etag: str
    """"""
