"""


No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

The version of the OpenAPI document: 1.0.0
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""

from __future__ import annotations

import json
import pprint
from typing import Any, Dict, Optional, Set, Union

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator
from typing_extensions import Self

from annofabapi.pydantic_models.annotation_type_field_definition_annotation_editor_feature import AnnotationTypeFieldDefinitionAnnotationEditorFeature
from annofabapi.pydantic_models.annotation_type_field_definition_display_line_direction import AnnotationTypeFieldDefinitionDisplayLineDirection
from annofabapi.pydantic_models.annotation_type_field_definition_margin_of_error_tolerance import AnnotationTypeFieldDefinitionMarginOfErrorTolerance
from annofabapi.pydantic_models.annotation_type_field_definition_minimum_area2d import AnnotationTypeFieldDefinitionMinimumArea2d
from annofabapi.pydantic_models.annotation_type_field_definition_minimum_size2d import AnnotationTypeFieldDefinitionMinimumSize2d
from annofabapi.pydantic_models.annotation_type_field_definition_minimum_size2d_with_default_insert_position import (
    AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition,
)
from annofabapi.pydantic_models.annotation_type_field_definition_one_boolean_field import AnnotationTypeFieldDefinitionOneBooleanField
from annofabapi.pydantic_models.annotation_type_field_definition_one_integer_field import AnnotationTypeFieldDefinitionOneIntegerField
from annofabapi.pydantic_models.annotation_type_field_definition_one_string_field import AnnotationTypeFieldDefinitionOneStringField
from annofabapi.pydantic_models.annotation_type_field_definition_vertex_count_min_max import AnnotationTypeFieldDefinitionVertexCountMinMax

USERDEFINEDANNOTATIONTYPEFIELDDEFINITION_ONE_OF_SCHEMAS = [
    "AnnotationTypeFieldDefinitionAnnotationEditorFeature",
    "AnnotationTypeFieldDefinitionDisplayLineDirection",
    "AnnotationTypeFieldDefinitionMarginOfErrorTolerance",
    "AnnotationTypeFieldDefinitionMinimumArea2d",
    "AnnotationTypeFieldDefinitionMinimumSize2d",
    "AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition",
    "AnnotationTypeFieldDefinitionOneBooleanField",
    "AnnotationTypeFieldDefinitionOneIntegerField",
    "AnnotationTypeFieldDefinitionOneStringField",
    "AnnotationTypeFieldDefinitionVertexCountMinMax",
]


class UserDefinedAnnotationTypeFieldDefinition(BaseModel):
    """
    ユーザー定義のアノテーション種別に設定可能なフィールドについての定義です。
    """

    # data type: AnnotationTypeFieldDefinitionMinimumSize2d
    oneof_schema_1_validator: Optional[AnnotationTypeFieldDefinitionMinimumSize2d] = None
    # data type: AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition
    oneof_schema_2_validator: Optional[AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition] = None
    # data type: AnnotationTypeFieldDefinitionMarginOfErrorTolerance
    oneof_schema_3_validator: Optional[AnnotationTypeFieldDefinitionMarginOfErrorTolerance] = None
    # data type: AnnotationTypeFieldDefinitionVertexCountMinMax
    oneof_schema_4_validator: Optional[AnnotationTypeFieldDefinitionVertexCountMinMax] = None
    # data type: AnnotationTypeFieldDefinitionMinimumArea2d
    oneof_schema_5_validator: Optional[AnnotationTypeFieldDefinitionMinimumArea2d] = None
    # data type: AnnotationTypeFieldDefinitionDisplayLineDirection
    oneof_schema_6_validator: Optional[AnnotationTypeFieldDefinitionDisplayLineDirection] = None
    # data type: AnnotationTypeFieldDefinitionAnnotationEditorFeature
    oneof_schema_7_validator: Optional[AnnotationTypeFieldDefinitionAnnotationEditorFeature] = None
    # data type: AnnotationTypeFieldDefinitionOneIntegerField
    oneof_schema_8_validator: Optional[AnnotationTypeFieldDefinitionOneIntegerField] = None
    # data type: AnnotationTypeFieldDefinitionOneStringField
    oneof_schema_9_validator: Optional[AnnotationTypeFieldDefinitionOneStringField] = None
    # data type: AnnotationTypeFieldDefinitionOneBooleanField
    oneof_schema_10_validator: Optional[AnnotationTypeFieldDefinitionOneBooleanField] = None
    actual_instance: Optional[
        Union[
            AnnotationTypeFieldDefinitionAnnotationEditorFeature,
            AnnotationTypeFieldDefinitionDisplayLineDirection,
            AnnotationTypeFieldDefinitionMarginOfErrorTolerance,
            AnnotationTypeFieldDefinitionMinimumArea2d,
            AnnotationTypeFieldDefinitionMinimumSize2d,
            AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition,
            AnnotationTypeFieldDefinitionOneBooleanField,
            AnnotationTypeFieldDefinitionOneIntegerField,
            AnnotationTypeFieldDefinitionOneStringField,
            AnnotationTypeFieldDefinitionVertexCountMinMax,
        ]
    ] = None
    one_of_schemas: Set[str] = {
        "AnnotationTypeFieldDefinitionAnnotationEditorFeature",
        "AnnotationTypeFieldDefinitionDisplayLineDirection",
        "AnnotationTypeFieldDefinitionMarginOfErrorTolerance",
        "AnnotationTypeFieldDefinitionMinimumArea2d",
        "AnnotationTypeFieldDefinitionMinimumSize2d",
        "AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition",
        "AnnotationTypeFieldDefinitionOneBooleanField",
        "AnnotationTypeFieldDefinitionOneIntegerField",
        "AnnotationTypeFieldDefinitionOneStringField",
        "AnnotationTypeFieldDefinitionVertexCountMinMax",
    }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )

    discriminator_value_class_map: Dict[str, str] = {}

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator("actual_instance")
    def actual_instance_must_validate_oneof(cls, v):
        instance = UserDefinedAnnotationTypeFieldDefinition.model_construct()
        error_messages = []
        match = 0
        # validate data type: AnnotationTypeFieldDefinitionMinimumSize2d
        if not isinstance(v, AnnotationTypeFieldDefinitionMinimumSize2d):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationTypeFieldDefinitionMinimumSize2d`")
        else:
            match += 1
        # validate data type: AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition
        if not isinstance(v, AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition`")
        else:
            match += 1
        # validate data type: AnnotationTypeFieldDefinitionMarginOfErrorTolerance
        if not isinstance(v, AnnotationTypeFieldDefinitionMarginOfErrorTolerance):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationTypeFieldDefinitionMarginOfErrorTolerance`")
        else:
            match += 1
        # validate data type: AnnotationTypeFieldDefinitionVertexCountMinMax
        if not isinstance(v, AnnotationTypeFieldDefinitionVertexCountMinMax):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationTypeFieldDefinitionVertexCountMinMax`")
        else:
            match += 1
        # validate data type: AnnotationTypeFieldDefinitionMinimumArea2d
        if not isinstance(v, AnnotationTypeFieldDefinitionMinimumArea2d):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationTypeFieldDefinitionMinimumArea2d`")
        else:
            match += 1
        # validate data type: AnnotationTypeFieldDefinitionDisplayLineDirection
        if not isinstance(v, AnnotationTypeFieldDefinitionDisplayLineDirection):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationTypeFieldDefinitionDisplayLineDirection`")
        else:
            match += 1
        # validate data type: AnnotationTypeFieldDefinitionAnnotationEditorFeature
        if not isinstance(v, AnnotationTypeFieldDefinitionAnnotationEditorFeature):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationTypeFieldDefinitionAnnotationEditorFeature`")
        else:
            match += 1
        # validate data type: AnnotationTypeFieldDefinitionOneIntegerField
        if not isinstance(v, AnnotationTypeFieldDefinitionOneIntegerField):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationTypeFieldDefinitionOneIntegerField`")
        else:
            match += 1
        # validate data type: AnnotationTypeFieldDefinitionOneStringField
        if not isinstance(v, AnnotationTypeFieldDefinitionOneStringField):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationTypeFieldDefinitionOneStringField`")
        else:
            match += 1
        # validate data type: AnnotationTypeFieldDefinitionOneBooleanField
        if not isinstance(v, AnnotationTypeFieldDefinitionOneBooleanField):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationTypeFieldDefinitionOneBooleanField`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when setting `actual_instance` in UserDefinedAnnotationTypeFieldDefinition with oneOf schemas: AnnotationTypeFieldDefinitionAnnotationEditorFeature, AnnotationTypeFieldDefinitionDisplayLineDirection, AnnotationTypeFieldDefinitionMarginOfErrorTolerance, AnnotationTypeFieldDefinitionMinimumArea2d, AnnotationTypeFieldDefinitionMinimumSize2d, AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition, AnnotationTypeFieldDefinitionOneBooleanField, AnnotationTypeFieldDefinitionOneIntegerField, AnnotationTypeFieldDefinitionOneStringField, AnnotationTypeFieldDefinitionVertexCountMinMax. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when setting `actual_instance` in UserDefinedAnnotationTypeFieldDefinition with oneOf schemas: AnnotationTypeFieldDefinitionAnnotationEditorFeature, AnnotationTypeFieldDefinitionDisplayLineDirection, AnnotationTypeFieldDefinitionMarginOfErrorTolerance, AnnotationTypeFieldDefinitionMinimumArea2d, AnnotationTypeFieldDefinitionMinimumSize2d, AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition, AnnotationTypeFieldDefinitionOneBooleanField, AnnotationTypeFieldDefinitionOneIntegerField, AnnotationTypeFieldDefinitionOneStringField, AnnotationTypeFieldDefinitionVertexCountMinMax. Details: "
                + ", ".join(error_messages)
            )
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # deserialize data into AnnotationTypeFieldDefinitionMinimumSize2d
        try:
            instance.actual_instance = AnnotationTypeFieldDefinitionMinimumSize2d.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition
        try:
            instance.actual_instance = AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationTypeFieldDefinitionMarginOfErrorTolerance
        try:
            instance.actual_instance = AnnotationTypeFieldDefinitionMarginOfErrorTolerance.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationTypeFieldDefinitionVertexCountMinMax
        try:
            instance.actual_instance = AnnotationTypeFieldDefinitionVertexCountMinMax.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationTypeFieldDefinitionMinimumArea2d
        try:
            instance.actual_instance = AnnotationTypeFieldDefinitionMinimumArea2d.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationTypeFieldDefinitionDisplayLineDirection
        try:
            instance.actual_instance = AnnotationTypeFieldDefinitionDisplayLineDirection.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationTypeFieldDefinitionAnnotationEditorFeature
        try:
            instance.actual_instance = AnnotationTypeFieldDefinitionAnnotationEditorFeature.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationTypeFieldDefinitionOneIntegerField
        try:
            instance.actual_instance = AnnotationTypeFieldDefinitionOneIntegerField.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationTypeFieldDefinitionOneStringField
        try:
            instance.actual_instance = AnnotationTypeFieldDefinitionOneStringField.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationTypeFieldDefinitionOneBooleanField
        try:
            instance.actual_instance = AnnotationTypeFieldDefinitionOneBooleanField.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when deserializing the JSON string into UserDefinedAnnotationTypeFieldDefinition with oneOf schemas: AnnotationTypeFieldDefinitionAnnotationEditorFeature, AnnotationTypeFieldDefinitionDisplayLineDirection, AnnotationTypeFieldDefinitionMarginOfErrorTolerance, AnnotationTypeFieldDefinitionMinimumArea2d, AnnotationTypeFieldDefinitionMinimumSize2d, AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition, AnnotationTypeFieldDefinitionOneBooleanField, AnnotationTypeFieldDefinitionOneIntegerField, AnnotationTypeFieldDefinitionOneStringField, AnnotationTypeFieldDefinitionVertexCountMinMax. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when deserializing the JSON string into UserDefinedAnnotationTypeFieldDefinition with oneOf schemas: AnnotationTypeFieldDefinitionAnnotationEditorFeature, AnnotationTypeFieldDefinitionDisplayLineDirection, AnnotationTypeFieldDefinitionMarginOfErrorTolerance, AnnotationTypeFieldDefinitionMinimumArea2d, AnnotationTypeFieldDefinitionMinimumSize2d, AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition, AnnotationTypeFieldDefinitionOneBooleanField, AnnotationTypeFieldDefinitionOneIntegerField, AnnotationTypeFieldDefinitionOneStringField, AnnotationTypeFieldDefinitionVertexCountMinMax. Details: "
                + ", ".join(error_messages)
            )
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(
        self,
    ) -> Optional[
        Union[
            Dict[str, Any],
            AnnotationTypeFieldDefinitionAnnotationEditorFeature,
            AnnotationTypeFieldDefinitionDisplayLineDirection,
            AnnotationTypeFieldDefinitionMarginOfErrorTolerance,
            AnnotationTypeFieldDefinitionMinimumArea2d,
            AnnotationTypeFieldDefinitionMinimumSize2d,
            AnnotationTypeFieldDefinitionMinimumSize2dWithDefaultInsertPosition,
            AnnotationTypeFieldDefinitionOneBooleanField,
            AnnotationTypeFieldDefinitionOneIntegerField,
            AnnotationTypeFieldDefinitionOneStringField,
            AnnotationTypeFieldDefinitionVertexCountMinMax,
        ]
    ]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())
