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
from typing_extensions import Annotated, Self

from annofabapi.pydantic_models.annotation_type_field_min_warn_rule import AnnotationTypeFieldMinWarnRule


class AnnotationTypeFieldValueMinimumSize(BaseModel):
    """
    アノテーションの最小サイズに関する設定
    """

    type: StrictStr = Field(alias="_type")
    min_warn_rule: AnnotationTypeFieldMinWarnRule
    min_width: Annotated[int, Field(strict=True, ge=1)]
    min_height: Annotated[int, Field(strict=True, ge=1)]
    __properties: ClassVar[List[str]] = ["_type", "min_warn_rule", "min_width", "min_height"]

    @field_validator("type")
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(["MinimumSize2d"]):
            raise ValueError("must be one of enum values ('MinimumSize2d')")
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
        """Create an instance of AnnotationTypeFieldValueMinimumSize from a JSON string"""
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
        """Create an instance of AnnotationTypeFieldValueMinimumSize from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "_type": obj.get("_type"),
                "min_warn_rule": obj.get("min_warn_rule"),
                "min_width": obj.get("min_width"),
                "min_height": obj.get("min_height"),
            }
        )
        return _obj
