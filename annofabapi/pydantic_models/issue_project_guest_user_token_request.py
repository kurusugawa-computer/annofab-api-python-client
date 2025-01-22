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
from typing import Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing_extensions import Self

from annofabapi.pydantic_models.project_guest_user_profile import ProjectGuestUserProfile


class IssueProjectGuestUserTokenRequest(BaseModel):
    """
    IssueProjectGuestUserTokenRequest
    """

    project_id: StrictStr = Field(description="ゲストユーザーがアクセスするプロジェクトのID")
    app_token: StrictStr = Field(description="ゲストユーザートークンを要求するアプリケーションに提供されているトークン")
    project_token: StrictStr = Field(description="[issueProjectToken](#operation/issueProjectToken)で発行されたトークン文字列")
    role: StrictStr = Field(description="ゲストユーザーのプロジェクト上でのロール * `worker` - アノテーター * `accepter` - チェッカー ")
    profile: ProjectGuestUserProfile
    __properties: ClassVar[List[str]] = ["project_id", "app_token", "project_token", "role", "profile"]

    @field_validator("role")
    def role_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(["worker", "accepter"]):
            raise ValueError("must be one of enum values ('worker', 'accepter')")
        return value

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
        """Create an instance of IssueProjectGuestUserTokenRequest from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of profile
        if self.profile:
            _dict["profile"] = self.profile.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of IssueProjectGuestUserTokenRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "project_id": obj.get("project_id"),
                "app_token": obj.get("app_token"),
                "project_token": obj.get("project_token"),
                "role": obj.get("role"),
                "profile": ProjectGuestUserProfile.from_dict(obj["profile"]) if obj.get("profile") is not None else None,
            }
        )
        return _obj
