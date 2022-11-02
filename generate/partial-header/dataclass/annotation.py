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