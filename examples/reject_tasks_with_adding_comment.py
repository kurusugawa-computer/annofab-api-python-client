"""
検査コメントを付与してタスクを差し戻します。
"""

import argparse
import logging
import time
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import

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


def reject_tasks_with_adding_comment(
        project_id: str,
        task_id_list: List[str],
        inspection_comment: str,
        commenter_user_id: str,
        assign_last_annotator: bool = False,
        assigned_annotator_user_id: Optional[str] = None):
    """
    検査コメントを付与して、タスクを差し戻す
    Args:
        project_id:
        task_id_list:
        inspection_comment: 検査コメントの中身
        commenter_user_id: 検査コメントを付与して、タスクを差し戻すユーザのuser_id
        assign_last_annotator: Trueなら差し戻したタスクに対して、最後のannotation phaseを担当者を割り当てる
        assigned_annotator_user_id: 差し戻したタスクに割り当てるユーザのuser_id. assign_last_annotatorがTrueの場合、この引数は無視される。

    """

    commenter_account_id = examples_wrapper.get_account_id_from_user_id(
        project_id, commenter_user_id)

    assigned_annotator_account_id = examples_wrapper.get_account_id_from_user_id(
        project_id, assigned_annotator_user_id
    ) if assigned_annotator_user_id is not None else None

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
            logger.debug(
                f"task_id = {task_id}, phase={task['phase']}, {commenter_user_id}に担当者変更 完了"
            )

            examples_wrapper.change_to_working_phase(project_id, task_id,
                                                     commenter_account_id)
            logger.debug(
                f"task_id = {task_id}, phase={task['phase']}, working statusに変更 完了"
            )
        except requests.exceptions.HTTPError as e:
            logger.error(e)
            logger.info(
                f"task_id = {task_id}, phase={task['phase']} の担当者変更 or 作業phaseへの変更に失敗"
            )
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
            if assign_last_annotator:
                # 最後のannotation phaseに担当を割り当てる
                examples_wrapper.reject_task_assign_last_annotator(
                    project_id, task_id, commenter_account_id)
            else:
                # 指定したユーザに担当を割り当てる
                examples_wrapper.reject_task(
                    project_id,
                    task_id,
                    account_id=commenter_account_id,
                    annotator_account_id=assigned_annotator_account_id)

        except requests.exceptions.HTTPError as e:
            logger.error(e)
            logger.info(f"task_id = {task_id} タスクの差し戻しに失敗")
            continue

        logger.info(f"task_id = {task_id} の差し戻し完了")


def validate_args(args):
    if args.assign_last_annotator and args.assigned_annotator_user_id is not None:
        logger.error(
            "引数に --assign_last_annotator と --assigned_annotator_user_id は同時に指定できません"
        )
        return False

    return True


def main(args):
    logger.debug(args)

    if not validate_args(args):
        return

    task_id_list = read_lines(args.task_id_file)
    user_id = service.api.login_user_id
    reject_tasks_with_adding_comment(
        args.project_id,
        task_id_list,
        args.comment,
        commenter_user_id=user_id,
        assign_last_annotator=args.assign_last_annotator,
        assigned_annotator_user_id=args.assigned_annotator_user_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="検査コメントを付与してタスクを差し戻す。検査コメントは先頭の画像の左上(0,0)に付与する。"
        "AnnoFab認証情報は`.netrc`に記載すること")
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
        help=
        '差し戻すタスク(inspection/acceptance phase)のtask_idの一覧が記載されたファイル。task_idは改行(LF or CRLF)で区切る。'
    )

    parser.add_argument('--comment',
                        metavar='comment',
                        type=str,
                        required=True,
                        help='差し戻すときに付与する検査コメントの内容')

    parser.add_argument('--assign_last_annotator',
                        action="store_true",
                        help='指定した場合、差し戻したタスクに、最後のannotation phaseの担当者を割り当てる。')

    parser.add_argument(
        '--assigned_annotator_user_id',
        metavar='annotator_user_id',
        type=str,
        help=
        '差し戻したタスクに割り当てるユーザのuser_id. 指定しなければ割り当てない。`--assign_last_annotator`と同時に指定できない'
    )

    service = annofabapi.build_from_netrc()
    examples_wrapper = ExamplesWrapper(service)

    try:
        main(parser.parse_args())

    except Exception as e:
        logger.exception(e)
