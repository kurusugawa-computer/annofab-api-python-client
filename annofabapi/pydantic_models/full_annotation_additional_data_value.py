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

from annofabapi.pydantic_models.full_annotation_additional_data_value_choice import FullAnnotationAdditionalDataValueChoice
from annofabapi.pydantic_models.full_annotation_additional_data_value_comment import FullAnnotationAdditionalDataValueComment
from annofabapi.pydantic_models.full_annotation_additional_data_value_flag import FullAnnotationAdditionalDataValueFlag
from annofabapi.pydantic_models.full_annotation_additional_data_value_integer import FullAnnotationAdditionalDataValueInteger
from annofabapi.pydantic_models.full_annotation_additional_data_value_link import FullAnnotationAdditionalDataValueLink
from annofabapi.pydantic_models.full_annotation_additional_data_value_tracking import FullAnnotationAdditionalDataValueTracking

FULLANNOTATIONADDITIONALDATAVALUE_ONE_OF_SCHEMAS = [
    "FullAnnotationAdditionalDataValueChoice",
    "FullAnnotationAdditionalDataValueComment",
    "FullAnnotationAdditionalDataValueFlag",
    "FullAnnotationAdditionalDataValueInteger",
    "FullAnnotationAdditionalDataValueLink",
    "FullAnnotationAdditionalDataValueTracking",
]


