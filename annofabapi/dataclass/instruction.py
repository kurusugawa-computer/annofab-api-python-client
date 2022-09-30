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

warnings.warn("'annofabapi.dataclass.instruction'モジュールは2022-12-01以降に廃止する予定です。", FutureWarning, stacklevel=2)


@dataclass
class Instruction(DataClassJsonMixin):
    """ """

    html: str
    """作業ガイドのHTML"""

    last_updated_datetime: str
    """更新日時"""


@dataclass
class InstructionHistory(DataClassJsonMixin):
    """ """

    history_id: str
    """作業ガイドの履歴ID"""

    account_id: str
    """作業ガイドを更新したユーザーのアカウントID"""

    updated_datetime: str
    """作業ガイドの最終更新日時"""


@dataclass
class InstructionImage(DataClassJsonMixin):
    """ """

    image_id: str
    """作業ガイド画像ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    path: str
    """作業ガイド画像の実体が保存されたパスです。 """

    url: str
    """作業ガイド画像を取得するためのシステム内部用のURLです。"""

    etag: str
    """[HTTPレスポンスヘッダー ETag](https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/ETag)に相当する値です。 """
