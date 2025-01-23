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

from annofabapi.pydantic_models.additional_data_v2 import AdditionalDataV2
from annofabapi.pydantic_models.annotation_detail_content_input import AnnotationDetailContentInput
from annofabapi.pydantic_models.annotation_props_for_editor import AnnotationPropsForEditor


class AnnotationDetailV2Create(BaseModel):
    """
    新規にアノテーションを作成する場合にこの型を利用します。
    """

    type: StrictStr = Field(alias="_type")
    annotation_id: StrictStr = Field(
        description="アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 "
    )
    label_id: StrictStr = Field(description="ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    body: AnnotationDetailContentInput
    additional_data_list: List[AdditionalDataV2]
    editor_props: AnnotationPropsForEditor
    __properties: ClassVar[List[str]] = ["_type", "annotation_id", "label_id", "body", "additional_data_list", "editor_props"]

    @field_validator("type")
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(["Create"]):
            raise ValueError("must be one of enum values ('Create')")
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
        """Create an instance of AnnotationDetailV2Create from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of body
        if self.body:
            _dict["body"] = self.body.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in additional_data_list (list)
        _items = []
        if self.additional_data_list:
            for _item_additional_data_list in self.additional_data_list:
                if _item_additional_data_list:
                    _items.append(_item_additional_data_list.to_dict())
            _dict["additional_data_list"] = _items
        # override the default output from pydantic by calling `to_dict()` of editor_props
        if self.editor_props:
            _dict["editor_props"] = self.editor_props.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AnnotationDetailV2Create from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "_type": obj.get("_type"),
                "annotation_id": obj.get("annotation_id"),
                "label_id": obj.get("label_id"),
                "body": AnnotationDetailContentInput.from_dict(obj["body"]) if obj.get("body") is not None else None,
                "additional_data_list": [AdditionalDataV2.from_dict(_item) for _item in obj["additional_data_list"]]
                if obj.get("additional_data_list") is not None
                else None,
                "editor_props": AnnotationPropsForEditor.from_dict(obj["editor_props"]) if obj.get("editor_props") is not None else None,
            }
        )
        return _obj
