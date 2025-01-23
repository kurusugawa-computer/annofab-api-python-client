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


class PricePlan(str, Enum):
    """
    料金プラン * `free` - フリープラン * `business` - ビジネスプラン
    """

    """
    allowed enum values
    """
    FREE = "free"
    BUSINESS = "business"

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of PricePlan from a JSON string"""
        return cls(json.loads(json_str))