class FullAnnotationAdditionalDataValue(BaseModel):
    """
    属性値
    """

    # data type: FullAnnotationAdditionalDataValueFlag
    oneof_schema_1_validator: Optional[FullAnnotationAdditionalDataValueFlag] = None
    # data type: FullAnnotationAdditionalDataValueInteger
    oneof_schema_2_validator: Optional[FullAnnotationAdditionalDataValueInteger] = None
    # data type: FullAnnotationAdditionalDataValueComment
    oneof_schema_3_validator: Optional[FullAnnotationAdditionalDataValueComment] = None
    # data type: FullAnnotationAdditionalDataValueChoice
    oneof_schema_4_validator: Optional[FullAnnotationAdditionalDataValueChoice] = None
    # data type: FullAnnotationAdditionalDataValueTracking
    oneof_schema_5_validator: Optional[FullAnnotationAdditionalDataValueTracking] = None
    # data type: FullAnnotationAdditionalDataValueLink
    oneof_schema_6_validator: Optional[FullAnnotationAdditionalDataValueLink] = None
    actual_instance: Optional[
        Union[
            FullAnnotationAdditionalDataValueChoice,
            FullAnnotationAdditionalDataValueComment,
            FullAnnotationAdditionalDataValueFlag,
            FullAnnotationAdditionalDataValueInteger,
            FullAnnotationAdditionalDataValueLink,
            FullAnnotationAdditionalDataValueTracking,
        ]
    ] = None
    one_of_schemas: Set[str] = {
        "FullAnnotationAdditionalDataValueChoice",
        "FullAnnotationAdditionalDataValueComment",
        "FullAnnotationAdditionalDataValueFlag",
        "FullAnnotationAdditionalDataValueInteger",
        "FullAnnotationAdditionalDataValueLink",
        "FullAnnotationAdditionalDataValueTracking",
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
        instance = FullAnnotationAdditionalDataValue.model_construct()
        error_messages = []
        match = 0
        # validate data type: FullAnnotationAdditionalDataValueFlag
        if not isinstance(v, FullAnnotationAdditionalDataValueFlag):
            error_messages.append(f"Error! Input type `{type(v)}` is not `FullAnnotationAdditionalDataValueFlag`")
        else:
            match += 1
        # validate data type: FullAnnotationAdditionalDataValueInteger
        if not isinstance(v, FullAnnotationAdditionalDataValueInteger):
            error_messages.append(f"Error! Input type `{type(v)}` is not `FullAnnotationAdditionalDataValueInteger`")
        else:
            match += 1
        # validate data type: FullAnnotationAdditionalDataValueComment
        if not isinstance(v, FullAnnotationAdditionalDataValueComment):
            error_messages.append(f"Error! Input type `{type(v)}` is not `FullAnnotationAdditionalDataValueComment`")
        else:
            match += 1
        # validate data type: FullAnnotationAdditionalDataValueChoice
        if not isinstance(v, FullAnnotationAdditionalDataValueChoice):
            error_messages.append(f"Error! Input type `{type(v)}` is not `FullAnnotationAdditionalDataValueChoice`")
        else:
            match += 1
        # validate data type: FullAnnotationAdditionalDataValueTracking
        if not isinstance(v, FullAnnotationAdditionalDataValueTracking):
            error_messages.append(f"Error! Input type `{type(v)}` is not `FullAnnotationAdditionalDataValueTracking`")
        else:
            match += 1
        # validate data type: FullAnnotationAdditionalDataValueLink
        if not isinstance(v, FullAnnotationAdditionalDataValueLink):
            error_messages.append(f"Error! Input type `{type(v)}` is not `FullAnnotationAdditionalDataValueLink`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when setting `actual_instance` in FullAnnotationAdditionalDataValue with oneOf schemas: FullAnnotationAdditionalDataValueChoice, FullAnnotationAdditionalDataValueComment, FullAnnotationAdditionalDataValueFlag, FullAnnotationAdditionalDataValueInteger, FullAnnotationAdditionalDataValueLink, FullAnnotationAdditionalDataValueTracking. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when setting `actual_instance` in FullAnnotationAdditionalDataValue with oneOf schemas: FullAnnotationAdditionalDataValueChoice, FullAnnotationAdditionalDataValueComment, FullAnnotationAdditionalDataValueFlag, FullAnnotationAdditionalDataValueInteger, FullAnnotationAdditionalDataValueLink, FullAnnotationAdditionalDataValueTracking. Details: "
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

        # deserialize data into FullAnnotationAdditionalDataValueFlag
        try:
            instance.actual_instance = FullAnnotationAdditionalDataValueFlag.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into FullAnnotationAdditionalDataValueInteger
        try:
            instance.actual_instance = FullAnnotationAdditionalDataValueInteger.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into FullAnnotationAdditionalDataValueComment
        try:
            instance.actual_instance = FullAnnotationAdditionalDataValueComment.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into FullAnnotationAdditionalDataValueChoice
        try:
            instance.actual_instance = FullAnnotationAdditionalDataValueChoice.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into FullAnnotationAdditionalDataValueTracking
        try:
            instance.actual_instance = FullAnnotationAdditionalDataValueTracking.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into FullAnnotationAdditionalDataValueLink
        try:
            instance.actual_instance = FullAnnotationAdditionalDataValueLink.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when deserializing the JSON string into FullAnnotationAdditionalDataValue with oneOf schemas: FullAnnotationAdditionalDataValueChoice, FullAnnotationAdditionalDataValueComment, FullAnnotationAdditionalDataValueFlag, FullAnnotationAdditionalDataValueInteger, FullAnnotationAdditionalDataValueLink, FullAnnotationAdditionalDataValueTracking. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when deserializing the JSON string into FullAnnotationAdditionalDataValue with oneOf schemas: FullAnnotationAdditionalDataValueChoice, FullAnnotationAdditionalDataValueComment, FullAnnotationAdditionalDataValueFlag, FullAnnotationAdditionalDataValueInteger, FullAnnotationAdditionalDataValueLink, FullAnnotationAdditionalDataValueTracking. Details: "
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
            FullAnnotationAdditionalDataValueChoice,
            FullAnnotationAdditionalDataValueComment,
            FullAnnotationAdditionalDataValueFlag,
            FullAnnotationAdditionalDataValueInteger,
            FullAnnotationAdditionalDataValueLink,
            FullAnnotationAdditionalDataValueTracking,
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
