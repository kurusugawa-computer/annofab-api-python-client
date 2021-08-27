from annofabapi.models import (
    AdditionalDataDefinitionType,
    AnnotationDataHoldingType,
    AnnotationType,
    InternationalizationMessage,
    TaskPhase,
    TaskStatus,
)

AnnotationData = Union[str, Dict[str, Any]]
FullAnnotationData = Any
AdditionalDataValue = Dict[str, Any]
