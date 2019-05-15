"""
受け入れ完了タスクを、受け入れ取り消しする。

# ORG組織配下のすべてのプロジェクトに、userをownerロールで割り当てる
$ python cancel_acceptance.py --project_id --user_id user --role owner --organization ORG

# prj1, prj2のプロジェクトに、userをownerロールで割り当てる
$ python invite_user_to_projects.py --user_id user --role owner --project_id prj1 prj2
"""

import argparse
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import requests

import annofabapi

from example_utils import read_lines

logging_formatter = '%(levelname)s : %(asctime)s : %(name)s : %(funcName)s : %(message)s'
logging.basicConfig(format=logging_formatter)
logging.getLogger("annofabapi").setLevel(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


def get_account_id_from_user_id(project_id: str, user_id: str):
    member, _ = service.api.get_project_member(project_id, user_id)
    return member['account_id']


def cancel_acceptance(project_id: str, task_id_list: List[str], acceptor_user_id: Optional[str] = None):
    acceptor_account_id = get_account_id_from_user_id(project_id,
                                                      acceptor_user_id) if acceptor_user_id is not None else None

    for task_id in task_id_list:
        try:
            task, _ = service.api.get_task(project_id, task_id)
            if task["status"] != "complete":
                logger.warning(f"task_id = {task_id} は受入完了でありません。status = {task['status']}, phase={task['phase']}")
            request_body = {
                "status": "not_started",
                "account_id": acceptor_account_id,
                "last_updated_datetime": task["updated_datetime"],

            }
            operated_task, _ = service.api.operate_task(project_id, task_id, request_body=request_body)
            logger.info(f"task_id = {task_id} の受け入れ取り消し完了")

        except requests.exceptions.HTTPError as e:
            logger.error(e)
            logger.info(f"task_id = {task_id} の受け入れ取り消し失敗")


def main(args):
    task_id_list = read_lines(args.task_id_file)
    cancel_acceptance(args.project_id, task_id_list, args.user_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="受け入れ完了タスクを、受け入れ取り消しする。AnnoFab認証情報は`.netrc`に記載すること")
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
        'task_idの一覧が記載されたファイル。task_idは改行(LF or CRLF)で区切る。')

    parser.add_argument('--user_id',
                        metavar='user_id',
                        dest='user_id',
                        type=str,
                        help='再度受入を担当させたいユーザのuser_id。指定しなければ未割り当てになる。')

    args = parser.parse_args()

    logger.info(args)

    service = annofabapi.build_from_netrc()

    try:
        main(args)

    except Exception as e:
        logger.exception(e)
