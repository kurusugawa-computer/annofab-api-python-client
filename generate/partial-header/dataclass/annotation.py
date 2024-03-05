# ruff: noqa: E501
from annofabapi.models import (
    AdditionalDataDefinitionType,
    AnnotationDataHoldingType,
    InternationalizationMessage,
    TaskPhase,
    TaskStatus,
)

AnnotationDataV1 = Union[str, Dict[str, Any]]
FullAnnotationData = Any
AdditionalDataValue = Dict[str, Any]
FullAnnotationAdditionalDataValue = Dict[str, Any]
AnnotationDetailV2Input = Dict[str, Any]
AnnotationDetailContentOutput = Dict[str, Any]

AnnotationType = str


AnnotationDetailContentInput = Dict[str, Any]
AnnotationDetailV2Output  = Dict[str, Any]