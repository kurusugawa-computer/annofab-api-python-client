from annofabapi.models import (
    AnnotationDataHoldingType,
    InternationalizationMessage,
    AdditionalDataDefinitionType,
    AnnotationType,
    TaskPhase,
    TaskStatus,
)

AnnotationData = Union[str, Dict[str, Any]]
FullAnnotationData = Dict[str, Any]
AdditionalDataValue = Dict[str, Any]
