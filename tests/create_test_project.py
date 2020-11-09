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
        label_id = str(uuid.uuid4())
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

    def create_input_data(self, project_id: str, image_path: str) -> Dict[str, Any]:
        """
        サンプルの入力データを登録する。
        """
        request_body = {
            "input_data_name": "AnnoFab Logo Image",
            "input_data_path": "https://annofab.com/images/logo.png",
        }
        input_data = self.service.wrapper.put_input_data_from_file(
            project_id, input_data_id=str(uuid.uuid4()), file_path=image_path, request_body=request_body
        )
        return input_data

    def create_task(self, project_id: str, task_id: str, input_data_id_list: List[str]) -> Dict[str, Any]:
        """
        サンプルのタスクを登録する。
        """
        request_body = {
            "input_data_id_list": input_data_id_list,
        }
        task, _ = self.service.api.put_task(project_id, task_id=task_id, request_body=request_body)
        return task

    def upload_instruction(self, project_id: str) -> Dict[str, Any]:
        image_url = self.service.wrapper.upload_instruction_image(
            project_id, image_id=str(uuid.uuid4()), file_path="tests/data/lenna.png"
        )
        html_data = f"Test Instruction <img src='{image_url}'>"
        histories, _ = self.service.api.get_instruction_history(project_id)
        last_updated_datetime = histories[0]["updated_datetime"] if len(histories) > 0 else None
        put_request_body = {"html": html_data, "last_updated_datetime": last_updated_datetime}
        return self.service.api.put_instruction(project_id, request_body=put_request_body)[0]

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

        input_data = self.create_input_data(project_id, image_path="tests/data/lenna.png")
        input_data_id = input_data["input_data_id"]
        logger.debug(f"入力データを登録しました。input_data_id={input_data_id}")

        task_id = "test_task_1"
        self.create_task(project_id, task_id, input_data_id_list=[input_data_id])
        logger.debug(f"タスクを登録しました。task_id={task_id}")

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
