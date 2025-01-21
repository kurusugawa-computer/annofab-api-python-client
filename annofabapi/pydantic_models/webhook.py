"""
swagger-api-components.yaml に記載されたschemaを出力するためのヘッダ部分

No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

The version of the OpenAPI document: 1.0.0
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""

from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing_extensions import Self

from annofabapi.pydantic_models.webhook_event_type import WebhookEventType
from annofabapi.pydantic_models.webhook_header import WebhookHeader
from annofabapi.pydantic_models.webhook_http_method import WebhookHttpMethod
from annofabapi.pydantic_models.webhook_status import WebhookStatus


class Webhook(BaseModel):
    """
    Webhook
    """

    project_id: StrictStr = Field(description="プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    event_type: WebhookEventType
    webhook_id: StrictStr = Field(description="WebhookID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    webhook_status: WebhookStatus
    method: WebhookHttpMethod
    headers: List[WebhookHeader] = Field(description="Webhookが送信するHTTPリクエストのヘッダー")
    body: Optional[StrictStr] = Field(default=None, description="Webhookが送信するHTTPリクエストのボディ")
    url: StrictStr = Field(description="Webhookの送信先URL")
    created_datetime: datetime = Field(description="作成日時")
    updated_datetime: datetime = Field(description="更新日時")
    __properties: ClassVar[List[str]] = [
        "project_id",
        "event_type",
        "webhook_id",
        "webhook_status",
        "method",
        "headers",
        "body",
        "url",
        "created_datetime",
        "updated_datetime",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Webhook from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in headers (list)
        _items = []
        if self.headers:
            for _item_headers in self.headers:
                if _item_headers:
                    _items.append(_item_headers.to_dict())
            _dict["headers"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Webhook from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "project_id": obj.get("project_id"),
                "event_type": obj.get("event_type"),
                "webhook_id": obj.get("webhook_id"),
                "webhook_status": obj.get("webhook_status"),
                "method": obj.get("method"),
                "headers": [WebhookHeader.from_dict(_item) for _item in obj["headers"]] if obj.get("headers") is not None else None,
                "body": obj.get("body"),
                "url": obj.get("url"),
                "created_datetime": obj.get("created_datetime"),
                "updated_datetime": obj.get("updated_datetime"),
            }
        )
        return _obj
