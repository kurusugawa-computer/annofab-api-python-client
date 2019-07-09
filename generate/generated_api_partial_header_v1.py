# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace

"""
AbstractAnnofabApiのヘッダ部分
注意：このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照
"""

import abc
import annofabapi # pylint: disable=unused-import
import warnings # pylint: disable=unused-import
from typing import Any, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import
import requests


class AbstractAnnofabApi(abc.ABC):
    """
    AnnofabApiクラスの抽象クラス
    """

    @abc.abstractmethod
    def _request_wrapper(self,
                         http_method: str,
                         url_path: str,
                         query_params: Optional[Dict[str, Any]] = None,
                         header_params: Optional[Dict[str, Any]] = None,
                         request_body: Optional[Any] = None
                         ) -> Tuple[Any, requests.Response]:
        pass
