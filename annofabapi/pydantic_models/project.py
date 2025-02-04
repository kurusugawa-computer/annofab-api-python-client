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

from annofabapi.pydantic_models.input_data_type import InputDataType
from annofabapi.pydantic_models.project_configuration_get import ProjectConfigurationGet
from annofabapi.pydantic_models.project_status import ProjectStatus
from annofabapi.pydantic_models.project_summary import ProjectSummary


class Project(BaseModel):
    """
    Project
    """

    project_id: StrictStr = Field(description="プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    organization_id: StrictStr = Field(description="組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    title: StrictStr = Field(description="プロジェクトのタイトル")
    overview: Optional[StrictStr] = Field(default=None, description="プロジェクトの概要")
    project_status: ProjectStatus
    input_data_type: InputDataType
    configuration: ProjectConfigurationGet
    created_datetime: str = Field(description="作成日時")
    updated_datetime: str = Field(description="更新日時")
    summary: ProjectSummary
    __properties: ClassVar[List[str]] = [
        "project_id",
        "organization_id",
        "title",
        "overview",
        "project_status",
        "input_data_type",
        "configuration",
        "created_datetime",
        "updated_datetime",
        "summary",
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
        """Create an instance of Project from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of configuration
        if self.configuration:
            _dict["configuration"] = self.configuration.to_dict()
        # override the default output from pydantic by calling `to_dict()` of summary
        if self.summary:
            _dict["summary"] = self.summary.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Project from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "project_id": obj.get("project_id"),
                "organization_id": obj.get("organization_id"),
                "title": obj.get("title"),
                "overview": obj.get("overview"),
                "project_status": obj.get("project_status"),
                "input_data_type": obj.get("input_data_type"),
                "configuration": ProjectConfigurationGet.from_dict(obj["configuration"]) if obj.get("configuration") is not None else None,
                "created_datetime": obj.get("created_datetime"),
                "updated_datetime": obj.get("updated_datetime"),
                "summary": ProjectSummary.from_dict(obj["summary"]) if obj.get("summary") is not None else None,
            }
        )
        return _obj
