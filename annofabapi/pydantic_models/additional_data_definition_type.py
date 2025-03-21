"""


No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

The version of the OpenAPI document: 1.0.0
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""

from __future__ import annotations

import json
from enum import Enum

from typing_extensions import Self


class AdditionalDataDefinitionType(str, Enum):
    """
    属性の種類 * `flag` - 真偽値 * `integer` - 整数値 * `text` - 自由記述（1行） * `comment` - 自由記述（複数行） * `choice` - 選択肢（ラジオボタン式） * `select` - 選択肢（ドロップダウン式） * `tracking` - トラッキングID * `link` - アノテーションリンク
    """

    """
    allowed enum values
    """
    FLAG = "flag"
    INTEGER = "integer"
    TEXT = "text"
    COMMENT = "comment"
    CHOICE = "choice"
    SELECT = "select"
    TRACKING = "tracking"
    LINK = "link"

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of AdditionalDataDefinitionType from a JSON string"""
        return cls(json.loads(json_str))
