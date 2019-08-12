# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace

"""
annofabapiのmodelをDataClassで定義したクラス。(swagger.yamlの ``components.schemes`` )

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照.

    oneOf, allOfなどは正しく表現できない可能性がある。

"""

import warnings  # pylint: disable=unused-import
from typing import Any, Dict, List, Optional, Tuple, Union, NewType  # pylint: disable=unused-import
from dataclasses import dataclass
from dataclasses_json import dataclass_json

### 以下は自動生成の部分
