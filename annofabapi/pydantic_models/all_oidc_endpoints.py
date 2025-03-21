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

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing_extensions import Self


class AllOidcEndpoints(BaseModel):
    """
    OIDCエンドポイント
    """

    type: StrictStr = Field(alias="_type")
    issuer: StrictStr = Field(description="RFC 8414で定義されるissuerの値。 `.well-known/openid-configuration`のissuer。")
    authorize_url: StrictStr = Field(description="RFC 8414（及びRFC6749）で定義される、authorization_endpointのURL")
    token_url: StrictStr = Field(description="RFC 8414（及びRFC6749）で定義される、token_endpointのURL")
    userinfo_url: StrictStr = Field(description="OpenID Connect Core 1.0で定義される、UserInfo EndpointのURL")
    jwks_url: StrictStr = Field(description="RFC 8414で定義される、jwks_uriの値")
    __properties: ClassVar[List[str]] = ["_type", "issuer", "authorize_url", "token_url", "userinfo_url", "jwks_url"]

    @field_validator("type")
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(["All"]):
            raise ValueError("must be one of enum values ('All')")
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
        """Create an instance of AllOidcEndpoints from a JSON string"""
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
        """Create an instance of AllOidcEndpoints from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "_type": obj.get("_type"),
                "issuer": obj.get("issuer"),
                "authorize_url": obj.get("authorize_url"),
                "token_url": obj.get("token_url"),
                "userinfo_url": obj.get("userinfo_url"),
                "jwks_url": obj.get("jwks_url"),
            }
        )
        return _obj
