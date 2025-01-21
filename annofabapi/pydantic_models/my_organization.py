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

from annofabapi.pydantic_models.organization_member_role import OrganizationMemberRole
from annofabapi.pydantic_models.organization_member_status import OrganizationMemberStatus
from annofabapi.pydantic_models.price_plan import PricePlan


class MyOrganization(BaseModel):
    """
    MyOrganization
    """

    organization_id: Optional[StrictStr] = Field(default=None, description="組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    name: Optional[StrictStr] = None
    email: Optional[StrictStr] = None
    price_plan: Optional[PricePlan] = None
    summary: Optional[Dict[str, Any]] = Field(default=None, description="廃止予定のプロパティです。常に中身は空です。 ")
    created_datetime: Optional[datetime] = Field(default=None, description="作成日時")
    updated_datetime: Optional[datetime] = Field(default=None, description="更新日時")
    my_role: Optional[OrganizationMemberRole] = None
    my_status: Optional[OrganizationMemberStatus] = None
    __properties: ClassVar[List[str]] = [
        "organization_id",
        "name",
        "email",
        "price_plan",
        "summary",
        "created_datetime",
        "updated_datetime",
        "my_role",
        "my_status",
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
        """Create an instance of MyOrganization from a JSON string"""
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
        """Create an instance of MyOrganization from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "organization_id": obj.get("organization_id"),
                "name": obj.get("name"),
                "email": obj.get("email"),
                "price_plan": obj.get("price_plan"),
                "summary": obj.get("summary"),
                "created_datetime": obj.get("created_datetime"),
                "updated_datetime": obj.get("updated_datetime"),
                "my_role": obj.get("my_role"),
                "my_status": obj.get("my_status"),
            }
        )
        return _obj
