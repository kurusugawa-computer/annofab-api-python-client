"""
複数のプロジェクトに、ユーザを招待する。
"""

import argparse
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import

import requests

import annofabapi

import annofabcli

logger = logging.getLogger(__name__)


def assign_role_with_organization(organization_name: str,
                                  user_id_list: List[str], member_role: str):
    projects = service.wrapper.get_all_projects_of_organization(
        organization_name)

    for project in projects:
        project_id = project["project_id"]
        project_title = project["title"]

        try:
            service.wrapper.assign_role_to_project_members(
                project_id, user_id_list, member_role)
            logger.info(f"{project_title}に招待成功")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == requests.codes.not_found:
                logger.warning(f"プロジェクトオーナでないので、{project_title} に招待できなかった。")
            else:
                logger.warning(e)
                logger.warning(f"エラーのため、{project_title} に招待できなかった。")


def assign_role_with_project_id(project_id_list: List[str],
                                user_id_list: List[str], member_role: str):
    for project_id in project_id_list:
        try:
            project_title = service.api.get_project(project_id)[0]["title"]
            service.wrapper.assign_role_to_project_members(
                project_id, user_id_list, member_role)
            logger.info(f"{project_title}に招待成功. project_id={project_id}")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == requests.codes.not_found:
                logger.warning("プロジェクトオーナでないので、招待できなかった。project_id={project_id}")
            else:
                logger.warning(e)
                logger.warning("エラーのため、招待できなかった。project_id={project_id}")


def main(args):
    annofabcli.utils.load_logging_config(args, __file__)

    logger.info(args)

    if args.organization_name is not None:
        assign_role_with_organization(args.organization_name,
                                      args.user_id_list, args.member_role)

    elif args.project_id_list is not None:
        assign_role_with_project_id(args.project_id_list, args.user_id_list,
                                    args.member_role)

    else:
        logger.error("引数に`--organization` or `--project_id_list`を指定してください。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="複数のプロジェクトに、ユーザを招待する。",
        epilog="AnnoFab認証情報は`.netrc`に記載すること",
        parents=[annofabcli.utils.create_parent_parser()])
    parser.add_argument('--user_id',
                        metavar='user_id',
                        dest='user_id_list',
                        type=str,
                        nargs='+',
                        required=True,
                        help='招待するユーザのuser_id')
    parser.add_argument(
        '--role',
        metavar='role',
        dest='member_role',
        type=str,
        required=True,
        choices=['owner', 'worker', 'accepter', 'training_data_user'],
        help='ユーザに割り当てるロール')
    parser.add_argument('--organization',
                        metavar='organization',
                        dest='organization_name',
                        type=str,
                        nargs='?',
                        help='招待先の組織名.組織配下のプロジェクトに招待する。')
    parser.add_argument('--project_id',
                        metavar='project_id',
                        dest='project_id_list',
                        type=str,
                        nargs='*',
                        help='組織名が指定されていない場合は、必要')

    service = annofabapi.build_from_netrc()

    try:
        main(parser.parse_args())

    except Exception as e:
        logger.exception(e)
