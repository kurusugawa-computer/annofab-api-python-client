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

from annofabapi.pydantic_models.worktime_statistics_data import WorktimeStatisticsData


class WorktimeStatisticsByAccount(BaseModel):
    """
    WorktimeStatisticsByAccount
    """

    project_id: StrictStr = Field(description="プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    account_id: StrictStr = Field(description="アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    data_series: List[WorktimeStatisticsData] = Field(description="プロジェクトメンバーの日毎の作業時間統計データ")
    __properties: ClassVar[List[str]] = ["project_id", "account_id", "data_series"]

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
        """Create an instance of WorktimeStatisticsByAccount from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in data_series (list)
        _items = []
        if self.data_series:
            for _item_data_series in self.data_series:
                if _item_data_series:
                    _items.append(_item_data_series.to_dict())
            _dict["data_series"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of WorktimeStatisticsByAccount from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "project_id": obj.get("project_id"),
                "account_id": obj.get("account_id"),
                "data_series": [WorktimeStatisticsData.from_dict(_item) for _item in obj["data_series"]]
                if obj.get("data_series") is not None
                else None,
            }
        )
        return _obj
