# ruff: noqa: E501
from annofabapi.models import (
    AdditionalDataDefinitionType,
    AnnotationDataHoldingType,
    InternationalizationMessage,
    TaskPhase,
    TaskStatus,
)

AnnotationDataV1 = Union[str, dict[str, Any]]
FullAnnotationData = Any
AdditionalDataValue = dict[str, Any]
FullAnnotationAdditionalDataValue = dict[str, Any]
AnnotationDetailV2Input = dict[str, Any]
AnnotationDetailContentOutput = dict[str, Any]

AnnotationType = str


AnnotationDetailContentInput = dict[str, Any]
AnnotationDetailV2Output  = dict[str, Any]