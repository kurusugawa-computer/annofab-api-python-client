from typing import Any, Dict, List, Optional, Tuple, Union

import annofabapi


def read_lines(filepath: str) -> List[str]:
    """ファイルを行単位で読み込む。改行コードを除く"""
    with open(filepath) as f:
        lines = f.readlines()
    return [e.rstrip('\r\n') for e in lines]


class ExamplesWrapper:
    """
    Exampleツール用のWrapperクラス
    Returns:

    """

    def __init__(self, service: annofabapi.Resource):
        self.service = service

    def get_account_id_last_annotation_phase(
            self, task_histories: List[Dict[str, Any]]):
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

    def get_account_id_from_user_id(self, project_id: str, user_id: str):
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

    def reject_task(self, project_id: str, task_id: str, account_id: str):
        """
        タスクを差し戻したあと、最後のannotation phase担当者に割り当てる。
        Args:
            task_id:
            account_id: 差し戻すときのユーザのaccount_id

        Returns:
            変更あとのtask情報

        """

        # タスクを差し戻す
        task, _ = self.service.api.get_task(project_id, task_id)
        annotator_account_id = self.get_account_id_last_annotation_phase(
            task["histories_by_phase"])

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
