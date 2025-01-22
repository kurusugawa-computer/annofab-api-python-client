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
import re  # noqa: F401
from typing import Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing_extensions import Self


class CountResult(BaseModel):
    """
    CountResult
    """

    type: Optional[StrictStr] = Field(default=None, description="`CountResult` [詳しくはこちら](#section/API-Convention/API-_type) ", alias="_type")
    name: Optional[StrictStr] = Field(
        default=None,
        description="複数の集約を区別するための名前です。  `(フィールド名)_(集約内容)` のように命名されます。例えば `account_id` フィールドを `count` する場合、`account_id_count` となります。 ",
    )
    var_field: Optional[StrictStr] = Field(
        default=None,
        description="集約に使われたリソースのフィールド名です。  リソースの属性のさらに属性を参照するときは、`foo.bar.buz` のようにドット区切りになります。 ",
        alias="field",
    )
    doc_count: Optional[StrictInt] = Field(default=None, description="集約の件数です。 ")
    items: Optional[List[Count]] = Field(default=None, description="集約結果の値です。 ")
    __properties: ClassVar[List[str]] = ["_type", "name", "field", "doc_count", "items"]

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
        """Create an instance of CountResult from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in items (list)
        _items = []
        if self.items:
            for _item_items in self.items:
                if _item_items:
                    _items.append(_item_items.to_dict())
            _dict["items"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CountResult from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "_type": obj.get("_type"),
                "name": obj.get("name"),
                "field": obj.get("field"),
                "doc_count": obj.get("doc_count"),
                "items": [Count.from_dict(_item) for _item in obj["items"]] if obj.get("items") is not None else None,
            }
        )
        return _obj


from annofabapi.pydantic_models.count import Count

# TODO: Rewrite to not use raise_errors
CountResult.model_rebuild(raise_errors=False)
