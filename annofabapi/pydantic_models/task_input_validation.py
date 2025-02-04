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

from annofabapi.pydantic_models.inspection_validation_error import InspectionValidationError
from annofabapi.pydantic_models.validation_error import ValidationError


class TaskInputValidation(BaseModel):
    """
    タスクの提出操作に対する入力データID別のバリデーション結果です。
    """

    input_data_id: Optional[StrictStr] = Field(default=None, description="入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    annotation_errors: Optional[List[ValidationError]] = None
    inspection_errors: Optional[List[InspectionValidationError]] = None
    __properties: ClassVar[List[str]] = ["input_data_id", "annotation_errors", "inspection_errors"]

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
        """Create an instance of TaskInputValidation from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in annotation_errors (list)
        _items = []
        if self.annotation_errors:
            for _item_annotation_errors in self.annotation_errors:
                if _item_annotation_errors:
                    _items.append(_item_annotation_errors.to_dict())
            _dict["annotation_errors"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in inspection_errors (list)
        _items = []
        if self.inspection_errors:
            for _item_inspection_errors in self.inspection_errors:
                if _item_inspection_errors:
                    _items.append(_item_inspection_errors.to_dict())
            _dict["inspection_errors"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TaskInputValidation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "input_data_id": obj.get("input_data_id"),
                "annotation_errors": [ValidationError.from_dict(_item) for _item in obj["annotation_errors"]]
                if obj.get("annotation_errors") is not None
                else None,
                "inspection_errors": [InspectionValidationError.from_dict(_item) for _item in obj["inspection_errors"]]
                if obj.get("inspection_errors") is not None
                else None,
            }
        )
        return _obj
