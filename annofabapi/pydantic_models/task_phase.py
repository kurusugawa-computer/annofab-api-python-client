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


class TaskPhase(str, Enum):
    """
    タスクのフェーズ * `annotation` - 教師付け * `inspection` - 検査 * `acceptance` - 受入
    """

    """
    allowed enum values
    """
    ANNOTATION = "annotation"
    INSPECTION = "inspection"
    ACCEPTANCE = "acceptance"

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of TaskPhase from a JSON string"""
        return cls(json.loads(json_str))
