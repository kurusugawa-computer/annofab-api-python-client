import argparse
import logging
import os
import uuid
from argparse import ArgumentParser
from typing import Any, Dict, List, Optional

import annofabapi

logger = logging.getLogger(__name__)


class CreatingTestProject:
    def __init__(self, service: annofabapi.Resource):
        self.service = service

        self.labels_dict = {
            "car": "car_label_id"
        }


    def create_project(self, organization_name: str, project_title: Optional[str] = None) -> Dict[str, Any]:
        project_id = str(uuid.uuid4())
        DEFAULT_PROJECT_TITLE = "annofabapiのテスト用プロジェクト（自動生成）"

        request_body = {
            "title": project_title if project_title is not None else DEFAULT_PROJECT_TITLE,
            "status": "active",
            "organization_name": organization_name,
            "configuration": {},
        }
        new_project, _ = self.service.api.put_project(project_id, request_body=request_body)
        return new_project

    def _create_bbox_label(self) -> Dict[str, Any]:
        label_name = "car"
        label_id = self.labels_dict[label_name]
        return {
            "label_id": label_id,
            "label_name": {
                "messages": [{"lang": "ja-JP", "message": label_name}, {"lang": "en-US", "message": label_name}],
                "default_lang": "ja-JP",
            },
            "annotation_type": "bounding_box",
            "keybind": [],
            "additional_data_definitions": [],
            "color": {"red": 255, "green": 0, "blue": 0},
            "annotation_editor_feature": {
                "append": False,
                "erase": False,
                "freehand": False,
                "rectangle_fill": False,
                "polygon_fill": False,
                "fill_near": False,
            },
        }

    def create_annotation_specs(self, project_id: str) -> Dict[str, Any]:
        old_annotation_specs, _ = self.service.api.get_annotation_specs(project_id)
        request_body = {
            "labels": [self._create_bbox_label()],
            "last_updated_datetime": old_annotation_specs["updated_datetime"],
        }
        annotation_specs, _ = self.service.api.put_annotation_specs(project_id, request_body=request_body)
        return annotation_specs

    def create_input_data(self, project_id: str, input_data_id:str,  image_path: str):
        """
        サンプルの入力データを登録する。
        """
        old_input_data = self.service.wrapper.get_input_data_or_none(project_id, input_data_id)
        if old_input_data is not None:
            logger.debug(f"入力データをすでに存在していたので、登録しません。input_data_id={input_data_id}")
            return

        request_body = {
            "input_data_name": "AnnoFab Logo Image",
            "input_data_path": "https://annofab.com/images/logo.png",
        }
        self.service.wrapper.put_input_data_from_file(
            project_id, input_data_id=input_data_id, file_path=image_path, request_body=request_body
        )
        logger.debug(f"入力データを登録しました。input_data_id={input_data_id}")
        return

    def create_task(self, project_id: str, task_id: str, input_data_id_list: List[str]):
        """
        サンプルのタスクを登録する。
        """
        old_task = self.service.wrapper.get_task_or_none(project_id, task_id)
        if old_task is not None:
            logger.debug(f"タスクはすでに存在していたので、登録しません。task_id={task_id}")

        request_body = {
            "input_data_id_list": input_data_id_list,
        }
        self.service.api.put_task(project_id, task_id=task_id, request_body=request_body)
        logger.debug(f"タスクを登録しました。task_id={task_id}")
        return

    def upload_instruction(self, project_id: str):
        histories, _ = self.service.api.get_instruction_history(project_id)
        if len(histories) > 0:
            logger.debug("作業ガイドはすでに登録されているので、登録しません。")
            return

        image_url = self.service.wrapper.upload_instruction_image(
            project_id, image_id=str(uuid.uuid4()), file_path="tests/data/lenna.png"
        )
        html_data = f"Test Instruction <img src='{image_url}'>"
        last_updated_datetime = histories[0]["updated_datetime"] if len(histories) > 0 else None
        put_request_body = {"html": html_data, "last_updated_datetime": last_updated_datetime}
        self.service.api.put_instruction(project_id, request_body=put_request_body)
        logger.debug("作業ガイドを登録しました。")

    def create_annotations(self, project_id:str, task_id:str, input_data_id:str):
        old_annotation, _ = self.service.api.get_editor_annotation(project_id, task_id, input_data_id)
        if len(old_annotation["details"]) > 0:
            logger.debug(f"task_id={task_id}, input_data_id={input_data_id}にすでにアノテーションは存在するので、アノテーションは登録しません。")
            return

        request_body = {
            "project_id": project_id,
            "task_id":task_id,
            "input_data_id": input_data_id,
            "details": [
                {
                    "annotation_id": str(uuid.uuid4()),
                    "account_id": self.service.api.account_id,
                    "label_id": self.labels_dict["car"],
                    "is_protected": False,
                    "data_holding_type": "inner",
                    "additional_data_list": [],
                    "data": {
                        "left_top":{"x":0,"y":0},"right_bottom": {"x":10,"y":10}, "_type": "BoundingBox"
                    },
                    "etag":None,
                    "url":None,
                    "path":None,
                    "created_datetime":None,
                    "updated_datetime":None

                }
            ],
            "updated_datetime":None
        }
        self.service.api.put_annotation(project_id, task_id, input_data_id, request_body=request_body)
        logger.debug(f"アノテーションを作成しました。task_id={task_id}, input_data_id={input_data_id}")

        return






    def change_operator_of_task(
        self, project_id: str, task_id: str, account_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        タスクの担当者を変更する
        Args:
            self:
            project_id:
            task_id:
            account_id: 新しい担当者のuser_id. Noneの場合未割り当てになる。

        Returns:
            変更後のtask情報

        """
        task, _ = self.service.api.get_task(project_id, task_id)

        req = {
            "status": "not_started",
            "account_id": account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        return self.service.api.operate_task(project_id, task_id, request_body=req)[0]

    def change_to_working_status(self, project_id: str, task_id: str, account_id: str) -> Dict[str, Any]:
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
        return self.service.api.operate_task(project_id, task_id, request_body=req)[0]

    def change_to_break_phase(self, project_id: str, task_id: str) -> Dict[str, Any]:
        """
        タスクを休憩中に変更する
        Returns:
            変更後のtask情報
        """
        task, _ = self.service.api.get_task(project_id, task_id)

        req = {
            "status": "break",
            "account_id": self.service.api.account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        return self.service.api.operate_task(project_id, task_id, request_body=req)[0]

    def reject_task(
        self, project_id: str, task_id: str, account_id: str, annotator_account_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        タスクを強制的に差し戻し、annotator_account_id　に担当を割り当てる。

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
            "force": True,
        }
        rejected_task, _ = self.service.api.operate_task(project_id, task_id, request_body=req_reject)

        req_change_operator = {
            "status": "not_started",
            "account_id": annotator_account_id,
            "last_updated_datetime": rejected_task["updated_datetime"],
        }
        updated_task, _ = self.service.api.operate_task(project_id, task["task_id"], request_body=req_change_operator)
        return updated_task

    def reject_task_assign_last_annotator(self, project_id: str, task_id: str) -> Dict[str, Any]:
        """
        タスクを差し戻したあとに、最後のannotation phase担当者に割り当てる。

        Args:
            task_id:
            account_id: 差し戻すときのユーザのaccount_id

        Returns:
            変更後のtask情報

        """

        task, _ = self.service.api.get_task(project_id, task_id)
        req_reject = {
            "status": "rejected",
            "account_id": self.service.api.account_id,
            "last_updated_datetime": task["updated_datetime"],
            "force": True,
        }
        rejected_task, _ = self.service.api.operate_task(project_id, task_id, request_body=req_reject)
        # 強制的に差し戻すと、タスクの担当者は直前の教師付け(annotation)フェーズの担当者を割り当てられるので、`operate_task`を実行しない。
        return rejected_task

    def complete_task(self, project_id: str, task_id: str) -> Dict[str, Any]:
        """
        タスクを完了状態にする。
        注意：サーバ側ではタスクの検査は実施されない。
        タスクを完了状態にする前にクライアント側であらかじめ「タスクの自動検査」を実施する必要がある。
        """
        task, _ = self.service.api.get_task(project_id, task_id)

        req = {
            "status": "complete",
            "account_id": self.service.api.account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        return self.service.api.operate_task(project_id, task_id, request_body=req)[0]


    def change_to_working_status(self, project_id:str, task_id:str) -> Task:
        """
        必要なら担当者を変更して、作業中状態にします。

        Args:
            task:

        Returns:
            作業中状態後のタスク
        """
        # 担当者変更
        my_account_id = self.service.api.account_id
        try:
            if task.account_id != my_account_id:
                self.facade.change_operator_of_task(task.project_id, task.task_id, my_account_id)
                logger.debug(f"{task.task_id}: 担当者を自分自身に変更しました。")

            dict_task = self.facade.change_to_working_status(
                project_id=task.project_id, task_id=task.task_id, account_id=my_account_id
            )
            return Task.from_dict(dict_task)

        except requests.HTTPError as e:
            logger.warning(f"{task.task_id}: 担当者の変更、または作業中状態への変更に失敗しました。")
            raise e


    def complete_task_for_annotation_phase(
        self,
        project_id:str,
        task_id:str
    ) -> bool:
        """
        annotation phaseのタスクを完了状態にする。

        Args:
            project_id:
            task: 操作対象のタスク。annotation phase状態であること前提。
            reply_comment: 未処置の検査コメントに対する返信コメント。Noneの場合、スキップする。

        Returns:
            成功したかどうか
        """

        unanswered_comment_list_dict: Dict[str, List[Inspection]] = {}
        for input_data_id in task.input_data_id_list:
            unanswered_comment_list = self.get_unanswered_comment_list(task, input_data_id)
            unanswered_comment_list_dict[input_data_id] = unanswered_comment_list

        unanswered_comment_count_for_task = sum([len(e) for e in unanswered_comment_list_dict.values()])
        if unanswered_comment_count_for_task == 0:
            if not self.confirm_processing(f"タスク'{task.task_id}'の教師付フェーズを次のフェーズに進めますか？"):
                return False

            self.change_to_working_status(task)
            self.facade.complete_task(task.project_id, task.task_id)
            logger.info(f"{task.task_id}: 教師付フェーズを次のフェーズに進めました。")
            return True
        else:
            logger.debug(f"{task.task_id}: 未回答の検査コメントが {unanswered_comment_count_for_task} 件あります。")
            if reply_comment is None:
                logger.warning(f"{task.task_id}: 未回答の検査コメントに対する返信コメント（'--reply_comment'）が指定されていないので、スキップします。")
                return False
            elif not self.confirm_processing(f"タスク'{task.task_id}'の教師付フェーズを次のフェーズに進めますか？"):
                return False
            else:
                changed_task = self.change_to_working_status(task)

                logger.debug(f"{task.task_id}: 未回答の検査コメント {unanswered_comment_count_for_task} 件に対して、返信コメントを付与します。")
                for input_data_id, unanswered_comment_list in unanswered_comment_list_dict.items():
                    if len(unanswered_comment_list) == 0:
                        continue
                    self.reply_inspection_comment(
                        changed_task,
                        input_data_id=input_data_id,
                        unanswered_comment_list=unanswered_comment_list,
                        reply_comment=reply_comment,
                    )

                self.facade.complete_task(task.project_id, task.task_id)
                logger.info(f"{task.task_id}: 教師付フェーズをフェーズに進めました。")
                return True

    def create_inspections(self, project_id:str, task_id:str, input_data_id:str):
        old_inspections, _ = self.service.api.get_inspections(project_id, task_id, input_data_id)
        if len(old_inspections) > 0:
            logger.debug(f"task_id={task_id}, input_data_id={input_data_id}にすでに検査コメントは存在するので、検査コメントは登録しません。")
            return

        request_body = {
            "project_id": project_id,
            "task_id":task_id,
            "input_data_id": input_data_id,
            "details": [
                {
                    "annotation_id": str(uuid.uuid4()),
                    "account_id": self.service.api.account_id,
                    "label_id": self.labels_dict["car"],
                    "is_protected": False,
                    "data_holding_type": "inner",
                    "additional_data_list": [],
                    "data": {
                        "left_top":{"x":0,"y":0},"right_bottom": {"x":10,"y":10}, "_type": "BoundingBox"
                    },
                    "etag":None,
                    "url":None,
                    "path":None,
                    "created_datetime":None,
                    "updated_datetime":None

                }
            ],
            "updated_datetime":None
        }
        self.service.api.put_annotation(project_id, task_id, input_data_id, request_body=request_body)
        logger.debug(f"アノテーションを作成しました。task_id={task_id}, input_data_id={input_data_id}")

        return


    def main(
        self, organization_name: Optional[str], project_id: Optional[str], project_title: Optional[str] = None
    ) -> None:
        if project_id is None:
            if organization_name is not None:
                project = self.create_project(organization_name=organization_name, project_title=project_title)
                project_id = project["project_id"]
                logger.debug(f"project_id={project_id} プロジェクトを作成しました。")
            else:
                raise RuntimeError(f"organization_name がNoneなので、プロジェクトを作成できません")

        annotation_specs = self.create_annotation_specs(project_id)
        logger.debug(f"アノテーション仕様を作成しました。")

        # プロジェクトトップに移動する
        now_dir = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")

        input_data_id = "test_input_1"
        self.create_input_data(project_id, input_data_id, image_path="tests/data/lenna.png")

        task_id = "test_task_1"
        self.create_task(project_id, task_id, input_data_id_list=[input_data_id])

        self.create_annotations(project_id, task_id, input_data_id)

        self.upload_instruction(project_id)
        logger.debug(f"作業ガイドを登録しました。")

        # 移動前のディレクトリに戻る
        os.chdir(now_dir)


def parse_args():
    parser = ArgumentParser(
        description="annofabapiのテスト用プロジェクトを生成します。", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    project_group = parser.add_mutually_exclusive_group(required=True)
    project_group.add_argument("-p", "--project_id", type=str, help="テスト用プロジェクトのproject_id。指定しない場合はプロジェクトを作成します。")
    project_group.add_argument("-org", "--organization", type=str, help="プロジェクトを作成する対象の組織を指定してください。")

    return parser.parse_args()


def set_logging():
    logging_formatter = "%(levelname)-8s : %(asctime)s : %(filename)s : %(name)s : %(funcName)s : %(message)s"
    logging.basicConfig(format=logging_formatter)
    logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)
    logging.getLogger("__main__").setLevel(level=logging.DEBUG)


def main() -> None:
    set_logging()

    args = parse_args()

    main_obj = CreatingTestProject(annofabapi.build())
    main_obj.main(organization_name=args.organization, project_id=args.project_id)


if __name__ == "__main__":
    main()
