"""
Semantic Segmentation(Multi Class)用の画像を生成する。
"""

import argparse
import json
import logging
import os
import os.path
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional  # pylint: disable=unused-import

import PIL.Image
import PIL.ImageDraw
import annofabcli
from annofabcli.common.typing import RGB, Annotation, InputDataSize, SubInputDataList

logger = logging.getLogger(__name__)

# 型タイプ
AnnotationSortKeyFunc = Callable[[Annotation], Any]
"""アノテーションをsortするときのkey関数のType"""


def _create_sub_input_data_list(sub_annotation_dir_list: List[str],
                                input_data_json: Path) -> SubInputDataList:
    """
    マージ対象の sub_input_data_listを生成する
    """
    sub_input_data_list: SubInputDataList = []

    for sub_annotation_dir in sub_annotation_dir_list:
        sub_annotation_dir_path = Path(sub_annotation_dir)
        sub_input_data_json = sub_annotation_dir_path / str(
            input_data_json.relative_to(input_data_json.parent.parent))
        sub_input_data_dir = sub_input_data_json.parent / sub_input_data_json.stem

        elm = (str(sub_input_data_json), str(sub_input_data_dir))
        sub_input_data_list.append(elm)

    return sub_input_data_list


def draw_annotation_list(annotation_list: List[Annotation],
                         input_data_dir: str, label_color_dict: Dict[str, RGB],
                         draw: PIL.ImageDraw.Draw) -> PIL.ImageDraw.Draw:
    """
    矩形、ポリゴン、塗りつぶし、塗りつぶしv2アノテーションを描画する。
    Args:
        annotation_list: アノテーション List
        input_data_dir: input_data_dir: 塗りつぶしアノテーションが格納されたディレクトリのパス
        label_color_dict: label_nameとRGBを対応付けたdict
        draw: (IN/OUT) PillowのDrawing Object. 変更される。
    Returns:
        描画したPillowのDrawing Object

    """
    for annotation in annotation_list:
        data = annotation["data"]
        if data is None:
            # 画像全体アノテーション
            continue

        data_type = data["_type"]
        if data_type not in [
                "BoundingBox", "Points", "SegmentationV2", "Segmentation"
        ]:
            continue

        color = label_color_dict.get(annotation["label"])
        if color is None:
            logger.warning(
                f"label_name = {annotation['label']} のcolorが指定されていません")
            color = (255, 255, 255)

        if data_type == "BoundingBox":
            xy = [(data["left_top"]["x"], data["left_top"]["y"]),
                  (data["right_bottom"]["x"], data["right_bottom"]["y"])]
            draw.rectangle(xy, fill=color)

        elif data_type == "Points":
            # Polygon
            xy = [(e["x"], e["y"]) for e in data["points"]]
            draw.polygon(xy, fill=color)

        elif data_type in ["SegmentationV2", "Segmentation"]:
            # 塗りつぶしv2 or 塗りつぶし
            outer_image_path = Path(input_data_dir, data["data_uri"])
            if not outer_image_path.exists():
                logger.warning(f"{outer_image_path} が存在しません")
                continue

            outer_image = PIL.Image.open(outer_image_path)
            draw.bitmap([0, 0], outer_image, fill=color)

    return draw


def draw_sub_input_data(
        sub_input_data_list: SubInputDataList,
        label_color_dict: Dict[str, RGB],
        draw: PIL.ImageDraw.Draw,
        task_status_complete: bool = False,
        annotation_sort_key_func: Optional[AnnotationSortKeyFunc] = None
) -> PIL.ImageDraw.Draw:
    """
    他のプロジェクトのアノテーション情報を描画する。
    Args:
        sub_input_data_list:
        label_color_dict:
        draw:
        task_status_complete:
        annotation_sort_key_func:

    Returns:

    """

    for sub_input_data_json_file, sub_input_data_dir in sub_input_data_list:
        if not os.path.exists(sub_input_data_json_file):
            logger.warning(f"{sub_input_data_json_file} は存在しません.")
            continue

        with open(sub_input_data_json_file) as f:
            sub_input_data_json = json.load(f)

        task_status = sub_input_data_json["task_status"]
        if task_status_complete and task_status != "complete":
            logger.warning(
                f"task_statusがcompleteでない( {task_status})ため、{sub_input_data_json_file} のアノテーションは描画しない"
            )
            continue

        sub_annotation_list = sub_input_data_json[
            "details"] if annotation_sort_key_func is None else sorted(
                sub_input_data_json["details"], key=annotation_sort_key_func)

        draw_annotation_list(sub_annotation_list, sub_input_data_dir,
                             label_color_dict, draw)

    return draw


