"""
タスクを一括で受け入れ完了にする
"""

import argparse
import logging
from typing import Any, Callable, Dict, List, Optional  # pylint: disable=unused-import

import annofabapi
import annofabcli
from annofabapi.typing import Inspection, Task
from annofabcli.common.utils import AnnofabApiFacade

logger = logging.getLogger(__name__)


def complete_tasks_with_changing_inspection_status(
        project_id: str, task_id_list: List[str], inspection_status: str,
        filter_inspection: Callable[[Inspection], bool]):

    account_id = facade.get_my_account_id()

    for task_id in task_id_list:
        task, _ = service.api.get_task(project_id, task_id)
        if task["phase"] != "acceptance":
            logger.warning(f"task_id: {task_id}, phase: {task['phase']} ")
            continue

        try:
            complete_acceptance_task(project_id, task, inspection_status,
                                     filter_inspection, account_id)
        except Exception as e:
            logger.warning(e)
            logger.warning(f"{task_id} の受入完了に失敗")
            continue


def complete_acceptance_task(project_id: str, task: Task,
                             inspection_status: str,
                             filter_inspection: Callable[[Inspection], bool],
                             account_id: str):
    task_id = task["task_id"]

    facade.change_operator_of_task(project_id, task_id, account_id)
    facade.change_to_working_phase(project_id, task_id, account_id)
    logger.debug(f"{task_id}: 担当者を変更した")

    # 検査コメントの状態を変更する
    for input_data_id in task["input_data_id_list"]:
        service.wrapper.update_status_of_inspections(project_id, task_id,
                                                     input_data_id,
                                                     filter_inspection,
                                                     inspection_status)
        logger.debug(f"{task_id}, {input_data_id}, 検査コメントの状態を変更")

    facade.complete_task(project_id, task_id, account_id)
    logger.info(f"{task_id}: タスクを受入完了にした")


def main(args):
    def filter_inspection(arg_inspection: Inspection) -> bool:
        """
        statusを変更する検査コメントの条件。
        TODO スクリプトを使う人が修正する
        Args:
            arg_inspection: 検査コメント

        Returns:
            検査コメントが変更対象ならば、Trueを返す。

        """

        # 未処置コメントのみ、変更する
        if arg_inspection["status"] != "annotator_action_required":
            return False

        # TODO
        return True

    annofabcli.utils.load_logging_config_from_args(args, __file__)
    logger.info(f"args: {args}")

    task_id_list = annofabcli.utils.read_lines(args.task_id_file)

    complete_tasks_with_changing_inspection_status(args.project_id,
                                                   task_id_list,
                                                   args.inspection_status,
                                                   filter_inspection)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="deprecated: タスクを受け入れ完了にする。その際、検査コメントを適切な状態にする。"
        "注意：ユーザがスクリプトを修正すること。",
        parents=[annofabcli.utils.create_parent_parser()])

    parser.add_argument('--project_id',
                        type=str,
                        required=True,
                        help='対象のプロジェクトのproject_id')

    parser.add_argument('--task_id_file',
                        type=str,
                        required=True,
                        help='受入を完了するタスクのtask_idの一覧が記載されたファイル')

    parser.add_argument('--inspection_status',
                        type=str,
                        required=True,
                        choices=["error_corrected", "no_correction_required"],
                        help='未処置の検査コメントをどの状態に変更するか。' \
                             'error_corrected: 対応完了,' \
                             'no_correction_required: 対応不要')

    try:
        service = annofabapi.build_from_netrc()
        facade = AnnofabApiFacade(service)

        main(parser.parse_args())

    except Exception as e:
        logger.exception(e)
