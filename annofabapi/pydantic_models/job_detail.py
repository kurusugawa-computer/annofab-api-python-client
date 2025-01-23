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

from annofabapi.pydantic_models.job_detail_copy_project import JobDetailCopyProject
from annofabapi.pydantic_models.job_detail_gen_inputs import JobDetailGenInputs
from annofabapi.pydantic_models.job_detail_gen_tasks import JobDetailGenTasks
from annofabapi.pydantic_models.job_detail_invoke_hook import JobDetailInvokeHook
from annofabapi.pydantic_models.job_detail_move_project import JobDetailMoveProject

JOBDETAIL_ONE_OF_SCHEMAS = ["JobDetailCopyProject", "JobDetailGenInputs", "JobDetailGenTasks", "JobDetailInvokeHook", "JobDetailMoveProject"]


class JobDetail(BaseModel):
    """
    ジョブ結果の内部情報
    """

    # data type: JobDetailGenInputs
    oneof_schema_1_validator: Optional[JobDetailGenInputs] = None
    # data type: JobDetailGenTasks
    oneof_schema_2_validator: Optional[JobDetailGenTasks] = None
    # data type: JobDetailCopyProject
    oneof_schema_3_validator: Optional[JobDetailCopyProject] = None
    # data type: JobDetailMoveProject
    oneof_schema_4_validator: Optional[JobDetailMoveProject] = None
    # data type: JobDetailInvokeHook
    oneof_schema_5_validator: Optional[JobDetailInvokeHook] = None
    actual_instance: Optional[Union[JobDetailCopyProject, JobDetailGenInputs, JobDetailGenTasks, JobDetailInvokeHook, JobDetailMoveProject]] = None
    one_of_schemas: Set[str] = {"JobDetailCopyProject", "JobDetailGenInputs", "JobDetailGenTasks", "JobDetailInvokeHook", "JobDetailMoveProject"}

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
        instance = JobDetail.model_construct()
        error_messages = []
        match = 0
        # validate data type: JobDetailGenInputs
        if not isinstance(v, JobDetailGenInputs):
            error_messages.append(f"Error! Input type `{type(v)}` is not `JobDetailGenInputs`")
        else:
            match += 1
        # validate data type: JobDetailGenTasks
        if not isinstance(v, JobDetailGenTasks):
            error_messages.append(f"Error! Input type `{type(v)}` is not `JobDetailGenTasks`")
        else:
            match += 1
        # validate data type: JobDetailCopyProject
        if not isinstance(v, JobDetailCopyProject):
            error_messages.append(f"Error! Input type `{type(v)}` is not `JobDetailCopyProject`")
        else:
            match += 1
        # validate data type: JobDetailMoveProject
        if not isinstance(v, JobDetailMoveProject):
            error_messages.append(f"Error! Input type `{type(v)}` is not `JobDetailMoveProject`")
        else:
            match += 1
        # validate data type: JobDetailInvokeHook
        if not isinstance(v, JobDetailInvokeHook):
            error_messages.append(f"Error! Input type `{type(v)}` is not `JobDetailInvokeHook`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when setting `actual_instance` in JobDetail with oneOf schemas: JobDetailCopyProject, JobDetailGenInputs, JobDetailGenTasks, JobDetailInvokeHook, JobDetailMoveProject. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when setting `actual_instance` in JobDetail with oneOf schemas: JobDetailCopyProject, JobDetailGenInputs, JobDetailGenTasks, JobDetailInvokeHook, JobDetailMoveProject. Details: "
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

        # deserialize data into JobDetailGenInputs
        try:
            instance.actual_instance = JobDetailGenInputs.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into JobDetailGenTasks
        try:
            instance.actual_instance = JobDetailGenTasks.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into JobDetailCopyProject
        try:
            instance.actual_instance = JobDetailCopyProject.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into JobDetailMoveProject
        try:
            instance.actual_instance = JobDetailMoveProject.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into JobDetailInvokeHook
        try:
            instance.actual_instance = JobDetailInvokeHook.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when deserializing the JSON string into JobDetail with oneOf schemas: JobDetailCopyProject, JobDetailGenInputs, JobDetailGenTasks, JobDetailInvokeHook, JobDetailMoveProject. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when deserializing the JSON string into JobDetail with oneOf schemas: JobDetailCopyProject, JobDetailGenInputs, JobDetailGenTasks, JobDetailInvokeHook, JobDetailMoveProject. Details: "
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
    ) -> Optional[Union[Dict[str, Any], JobDetailCopyProject, JobDetailGenInputs, JobDetailGenTasks, JobDetailInvokeHook, JobDetailMoveProject]]:
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
