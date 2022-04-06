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

from annofabapi.models import WebhookEventType, WebhookHttpMethod, WebhookStatus


@dataclass
class WebhookHeader(DataClassJsonMixin):
    """ """

    name: str
    """HTTPヘッダーのフィールド名"""

    value: str
    """HTTPヘッダーの値"""


@dataclass
class Webhook(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    event_type: WebhookEventType
    """"""

    webhook_id: str
    """WebhookID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    webhook_status: WebhookStatus
    """"""

    method: WebhookHttpMethod
    """"""

    headers: List[WebhookHeader]
    """Webhookが送信するHTTPリクエストのヘッダー"""

    body: Optional[str]
    """Webhookが送信するHTTPリクエストのボディ"""

    url: str
    """Webhookの送信先URL"""

    created_datetime: str
    """作成日時"""

    updated_datetime: str
    """更新日時"""
