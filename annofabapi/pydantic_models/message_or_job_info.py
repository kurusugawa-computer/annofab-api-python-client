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

from annofabapi.pydantic_models.message import Message
from annofabapi.pydantic_models.project_job_info import ProjectJobInfo

MESSAGEORJOBINFO_ONE_OF_SCHEMAS = ["Message", "ProjectJobInfo"]


class MessageOrJobInfo(BaseModel):
    """
    MessageOrJobInfo
    """

    # data type: Message
    oneof_schema_1_validator: Optional[Message] = None
    # data type: ProjectJobInfo
    oneof_schema_2_validator: Optional[ProjectJobInfo] = None
    actual_instance: Optional[Union[Message, ProjectJobInfo]] = None
    one_of_schemas: Set[str] = {"Message", "ProjectJobInfo"}

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )

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
        instance = MessageOrJobInfo.model_construct()
        error_messages = []
        match = 0
        # validate data type: Message
        if not isinstance(v, Message):
            error_messages.append(f"Error! Input type `{type(v)}` is not `Message`")
        else:
            match += 1
        # validate data type: ProjectJobInfo
        if not isinstance(v, ProjectJobInfo):
            error_messages.append(f"Error! Input type `{type(v)}` is not `ProjectJobInfo`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when setting `actual_instance` in MessageOrJobInfo with oneOf schemas: Message, ProjectJobInfo. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when setting `actual_instance` in MessageOrJobInfo with oneOf schemas: Message, ProjectJobInfo. Details: "
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

        # deserialize data into Message
        try:
            instance.actual_instance = Message.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into ProjectJobInfo
        try:
            instance.actual_instance = ProjectJobInfo.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when deserializing the JSON string into MessageOrJobInfo with oneOf schemas: Message, ProjectJobInfo. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when deserializing the JSON string into MessageOrJobInfo with oneOf schemas: Message, ProjectJobInfo. Details: "
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

    def to_dict(self) -> Optional[Union[Dict[str, Any], Message, ProjectJobInfo]]:
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
