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

from annofabapi.pydantic_models.internationalization_message_messages_inner import InternationalizationMessageMessagesInner


class InternationalizationMessage(BaseModel):
    """
    InternationalizationMessage
    """

    messages: List[InternationalizationMessageMessagesInner] = Field(
        description="言語コードとメッセージ（テキスト）のリスト。  * アノテーションエディタなどでは、Annofabの表示言語（各ユーザーが個人設定で選んだ言語）のメッセージが使われます * 以下の名前は、[Simple Annotation](#section/Simple-Annotation-ZIP) では `en-US` のメッセージが使われます     * ラベル名     * 属性名     * 選択肢名 * いずれの場合でも、表示しようとした言語が `messages` に含まれない場合、 `default_lang` に指定した言語のメッセージが使われます "
    )
    default_lang: StrictStr = Field(description="希望された言語のメッセージが存在しない場合に、フォールバック先として使われる言語コード")
    __properties: ClassVar[List[str]] = ["messages", "default_lang"]

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
        """Create an instance of InternationalizationMessage from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in messages (list)
        _items = []
        if self.messages:
            for _item_messages in self.messages:
                if _item_messages:
                    _items.append(_item_messages.to_dict())
            _dict["messages"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of InternationalizationMessage from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "messages": [InternationalizationMessageMessagesInner.from_dict(_item) for _item in obj["messages"]]
                if obj.get("messages") is not None
                else None,
                "default_lang": obj.get("default_lang"),
            }
        )
        return _obj
