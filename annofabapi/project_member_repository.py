from collections.abc import Callable

import more_itertools

from annofabapi import Resource
from annofabapi.models import ProjectMember


class ProjectMemberRepository:
    def __init__(self, resource: Resource) -> None:
        self.resource = resource
        self._members_by_project_id: dict[str, list[ProjectMember]] = {}

    def _get_project_member_with_predicate(self, project_id: str, predicate: Callable[[ProjectMember], bool]) -> ProjectMember | None:
        """
        project_memberを取得する

        Args:
            project_id:
            predicate: 組織メンバの検索条件

        Returns:
            プロジェクトメンバ
        """
        project_member_list = self._members_by_project_id.get(project_id)
        if project_member_list is None:
            project_member_list = self.resource.wrapper.get_all_project_members(project_id, query_params={"include_inactive_member": True})
            self._members_by_project_id[project_id] = project_member_list
        return more_itertools.first_true(project_member_list, pred=predicate)

    def get_project_member_from_account_id(self, project_id: str, account_id: str) -> ProjectMember | None:
        """
        account_idからプロジェクトメンバを取得する。

        Args:
            project_id:
            account_id:

        Returns:
            プロジェクトメンバ。見つからない場合はNone
        """
        return self._get_project_member_with_predicate(project_id, predicate=lambda e: e["account_id"] == account_id)

    def get_project_member_from_user_id(self, project_id: str, user_id: str) -> ProjectMember | None:
        """
        user_idからプロジェクトメンバを取得する。

        Args:
            project_id:
            user_id:

        Returns:
            プロジェクトメンバ。見つからない場合はNone
        """
        return self._get_project_member_with_predicate(project_id, predicate=lambda e: e["user_id"] == user_id)

    def get_user_id_from_account_id(self, project_id: str, account_id: str) -> str:
        """
        account_idからuser_idを取得する.
        インスタンス変数に組織メンバがあれば、WebAPIは実行しない。

        Args:
            project_id:
            account_id:

        Returns:
            user_id

        Raises:
            ValueError: 指定したaccount_idのプロジェクトメンバが見つからなかった場合
        """
        member = self.get_project_member_from_account_id(project_id, account_id)
        if member is None:
            raise ValueError(f"project_member is not found. project_id='{project_id}', account_id='{account_id}'")
        return member["user_id"]

    def get_account_id_from_user_id(self, project_id: str, user_id: str) -> str | None:
        """
        user_idからaccount_idを取得する。
        インスタンス変数に組織メンバがあれば、WebAPIは実行しない。

        Args:
            project_id:
            user_id:

        Returns:
            account_id. 見つからなければNone

        """
        member = self.get_project_member_from_user_id(project_id, user_id)
        if member is None:
            return None
        return member["account_id"]
