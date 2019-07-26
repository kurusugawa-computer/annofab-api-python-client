# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace

"""
annofabapiのmodel(swagger.yamlの ``components.schemes`` )
enumならば列挙体として定義する。
それ以外は型ヒントしてして宣言する。

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照
"""

import warnings  # pylint: disable=unused-import
from typing import Any, Dict, List, Optional, Tuple, Union, NewType  # pylint: disable=unused-import
from enum import Enum

AccountId = NewType('AccountId', str)

UserId = NewType('UserId', str)

OrganizationId = NewType('OrganizationId', str)

ProjectId = NewType('ProjectId', str)

LabelId = NewType('LabelId', str)

AdditionalDataDefinitionId = NewType('AdditionalDataDefinitionId', str)

ChoiceId = NewType('ChoiceId', str)

PhraseId = NewType('PhraseId', str)

TaskId = NewType('TaskId', str)

InputDataId = NewType('InputDataId', str)

SupplementaryDataId = NewType('SupplementaryDataId', str)

TaskHistoryId = NewType('TaskHistoryId', str)

AnnotationId = NewType('AnnotationId', str)

InspectionId = NewType('InspectionId', str)

JobId = NewType('JobId', str)

WebhookId = NewType('WebhookId', str)

Duration = NewType('Duration', str)

