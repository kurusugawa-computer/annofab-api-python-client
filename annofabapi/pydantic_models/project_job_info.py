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

from annofabapi.pydantic_models.errors import Errors
from annofabapi.pydantic_models.job_detail import JobDetail
from annofabapi.pydantic_models.job_status import JobStatus
from annofabapi.pydantic_models.project_job_type import ProjectJobType


class ProjectJobInfo(BaseModel):
    """
    ProjectJobInfo
    """

    project_id: StrictStr = Field(description="プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    job_type: ProjectJobType
    job_id: StrictStr = Field(description="ジョブID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    job_status: JobStatus
    job_execution: Optional[Dict[str, Any]] = Field(default=None, description="ジョブの内部情報")
    job_detail: Optional[JobDetail] = None
    errors: Errors
    created_datetime: str = Field(description="作成日時")
    updated_datetime: str = Field(description="更新日時")
    __properties: ClassVar[List[str]] = [
        "project_id",
        "job_type",
        "job_id",
        "job_status",
        "job_execution",
        "job_detail",
        "errors",
        "created_datetime",
        "updated_datetime",
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
        """Create an instance of ProjectJobInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of job_detail
        if self.job_detail:
            _dict["job_detail"] = self.job_detail.to_dict()
        # override the default output from pydantic by calling `to_dict()` of errors
        if self.errors:
            _dict["errors"] = self.errors.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProjectJobInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "project_id": obj.get("project_id"),
                "job_type": obj.get("job_type"),
                "job_id": obj.get("job_id"),
                "job_status": obj.get("job_status"),
                "job_execution": obj.get("job_execution"),
                "job_detail": JobDetail.from_dict(obj["job_detail"]) if obj.get("job_detail") is not None else None,
                "errors": Errors.from_dict(obj["errors"]) if obj.get("errors") is not None else None,
                "created_datetime": obj.get("created_datetime"),
                "updated_datetime": obj.get("updated_datetime"),
            }
        )
        return _obj
