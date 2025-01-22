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
from typing import Annotated, Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing_extensions import Self

from annofabapi.pydantic_models.key_layout import KeyLayout
from annofabapi.pydantic_models.lang import Lang


class PutMyAccountRequest(BaseModel):
    """
    PutMyAccountRequest
    """

    user_id: StrictStr = Field(description="ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    username: StrictStr = Field(description="ユーザー名")
    lang: Lang
    keylayout: KeyLayout
    biography: Optional[Annotated[str, Field(min_length=0, strict=True, max_length=100)]] = Field(
        default=None,
        description="人物紹介、略歴。  この属性は、Annofab外の所属先や肩書などを表すために用います。 Annofab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 ",
    )
    last_updated_datetime: Optional[str] = Field(default=None, description="新規作成時は未指定、更新時は必須（更新前の日時） ")
    __properties: ClassVar[List[str]] = ["user_id", "username", "lang", "keylayout", "biography", "last_updated_datetime"]

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
        """Create an instance of PutMyAccountRequest from a JSON string"""
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
        """Create an instance of PutMyAccountRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "user_id": obj.get("user_id"),
                "username": obj.get("username"),
                "lang": obj.get("lang"),
                "keylayout": obj.get("keylayout"),
                "biography": obj.get("biography"),
                "last_updated_datetime": obj.get("last_updated_datetime"),
            }
        )
        return _obj
