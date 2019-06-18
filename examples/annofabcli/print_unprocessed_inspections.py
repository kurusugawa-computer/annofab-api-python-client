"""
タスクを一括で受け入れ完了にする
"""

import argparse
import json
import logging
import time
from typing import Any, Callable, Dict, List, Optional  # pylint: disable=unused-import

import requests

import annofabapi
import annofabcli
from annofabapi.typing import Inspection, Task
from annofabcli.common.utils import AnnofabApiFacade

logger = logging.getLogger(__name__)


class PrintUnprocessedInspections:
    """
    検査コメントIDのList(task_id, input_data_idごと)を出力する
    """

    def __init__(self, service: annofabapi.Resource, facade: AnnofabApiFacade):
        self.service = service
        self.facade = facade

    def get_unprocessed_inspections(
            self,
            project_id: str,
            task_id: str,
            input_data_id: str,
            inspection_comment: Optional[str] = None,
            commenter_account_id: Optional[str] = None):
        """
        対象の検査コメント一覧を取得する

        Args:
            project_id:
            task_id:
            input_data_id:
            inspection_comment:
            commenter_account_id:

        Returns:
            対象の検査コメント一覧
        """

        def filter_inspection(arg_inspection: Inspection) -> bool:
            # 未処置コメントのみ、変更する
            if arg_inspection["status"] != "annotator_action_required":
                return False

            # 返信コメントを除く
            if arg_inspection["parent_inspection_id"] is not None:
                return False

            if commenter_account_id is not None:
                if arg_inspection[
                        "commenter_account_id"] != commenter_account_id:
                    return False

            if inspection_comment is not None:
                if arg_inspection["comment"] != inspection_comment:
                    return False

            return True

        inspectins, _ = self.service.api.get_inspections(
            project_id, task_id, input_data_id)
        return [i for i in inspectins if filter_inspection(i)]

    def print_unprocessed_inspections(self,
                                      project_id: str,
                                      task_id_list: List[str],
                                      inspection_comment: Optional[str] = None,
                                      commenter_user_id: Optional[str] = None):
        """
        未処置の検査コメントを出力する。

        Args:
            project_id: 対象のproject_id
            task_id_list: 受け入れ完了にするタスクのtask_idのList
            inspection_comment: 絞り込み条件となる、検査コメントの中身
            commenter_user_id: 絞り込み条件となる、検査コメントを付与したユーザのuser_id

        Returns:

        """

        commenter_account_id = self.facade.get_account_id_from_user_id(
            project_id,
            commenter_user_id) if (commenter_user_id is not None) else None

        task_dict = {}

        for task_id in task_id_list:
            task, _ = self.service.api.get_task(project_id, task_id)

            input_data_dict = {}
            for input_data_id in task["input_data_id_list"]:

                inspections = self.get_unprocessed_inspections(
                    project_id,
                    task_id,
                    input_data_id,
                    inspection_comment=inspection_comment,
                    commenter_account_id=commenter_account_id)

                input_data_dict[input_data_id] = inspections

            task_dict[task_id] = input_data_dict

        # 出力
        print(json.dumps(task_dict, indent=2))

    def main(self, args):

        annofabcli.utils.load_logging_config_from_args(args, __file__)
        logger.info(f"args: {args}")

        task_id_list = annofabcli.utils.read_lines(args.task_id_file)

        self.print_unprocessed_inspections(args.project_id, task_id_list,
                                           args.inspection_comment,
                                           args.commenter_user_id)


def parse_args(parser: argparse.ArgumentParser):
    parser.add_argument('--project_id',
                        type=str,
                        required=True,
                        help='対象のプロジェクトのproject_id')

    parser.add_argument('--task_id_file',
                        type=str,
                        required=True,
                        help='対象のタスクのtask_idの一覧が記載されたファイル')

    parser.add_argument('--inspection_comment',
                        type=str,
                        help='絞り込み条件となる、検査コメントの中身。指定しない場合は絞り込まない。')

    parser.add_argument(
        '--commenter_user_id',
        type=str,
        help='絞り込み条件となる、検査コメントを付与したユーザのuser_id。 指定しない場合は絞り込まない。')

    parser.set_defaults(subcommand_func=main)


def main(args):
    try:
        service = annofabapi.build_from_netrc()
        facade = AnnofabApiFacade(service)

        PrintUnprocessedInspections(service, facade).main(args)

    except Exception as e:
        logger.exception(e)
