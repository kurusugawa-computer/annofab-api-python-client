"""
プロジェクト間のプロジェクトメンバの差分を表示する
"""

import argparse
import logging
import pprint
from typing import Any, Dict, List  # pylint: disable=unused-import

import dictdiffer

import annofabcli
import annofabapi
from annofabcli.common.utils import AnnofabApiFacade

logger = logging.getLogger(__name__)


def sorted_project_members(project_members: List[Dict[str, Any]]):
    return sorted(project_members, key=lambda e: e["user_id"])


def diff_project_members(project_id1: str, project_id2: str):
    """
    プロジェクト間のプロジェクトメンバの差分を表示する。
    Args:
        project_id1: 比較対象のプロジェクトのproject_id
        project_id2: 比較対象のプロジェクトのproject_id

    """

    project_members1 = service.wrapper.get_all_project_members(project_id1)
    project_members2 = service.wrapper.get_all_project_members(project_id2)

    # プロジェクトメンバは順番に意味がないので、ソートしたリストを比較する
    sorted_members1 = sorted_project_members(project_members1)
    sorted_members2 = sorted_project_members(project_members2)

    user_ids1 = [e["user_id"] for e in sorted_members1]
    user_ids2 = [e["user_id"] for e in sorted_members2]

    if user_ids1 != user_ids2:
        print("user_idのListに差分あり")
        print(
            f"set(user_ids1) - set(user_ids2) = {set(user_ids1) - set(user_ids2)}"
        )
        print(
            f"set(user_ids2) - set(user_ids1) = {set(user_ids2) - set(user_ids1)}"
        )
        return True

    is_different = False
    for member1, member2 in zip(sorted_members1,
                                sorted_members2):
        ignored_key = {"updated_datetime", "created_datetime", "project_id"}
        diff_result = list(dictdiffer.diff(member1, member2, ignore=ignored_key))
        if len(diff_result) > 0:
            is_different = True
            print(f"差分のあるuser_id: {member1['user_id']}")
            pprint.pprint(diff_result)

    if not is_different:
        print("プロジェクトメンバは同一")

    return is_different


def validate_args(args):
    return True


def main(args):
    annofabcli.utils.load_logging_config_from_args(args, __file__)

    logger.info(f"args: {args}")

    if not validate_args(args):
        return

    diff_project_members(args.project_id1, args.project_id2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="プロジェクト間のプロジェクトメンバの差分を表示する。"
                                                 "AnnoFab認証情報は`.netrc`に記載すること")

    parser.add_argument('project_id1', type=str, help='比較対象のプロジェクトのproject_id')

    parser.add_argument('project_id2', type=str, help='比較対象のプロジェクトのproject_id')

    annofabcli.utils.add_common_arguments_to_parser(parser)

    service = annofabapi.build_from_netrc()
    examples_wrapper = AnnofabApiFacade(service)

    try:
        main(parser.parse_args())

    except Exception as e:
        logger.exception(e)
