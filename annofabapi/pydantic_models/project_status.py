"""
swagger-api-components.yaml に記載されたschemaを出力するためのヘッダ部分

No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

The version of the OpenAPI document: 1.0.0
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""

from __future__ import annotations

import json
from enum import Enum

from typing_extensions import Self


class ProjectStatus(str, Enum):
    """
    プロジェクトの状態 * `active` - プロジェクトが進行中 * `suspended` - プロジェクトが停止中 * `initializing` - プロジェクトが初期化中
    """

    """
    allowed enum values
    """
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INITIALIZING = "initializing"

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ProjectStatus from a JSON string"""
        return cls(json.loads(json_str))
