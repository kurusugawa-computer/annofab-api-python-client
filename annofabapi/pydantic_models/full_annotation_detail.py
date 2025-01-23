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

from annofabapi.pydantic_models.annotation_data_holding_type import AnnotationDataHoldingType
from annofabapi.pydantic_models.annotation_type import AnnotationType
from annofabapi.pydantic_models.full_annotation_additional_data import FullAnnotationAdditionalData
from annofabapi.pydantic_models.full_annotation_data import FullAnnotationData
from annofabapi.pydantic_models.internationalization_message import InternationalizationMessage


class FullAnnotationDetail(BaseModel):
    """
    FullAnnotationDetail
    """

    annotation_id: StrictStr = Field(
        description="アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 "
    )
    user_id: StrictStr = Field(description="ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    label_id: StrictStr = Field(description="ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    label_name: InternationalizationMessage
    annotation_type: AnnotationType
    data_holding_type: AnnotationDataHoldingType
    data: FullAnnotationData
    additional_data_list: List[FullAnnotationAdditionalData] = Field(description="属性情報。 ")
    __properties: ClassVar[List[str]] = [
        "annotation_id",
        "user_id",
        "label_id",
        "label_name",
        "annotation_type",
        "data_holding_type",
        "data",
        "additional_data_list",
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
        """Create an instance of FullAnnotationDetail from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of label_name
        if self.label_name:
            _dict["label_name"] = self.label_name.to_dict()
        # override the default output from pydantic by calling `to_dict()` of annotation_type
        if self.annotation_type:
            _dict["annotation_type"] = self.annotation_type.to_dict()
        # override the default output from pydantic by calling `to_dict()` of data
        if self.data:
            _dict["data"] = self.data.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in additional_data_list (list)
        _items = []
        if self.additional_data_list:
            for _item_additional_data_list in self.additional_data_list:
                if _item_additional_data_list:
                    _items.append(_item_additional_data_list.to_dict())
            _dict["additional_data_list"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of FullAnnotationDetail from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "annotation_id": obj.get("annotation_id"),
                "user_id": obj.get("user_id"),
                "label_id": obj.get("label_id"),
                "label_name": InternationalizationMessage.from_dict(obj["label_name"]) if obj.get("label_name") is not None else None,
                "annotation_type": AnnotationType.from_dict(obj["annotation_type"]) if obj.get("annotation_type") is not None else None,
                "data_holding_type": obj.get("data_holding_type"),
                "data": FullAnnotationData.from_dict(obj["data"]) if obj.get("data") is not None else None,
                "additional_data_list": [FullAnnotationAdditionalData.from_dict(_item) for _item in obj["additional_data_list"]]
                if obj.get("additional_data_list") is not None
                else None,
            }
        )
        return _obj
