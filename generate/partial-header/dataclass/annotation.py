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
AnnotationDetailV2Input = Union[AnnotationDetailV2Create, AnnotationDetailV2Import, AnnotationDetailV2Update]
AnnotationDetailContentOutput = Union[AnnotationDetailContentOutputInner, AnnotationDetailContentOutputInnerUnknown, AnnotationDetailContentOutputOuter, AnnotationDetailContentOutputOuterUnresolved]
