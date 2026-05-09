import pytest

from annofabapi.project_member_repository import ProjectMemberRepository

PROJECT_ID = "project_id"


def create_repository_with_members(members):
    repository = object.__new__(ProjectMemberRepository)
    repository._members_by_project_id = {PROJECT_ID: members}
    return repository


def test_get_user_id_from_account_id__存在するaccount_idならuser_idを返す():
    repository = create_repository_with_members(
        [
            {
                "project_id": PROJECT_ID,
                "account_id": "account_id",
                "user_id": "user_id",
            }
        ]
    )

    assert repository.get_user_id_from_account_id(PROJECT_ID, "account_id") == "user_id"


def test_get_user_id_from_account_id__存在しないaccount_idならValueErrorを送出する():
    repository = create_repository_with_members([])

    with pytest.raises(ValueError):
        repository.get_user_id_from_account_id(PROJECT_ID, "unknown_account_id")


def test_get_account_id_from_user_id__存在するuser_idならaccount_idを返す():
    repository = create_repository_with_members(
        [
            {
                "project_id": PROJECT_ID,
                "account_id": "account_id",
                "user_id": "user_id",
            }
        ]
    )

    assert repository.get_account_id_from_user_id(PROJECT_ID, "user_id") == "account_id"


def test_get_account_id_from_user_id__存在しないuser_idならValueErrorを送出する():
    repository = create_repository_with_members([])

    with pytest.raises(ValueError):
        repository.get_account_id_from_user_id(PROJECT_ID, "unknown_user_id")
