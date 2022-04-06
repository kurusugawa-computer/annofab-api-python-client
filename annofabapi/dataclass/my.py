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

from annofabapi.models import KeyLayout, Lang, OrganizationMemberRole, OrganizationMemberStatus, PricePlan


@dataclass
class MyOrganization(DataClassJsonMixin):
    """ """

    organization_id: Optional[str]
    """組織ID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    name: Optional[str]
    """"""

    email: Optional[str]
    """"""

    price_plan: Optional[PricePlan]
    """"""

    summary: Optional[Dict[str, Any]]
    """"""

    created_datetime: Optional[str]
    """"""

    updated_datetime: Optional[str]
    """"""

    my_role: Optional[OrganizationMemberRole]
    """"""

    my_status: Optional[OrganizationMemberStatus]
    """"""


@dataclass
class MyAccount(DataClassJsonMixin):
    """ """

    account_id: str
    """アカウントID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    user_id: str
    """ユーザーID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    username: str
    """ユーザー名"""

    email: str
    """メールアドレス"""

    lang: Lang
    """"""

    biography: Optional[str]
    """人物紹介、略歴。  この属性は、AnnoFab外の所属先や肩書などを表すために用います。 AnnoFab上の「複数の組織」で活動する場合、本籍を示すのに便利です。 """

    keylayout: KeyLayout
    """"""

    authority: str
    """システム内部用のプロパティ"""

    is_external_account: bool
    """[外部アカウントだけで作成したアカウント](/docs/faq/#v1u344)の場合はtrue。  外部アカウント連携していないAnnoFabアカウントや、後から[外部アカウントとの紐付け](/docs/faq/#yyyub0)をしたAnnoFabアカウントの場合はfalse。 """

    updated_datetime: str
    """更新日時"""

    reset_requested_email: Optional[str]
    """システム内部用のプロパティ"""

    errors: List[str]
    """システム内部用のプロパティ"""