def write_one_semantic_segmentation_image(
        input_data_json_file: str,
        input_data_dir: str,
        input_dat_size: InputDataSize,
        label_color_dict: Dict[str, RGB],
        output_image_file: str,
        task_status_complete: bool = False,
        annotation_sort_key_func: Optional[AnnotationSortKeyFunc] = None,
        sub_input_data_list: Optional[SubInputDataList] = None):
    """
    アノテーション情報が記載されたJSONファイルから、Semantic Segmentation用の画像を生成する。
    Semantic Segmentation用のアノテーションがなくても、画像は生成する。

    Args:
        input_data_json_file: JSONファイルのパス
        input_data_dir: 塗りつぶしアノテーションが格納されたディレクトリのパス
        input_dat_size: 画像データのサイズ Tupple[width, height]
        label_color_dict: label_nameとRGBを対応付けたdict
        output_image_file: 出力する画像ファイル
        task_status_complete: Trueならばtask_statusがcompleteのときのみ画像を生成する。
        annotation_sort_key_func: アノテーションをsortするときのkey関数. Noneならばsortしない
        sub_input_data_list: マージ対象の入力データ情報

    """
    logger.debug(
        f"args: {input_data_json_file}, {input_data_dir}, {input_dat_size}, {output_image_file}"
    )
    with open(input_data_json_file) as f:
        input_data_json = json.load(f)

    if task_status_complete and input_data_json["task_status"] != "complete":
        logger.info(
            f"task_statusがcompleteでない( {input_data_json['task_status']})ため、{output_image_file} は生成しない。"
        )
        return

    image = PIL.Image.new(mode="RGB", size=input_dat_size)
    draw = PIL.ImageDraw.Draw(image)

    annotation_list = input_data_json[
        "details"] if annotation_sort_key_func is None else sorted(
            input_data_json["details"], key=annotation_sort_key_func)
    # アノテーションを描画する
    draw_annotation_list(annotation_list, input_data_dir, label_color_dict,
                         draw)

    if sub_input_data_list is not None:
        draw_sub_input_data(sub_input_data_list=sub_input_data_list,
                            label_color_dict=label_color_dict,
                            draw=draw,
                            task_status_complete=task_status_complete,
                            annotation_sort_key_func=annotation_sort_key_func)

    Path(output_image_file).parent.mkdir(parents=True, exist_ok=True)
    image.save(output_image_file)

    logger.info(f"{str(output_image_file)} の生成完了")


def write_semantic_segmentation_images(
        annotation_dir: str,
        default_input_data_size: InputDataSize,
        label_color_dict: Dict[str, RGB],
        output_dir: str,
        output_image_extension: str,
        task_status_complete: bool = False,
        annotation_sort_key_func: Optional[AnnotationSortKeyFunc] = None,
        sub_annotation_dir_list: Optional[List[str]] = None):
    """
    アノテーションzipを展開したディレクトリから、Semantic Segmentation用の画像を生成する。
    出力ディレクトリの構成は `{output_dir/{task_id}/{input_data_name}.{image_extension}`

    Args:
        annotation_dir: アノテーションzipを展開したディレクトリのパス
        default_input_data_size: 入力データ画像のサイズ(width, height)
        output_image_extension: 出力画像の拡張子
        label_color_dict: label_nameとRGBを対応付けたdict
        output_dir: 出力ディレクトリのパス
        task_status_complete: Trueならばtask_statusがcompleteのときのみ画像を生成する。
        annotation_sort_key_func: アノテーションをsortするときのkey関数. Noneならばsortしない
        sub_annotation_dir_list: マージ対象のアノテーションディレクトリList

    Returns:

    """
    logger.debug(
        f"args: {annotation_dir}, {default_input_data_size}, {label_color_dict}, {output_dir}, {output_image_extension}"
    )
    annotation_dir_path = Path(annotation_dir)
    output_dir_path = Path(output_dir)

    output_dir_path.mkdir(exist_ok=True)

    for task_dir in annotation_dir_path.iterdir():
        if not task_dir.is_dir():
            continue

        for input_data_json in task_dir.iterdir():
            if not input_data_json.is_file():
                continue

            input_data_dir = task_dir / input_data_json.stem
            output_file = output_dir_path / task_dir.name / f"{str(input_data_json.stem)}.{output_image_extension}"

            sub_input_data_list = _create_sub_input_data_list(
                sub_annotation_dir_list, input_data_json) if (
                    sub_annotation_dir_list is not None) else None

            try:
                write_one_semantic_segmentation_image(
                    str(input_data_json),
                    str(input_data_dir),
                    input_dat_size=default_input_data_size,
                    label_color_dict=label_color_dict,
                    output_image_file=str(output_file),
                    task_status_complete=task_status_complete,
                    annotation_sort_key_func=annotation_sort_key_func,
                    sub_input_data_list=sub_input_data_list)

            except Exception as e:
                logger.warning(e)
                logger.warning(f"{str(output_file)} の生成失敗")


