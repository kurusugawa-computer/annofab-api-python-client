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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing_extensions import Self

from annofabapi.pydantic_models.internationalization_message import InternationalizationMessage
from annofabapi.pydantic_models.user_defined_annotation_data_type import UserDefinedAnnotationDataType
from annofabapi.pydantic_models.user_defined_annotation_type_definition_field_definitions_inner import (
    UserDefinedAnnotationTypeDefinitionFieldDefinitionsInner,
)


class UserDefinedAnnotationTypeDefinition(BaseModel):
    """
    UserDefinedAnnotationTypeDefinition
    """

    annotation_type_name: InternationalizationMessage
    field_definitions: List[UserDefinedAnnotationTypeDefinitionFieldDefinitionsInner] = Field(
        description="ユーザーが定義するアノテーション種別のフィールド定義です。 フィールドIDをキー、フィールド定義を値とするオブジェクトを設定します。 "
    )
    metadata: Dict[str, StrictStr] = Field(description="アノテーション種別を設定した際に、ラベルのメタデータとしてデフォルトで設定される値です。 ")
    annotation_data_type: UserDefinedAnnotationDataType
    __properties: ClassVar[List[str]] = ["annotation_type_name", "field_definitions", "metadata", "annotation_data_type"]

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
        """Create an instance of UserDefinedAnnotationTypeDefinition from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of annotation_type_name
        if self.annotation_type_name:
            _dict["annotation_type_name"] = self.annotation_type_name.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in field_definitions (list)
        _items = []
        if self.field_definitions:
            for _item_field_definitions in self.field_definitions:
                if _item_field_definitions:
                    _items.append(_item_field_definitions.to_dict())
            _dict["field_definitions"] = _items
        # override the default output from pydantic by calling `to_dict()` of annotation_data_type
        if self.annotation_data_type:
            _dict["annotation_data_type"] = self.annotation_data_type.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UserDefinedAnnotationTypeDefinition from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "annotation_type_name": InternationalizationMessage.from_dict(obj["annotation_type_name"])
                if obj.get("annotation_type_name") is not None
                else None,
                "field_definitions": [UserDefinedAnnotationTypeDefinitionFieldDefinitionsInner.from_dict(_item) for _item in obj["field_definitions"]]
                if obj.get("field_definitions") is not None
                else None,
                "metadata": obj.get("metadata"),
                "annotation_data_type": UserDefinedAnnotationDataType.from_dict(obj["annotation_data_type"])
                if obj.get("annotation_data_type") is not None
                else None,
            }
        )
        return _obj
