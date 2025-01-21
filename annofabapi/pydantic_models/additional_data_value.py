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
from typing import Any, Dict, Optional, Set, Union

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator
from typing_extensions import Self

from annofabapi.pydantic_models.additional_data_value_choice import AdditionalDataValueChoice
from annofabapi.pydantic_models.additional_data_value_comment import AdditionalDataValueComment
from annofabapi.pydantic_models.additional_data_value_flag import AdditionalDataValueFlag
from annofabapi.pydantic_models.additional_data_value_integer import AdditionalDataValueInteger
from annofabapi.pydantic_models.additional_data_value_link import AdditionalDataValueLink
from annofabapi.pydantic_models.additional_data_value_select import AdditionalDataValueSelect
from annofabapi.pydantic_models.additional_data_value_text import AdditionalDataValueText
from annofabapi.pydantic_models.additional_data_value_tracking import AdditionalDataValueTracking

ADDITIONALDATAVALUE_ONE_OF_SCHEMAS = [
    "AdditionalDataValueChoice",
    "AdditionalDataValueComment",
    "AdditionalDataValueFlag",
    "AdditionalDataValueInteger",
    "AdditionalDataValueLink",
    "AdditionalDataValueSelect",
    "AdditionalDataValueText",
    "AdditionalDataValueTracking",
]


class AdditionalDataValue(BaseModel):
    """
    属性値
    """

    # data type: AdditionalDataValueFlag
    oneof_schema_1_validator: Optional[AdditionalDataValueFlag] = None
    # data type: AdditionalDataValueInteger
    oneof_schema_2_validator: Optional[AdditionalDataValueInteger] = None
    # data type: AdditionalDataValueComment
    oneof_schema_3_validator: Optional[AdditionalDataValueComment] = None
    # data type: AdditionalDataValueText
    oneof_schema_4_validator: Optional[AdditionalDataValueText] = None
    # data type: AdditionalDataValueChoice
    oneof_schema_5_validator: Optional[AdditionalDataValueChoice] = None
    # data type: AdditionalDataValueSelect
    oneof_schema_6_validator: Optional[AdditionalDataValueSelect] = None
    # data type: AdditionalDataValueTracking
    oneof_schema_7_validator: Optional[AdditionalDataValueTracking] = None
    # data type: AdditionalDataValueLink
    oneof_schema_8_validator: Optional[AdditionalDataValueLink] = None
    actual_instance: Optional[
        Union[
            AdditionalDataValueChoice,
            AdditionalDataValueComment,
            AdditionalDataValueFlag,
            AdditionalDataValueInteger,
            AdditionalDataValueLink,
            AdditionalDataValueSelect,
            AdditionalDataValueText,
            AdditionalDataValueTracking,
        ]
    ] = None
    one_of_schemas: Set[str] = {
        "AdditionalDataValueChoice",
        "AdditionalDataValueComment",
        "AdditionalDataValueFlag",
        "AdditionalDataValueInteger",
        "AdditionalDataValueLink",
        "AdditionalDataValueSelect",
        "AdditionalDataValueText",
        "AdditionalDataValueTracking",
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
        instance = AdditionalDataValue.model_construct()
        error_messages = []
        match = 0
        # validate data type: AdditionalDataValueFlag
        if not isinstance(v, AdditionalDataValueFlag):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AdditionalDataValueFlag`")
        else:
            match += 1
        # validate data type: AdditionalDataValueInteger
        if not isinstance(v, AdditionalDataValueInteger):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AdditionalDataValueInteger`")
        else:
            match += 1
        # validate data type: AdditionalDataValueComment
        if not isinstance(v, AdditionalDataValueComment):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AdditionalDataValueComment`")
        else:
            match += 1
        # validate data type: AdditionalDataValueText
        if not isinstance(v, AdditionalDataValueText):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AdditionalDataValueText`")
        else:
            match += 1
        # validate data type: AdditionalDataValueChoice
        if not isinstance(v, AdditionalDataValueChoice):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AdditionalDataValueChoice`")
        else:
            match += 1
        # validate data type: AdditionalDataValueSelect
        if not isinstance(v, AdditionalDataValueSelect):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AdditionalDataValueSelect`")
        else:
            match += 1
        # validate data type: AdditionalDataValueTracking
        if not isinstance(v, AdditionalDataValueTracking):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AdditionalDataValueTracking`")
        else:
            match += 1
        # validate data type: AdditionalDataValueLink
        if not isinstance(v, AdditionalDataValueLink):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AdditionalDataValueLink`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when setting `actual_instance` in AdditionalDataValue with oneOf schemas: AdditionalDataValueChoice, AdditionalDataValueComment, AdditionalDataValueFlag, AdditionalDataValueInteger, AdditionalDataValueLink, AdditionalDataValueSelect, AdditionalDataValueText, AdditionalDataValueTracking. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when setting `actual_instance` in AdditionalDataValue with oneOf schemas: AdditionalDataValueChoice, AdditionalDataValueComment, AdditionalDataValueFlag, AdditionalDataValueInteger, AdditionalDataValueLink, AdditionalDataValueSelect, AdditionalDataValueText, AdditionalDataValueTracking. Details: "
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

        # deserialize data into AdditionalDataValueFlag
        try:
            instance.actual_instance = AdditionalDataValueFlag.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AdditionalDataValueInteger
        try:
            instance.actual_instance = AdditionalDataValueInteger.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AdditionalDataValueComment
        try:
            instance.actual_instance = AdditionalDataValueComment.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AdditionalDataValueText
        try:
            instance.actual_instance = AdditionalDataValueText.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AdditionalDataValueChoice
        try:
            instance.actual_instance = AdditionalDataValueChoice.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AdditionalDataValueSelect
        try:
            instance.actual_instance = AdditionalDataValueSelect.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AdditionalDataValueTracking
        try:
            instance.actual_instance = AdditionalDataValueTracking.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AdditionalDataValueLink
        try:
            instance.actual_instance = AdditionalDataValueLink.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when deserializing the JSON string into AdditionalDataValue with oneOf schemas: AdditionalDataValueChoice, AdditionalDataValueComment, AdditionalDataValueFlag, AdditionalDataValueInteger, AdditionalDataValueLink, AdditionalDataValueSelect, AdditionalDataValueText, AdditionalDataValueTracking. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when deserializing the JSON string into AdditionalDataValue with oneOf schemas: AdditionalDataValueChoice, AdditionalDataValueComment, AdditionalDataValueFlag, AdditionalDataValueInteger, AdditionalDataValueLink, AdditionalDataValueSelect, AdditionalDataValueText, AdditionalDataValueTracking. Details: "
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
            AdditionalDataValueChoice,
            AdditionalDataValueComment,
            AdditionalDataValueFlag,
            AdditionalDataValueInteger,
            AdditionalDataValueLink,
            AdditionalDataValueSelect,
            AdditionalDataValueText,
            AdditionalDataValueTracking,
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
