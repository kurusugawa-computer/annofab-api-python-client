from typing import Any, Callable, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import

import annofabapi
from example_typing import InputDataSize
import yaml
import logging.config
import argparse
from pathlib import Path

def read_lines(filepath: str) -> List[str]:
    """ファイルを行単位で読み込む。改行コードを除く"""
    with open(filepath) as f:
        lines = f.readlines()
    return [e.rstrip('\r\n') for e in lines]


def get_input_data_size(str_input_data_size: str) -> InputDataSize:
    """400x300を(400,300)に変換する"""
    splited_list = str_input_data_size.split("x")
    return (int(splited_list[0]), int(splited_list[1]))

def load_logging_config(args, logging_yaml_file: str = "./logging.yaml"):
    """./logging.yamlを読み込む"""

    with open(logging_yaml_file, encoding='utf-8') as f:
        logging_config = yaml.safe_load(f)

        if hasattr(args, "logdir"):
            logdir = Path(args.logdir)
            logdir.mkdir(exist_ok=True, parents=True)

            log_filename = f"{str(logdir)}/examples.log"
            logging_config["handlers"]["fileRotatingHandler"]["filename"] = log_filename

        logging.config.dictConfig(logging_config)


def add_common_arguments_to_parser(parser: argparse.ArgumentParser):
    """共通のコマンドライン引数を設定する"""
    parser.add_argument('--logdir',type=str, default=".log",
        help='ログファイルを保存するディレクトリ'
    )


class ExamplesWrapper:
    """
    Exampleツール用のWrapperクラス
    Returns:

    """

    def __init__(self, service: annofabapi.Resource):
        self.service = service

    @staticmethod
    def get_account_id_last_annotation_phase(
            task_histories: List[Dict[str, Any]]):
        """
        タスク履歴の最後のannotation phaseを担当したaccount_idを取得する. なければNoneを返す
        Args:
            task_histories:

        Returns:


        """
        annotation_histories = [
            e for e in task_histories if e["phase"] == "annotation"
        ]
        if len(annotation_histories) > 0:
            last_history = annotation_histories[-1]
            return last_history["account_id"]
        else:
            return None

    def get_my_account_id(self) -> str:
        """
        自分自身のaccount_idを取得する
        Returns:
            account_id

        """
        account, _ = self.service.api.get_my_account()
        return account['account_id']

    def get_account_id_from_user_id(self, project_id: str,
                                    user_id: str) -> str:
        """
        usre_idからaccount_idを取得する
        Args:
            project_id:
            user_id:

        Returns:
            account_id

        """
        member, _ = self.service.api.get_project_member(project_id, user_id)
        return member['account_id']

    def change_operator_of_task(self, project_id: str, task_id: str,
                                account_id: str) -> Dict[str, Any]:
        """
        タスクの担当者を変更する
        Args:
            self:
            project_id:
            task_id:
            account_id:

        Returns:
            変更後のtask情報

        """
        task, _ = self.service.api.get_task(project_id, task_id)

        req = {
            "status": "not_started",
            "account_id": account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        return self.service.api.operate_task(project_id,
                                             task_id,
                                             request_body=req)[0]

    def change_to_working_phase(self, project_id: str, task_id: str,
                                account_id: str) -> Dict[str, Any]:
        """
        タスクを作業中に変更する
        Args:
            self:
            project_id:
            task_id:
            account_id:

        Returns:
            変更後のtask情報

        """
        task, _ = self.service.api.get_task(project_id, task_id)

        req = {
            "status": "working",
            "account_id": account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        return self.service.api.operate_task(project_id,
                                             task_id,
                                             request_body=req)[0]

    def change_to_break_phase(self, project_id: str, task_id: str,
                              account_id: str) -> Dict[str, Any]:
        """
        タスクを休憩中に変更する
        Returns:
            変更後のtask情報
        """
        task, _ = self.service.api.get_task(project_id, task_id)

        req = {
            "status": "break",
            "account_id": account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        return self.service.api.operate_task(project_id,
                                             task_id,
                                             request_body=req)[0]

    def reject_task(self,
                    project_id: str,
                    task_id: str,
                    account_id: str,
                    annotator_account_id: Optional[str] = None):
        """
        タスクを差し戻し、annotator_account_id　に担当を割り当てる。
        Args:
            task_id:
            account_id: 差し戻すときのユーザのaccount_id
            annotator_account_id: 差し戻したあとに割り当てるユーザ。Noneの場合は直前のannotation phase担当者に割り当てる。

        Returns:
            変更あとのtask情報

        """

        # タスクを差し戻す
        task, _ = self.service.api.get_task(project_id, task_id)

        req_reject = {
            "status": "rejected",
            "account_id": account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        rejected_task, _ = self.service.api.operate_task(
            project_id, task_id, request_body=req_reject)

        req_change_operator = {
            "status": "not_started",
            "account_id": annotator_account_id,
            "last_updated_datetime": rejected_task["updated_datetime"],
        }
        updated_task, _ = self.service.api.operate_task(
            project_id, task["task_id"], request_body=req_change_operator)
        return updated_task

    def reject_task_assign_last_annotator(self, project_id: str, task_id: str,
                                          account_id: str):
        """
        タスクを差し戻したあとに、最後のannotation phase担当者に割り当てる。
        Args:
            task_id:
            account_id: 差し戻すときのユーザのaccount_id

        Returns:
            変更あとのtask情報

        """

        # タスクを差し戻す
        task, _ = self.service.api.get_task(project_id, task_id)
        last_annotator_account_id = self.get_account_id_last_annotation_phase(
            task["histories_by_phase"])

        return self.reject_task(project_id, task_id, account_id,
                                last_annotator_account_id)
