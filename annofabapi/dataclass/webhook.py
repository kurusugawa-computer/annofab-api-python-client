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

from annofabapi.models import WebhookEventType, WebhookHttpMethod, WebhookStatus


@dataclass_json
@dataclass
class WebhookHeader:
    """
    
    """

    name: Optional[str]
    """"""

    value: Optional[str]
    """"""


@dataclass_json
@dataclass
class Webhook:
    """
    
    """

    project_id: Optional[str]
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    event_type: Optional[WebhookEventType]
    """"""

    webhook_id: Optional[str]
    """WebhookID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    webhook_status: Optional[WebhookStatus]
    """"""

    method: Optional[WebhookHttpMethod]
    """"""

    headers: Optional[List[WebhookHeader]]
    """"""

    body: Optional[str]
    """"""

    url: Optional[str]
    """"""

    created_datetime: Optional[str]
    """"""

    updated_datetime: Optional[str]
    """"""
