# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace
"""
annofabapiのmodelをDataClassで定義したクラス

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照.
    oneOf, allOfなどは正しく表現できない可能性がある。
"""

import warnings  # pylint: disable=unused-import
from dataclasses import dataclass
from typing import Any, Dict, List, NewType, Optional, Tuple, Union  # pylint: disable=unused-import

from dataclasses_json import dataclass_json

from annofabapi.models import ProjectMemberRole, ProjectMemberStatus


@dataclass_json
@dataclass
class ProjectMember:
    """
    
    """
    project_id: str
    """"""

    account_id: str
    """"""

    user_id: str
    """"""

    username: str
    """"""

    member_status: ProjectMemberStatus
    """"""

    member_role: ProjectMemberRole
    """"""

    updated_datetime: Optional[str]
    """"""

    created_datetime: Optional[str]
    """"""

    sampling_inspection_rate: Optional[int]
    """メンバー固有の抜取検査率。0-100のパーセント値で指定する。値が指定された場合、プロジェクトの抜取検査率を指定の値で上書きする。"""
