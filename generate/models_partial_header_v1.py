# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace

"""
annofabapiのmodel(swagger.yamlの`components.schemes`)
enumならば列挙体として定義する。
それ以外は型ヒントしてして宣言する。

Notes:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照
"""

import warnings # pylint: disable=unused-import
from typing import Any, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import
from enum import Enum

