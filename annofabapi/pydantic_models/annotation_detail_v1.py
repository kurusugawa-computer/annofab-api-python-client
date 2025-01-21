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
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing_extensions import Self

from annofabapi.pydantic_models.additional_data_v1 import AdditionalDataV1
from annofabapi.pydantic_models.annotation_data_holding_type import AnnotationDataHoldingType
from annofabapi.pydantic_models.annotation_data_v1 import AnnotationDataV1


class AnnotationDetailV1(BaseModel):
    """
    AnnotationDetailV1
    """

    annotation_id: StrictStr = Field(
        description="アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)  `annotation_type`が`classification`の場合は label_id と同じ値が格納されます。 "
    )
    account_id: StrictStr = Field(description="アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    label_id: StrictStr = Field(description="ラベルID。[値の制約についてはこちら。](#section/API-Convention/APIID) ")
    is_protected: StrictBool = Field(
        description="`true`の場合、アノテーションをアノテーションエディタ上での削除から保護できます。 外部から取り込んだアノテーションに属性を追加するときなどに指定すると、データの削除を防げます。 "
    )
    data_holding_type: AnnotationDataHoldingType
    data: Optional[AnnotationDataV1] = None
    path: Optional[StrictStr] = Field(
        default=None,
        description="外部ファイルに保存されたアノテーションのパス。`data_holding_type`が`inner`の場合は未指定です。 レスポンスの場合は`annotation_id`と同じ値が格納されます。  [putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は、[createTempPath](#operation/createTempPath) APIで取得できる一時データ保存先パスを格納してください。 更新しない場合は、[getEditorAnnotation](#operation/getEditorAnnotation) APIで取得した`path`をそのまま渡せます。  外部ファイルのフォーマットは下表の通りです。  <table> <tr><th>annotation_type</th><th>形式</th></tr> <tr><td>segmentation / segmentation_v2   </td><td>PNG画像。塗りつぶした部分は<code>rgba(255, 255, 255, 1) </code>、塗りつぶしていない部分は<code>rgba(0, 0, 0, 0) </code>。</td></tr> </table> ",
    )
    etag: Optional[StrictStr] = Field(
        default=None,
        description="外部ファイルに保存されたアノテーションのETag。`data_holding_type`が`inner`の場合、または[putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は未指定です。",
    )
    url: Optional[StrictStr] = Field(
        default=None,
        description="外部ファイルに保存されたアノテーションの認証済み一時URL。`data_holding_type`が`inner`の場合、または[putAnnotation](#operation/putAnnotation) APIのリクエストボディに渡す場合は未指定です。",
    )
    additional_data_list: List[AdditionalDataV1] = Field(
        description="属性情報。  アノテーション属性の種類（`additional_data_definition`の`type`）によって、属性値を格納するプロパティは変わります。  | 属性の種類 | `additional_data_definition`の`type` | 属性値を格納するプロパティ                    | |------------|-------------------------|----------------------| | ON/OFF | flag       | flag                                          | | 整数 | integer    | integer                                       | | 自由記述（1行）| text       | comment                                       | | 自由記述（複数行）| comment    | comment                                       | | トラッキングID  | tracking | comment                                       | | アノテーションリンク    | link   | comment                                       | | 排他選択（ラジオボタン）  |choice   | choice                                        | | 排他選択（ドロップダウン） | select    | choice                                        | "
    )
    created_datetime: Optional[datetime] = Field(default=None, description="作成日時")
    updated_datetime: Optional[datetime] = Field(default=None, description="更新日時")
    __properties: ClassVar[List[str]] = [
        "annotation_id",
        "account_id",
        "label_id",
        "is_protected",
        "data_holding_type",
        "data",
        "path",
        "etag",
        "url",
        "additional_data_list",
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
        """Create an instance of AnnotationDetailV1 from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of data
        if self.data:
            _dict["data"] = self.data.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in additional_data_list (list)
        _items = []
        if self.additional_data_list:
            for _item_additional_data_list in self.additional_data_list:
                if _item_additional_data_list:
                    _items.append(_item_additional_data_list.to_dict())
            _dict["additional_data_list"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AnnotationDetailV1 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "annotation_id": obj.get("annotation_id"),
                "account_id": obj.get("account_id"),
                "label_id": obj.get("label_id"),
                "is_protected": obj.get("is_protected") if obj.get("is_protected") is not None else False,
                "data_holding_type": obj.get("data_holding_type"),
                "data": AnnotationDataV1.from_dict(obj["data"]) if obj.get("data") is not None else None,
                "path": obj.get("path"),
                "etag": obj.get("etag"),
                "url": obj.get("url"),
                "additional_data_list": [AdditionalDataV1.from_dict(_item) for _item in obj["additional_data_list"]]
                if obj.get("additional_data_list") is not None
                else None,
                "created_datetime": obj.get("created_datetime"),
                "updated_datetime": obj.get("updated_datetime"),
            }
        )
        return _obj
