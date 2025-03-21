"""


No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

The version of the OpenAPI document: 1.0.0
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""

from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing_extensions import Self

from annofabapi.pydantic_models.project_extra_data_value import ProjectExtraDataValue


class ProjectExtraData(BaseModel):
    """
    プロジェクトの追加データ。 追加のプロジェクトの設定や、プロジェクトに対するユーザ毎のデータを表す。 (project_id, account_id, kind_id)の組み合わせで一意になり、account_idが指定指定されていない場合はユーザに割りつかず、プロジェクト自体に割りついている値を表す。
    """

    project_id: StrictStr = Field(description="プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    account_id: Optional[StrictStr] = Field(default=None, description="アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    kind_id: StrictStr = Field(description="プロジェクト追加データの種別ID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    value: ProjectExtraDataValue
    __properties: ClassVar[List[str]] = ["project_id", "account_id", "kind_id", "value"]

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
        """Create an instance of ProjectExtraData from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of value
        if self.value:
            _dict["value"] = self.value.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProjectExtraData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "project_id": obj.get("project_id"),
                "account_id": obj.get("account_id"),
                "kind_id": obj.get("kind_id"),
                "value": ProjectExtraDataValue.from_dict(obj["value"]) if obj.get("value") is not None else None,
            }
        )
        return _obj
