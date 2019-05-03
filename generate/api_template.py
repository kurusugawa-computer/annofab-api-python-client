"""
Annofab WebAPIに対応する関数
注意：このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照
"""

from annofabapi.mixin import AnnofabApiMixin
from typing import Dict, List, Any, Optional, Union, Tuple
import requests
import warnings
from annofabapi.mixin import AnnofabApiMixin


class AnnofabApi(AnnofabApiMixin):
    """
    Web APIに対応するメソッドを定義したクラス
    """

    def __init__(self, login_user_id: str, login_password: str):
        """
        Args:
            login_user_id: AnnoFabにログインするときのユーザID
            login_password: AnnoFabにログインするときのパスワード
        """
        super().__init__(login_user_id, login_password)
