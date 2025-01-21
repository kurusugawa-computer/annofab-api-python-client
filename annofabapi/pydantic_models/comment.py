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
from typing import Annotated, Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing_extensions import Self

from annofabapi.pydantic_models.comment_node import CommentNode
from annofabapi.pydantic_models.comment_type import CommentType
from annofabapi.pydantic_models.task_phase import TaskPhase


class Comment(BaseModel):
    """
    コメント
    """

    project_id: StrictStr = Field(description="プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    task_id: StrictStr = Field(description="タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    input_data_id: StrictStr = Field(description="入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    comment_id: StrictStr = Field(description="コメントのID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    phase: TaskPhase
    phase_stage: Annotated[int, Field(strict=True, ge=1)] = Field(description="コメントを作成したときのフェーズのステージ。")
    account_id: StrictStr = Field(description="アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    comment_type: CommentType
    phrases: Optional[List[StrictStr]] = Field(
        default=None,
        description="`comment_type` の値によって扱いが異なります。  * `onhold` の場合   * 使用しません（空配列） * `inspection` の場合   * 参照している定型指摘のIDリスト ",
    )
    comment: StrictStr = Field(description="コメント本文。 ")
    comment_node: CommentNode
    datetime_for_sorting: str = Field(
        description="コメントのソート順を決める日時。  Annofab標準エディタでは、コメントはここで指定した日時にしたがってスレッドごとに昇順で表示されます。 "
    )
    created_datetime: str = Field(description="コメントの作成日時。")
    updated_datetime: str = Field(description="コメントの更新日時。")
    __properties: ClassVar[List[str]] = [
        "project_id",
        "task_id",
        "input_data_id",
        "comment_id",
        "phase",
        "phase_stage",
        "account_id",
        "comment_type",
        "phrases",
        "comment",
        "comment_node",
        "datetime_for_sorting",
        "created_datetime",
        "updated_datetime",
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
        """Create an instance of Comment from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of comment_node
        if self.comment_node:
            _dict["comment_node"] = self.comment_node.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Comment from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "project_id": obj.get("project_id"),
                "task_id": obj.get("task_id"),
                "input_data_id": obj.get("input_data_id"),
                "comment_id": obj.get("comment_id"),
                "phase": obj.get("phase"),
                "phase_stage": obj.get("phase_stage") if obj.get("phase_stage") is not None else 1,
                "account_id": obj.get("account_id"),
                "comment_type": obj.get("comment_type"),
                "phrases": obj.get("phrases"),
                "comment": obj.get("comment"),
                "comment_node": CommentNode.from_dict(obj["comment_node"]) if obj.get("comment_node") is not None else None,
                "datetime_for_sorting": obj.get("datetime_for_sorting"),
                "created_datetime": obj.get("created_datetime"),
                "updated_datetime": obj.get("updated_datetime"),
            }
        )
        return _obj
