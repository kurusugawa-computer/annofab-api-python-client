from collections.abc import Callable

import more_itertools

from annofabapi import Resource
from annofabapi.models import ProjectMember


class ProjectMemberRepository:
    """プロジェクトメンバ情報を取得するRepository。"""

    def __init__(self, resource: Resource) -> None:
        self.resource = resource
        self._members_by_project_id: dict[str, list[ProjectMember]] = {}

    def _get_project_member_with_predicate(self, project_id: str, predicate: Callable[[ProjectMember], bool]) -> ProjectMember | None:
        """条件に一致するプロジェクトメンバを取得する。

        プロジェクトメンバの一覧をプロジェクトIDごとにキャッシュする。

        Args:
            project_id: プロジェクトID
            predicate: プロジェクトメンバの検索条件

        Returns:
            条件に一致するプロジェクトメンバ。見つからない場合はNone。
        """
        project_member_list = self._members_by_project_id.get(project_id)
        if project_member_list is None:
            project_member_list = self.resource.wrapper.get_all_project_members(project_id, query_params={"include_inactive_member": True})
            self._members_by_project_id[project_id] = project_member_list
        return more_itertools.first_true(project_member_list, pred=predicate)

    def get_project_member_from_account_id(self, project_id: str, account_id: str) -> ProjectMember | None:
        """account_idからプロジェクトメンバを取得する。

        Args:
            project_id: プロジェクトID
            account_id: アカウントID

        Returns:
            指定したaccount_idのプロジェクトメンバ。見つからない場合はNone。
        """
        return self._get_project_member_with_predicate(project_id, predicate=lambda e: e["account_id"] == account_id)

    def get_project_member_from_user_id(self, project_id: str, user_id: str) -> ProjectMember | None:
        """user_idからプロジェクトメンバを取得する。

        Args:
            project_id: プロジェクトID
            user_id: ユーザーID

        Returns:
            指定したuser_idのプロジェクトメンバ。見つからない場合はNone。
        """
        return self._get_project_member_with_predicate(project_id, predicate=lambda e: e["user_id"] == user_id)

    def get_user_id_from_account_id(self, project_id: str, account_id: str) -> str:
        """account_idからuser_idを取得する。

        Args:
            project_id: プロジェクトID
            account_id: アカウントID

        Returns:
            指定したaccount_idに対応するユーザーID。

        Raises:
            ValueError: 指定したaccount_idのプロジェクトメンバが見つからない場合。
        """
        member = self.get_project_member_from_account_id(project_id, account_id)
        if member is None:
            raise ValueError(f"project_member is not found. project_id='{project_id}', account_id='{account_id}'")
        return member["user_id"]

    def get_account_id_from_user_id(self, project_id: str, user_id: str) -> str:
        """user_idからaccount_idを取得する。

        Args:
            project_id: プロジェクトID
            user_id: ユーザーID

        Returns:
            指定したuser_idに対応するアカウントID。

        Raises:
            ValueError: 指定したuser_idのプロジェクトメンバが見つからない場合。
        """
        member = self.get_project_member_from_user_id(project_id, user_id)
        if member is None:
            raise ValueError(f"project_member is not found. project_id='{project_id}', user_id='{user_id}'")
        return member["account_id"]
