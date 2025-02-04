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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing_extensions import Annotated, Self

from annofabapi.pydantic_models.task_history_short import TaskHistoryShort
from annofabapi.pydantic_models.task_phase import TaskPhase
from annofabapi.pydantic_models.task_status import TaskStatus


class Task(BaseModel):
    """
    Task
    """

    project_id: StrictStr = Field(description="プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    task_id: StrictStr = Field(description="タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    phase: TaskPhase
    phase_stage: Annotated[int, Field(strict=True, ge=1)] = Field(description="タスクのフェーズのステージ番号")
    status: TaskStatus
    input_data_id_list: List[StrictStr] = Field(description="タスクに含まれる入力データのID")
    account_id: Optional[StrictStr] = Field(default=None, description="アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    histories_by_phase: List[TaskHistoryShort] = Field(description="簡易的なタスク履歴（あるフェーズを誰が担当したか）")
    work_time_span: StrictInt = Field(description="累計実作業時間(ミリ秒)")
    number_of_rejections: StrictInt = Field(
        description="このタスクが差戻しされた回数（すべてのフェーズでの差戻し回数の合計  このフィールドは、どのフェーズで何回差戻されたかを区別できないため、廃止予定です。 `histories_by_phase` で各フェーズの回数を計算することで、差戻し回数が分かります。  例）`acceptance`フェーズが3回ある場合、`acceptance`フェーズで2回差し戻しされたことになります。 "
    )
    started_datetime: Optional[str] = Field(default=None, description="現在のフェーズが開始された日時")
    updated_datetime: str = Field(description="更新日時")
    operation_updated_datetime: Optional[str] = Field(default=None, description="タスクのステータスやフェーズ、担当者などが更新されたときの日時")
    sampling: Optional[StrictStr] = Field(
        default=None,
        description="検査抜取検査/抜取受入によって、どのフェーズがスキップされたか  * `inspection_skipped` - 抜取検査の対象外となり、検査フェーズがスキップされた * `inspection_stages_skipped` - 抜取検査の対象外となり、検査フェーズのステージの一部がスキップされた * `acceptance_skipped` - 抜取受入の対象外となり、受入フェーズがスキップされた * `inspection_and_acceptance_skipped` - 抜取検査・抜取受入の対象外となり、検査・受入フェーズがスキップされた  未指定ならば、どのフェーズもスキップされていません。 ",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="ユーザーが自由に登録できるkey-value型のメタデータです。 keyにはメタデータ名、valueには値を指定してください。  keyに指定できる文字種は次の通りです。  * 半角英数字 * `_` (アンダースコア) * `-` (ハイフン)  valueに指定できる値は次の通りです。  * 文字列 * 数値 * 真偽値 ",
    )
    __properties: ClassVar[List[str]] = [
        "project_id",
        "task_id",
        "phase",
        "phase_stage",
        "status",
        "input_data_id_list",
        "account_id",
        "histories_by_phase",
        "work_time_span",
        "number_of_rejections",
        "started_datetime",
        "updated_datetime",
        "operation_updated_datetime",
        "sampling",
        "metadata",
    ]

    @field_validator("sampling")
    def sampling_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(["inspection_skipped", "inspection_stages_skipped", "acceptance_skipped", "inspection_and_acceptance_skipped"]):
            raise ValueError(
                "must be one of enum values ('inspection_skipped', 'inspection_stages_skipped', 'acceptance_skipped', 'inspection_and_acceptance_skipped')"
            )
        return value

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
        """Create an instance of Task from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in histories_by_phase (list)
        _items = []
        if self.histories_by_phase:
            for _item_histories_by_phase in self.histories_by_phase:
                if _item_histories_by_phase:
                    _items.append(_item_histories_by_phase.to_dict())
            _dict["histories_by_phase"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Task from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "project_id": obj.get("project_id"),
                "task_id": obj.get("task_id"),
                "phase": obj.get("phase"),
                "phase_stage": obj.get("phase_stage"),
                "status": obj.get("status"),
                "input_data_id_list": obj.get("input_data_id_list"),
                "account_id": obj.get("account_id"),
                "histories_by_phase": [TaskHistoryShort.from_dict(_item) for _item in obj["histories_by_phase"]]
                if obj.get("histories_by_phase") is not None
                else None,
                "work_time_span": obj.get("work_time_span"),
                "number_of_rejections": obj.get("number_of_rejections"),
                "started_datetime": obj.get("started_datetime"),
                "updated_datetime": obj.get("updated_datetime"),
                "operation_updated_datetime": obj.get("operation_updated_datetime"),
                "sampling": obj.get("sampling"),
                "metadata": obj.get("metadata"),
            }
        )
        return _obj
