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

from annofabapi.pydantic_models.annotation_detail_content_output_inner import AnnotationDetailContentOutputInner
from annofabapi.pydantic_models.annotation_detail_content_output_inner_unknown import AnnotationDetailContentOutputInnerUnknown
from annofabapi.pydantic_models.annotation_detail_content_output_outer import AnnotationDetailContentOutputOuter
from annofabapi.pydantic_models.annotation_detail_content_output_outer_unresolved import AnnotationDetailContentOutputOuterUnresolved

ANNOTATIONDETAILCONTENTOUTPUT_ONE_OF_SCHEMAS = [
    "AnnotationDetailContentOutputInner",
    "AnnotationDetailContentOutputInnerUnknown",
    "AnnotationDetailContentOutputOuter",
    "AnnotationDetailContentOutputOuterUnresolved",
]


class AnnotationDetailContentOutput(BaseModel):
    """
    - **AnnotationDetailContentOutputInner**   - アノテーションのデータ部をJSON内部に保持している場合、通常はこの型の値となります - **AnnotationDetailContentOutputInnerUnknown**   - アノテーションのデータ部をJSON内部に保持しており、且つ、AnnotationDetailV1の形式で保存されていたデータのAnnotationTypeが特定できない場合にこの値となります   - 典型的な例では、アノテーションの保存後にアノテーション仕様が書き換わっていた場合が該当します - **AnnotationDetailContentOutputOuter**   - アノテーションのデータ部を外部ファイルの形式（画像など）で保持している場合、通常はこの型の値となります - **AnnotationDetailContentOutputOuterUnresolved**   - アノテーションのデータ部を外部ファイルの形式（画像など）で保持しており、且つ、Outerのurl / etagを解決しなかった場合（過去のアノテーションを取得した場合等）にこの値となります
    """

    # data type: AnnotationDetailContentOutputInner
    oneof_schema_1_validator: Optional[AnnotationDetailContentOutputInner] = None
    # data type: AnnotationDetailContentOutputInnerUnknown
    oneof_schema_2_validator: Optional[AnnotationDetailContentOutputInnerUnknown] = None
    # data type: AnnotationDetailContentOutputOuter
    oneof_schema_3_validator: Optional[AnnotationDetailContentOutputOuter] = None
    # data type: AnnotationDetailContentOutputOuterUnresolved
    oneof_schema_4_validator: Optional[AnnotationDetailContentOutputOuterUnresolved] = None
    actual_instance: Optional[
        Union[
            AnnotationDetailContentOutputInner,
            AnnotationDetailContentOutputInnerUnknown,
            AnnotationDetailContentOutputOuter,
            AnnotationDetailContentOutputOuterUnresolved,
        ]
    ] = None
    one_of_schemas: Set[str] = {
        "AnnotationDetailContentOutputInner",
        "AnnotationDetailContentOutputInnerUnknown",
        "AnnotationDetailContentOutputOuter",
        "AnnotationDetailContentOutputOuterUnresolved",
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
        instance = AnnotationDetailContentOutput.model_construct()
        error_messages = []
        match = 0
        # validate data type: AnnotationDetailContentOutputInner
        if not isinstance(v, AnnotationDetailContentOutputInner):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationDetailContentOutputInner`")
        else:
            match += 1
        # validate data type: AnnotationDetailContentOutputInnerUnknown
        if not isinstance(v, AnnotationDetailContentOutputInnerUnknown):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationDetailContentOutputInnerUnknown`")
        else:
            match += 1
        # validate data type: AnnotationDetailContentOutputOuter
        if not isinstance(v, AnnotationDetailContentOutputOuter):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationDetailContentOutputOuter`")
        else:
            match += 1
        # validate data type: AnnotationDetailContentOutputOuterUnresolved
        if not isinstance(v, AnnotationDetailContentOutputOuterUnresolved):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AnnotationDetailContentOutputOuterUnresolved`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when setting `actual_instance` in AnnotationDetailContentOutput with oneOf schemas: AnnotationDetailContentOutputInner, AnnotationDetailContentOutputInnerUnknown, AnnotationDetailContentOutputOuter, AnnotationDetailContentOutputOuterUnresolved. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when setting `actual_instance` in AnnotationDetailContentOutput with oneOf schemas: AnnotationDetailContentOutputInner, AnnotationDetailContentOutputInnerUnknown, AnnotationDetailContentOutputOuter, AnnotationDetailContentOutputOuterUnresolved. Details: "
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

        # deserialize data into AnnotationDetailContentOutputInner
        try:
            instance.actual_instance = AnnotationDetailContentOutputInner.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationDetailContentOutputInnerUnknown
        try:
            instance.actual_instance = AnnotationDetailContentOutputInnerUnknown.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationDetailContentOutputOuter
        try:
            instance.actual_instance = AnnotationDetailContentOutputOuter.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationDetailContentOutputOuterUnresolved
        try:
            instance.actual_instance = AnnotationDetailContentOutputOuterUnresolved.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when deserializing the JSON string into AnnotationDetailContentOutput with oneOf schemas: AnnotationDetailContentOutputInner, AnnotationDetailContentOutputInnerUnknown, AnnotationDetailContentOutputOuter, AnnotationDetailContentOutputOuterUnresolved. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when deserializing the JSON string into AnnotationDetailContentOutput with oneOf schemas: AnnotationDetailContentOutputInner, AnnotationDetailContentOutputInnerUnknown, AnnotationDetailContentOutputOuter, AnnotationDetailContentOutputOuterUnresolved. Details: "
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
            AnnotationDetailContentOutputInner,
            AnnotationDetailContentOutputInnerUnknown,
            AnnotationDetailContentOutputOuter,
            AnnotationDetailContentOutputOuterUnresolved,
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
