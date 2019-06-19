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

TaskId = str
InputDataId = str
InspectionJson = Dict[TaskId, Dict[InputDataId, List[Inspection]]]


class ComleteTasks:
    """
    タスクを受け入れ完了にする
    """

    def __init__(self, service: annofabapi.Resource, facade: AnnofabApiFacade):
        self.service = service
        self.facade = facade

    def complete_tasks_with_changing_inspection_status(
            self, project_id: str, task_id_list: List[str],
            inspection_status: str, inspection_json: InspectionJson):
        """
        検査コメントのstatusを変更（対応完了 or 対応不要）にした上で、タスクを受け入れ完了状態にする
        Args:
            project_id: 対象のproject_id
            task_id_list: 受け入れ完了にするタスクのtask_idのList
            inspection_status: 変更後の検査コメントの状態
            inspection_json: 変更対象の検査コメントのJSON情報

        """

        account_id = self.facade.get_my_account_id()

        for task_id in task_id_list:
            task, _ = self.service.api.get_task(project_id, task_id)
            if task["phase"] != "acceptance":
                logger.warning(f"task_id: {task_id}, phase: {task['phase']} ")
                continue

            # 担当者変更
            try:
                self.facade.change_operator_of_task(project_id, task_id,
                                                    account_id)
                self.facade.change_to_working_phase(project_id, task_id,
                                                    account_id)
                logger.debug(f"{task_id}: 担当者を変更した")

            except requests.HTTPError as e:
                logger.warning(e)
                logger.warning(f"{task_id} の担当者変更に失敗")

            # 担当者変更してから数秒待たないと、検査コメントの付与に失敗する(「検査コメントの作成日時が不正です」と言われる）
            time.sleep(3)

            # 検査コメントを付与して、タスクを受け入れ完了にする
            try:
                self.complete_acceptance_task(project_id, task,
                                              inspection_status,
                                              inspection_json, account_id)
            except requests.HTTPError as e:
                logger.warning(e)
                logger.warning(f"{task_id} の受入完了に失敗")

                self.facade.change_to_break_phase(project_id, task_id,
                                                  account_id)
                continue

    def update_status_of_inspections(self, project_id: str, task_id: str,
                                     input_data_id: str,
                                     inspection_json: InspectionJson,
                                     inspection_status: str):
        target_insepctions = inspection_json.get(task_id,
                                                 {}).get(input_data_id)

        if target_insepctions is None or len(target_insepctions) == 0:
            logger.warning(
                f"変更対象の検査コメントはなかった。task_id = {task_id}, input_data_id = {input_data_id}"
            )
            return

        target_inspection_id_list = [
            inspection["inspection_id"] for inspection in target_insepctions
        ]

        def filter_inspection(arg_inspection: Inspection) -> bool:
            """
            statusを変更する検査コメントの条件。
            """

            return arg_inspection["inspection_id"] in target_inspection_id_list

        self.service.wrapper.update_status_of_inspections(
            project_id, task_id, input_data_id, filter_inspection,
            inspection_status)
        logger.debug(
            f"{task_id}, {input_data_id}, {len(target_insepctions)}件 検査コメントの状態を変更"
        )

    def complete_acceptance_task(self, project_id: str, task: Task,
                                 inspection_status: str,
                                 inspection_json: InspectionJson,
                                 account_id: str):
        """
        検査コメントのstatusを変更（対応完了 or 対応不要）にした上で、タスクを受け入れ完了状態にする
        """

        task_id = task["task_id"]

        # 検査コメントの状態を変更する
        for input_data_id in task["input_data_id_list"]:
            self.update_status_of_inspections(project_id, task_id,
                                              input_data_id, inspection_json,
                                              inspection_status)

        # タスクの状態を検査する
        if self.validate_task(project_id, task_id):
            self.facade.complete_task(project_id, task_id, account_id)
            logger.info(f"{task_id}: タスクを受入完了にした")
        else:
            logger.warning(f"{task_id}, タスク検査で警告/エラーがあったので、タスクを受入完了できなかった")
            self.facade.change_to_break_phase(project_id, task_id, account_id)

    def validate_task(self, project_id: str, task_id: str) -> bool:
        # Validation
        validation, _ = self.service.api.get_task_validation(
            project_id, task_id)
        validation_inputs = validation["inputs"]
        is_valid = True
        for validation in validation_inputs:
            input_data_id = validation["input_data_id"]
            inspection_summary = validation["inspection_summary"]
            if inspection_summary in [
                    "unprocessed", "new_unprocessed_inspection"
            ]:
                logger.warning(
                    f"{task_id}, {input_data_id}, {inspection_summary}, 未処置の検査コメントがある。"
                )
                is_valid = False

            annotation_summaries = validation["annotation_summaries"]
            if len(annotation_summaries) > 0:
                logger.warning(
                    f"{task_id}, {input_data_id}, {inspection_summary}, アノテーションにエラーがある。{annotation_summaries}"
                )
                is_valid = False

        return is_valid

    def main(self, args):
        annofabcli.utils.load_logging_config_from_args(args, __file__)
        logger.info(f"args: {args}")

        task_id_list = annofabcli.utils.read_lines(args.task_id_file)

        with open(args.inspection_json) as f:
            inspection_json = json.load(f)

        self.complete_tasks_with_changing_inspection_status(
            args.project_id, task_id_list, args.inspection_status,
            inspection_json)


def parse_args(parser: argparse.ArgumentParser):
    parser.add_argument('--project_id',
                        type=str,
                        required=True,
                        help='対象のプロジェクトのproject_id')

    parser.add_argument('--task_id_file',
                        type=str,
                        required=True,
                        help='受入を完了するタスクのtask_idの一覧が記載されたファイル')

    parser.add_argument(
        '--inspection_json',
        type=str,
        required=True,
        help='未処置の検査コメントの一覧。このファイルに記載された検査コメントの状態を変更する。'
        'jsonの構成は`Dict[TaskId, Dict[InputDatId, List[Inspection]]]。'
        '`print_unprocessed_inspections`ツールの出力結果である。')

    parser.add_argument('--inspection_status',
                        type=str,
                        required=True,
                        choices=["error_corrected", "no_correction_required"],
                        help='未処置の検査コメントをどの状態に変更するか。'
                        'error_corrected: 対応完了,'
                        'no_correction_required: 対応不要')

    parser.set_defaults(subcommand_func=main)


def main(args):
    try:
        service = annofabapi.build_from_netrc()
        facade = AnnofabApiFacade(service)

        ComleteTasks(service, facade).main(args)

    except Exception as e:
        logger.exception(e)

def add_parser(subparsers: argparse._SubParsersAction):
    subcommand_name = "complete_tasks"
    subcommand_help = "未処置の検査コメントを適切な状態に変更して、タスクを受け入れ完了にする。"
    description = ("未処置の検査コメントを適切な状態に変更して、タスクを受け入れ完了にする。"
                   "オーナ権限を持つユーザで実行すること。")

    annofabcli.utils.add_parser(subparsers, subcommand_name, subcommand_help, description)

