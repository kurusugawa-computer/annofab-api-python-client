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


class KeyLayout(str, Enum):
    """
    キーボードレイアウト * `ja-JP` - 日本語(106/109)配列 * `en-US` - 英語(101/104)配列 * `other` - その他
    """

    """
    allowed enum values
    """
    JA_MINUS_JP = "ja-JP"
    EN_MINUS_US = "en-US"
    OTHER = "other"

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of KeyLayout from a JSON string"""
        return cls(json.loads(json_str))
