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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing_extensions import Self

from annofabapi.pydantic_models.additional_data_definition_v2 import AdditionalDataDefinitionV2
from annofabapi.pydantic_models.additional_data_restriction import AdditionalDataRestriction
from annofabapi.pydantic_models.annotation_specs_option import AnnotationSpecsOption
from annofabapi.pydantic_models.inspection_phrase import InspectionPhrase
from annofabapi.pydantic_models.label_v2 import LabelV2


class AnnotationSpecsRequestV2(BaseModel):
    """
    AnnotationSpecsRequestV2
    """

    labels: List[LabelV2] = Field(description="ラベル")
    additionals: List[AdditionalDataDefinitionV2] = Field(description="属性")
    restrictions: List[AdditionalDataRestriction] = Field(description="属性の制約")
    inspection_phrases: List[InspectionPhrase] = Field(description="定型指摘")
    comment: Optional[StrictStr] = Field(default=None, description="変更内容のコメント")
    auto_marking: Optional[StrictBool] = Field(
        default=False,
        description='trueが指定された場合、各統計グラフにマーカーを自動追加します。 マーカーのタイトルには `comment` に指定された文字列が設定されます。 `comment` が指定されていなかった場合は "アノテーション仕様の変更" という文字列が設定されます。 ',
    )
    format_version: StrictStr = Field(description="アノテーション仕様のフォーマットのバージョン")
    last_updated_datetime: Optional[str] = Field(default=None, description="新規作成時は未指定、更新時は必須（更新前の日時） ")
    option: Optional[AnnotationSpecsOption] = None
    metadata: Optional[Dict[str, StrictStr]] = Field(default=None, description="ユーザーが自由に登録できるkey-value型のメタデータです。 ")
    __properties: ClassVar[List[str]] = [
        "labels",
        "additionals",
        "restrictions",
        "inspection_phrases",
        "comment",
        "auto_marking",
        "format_version",
        "last_updated_datetime",
        "option",
        "metadata",
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
        """Create an instance of AnnotationSpecsRequestV2 from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in labels (list)
        _items = []
        if self.labels:
            for _item_labels in self.labels:
                if _item_labels:
                    _items.append(_item_labels.to_dict())
            _dict["labels"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in additionals (list)
        _items = []
        if self.additionals:
            for _item_additionals in self.additionals:
                if _item_additionals:
                    _items.append(_item_additionals.to_dict())
            _dict["additionals"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in restrictions (list)
        _items = []
        if self.restrictions:
            for _item_restrictions in self.restrictions:
                if _item_restrictions:
                    _items.append(_item_restrictions.to_dict())
            _dict["restrictions"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in inspection_phrases (list)
        _items = []
        if self.inspection_phrases:
            for _item_inspection_phrases in self.inspection_phrases:
                if _item_inspection_phrases:
                    _items.append(_item_inspection_phrases.to_dict())
            _dict["inspection_phrases"] = _items
        # override the default output from pydantic by calling `to_dict()` of option
        if self.option:
            _dict["option"] = self.option.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AnnotationSpecsRequestV2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "labels": [LabelV2.from_dict(_item) for _item in obj["labels"]] if obj.get("labels") is not None else None,
                "additionals": [AdditionalDataDefinitionV2.from_dict(_item) for _item in obj["additionals"]]
                if obj.get("additionals") is not None
                else None,
                "restrictions": [AdditionalDataRestriction.from_dict(_item) for _item in obj["restrictions"]]
                if obj.get("restrictions") is not None
                else None,
                "inspection_phrases": [InspectionPhrase.from_dict(_item) for _item in obj["inspection_phrases"]]
                if obj.get("inspection_phrases") is not None
                else None,
                "comment": obj.get("comment"),
                "auto_marking": obj.get("auto_marking") if obj.get("auto_marking") is not None else False,
                "format_version": obj.get("format_version") if obj.get("format_version") is not None else "2.1.0",
                "last_updated_datetime": obj.get("last_updated_datetime"),
                "option": AnnotationSpecsOption.from_dict(obj["option"]) if obj.get("option") is not None else None,
                "metadata": obj.get("metadata"),
            }
        )
        return _obj
