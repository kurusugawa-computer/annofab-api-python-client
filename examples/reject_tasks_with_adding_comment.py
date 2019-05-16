"""
検査コメントを付与してタスクを差し戻します。
"""

import argparse
import logging
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union

import requests

import annofabapi
import annofabapi.utils
from example_utils import ExamplesWrapper, read_lines

logging_formatter = '%(levelname)s : %(asctime)s : %(name)s : %(funcName)s : %(message)s'
logging.basicConfig(format=logging_formatter)
logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


def add_inspection_comment(project_id: str, task: Dict[str, Any],
                           inspection_comment: str, commenter_account_id: str):
    """
    先頭画像の左上に検査コメントを付与する
    Args:
        project_id:
        task:
        inspection_comment:
        commenter_account_id:

    Returns:
        更新した検査コメントの一覧

    """
    first_input_data_id = task["input_data_id_list"][0]
    req_inspection = [{
        "data": {
            "project_id": project_id,
            "comment": inspection_comment,
            "task_id": task["task_id"],
            "input_data_id": first_input_data_id,
            "inspection_id": str(uuid.uuid4()),
            "phase": task["phase"],
            "commenter_account_id": commenter_account_id,
            "data": {
                "x": 0,
                "y": 0,
                "_type": "Point"
            },
            "status": "annotator_action_required",
            "created_datetime": annofabapi.utils.str_now()
        },
        "_type": "Put",
    }]

    return service.api.batch_update_inspections(project_id,
                                                task["task_id"],
                                                first_input_data_id,
                                                request_body=req_inspection)[0]


def reject_tasks_with_adding_comment(project_id: str, task_id_list: List[str],
                                     inspection_comment: str,
                                     commenter_user_id: str):
    """
    検査コメントを付与して、タスクを差し戻す
    Args:
        project_id:
        task_id_list:
        inspection_comment: 検査コメントの中身
        commenter_user_id: 検査コメントを付与して、タスクを差し戻すユーザのuser_id
    """

    commenter_account_id = examples_wrapper.get_account_id_from_user_id(
        project_id, commenter_user_id)

    for task_id in task_id_list:
        task, _ = service.api.get_task(project_id, task_id)
        logger.debug(f"task_id = {task_id}, {task['status']}, {task['phase']}")
        if task["phase"] == "annotation":
            logger.warning(
                f"task_id = {task_id} はannofation phaseのため、差し戻しできません。")
            continue

        try:
            # 担当者を変更して、作業中にする
            examples_wrapper.change_operator_of_task(project_id, task_id,
                                                     commenter_account_id)
            logger.debug(f"task_id = {task_id}, {commenter_user_id}に担当者変更 完了")

            examples_wrapper.change_to_working_phase(project_id, task_id,
                                                     commenter_account_id)
            logger.debug(f"task_id = {task_id}, working statusに変更 完了")
        except requests.exceptions.HTTPError as e:
            logger.error(e)
            logger.info(f"task_id = {task_id} の担当者変更 or 作業phaseへの変更に失敗")
            continue

        # 少し待たないと検査コメントが登録できない場合があるため
        time.sleep(3)
        try:
            # 検査コメントを付与する
            add_inspection_comment(project_id, task, inspection_comment,
                                   commenter_account_id)
            logger.debug(f"task_id = {task_id}, 検査コメントの付与 完了")
        except requests.exceptions.HTTPError as e:
            logger.error(e)
            logger.info(f"task_id = {task_id} 検査コメントの付与に失敗")
            continue

        try:
            # タスクを差し戻す
            rejected_task = examples_wrapper.reject_task(
                project_id, task_id, commenter_account_id)

        except requests.exceptions.HTTPError as e:
            logger.error(e)
            logger.info(f"task_id = {task_id} タスクの差し戻しに失敗")
            continue

        logger.info(f"task_id = {task_id} の差し戻し完了")
    return


def main(args):
    task_id_list = read_lines(args.task_id_file)
    user_id = service.api.login_user_id
    reject_tasks_with_adding_comment(args.project_id, task_id_list,
                                     args.comment, user_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        "検査コメントを付与してタスクを差し戻します。検査コメントは先頭の画像の左上(0,0)に付与します。AnnoFab認証情報は`.netrc`に記載すること"
    )
    parser.add_argument('--project_id',
                        metavar='project_id',
                        type=str,
                        required=True,
                        help='対象のプロジェクトのproject_id')

    parser.add_argument(
        '--task_id_file',
        metavar='file',
        type=str,
        required=True,
        help='task_idの一覧が記載されたファイル。task_idは改行(LF or CRLF)で区切る。')

    parser.add_argument('--comment',
                        metavar='comment',
                        type=str,
                        required=True,
                        help='差し戻すときに付与する検査コメントの中身')

    args = parser.parse_args()

    logger.info(args)

    service = annofabapi.build_from_netrc()
    examples_wrapper = ExamplesWrapper(service)

    try:
        main(args)

    except Exception as e:
        logger.exception(e)
