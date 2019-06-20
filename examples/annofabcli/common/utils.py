import argparse
import logging.config
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional  # pylint: disable=unused-import

import annofabapi
import yaml
from annofabcli.common.typing import InputDataSize


def create_parent_parser():
    """
    共通の引数セットを生成する。
    """
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--logdir',
                               type=str,
                               default=".log",
                               help='ログファイルを保存するディレクトリ。指定しない場合は`.log`ディレクトリ')
    return parent_parser


def read_lines(filepath: str) -> List[str]:
    """ファイルを行単位で読み込む。改行コードを除く"""
    with open(filepath) as f:
        lines = f.readlines()
    return [e.rstrip('\r\n') for e in lines]


def read_lines_except_blank_line(filepath: str) -> List[str]:
    """ファイルを行単位で読み込む。ただし、改行コード、空行を除く"""
    lines = read_lines_except_blank_line(filepath)
    return [line for line in lines if line != ""]


def get_input_data_size(str_input_data_size: str) -> InputDataSize:
    """400x300を(400,300)に変換する"""
    splited_list = str_input_data_size.split("x")
    return (int(splited_list[0]), int(splited_list[1]))


def add_parser(subparsers: argparse._SubParsersAction, subcommand_name: str, subcommand_help:str, description: str) -> argparse.ArgumentParser:
    """
    サブコマンド用にparserを追加する

    Args:
        subparsers:
        subcommand_name:
        subcommand_help:
        description:

    Returns:
        サブコマンドのparser

    """
    epilog="AnnoFabの認証情報は、`$HOME/.netrc`に記載すること"

    return subparsers.add_parser(subcommand_name,
                          parents=[create_parent_parser()],
                          description=description,
                          help=subcommand_help,
                          epilog=epilog)



def load_logging_config_from_args(args,
                                  py_filepath: str,
                                  logging_yaml_file: str = "./logging.yaml"):
    """
    args情報から、logging設定ファイルを読み込む
    Args:
        args: Command引数情報
        py_filepath: Python Filepath
        logging_yaml_file: logging設定ファイル

    Returns:

    """
    log_dir = args.logdir
    log_filename = f"{os.path.basename(py_filepath)}.log"
    load_logging_config(log_dir, log_filename, logging_yaml_file)


def load_logging_config(log_dir: str,
                        log_filename: str,
                        logging_yaml_file: str = "./logging.yaml"):
    """./logging.yamlを読み込む"""

    Path(log_dir).mkdir(exist_ok=True, parents=True)

    with open(logging_yaml_file, encoding='utf-8') as f:
        logging_config = yaml.safe_load(f)

        log_filename = f"{str(log_dir)}/{log_filename}"
        logging_config["handlers"]["fileRotatingHandler"][
            "filename"] = log_filename

        logging.config.dictConfig(logging_config)


class AnnofabApiFacade:
    """
    AnnofabApiのFacadeクラス。annofabapiの複雑な処理を簡単に呼び出せるようにする。
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

    @staticmethod
    def get_label_name_en(label: Dict[str, Any]):
        """label情報から英語名を取得する"""
        label_name_messages = label["label_name"]["messages"]
        return [
            e["message"] for e in label_name_messages if e["lang"] == "en-US"
        ][0]

    def get_project_title(self, project_id: str) -> str:
        """
        プロジェクトのタイトルを取得する
        Returns:
            プロジェクトのタイトル

        """
        project, _ = self.service.api.get_project(project_id)
        return project['title']

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

    def my_role_is_owner(self, project_id: str) -> bool:
        my_member, _ = self.service.api.get_my_member_in_project(project_id)
        return my_member["member_role"] == "owner"

    ##################
    # operateTaskのfacade
    ##################

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
                    annotator_account_id: Optional[str] = None
                    ) -> Dict[str, Any]:
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
                                          account_id: str) -> Dict[str, Any]:
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

    def complete_task(self, project_id: str, task_id: str,
                      account_id: str) -> Dict[str, Any]:
        """
        タスクを完了状態にする。
        注意：サーバ側ではタスクの検査は実施されない。
        タスクを完了状態にする前にクライアント側であらかじめ「タスクの自動検査」を実施する必要がある。
        """
        task, _ = self.service.api.get_task(project_id, task_id)

        req = {
            "status": "complete",
            "account_id": account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        return self.service.api.operate_task(project_id,
                                             task_id,
                                             request_body=req)[0]
