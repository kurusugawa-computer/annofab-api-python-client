"""
複数のプロジェクトに、ユーザを招待する。
"""

import argparse
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import

import requests

import annofabapi
import annofabcli
from annofabcli.common.utils import AnnofabApiFacade

logger = logging.getLogger(__name__)


class InviteUser:
    """
    ユーザをプロジェクトに招待する
    """

    def __init__(self, service: annofabapi.Resource, facade: AnnofabApiFacade):
        self.service = service
        self.facade = facade

    def assign_role_with_organization(self, organization_name: str,
                                      user_id_list: List[str],
                                      member_role: str):

        # 進行中で自分自身が所属しているプロジェクトの一覧を取得する
        my_account_id = self.facade.get_my_account_id()
        projects = self.service.wrapper.get_all_projects_of_organization(
            organization_name, query_params={"status":"active", "account_id": my_account_id})

        for project in projects:
            project_id = project["project_id"]
            project_title = project["title"]

            try:
                if not self.facade.my_role_is_owner(project_id):
                    logger.warning(f"オーナではないため、プロジェクトメンバを招待できません。"
                                   f"project_id = {project_id}, project_tilte = {project_title}")
                    continue

                self.service.wrapper.assign_role_to_project_members(
                    project_id, user_id_list, member_role)
                logger.info(f"{project_title}に招待成功. project_id = {project_id}")

            except requests.exceptions.HTTPError as e:
                logger.warning(e)
                logger.warning(f"エラーのため、{project_title} に招待できなかった。")

    def assign_role_with_project_id(self, project_id_list: List[str],
                                    user_id_list: List[str], member_role: str):
        for project_id in project_id_list:

            try:
                if not self.facade.my_role_is_owner(project_id):
                    logger.warning(f"オーナではないため、プロジェクトメンバを招待できません。"
                                   f"project_id = {project_id}")
                    continue

                project_title = self.service.api.get_project(
                    project_id)[0]["title"]
                self.service.wrapper.assign_role_to_project_members(
                    project_id, user_id_list, member_role)
                logger.info(f"{project_title}に招待成功. project_id={project_id}")

            except requests.exceptions.HTTPError as e:
                logger.warning(e)
                logger.warning(f"エラーのため、招待できなかった。project_id={project_id}")

    def main(self, args):
        annofabcli.utils.load_logging_config_from_args(args, __file__)
        logger.info(args)

        if args.organization is not None:
            self.assign_role_with_organization(args.organization, args.user_id,
                                               args.role)

        elif args.project_id is not None:
            self.assign_role_with_project_id(args.project_id, args.user_id,
                                             args.role)

        else:
            logger.error(
                "引数に`--organization` or `--project_id_list`を指定してください。")


def main(args):
    try:
        service = annofabapi.build_from_netrc()
        facade = AnnofabApiFacade(service)

        InviteUser(service, facade).main(args)

    except Exception as e:
        logger.exception(e)


def parse_args(parser: argparse.ArgumentParser):
    parser.add_argument('--user_id',
                        type=str,
                        nargs='+',
                        required=True,
                        help='招待するユーザのuser_id')
    parser.add_argument(
        '--role',
        type=str,
        required=True,
        choices=['owner', 'worker', 'accepter', 'training_data_user'],
        help='ユーザに割り当てるロール')

    parser.add_argument('--organization',
                        type=str,
                        help='招待先の組織名.組織配下のプロジェクトに招待する。')
    parser.add_argument('--project_id',
                        type=str,
                        nargs='+',
                        help='組織名が指定されていない場合は、必要')

    parser.set_defaults(subcommand_func=main)

def add_parser(subparsers: argparse._SubParsersAction):
    subcommand_name = "invite_users"
    subcommand_help = "複数のプロジェクトに、ユーザを招待する。"
    description = ("複数のプロジェクトに、ユーザを招待する。"
                   "オーナ権限を持つユーザで実行すること。")

    parser = annofabcli.utils.add_parser(subparsers, subcommand_name, subcommand_help, description)
    parse_args(parser)
