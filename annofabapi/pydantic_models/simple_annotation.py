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
from typing_extensions import Annotated, Self

from annofabapi.pydantic_models.simple_annotation_detail import SimpleAnnotationDetail
from annofabapi.pydantic_models.task_phase import TaskPhase
from annofabapi.pydantic_models.task_status import TaskStatus


class SimpleAnnotation(BaseModel):
    """
    SimpleAnnotation
    """

    annotation_format_version: StrictStr = Field(
        description="アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、Annofabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 "
    )
    project_id: StrictStr = Field(description="プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    task_id: StrictStr = Field(description="タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    task_phase: TaskPhase
    task_phase_stage: Annotated[int, Field(strict=True, ge=1)] = Field(description="タスクのフェーズのステージ番号")
    task_status: TaskStatus
    input_data_id: StrictStr = Field(description="入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    input_data_name: StrictStr = Field(description="入力データ名")
    details: List[SimpleAnnotationDetail] = Field(description="矩形、ポリゴン、全体アノテーションなど個々のアノテーションの配列。")
    updated_datetime: Optional[str] = Field(
        default=None, description="更新日時。アノテーションが一つもない場合（教師付作業が未着手のときなど）は、未指定。"
    )
    __properties: ClassVar[List[str]] = [
        "annotation_format_version",
        "project_id",
        "task_id",
        "task_phase",
        "task_phase_stage",
        "task_status",
        "input_data_id",
        "input_data_name",
        "details",
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
        """Create an instance of SimpleAnnotation from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in details (list)
        _items = []
        if self.details:
            for _item_details in self.details:
                if _item_details:
                    _items.append(_item_details.to_dict())
            _dict["details"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SimpleAnnotation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "annotation_format_version": obj.get("annotation_format_version"),
                "project_id": obj.get("project_id"),
                "task_id": obj.get("task_id"),
                "task_phase": obj.get("task_phase"),
                "task_phase_stage": obj.get("task_phase_stage"),
                "task_status": obj.get("task_status"),
                "input_data_id": obj.get("input_data_id"),
                "input_data_name": obj.get("input_data_name"),
                "details": [SimpleAnnotationDetail.from_dict(_item) for _item in obj["details"]] if obj.get("details") is not None else None,
                "updated_datetime": obj.get("updated_datetime"),
            }
        )
        return _obj
