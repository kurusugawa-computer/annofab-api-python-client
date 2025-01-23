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

from annofabapi.pydantic_models.histogram_item import HistogramItem
from annofabapi.pydantic_models.task_phase import TaskPhase


class WorktimeStatisticsItem(BaseModel):
    """
    WorktimeStatisticsItem
    """

    phase: TaskPhase
    histogram: List[HistogramItem] = Field(description="ヒストグラム情報")
    average: StrictStr = Field(description="作業時間の平均（ISO 8601 duration）")
    standard_deviation: StrictStr = Field(description="作業時間の標準偏差（ISO 8601 duration）")
    __properties: ClassVar[List[str]] = ["phase", "histogram", "average", "standard_deviation"]

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
        """Create an instance of WorktimeStatisticsItem from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in histogram (list)
        _items = []
        if self.histogram:
            for _item_histogram in self.histogram:
                if _item_histogram:
                    _items.append(_item_histogram.to_dict())
            _dict["histogram"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of WorktimeStatisticsItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "phase": obj.get("phase"),
                "histogram": [HistogramItem.from_dict(_item) for _item in obj["histogram"]] if obj.get("histogram") is not None else None,
                "average": obj.get("average"),
                "standard_deviation": obj.get("standard_deviation"),
            }
        )
        return _obj
