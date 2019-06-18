"""
受け入れ完了タスクを、受け入れ取り消しする。
"""

import argparse
import logging
from typing import List, Optional  # pylint: disable=unused-import

import requests

import annofabapi
import annofabcli
from annofabcli.common.utils import AnnofabApiFacade, read_lines

logger = logging.getLogger(__name__)


class CancelAcceptance:
    def __init__(self, service: annofabapi.Resource, facade: AnnofabApiFacade):
        self.service = service
        self.facade = facade

    def cancel_acceptance(self,
                          project_id: str,
                          task_id_list: List[str],
                          acceptor_user_id: Optional[str] = None):
        """
        タスクを受け入れ取り消しする

        Args:
            project_id:
            task_id_list: 受け入れ取り消しするtask_id_list
            acceptor_user_id: 再度受入を担当させたいユーザのuser_id
        """

        acceptor_account_id = self.facade.get_account_id_from_user_id(
            project_id,
            acceptor_user_id) if acceptor_user_id is not None else None

        for task_id in task_id_list:
            try:
                task, _ = self.service.api.get_task(project_id, task_id)
                if task["status"] != "complete":
                    logger.warning(
                        f"task_id = {task_id} は受入完了でありません。status = {task['status']}, phase={task['phase']}"
                    )
                request_body = {
                    "status": "not_started",
                    "account_id": acceptor_account_id,
                    "last_updated_datetime": task["updated_datetime"],
                }
                self.service.api.operate_task(project_id,
                                              task_id,
                                              request_body=request_body)
                logger.info(f"task_id = {task_id} の受け入れ取り消し完了")

            except requests.exceptions.HTTPError as e:
                logger.warning(e)
                logger.warning(f"task_id = {task_id} の受け入れ取り消し失敗")

    def main(self, args):
        annofabcli.utils.load_logging_config_from_args(args, __file__)

        logger.info(f"args: {args}")

        task_id_list = read_lines(args.task_id_file)
        self.cancel_acceptance(args.project_id, task_id_list, args.user_id)


def main(args):
    try:
        service = annofabapi.build_from_netrc()
        facade = AnnofabApiFacade(service)

        CancelAcceptance(service, facade).main(args)

    except Exception as e:
        logger.exception(e)


def parse_args(parser: argparse.ArgumentParser):

    parser.add_argument('--project_id',
                        type=str,
                        required=True,
                        help='対象のプロジェクトのproject_id')

    parser.add_argument(
        '--task_id_file',
        type=str,
        required=True,
        help='task_idの一覧が記載されたファイル。task_idは改行(LF or CRLF)で区切る。')

    parser.add_argument('--user_id',
                        type=str,
                        help='再度受入を担当させたいユーザのuser_id。指定しなければ未割り当てになる。')

    parser.set_defaults(subcommand_func=main)
