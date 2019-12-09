# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace
"""
annofabapiのmodelをDataClassで定義したクラス

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照.
    oneOf, allOfなどは正しく表現できない可能性がある。
"""

import warnings  # pylint: disable=unused-import
from dataclasses import dataclass
from typing import Any, Dict, List, NewType, Optional, Tuple, Union  # pylint: disable=unused-import

from dataclasses_json import dataclass_json

from annofabapi.models import (AdditionalDataDefinitionType, AnnotationDataHoldingType, AnnotationType,
                               InternationalizationMessage, TaskPhase, TaskStatus)

OneOfstringFullAnnotationData = Dict[str, Any]
FullAnnotationData = Dict[str, Any]
AdditionalDataValue = Dict[str, Any]


@dataclass_json
@dataclass
class Point:
    """
    座標
    """
    x: int
    """"""

    y: int
    """"""


@dataclass_json
@dataclass
class AdditionalData:
    """
    
    """
    additional_data_definition_id: str
    """"""

    flag: Optional[bool]
    """"""

    integer: Optional[int]
    """"""

    comment: Optional[str]
    """"""

    choice: Optional[str]
    """"""


@dataclass_json
@dataclass
class FullAnnotationAdditionalData:
    """
    
    """
    additional_data_definition_id: Optional[str]
    """"""

    additional_data_definition_name: Optional[InternationalizationMessage]
    """"""

    type: Optional[AdditionalDataDefinitionType]
    """"""

    value: Optional[AdditionalDataValue]
    """"""


@dataclass_json
@dataclass
class FullAnnotationDetail:
    """
    
    """
    annotation_id: Optional[str]
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 """

    user_id: Optional[str]
    """"""

    label_id: Optional[str]
    """"""

    label_name: Optional[InternationalizationMessage]
    """"""

    annotation_type: Optional[AnnotationType]
    """"""

    data_holding_type: Optional[AnnotationDataHoldingType]
    """"""

    data: Optional[FullAnnotationData]
    """"""

    additional_data_list: Optional[List[FullAnnotationAdditionalData]]
    """"""


@dataclass_json
@dataclass
class FullAnnotationDetailOld:
    """
    for v1
    """
    annotation_id: Optional[str]
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 """

    user_id: Optional[str]
    """"""

    label_id: Optional[str]
    """"""

    label_name: Optional[InternationalizationMessage]
    """"""

    annotation_type: Optional[AnnotationType]
    """"""

    data_holding_type: Optional[AnnotationDataHoldingType]
    """"""

    data: Optional[FullAnnotationData]
    """"""

    additional_data_list: Optional[List[AdditionalData]]
    """"""


@dataclass_json
@dataclass
class FullAnnotation:
    """
    
    """
    project_id: Optional[str]
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: Optional[str]
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_phase: Optional[TaskPhase]
    """"""

    task_phase_stage: Optional[int]
    """"""

    task_status: Optional[TaskStatus]
    """"""

    input_data_id: Optional[str]
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_name: Optional[str]
    """"""

    details: Optional[List[FullAnnotationDetail]]
    """"""

    detail: Optional[List[FullAnnotationDetailOld]]
    """use details"""

    updated_datetime: Optional[str]
    """"""

    annotation_format_version: Optional[str]
    """アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、AnnoFabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 """


@dataclass_json
@dataclass
class SimpleAnnotationDetail:
    """
    
    """
    label: str
    """アノテーション仕様のラベル名です。 """

    annotation_id: str
    """個々のアノテーションにつけられたIDです。 """

    data: FullAnnotationData
    """"""

    attributes: Dict[str, Any]
    """キーに属性の名前、値に各属性の値が入った辞書構造です。 """


@dataclass_json
@dataclass
class SimpleAnnotation:
    """
    
    """
    annotation_format_version: str
    """アノテーションフォーマットのバージョンです。 アノテーションフォーマットとは、プロジェクト個別のアノテーション仕様ではなく、AnnoFabのアノテーション構造のことです。 したがって、アノテーション仕様を更新しても、このバージョンは変化しません。  バージョンの読み方と更新ルールは、業界慣習の[Semantic Versioning](https://semver.org/)にもとづきます。  JSONに出力されるアノテーションフォーマットのバージョンは、アノテーションZIPが作成される時点のものが使われます。 すなわち、`1.0.0`の時点のタスクで作成したアノテーションであっても、フォーマットが `1.0.1` に上がった次のZIP作成時では `1.0.1` となります。 バージョンを固定してZIPを残しておきたい場合は、プロジェクトが完了した時点でZIPをダウンロードして保管しておくか、またはプロジェクトを「停止中」にします。 """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_phase: TaskPhase
    """"""

    task_phase_stage: int
    """"""

    task_status: TaskStatus
    """"""

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_name: str
    """"""

    details: List[SimpleAnnotationDetail]
    """"""

    updated_datetime: str
    """"""


@dataclass_json
@dataclass
class SingleAnnotationDetail:
    """
    
    """
    annotation_id: str
    """アノテーションID。[値の制約についてはこちら。](#section/API-Convention/APIID)<br> annotation_type が classification の場合は label_id と同じ値が格納されます。 """

    account_id: str
    """"""

    label_id: str
    """"""

    data_holding_type: AnnotationDataHoldingType
    """"""

    data: Optional[FullAnnotationData]
    """"""

    etag: Optional[str]
    """data_holding_typeがouterの場合のみ存在し、データのETagが格納される"""

    url: Optional[str]
    """data_holding_typeがouterの場合のみ存在し、データへの一時URLが格納される"""

    additional_data_list: List[AdditionalData]
    """"""

    created_datetime: str
    """"""

    updated_datetime: str
    """"""


@dataclass_json
@dataclass
class SingleAnnotation:
    """
    
    """
    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    task_id: str
    """タスクID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    input_data_id: str
    """入力データID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    detail: SingleAnnotationDetail
    """"""

    updated_datetime: str
    """"""
