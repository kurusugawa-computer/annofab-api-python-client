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


class TaskRequest(BaseModel):
    """
    TaskRequest
    """

    input_data_id_list: List[StrictStr] = Field(
        description="タスクに割り当てる入力データのID。タスクに割り当てることができる入力データの個数は最大200です。"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="ユーザーが自由に登録できるkey-value型のメタデータです。 keyにはメタデータ名、valueには値を指定してください。  keyに指定できる文字種は次の通りです。  * 半角英数字 * `_` (アンダースコア) * `-` (ハイフン)  valueに指定できる値は次の通りです。  * 文字列 * 数値 * 真偽値 ",
    )
    __properties: ClassVar[List[str]] = ["input_data_id_list", "metadata"]

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
        """Create an instance of TaskRequest from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TaskRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({"input_data_id_list": obj.get("input_data_id_list"), "metadata": obj.get("metadata")})
        return _obj
