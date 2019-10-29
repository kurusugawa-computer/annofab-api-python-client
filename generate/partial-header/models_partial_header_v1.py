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


### 手動の部分

AccountId = NewType('AccountId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``
    
"""

UserId = NewType('UserId', str)
"""

Example:
    ``john_doe``

"""

OrganizationId = NewType('OrganizationId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

ProjectId = NewType('ProjectId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

LabelId = NewType('LabelId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

AdditionalDataDefinitionId = NewType('AdditionalDataDefinitionId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

ChoiceId = NewType('ChoiceId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

PhraseId = NewType('PhraseId', str)
"""

Example:
    ``my_phrase_id``

"""

TaskId = NewType('TaskId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

InputDataId = NewType('InputDataId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

SupplementaryDataId = NewType('SupplementaryDataId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

TaskHistoryId = NewType('TaskHistoryId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

AnnotationId = NewType('AnnotationId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

InspectionId = NewType('InspectionId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

MakerId = NewType('MakerId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

JobId = NewType('JobId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

WebhookId = NewType('WebhookId', str)
"""

Example:
    ``12345678-abcd-1234-abcd-1234abcd5678``

"""

Duration = NewType('Duration', str)
"""

Example:
    ``PT34H17M36.789S``

"""

### 以下は自動生成の部分