def main(args):
    annofabcli.utils.load_logging_config_from_args(args, __file__)

    logger.debug(f"args: {args}")

    try:
        default_input_data_size = annofabcli.utils.get_input_data_size(
            args.default_input_data_size)

    except Exception as e:
        logger.error("--default_input_data_size のフォーマットが不正です")
        raise e

    try:
        with open(args.label_color_json_file) as f:
            label_color_dict = json.load(f)
            label_color_dict = {
                k: tuple(v)
                for k, v in label_color_dict.items()
            }

    except Exception as e:
        logger.error("--label_color_json_file のJSON Parseに失敗しました。")
        raise e

    try:
        if args.label_order_file is not None:
            labels = annofabcli.utils.read_lines(args.label_order_file)

            def annotation_sort_key_func(d: Annotation) -> int:
                """
                labelの順にアノテーションlistをソートする関数
                """
                if d["label"] not in labels:
                    return -1

                return labels.index(d["label"])
        else:
            annotation_sort_key_func = None

    except Exception as e:
        logger.error("--label_order_file のParseに失敗しました。")
        raise e

    try:
        write_semantic_segmentation_images(
            annotation_dir=args.annotation_dir,
            default_input_data_size=default_input_data_size,
            label_color_dict=label_color_dict,
            output_dir=args.output_dir,
            output_image_extension=args.output_image_extension,
            task_status_complete=args.task_status_complete,
            annotation_sort_key_func=annotation_sort_key_func,
            sub_annotation_dir_list=args.sub_annotation_dir)

    except Exception as e:
        logger.exception(e)
        raise e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        "アノテーションzipを展開したディレクトリから、アノテーションをSemantic Segmentation(Multi Class)用の画像をします。"
        "矩形、ポリゴン、塗りつぶし、塗りつぶしv2が対象です。"
        "複数のアノテーションディレクトリを指定して、画像をマージすることも可能です。")
    parser.add_argument('--annotation_dir',
                        type=str,
                        required=True,
                        help='アノテーションzipを展開したディレクトリのパス')

    parser.add_argument('--default_input_data_size',
                        type=str,
                        required=True,
                        help='入力データ画像のサイズ。{width}x{height}。ex. 1280x720')

    parser.add_argument(
        '--label_color_json_file',
        type=str,
        required=True,
        help='label_nameとRGBを対応付けたJSONファイルのパス. key: label_name, value:[R,G,B]')

    parser.add_argument('--output_dir',
                        type=str,
                        required=True,
                        help='出力ディレクトリのパス')

    parser.add_argument('--output_image_extension',
                        type=str,
                        default="png",
                        help='出力画像の拡張子')

    parser.add_argument('--task_status_complete',
                        action="store_true",
                        help='taskのstatusがcompleteの場合のみ画像を生成する')

    parser.add_argument(
        '--label_order_file',
        type=str,
        help=
        'ラベルごとのレイヤの順序を指定したファイル。ファイルに記載されたラベルの順に塗りつぶす。指定しなければ、アノテーションJSONに記載された順に塗りつぶす。'
    )

    parser.add_argument('--sub_annotation_dir',
                        type=str,
                        nargs="+",
                        help='`annotation_dir`にマージして描画するディレクトリ')

    main(parser.parse_args())
