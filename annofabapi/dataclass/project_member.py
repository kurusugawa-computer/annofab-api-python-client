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
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

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

    biography: Optional[str]
    """人物紹介、略歴。  この属性は、AnnoFab外の所属先や肩書などを表すために用います。 AnnoFab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 """

    updated_datetime: Optional[str]
    """"""

    created_datetime: Optional[str]
    """"""

    sampling_inspection_rate: Optional[int]
    """メンバー固有の抜取検査率（0-100のパーセント値）。"""

    sampling_acceptance_rate: Optional[int]
    """メンバー固有の抜取受入率（0-100のパーセント値）。"""
