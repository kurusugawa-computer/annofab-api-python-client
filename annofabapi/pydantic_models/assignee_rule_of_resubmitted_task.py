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


class AssigneeRuleOfResubmittedTask(str, Enum):
    """
    再提出されたタスクの検査/受入担当者の割当方法 * `no_assignee` - 以前の担当者で固定せず、未割当てにします。 * `fixed` - 以前の担当者が再度担当します。以前の担当者がいない(1回目の検査/受入)場合は未割当てになります。
    """

    """
    allowed enum values
    """
    NO_ASSIGNEE = "no_assignee"
    FIXED = "fixed"

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of AssigneeRuleOfResubmittedTask from a JSON string"""
        return cls(json.loads(json_str))
