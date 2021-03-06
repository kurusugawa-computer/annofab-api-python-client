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

from dataclasses_json import DataClassJsonMixin

from annofabapi.models import OrganizationMemberRole, OrganizationMemberStatus


@dataclass
class OrganizationMember(DataClassJsonMixin):
    """ """

    organization_id: str
    """組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    account_id: str
    """"""

    user_id: str
    """"""

    username: str
    """"""

    role: OrganizationMemberRole
    """"""

    status: OrganizationMemberStatus
    """"""

    biography: Optional[str]
    """人物紹介、略歴。  この属性は、AnnoFab外の所属先や肩書などを表すために用います。 AnnoFab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 """

    created_datetime: Optional[str]
    """"""

    updated_datetime: Optional[str]
    """"""
