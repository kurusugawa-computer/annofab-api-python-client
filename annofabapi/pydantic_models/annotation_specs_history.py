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


class AnnotationSpecsHistory(BaseModel):
    """
    AnnotationSpecsHistory
    """

    history_id: StrictStr = Field(description="アノテーション仕様の履歴ID")
    project_id: StrictStr = Field(description="プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    updated_datetime: datetime = Field(description="更新日時")
    url: StrictStr = Field(description="アノテーション仕様が格納されたJSONのURL。URLにアクセスするには認証認可が必要です。")
    account_id: Optional[StrictStr] = Field(default=None, description="アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    comment: Optional[StrictStr] = Field(default=None, description="変更内容のコメント")
    __properties: ClassVar[List[str]] = ["history_id", "project_id", "updated_datetime", "url", "account_id", "comment"]

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
        """Create an instance of AnnotationSpecsHistory from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AnnotationSpecsHistory from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "history_id": obj.get("history_id"),
                "project_id": obj.get("project_id"),
                "updated_datetime": obj.get("updated_datetime"),
                "url": obj.get("url"),
                "account_id": obj.get("account_id"),
                "comment": obj.get("comment"),
            }
        )
        return _obj
