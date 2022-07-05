from annofabapi.models import (
    AdditionalDataDefinitionType,
    AnnotationDataHoldingType,
    InternationalizationMessage,
    TaskPhase,
    TaskStatus,
)

AnnotationData = Union[str, Dict[str, Any]]
FullAnnotationData = Any
AdditionalDataValue = Dict[str, Any]
