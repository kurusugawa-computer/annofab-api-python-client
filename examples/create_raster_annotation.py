"""
ラスタ画像をアノテーションとして登録する
"""

import argparse
import logging
import example_utils
import json
import time
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import

import requests
import urllib
import urllib.parse
import annofabapi
import annofabapi.utils
import uuid
import PIL
import PIL.Image
import PIL.ImageDraw
from example_utils import ExamplesWrapper, read_lines
from example_typing import InputDataSize, Annotation

logging_formatter = '%(levelname)s : %(asctime)s : %(name)s : %(funcName)s : %(message)s'
logging.basicConfig(format=logging_formatter)
logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# def create_segmentation_image(input_dat_size: InputDataSize,):
#     image = PIL.Image.new(mode="RGBA", size=input_dat_size, color=(0,0,0,0))
#     draw = PIL.ImageDraw.Draw(image)
#     draw.rectangle([0,0,100,100], fill=(255,255,255,255))

label_dict: Dict[str, str]
"""key:label_id, value:label """


def draw_annotation_list(annotation_list: List[Annotation], draw: PIL.ImageDraw.Draw) -> PIL.ImageDraw.Draw:
    """
    矩形、ポリゴンを描画する。
    Args:
        annotation_list: アノテーション List
        draw: (IN/OUT) PillowのDrawing Object. 変更される。
    Returns:
        描画したPillowのDrawing Object

    """
    for annotation in annotation_list:
        data = annotation["data"]
        color = (255, 255, 255, 255)
        data_type = data["_type"]
        if data_type == "BoundingBox":
            xy = [(data["left_top"]["x"], data["left_top"]["y"]),
                  (data["right_bottom"]["x"], data["right_bottom"]["y"])]
            draw.rectangle(xy, fill=color)

        elif data_type == "Points":
            # Polygon
            xy = [(e["x"], e["y"]) for e in data["points"]]
            draw.polygon(xy, fill=color)

    return draw


def create_annotation_with_image(project_id: str, task_id: str, input_data_id: str, image_file_list: List[Any]):
    account_id = examples_wrapper.get_my_account_id()

    details = []
    for e in image_file_list:
        image_file = e["path"]
        label_id = e["label_id"]

        s3_path = service.wrapper.upload_file_to_s3(project_id, image_file, "image/png")
        annotation_id = str(uuid.uuid4())

        detail = {
            "account_id": account_id,
            "additional_data_list": [],
            "annotation_id": annotation_id,
            "created_datetime": None,
            "data": None,
            "data_holding_type": "outer",
            "etag": None,
            "is_protected": False,
            "label_id": label_id,
            "path": s3_path,
            "updated_datetime": None,
            "url": None,
        }

        details.append(detail)

    request_body = {
        "project_id": project_id,
        "task_id": task_id,
        "input_data_id": input_data_id,
        "details": details
    }

    return service.api.put_annotation(project_id, task_id, input_data_id, request_body=request_body)[0]


def write_segmentation_image(input_data: Dict[str, Any], label: str, tmp_image_path: Path,
                             input_data_size: InputDataSize,
                             task_status_complete: bool = False):
    if task_status_complete and input_data["task_status"] != "complete":
        logger.info(
            f"task_statusがcompleteでない( {input_data['task_status']})ため、除外 {input_data['task_id']}, {input_data['input_data_id']}"
        )
        return False

    image = PIL.Image.new(mode="RGBA", size=input_data_size, color=(0, 0, 0, 0))
    draw = PIL.ImageDraw.Draw(image)

    # labelで絞り込み
    annotation_list = [e for e in input_data["details"] if e["label"] == label]
    if len(annotation_list) == 0:
        logger.info(f"{input_data['task_id']}, {input_data['input_data_id']} に label:{label} のアノテーションがない")
        return False

    # アノテーションを描画する
    draw_annotation_list(annotation_list, draw)

    tmp_image_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(str(tmp_image_path))
    logger.info(f"{str(tmp_image_path)} の生成完了")
    return True


def create_segmentation_from_polygon(
        annotation_dir: str,
        default_input_data_size: InputDataSize,
        tmp_dir: str,
        labels: List[Dict[str, str]],
        project_id: str,
        task_status_complete: bool = False):
    annotation_dir_path = Path(annotation_dir)
    tmp_dir_path = Path(tmp_dir)

    tmp_dir_path.mkdir(exist_ok=True)

    for task_dir in annotation_dir_path.iterdir():
        if not task_dir.is_dir():
            continue

        task_id = task_dir.name
        for input_data_json in task_dir.iterdir():
            if not input_data_json.is_file():
                continue

            with open(str(input_data_json)) as f:
                input_data = json.load(f)

            input_data_id = input_data["input_data_id"]
            image_file_list = []
            for label_dict in labels:
                label = label_dict["label"]
                label_id = label_dict["label_id"]

                tmp_image_path = tmp_dir_path / task_dir.name / input_data_json.stem / f"{label}.png"

                try:
                    result = write_segmentation_image(input_data=input_data, label=label,
                                                      tmp_image_path=tmp_image_path,
                                                      input_data_size=default_input_data_size,
                                                      task_status_complete=task_status_complete)
                    if result:
                        image_file_list.append({
                            "path": str(tmp_image_path),
                            "label_id": label_id
                        })


                except Exception as e:
                    logger.warning(f"{str(tmp_image_path)} の生成失敗", e)
                    raise e

            if len(image_file_list) > 0:
                create_annotation_with_image(project_id, task_id, input_data_id, image_file_list)
                logger.info(f"{task_id}, {input_data_id} アノテーションの登録")


def create_labels(project_id, labels: List[str]):
    spec_labels = service.api.get_annotation_specs(project_id)[0]["labels"]
    return [e for e in spec_labels if e["label_name"] in labels]


def main(args):
    logger.debug(f"args: {args}")

    try:
        default_input_data_size = example_utils.get_input_data_size(args.default_input_data_size)

    except Exception as e:
        logger.error("--default_input_data_size のフォーマットが不正です", e)
        raise e

    try:
        with open(args.label_json_file) as f:
            labels = json.load(f)

    except Exception as e:
        logger.error("--label_json_file のParseに失敗しました。", e)
        raise e

    create_segmentation_from_polygon(annotation_dir=args.annotation_dir,
                                     default_input_data_size=default_input_data_size,
                                     tmp_dir=args.tmp_dir,
                                     labels=labels,
                                     project_id=args.project_id,
                                     task_status_complete=args.task_status_complete)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        "矩形/ポリゴンアノテーションを、塗りつぶしv2アノテーションとして登録する。")
    parser.add_argument('--annotation_dir',
                        type=str,
                        required=True,
                        help='アノテーションzipを展開したディレクトリのパス')

    parser.add_argument('--default_input_data_size',
                        type=str,
                        required=True,
                        help='入力データ画像のサイズ。{width}x{height}。ex. 1280x720')

    parser.add_argument('--label_json_file',
                        type=str,
                        required=True,
                        help='塗りつぶしに変換するlabelが記載されたファイル')

    parser.add_argument('--tmp_dir',
                        type=str,
                        required=True,
                        help='temporaryディレクトリのパス')

    parser.add_argument('--project_id',
                        type=str,
                        required=True,
                        help='塗りつぶしv2アノテーションを登録するプロジェクトのproject_id')

    parser.add_argument('--task_status_complete',
                        action="store_true",
                        help='taskのstatusがcompleteの場合のみ画像を生成する')

    try:
        service = annofabapi.build_from_netrc()
        examples_wrapper = ExamplesWrapper(service)

        main(parser.parse_args())

    except Exception as e:
        logger.exception(e)
