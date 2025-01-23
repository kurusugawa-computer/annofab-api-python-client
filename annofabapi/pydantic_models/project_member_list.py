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
from typing import Any, ClassVar, Dict, List, Optional, Set, Union

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt
from typing_extensions import Self

from annofabapi.pydantic_models.aggregation_result import AggregationResult
from annofabapi.pydantic_models.project_member import ProjectMember


class ProjectMemberList(BaseModel):
    """
    ProjectMemberList
    """

    list: List[ProjectMember] = Field(description="プロジェクトメンバーの一覧")
    page_no: Union[StrictFloat, StrictInt] = Field(description="現在のページ番号。")
    total_page_no: Union[StrictFloat, StrictInt] = Field(
        description="指定された条件にあてはまる検索結果の総ページ数。検索条件に当てはまるプロジェクトメンバーが0件であっても、総ページ数は1となります。"
    )
    total_count: Union[StrictFloat, StrictInt] = Field(description="検索結果の総件数。")
    over_limit: StrictBool = Field(description="検索結果が1万件を超えた場合にtrueとなる。")
    aggregations: List[AggregationResult] = Field(description="システム内部用のプロパティ ")
    __properties: ClassVar[List[str]] = ["list", "page_no", "total_page_no", "total_count", "over_limit", "aggregations"]

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
        """Create an instance of ProjectMemberList from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in list (list)
        _items = []
        if self.list:
            for _item_list in self.list:
                if _item_list:
                    _items.append(_item_list.to_dict())
            _dict["list"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in aggregations (list)
        _items = []
        if self.aggregations:
            for _item_aggregations in self.aggregations:
                if _item_aggregations:
                    _items.append(_item_aggregations.to_dict())
            _dict["aggregations"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProjectMemberList from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "list": [ProjectMember.from_dict(_item) for _item in obj["list"]] if obj.get("list") is not None else None,
                "page_no": obj.get("page_no"),
                "total_page_no": obj.get("total_page_no"),
                "total_count": obj.get("total_count"),
                "over_limit": obj.get("over_limit"),
                "aggregations": [AggregationResult.from_dict(_item) for _item in obj["aggregations"]]
                if obj.get("aggregations") is not None
                else None,
            }
        )
        return _obj
