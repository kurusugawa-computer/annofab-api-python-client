# ruff: noqa: E501
# pylint: disable=too-many-lines,trailing-whitespace

"""
annofabapiのmodelをDataClassで定義したクラス

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照.
    oneOf, allOfなどは正しく表現できない可能性がある。
"""

from dataclasses import dataclass
from typing import Optional  # pylint: disable=unused-import

from dataclasses_json import DataClassJsonMixin

from annofabapi.models import ProjectMemberRole, ProjectMemberStatus


@dataclass
class ProjectMember(DataClassJsonMixin):
    """ """

    project_id: str
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    account_id: str
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    user_id: str
    """ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    username: str
    """ユーザー名"""

    member_status: ProjectMemberStatus
    """"""

    member_role: ProjectMemberRole
    """"""

    biography: Optional[str]
    """人物紹介、略歴。  この属性は、Annofab外の所属先や肩書などを表すために用います。 Annofab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 """

    updated_datetime: str
    """更新日時"""

    created_datetime: str
    """作成日時"""

    sampling_inspection_rate: Optional[int]
    """抜取検査率（パーセント）"""

    sampling_acceptance_rate: Optional[int]
    """抜取受入率（パーセント）"""
