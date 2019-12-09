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
    """"""

    last_updated_datetime: Optional[str]
    """* `GetInstruction` の場合: 最後に作業ガイドを更新した日時。 * `PutInstruction` の場合: 最後に作業ガイドを更新した日時を指定する。まだ一度も保存した事がない場合は指定しない。 """


@dataclass_json
@dataclass
class InstructionHistory:
    """
    
    """
    history_id: Optional[str]
    """"""

    account_id: Optional[str]
    """"""

    updated_datetime: Optional[str]
    """"""


@dataclass_json
@dataclass
class InstructionImage:
    """
    
    """
    image_id: Optional[str]
    """"""

    path: Optional[str]
    """"""

    url: Optional[str]
    """"""

    etag: Optional[str]
    """"""
