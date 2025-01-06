import argparse
import logging
import os
import uuid
from argparse import ArgumentParser
from typing import Any, Optional

from more_itertools import first_true

import annofabapi
from annofabapi.api import DEFAULT_ENDPOINT_URL
from annofabapi.models import TaskPhase

logger = logging.getLogger(__name__)

DEFAULT_PROJECT_TITLE = "annofabapiのテスト用プロジェクト（自動生成）"


class CreatingTestProject:
    def __init__(self, service: annofabapi.Resource):
        self.service = service

        self.labels_dict = {"car": "car_label_id"}

    def create_project(self, organization_name: str, project_title: Optional[str] = None) -> dict[str, Any]:
        project_id = str(uuid.uuid4())

        request_body = {
            "title": project_title if project_title is not None else DEFAULT_PROJECT_TITLE,
            "status": "active",
            "organization_name": organization_name,
            "configuration": {},
        }
        new_project, _ = self.service.api.put_project(project_id, request_body=request_body)
        return new_project

    def create_webhook(self, project_id: str, webhook_id: str):
        request_body = {
            "project_id": project_id,
            "event_type": "annotation-archive-updated",
            "webhook_id": webhook_id,
            "webhook_status": "active",
            "method": "POST",
            "headers": [{"name": "Content-Type", "value": "application/json"}],
            "body": "test",
            "url": "https://annofab.com/",
            "created_datetime": None,
            "updated_datetime": None,
        }
        self.service.api.put_webhook(project_id, webhook_id, request_body=request_body)
        logger.debug(f"webhookを登録しました。webhook_id={webhook_id}")

    def _create_bbox_label(self) -> dict[str, Any]:
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

    def create_annotation_specs(self, project_id: str) -> dict[str, Any]:
        old_annotation_specs, _ = self.service.api.get_annotation_specs(project_id)
        request_body = {
            "labels": [self._create_bbox_label()],
            "last_updated_datetime": old_annotation_specs["updated_datetime"],
        }
        annotation_specs, _ = self.service.api.put_annotation_specs(project_id, request_body=request_body)
        return annotation_specs

    def create_input_data(self, project_id: str, input_data_id: str, image_path: str):
        """
        サンプルの入力データを登録する。
        """
        old_input_data = self.service.wrapper.get_input_data_or_none(project_id, input_data_id)
        if old_input_data is not None:
            logger.debug(f"入力データをすでに存在していたので、登録しません。input_data_id={input_data_id}")
            return

        request_body = {
            "input_data_name": "Annofab Logo Image",
            "input_data_path": "https://annofab.com/images/logo.png",
        }
        self.service.wrapper.put_input_data_from_file(project_id, input_data_id=input_data_id, file_path=image_path, request_body=request_body)
        logger.debug(f"入力データを登録しました。input_data_id={input_data_id}")
        return

    def create_supplementary_data(self, project_id: str, input_data_id: str, supplementary_data_id: str, supplementary_data_path: str):
        supplementary_data_list, _ = self.service.api.get_supplementary_data_list(project_id, input_data_id)
        old_supplementary_data = first_true(supplementary_data_list, pred=lambda e: e["supplementary_data_id"] == supplementary_data_id)
        if old_supplementary_data is not None:
            logger.debug(f"補助情報はすでに存在していたので、登録しません。supplementary_data_id={supplementary_data_id}")
            return

        # 適当なファイルをアップロードする
        self.service.wrapper.put_supplementary_data_from_file(
            project_id,
            input_data_id=input_data_id,
            supplementary_data_id=supplementary_data_id,
            file_path=supplementary_data_path,
            request_body={"supplementary_data_number": 1},
            content_type="image",
        )
        logger.debug(f"補助情報を登録しました。supplementary_data_id={supplementary_data_id}")
        return

    def create_task(self, project_id: str, task_id: str, input_data_id_list: list[str]):
        """
        サンプルのタスクを登録する。
        """
        old_task = self.service.wrapper.get_task_or_none(project_id, task_id)
        if old_task is not None:
            logger.debug(f"タスクはすでに存在していたので、登録しません。task_id={task_id}")
            return

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

        image_url = self.service.wrapper.upload_instruction_image(project_id, image_id=str(uuid.uuid4()), file_path="tests/data/lenna.png")
        html_data = f"Test Instruction <img src='{image_url}'>"
        last_updated_datetime = histories[0]["updated_datetime"] if len(histories) > 0 else None
        put_request_body = {"html": html_data, "last_updated_datetime": last_updated_datetime}
        self.service.api.put_instruction(project_id, request_body=put_request_body)
        logger.debug("作業ガイドを登録しました。")

    def create_annotations(self, project_id: str, task_id: str, input_data_id: str):
        old_annotation, _ = self.service.api.get_editor_annotation(project_id, task_id, input_data_id)
        if len(old_annotation["details"]) > 0:
            logger.debug(f"task_id={task_id}, input_data_id={input_data_id}にすでにアノテーションは存在するので、アノテーションは登録しません。")
            return

        request_body = {
            "project_id": project_id,
            "task_id": task_id,
            "input_data_id": input_data_id,
            "details": [
                {
                    "annotation_id": str(uuid.uuid4()),
                    "account_id": self.service.api.account_id,
                    "label_id": self.labels_dict["car"],
                    "is_protected": False,
                    "data_holding_type": "inner",
                    "additional_data_list": [],
                    "data": {"left_top": {"x": 0, "y": 0}, "right_bottom": {"x": 10, "y": 10}, "_type": "BoundingBox"},
                    "etag": None,
                    "url": None,
                    "path": None,
                    "created_datetime": None,
                    "updated_datetime": None,
                }
            ],
            "updated_datetime": None,
        }
        self.service.api.put_annotation(project_id, task_id, input_data_id, request_body=request_body)
        logger.debug(f"アノテーションを作成しました。task_id={task_id}, input_data_id={input_data_id}")

        return

    def add_inspection_comment(
        self,
        project_id: str,
        task: dict[str, Any],
        input_data_id: str,
        inspection_comment: str,
    ):
        """
        検査コメントを付与する。
        先頭画像の左上に付与する。
        """
        inspection_data = {"x": 0, "y": 0, "_type": "Point"}

        req_inspection = [
            {
                "data": {
                    "project_id": project_id,
                    "comment": inspection_comment,
                    "task_id": task["task_id"],
                    "input_data_id": input_data_id,
                    "inspection_id": str(uuid.uuid4()),
                    "phase": task["phase"],
                    "commenter_account_id": self.service.api.account_id,
                    "data": inspection_data,
                    "status": "annotator_action_required",
                    "created_datetime": task["updated_datetime"],
                },
                "_type": "Put",
            }
        ]

        return self.service.api.batch_update_inspections(project_id, task["task_id"], input_data_id, request_body=req_inspection)[0]

    def create_inspection_comment(self, project_id: str, task_id: str, input_data_id: str):
        """
        検査コメントを付与する。
        """

        old_inspections, _ = self.service.api.get_inspections(project_id, task_id, input_data_id)
        if len(old_inspections) > 0:
            logger.debug(f"task_id={task_id}, input_data_id={input_data_id}にすでに検査コメントは存在するので、検査コメントは登録しません。")
            return

        # 自分自身を担当者にする

        task, _ = self.service.api.get_task(project_id, task_id)
        if task["phase"] != TaskPhase.ACCEPTANCE.value:
            # 受け入れフェーズに移行する
            self.service.wrapper.change_task_operator(project_id, task_id, operator_account_id=self.service.api.account_id)
            self.service.wrapper.change_task_status_to_working(project_id, task_id)
            self.service.wrapper.complete_task(project_id, task_id)

        # 検査コメントの付与
        self.service.wrapper.change_task_operator(project_id, task_id, operator_account_id=self.service.api.account_id)
        self.service.wrapper.change_task_status_to_working(project_id, task_id)
        task, _ = self.service.api.get_task(project_id, task_id)
        self.add_inspection_comment(project_id, task, input_data_id=input_data_id, inspection_comment="テストコメント（自動生成）")
        logger.debug(f"検査コメントを作成しました。task_id={task_id}, input_data_id={input_data_id}")
        self.service.wrapper.change_task_status_to_break(project_id, task_id)

    def main(self, organization_name: str, project_title: Optional[str] = None) -> None:
        project = self.create_project(organization_name=organization_name, project_title=project_title)
        project_id = project["project_id"]
        logger.debug(f"project_id={project_id} プロジェクトを作成しました。")

        self.create_annotation_specs(project_id)
        logger.debug("アノテーション仕様を作成しました。")

        # プロジェクトトップに移動する
        now_dir = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")

        input_data_id = "test_input_1"
        self.create_input_data(project_id, input_data_id, image_path="tests/data/lenna.png")

        input_data_id = "test_input_1"
        supplementary_data_id = "test_supplementary_data_1"
        self.create_supplementary_data(
            project_id,
            input_data_id=input_data_id,
            supplementary_data_id=supplementary_data_id,
            supplementary_data_path="tests/data/lenna.png",
        )

        task_id = "test_task_1"
        self.create_task(project_id, task_id, input_data_id_list=[input_data_id])

        self.create_annotations(project_id, task_id, input_data_id)
        self.create_inspection_comment(project_id, task_id, input_data_id)

        self.upload_instruction(project_id)
        logger.debug("作業ガイドを登録しました。")

        self.create_webhook(project_id, webhook_id="test_webhook_1")
        logger.info(f"テストプロジェクトを作成しました。https://annofab.com/projects/{project_id}")
        # 移動前のディレクトリに戻る
        os.chdir(now_dir)


def parse_args():
    parser = ArgumentParser(
        description="annofabapiのテスト用プロジェクトを生成します。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-org", "--organization", type=str, required=True, help="プロジェクトを作成する対象の組織を指定してください。")
    parser.add_argument(
        "--project_title",
        type=str,
        default=DEFAULT_PROJECT_TITLE,
        help="作成するプロジェクトのタイトルを指定してください。",
    )
    parser.add_argument("--endpoint", type=str, default=DEFAULT_ENDPOINT_URL, help="接続先エンドポイントを指定してください")

    return parser.parse_args()


def set_logging():
    logging_formatter = "%(levelname)-8s : %(asctime)s : %(filename)s : %(name)s : %(funcName)s : %(message)s"
    logging.basicConfig(format=logging_formatter)
    logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)
    logging.getLogger("__main__").setLevel(level=logging.DEBUG)


def main() -> None:
    set_logging()

    args = parse_args()

    main_obj = CreatingTestProject(annofabapi.build(endpoint_url=args.endpoint))
    main_obj.main(organization_name=args.organization, project_title=args.project_title)


if __name__ == "__main__":
    main()
