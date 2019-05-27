"""
プロジェクト間のアノテーション仕様の差分を表示する。
"""

import argparse
import logging
import time
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import

import requests
import dictdiffer
import annofabapi
import annofabapi.utils
from example_utils import ExamplesWrapper, read_lines, load_logging_config
import example_utils
import pprint


logger = logging.getLogger(__name__)


def sorted_inspection_phrases(phrases: List[Dict[str, Any]]):
    return sorted(phrases, key=lambda e: e["id"])

def diff_labels_of_annotation_specs(label1: List[Dict[str, Any]], label2: List[Dict[str, Any]]):
    pass


def diff_inspection_phrases(inspection_phrases1: List[Dict[str, Any]], inspection_phrases2: List[Dict[str, Any]]) -> bool:
    """
    定型指摘の差分を表示する。定型指摘IDを基準に差分を表示する。

    Args:
        inspection_phrases1: 比較対象の定型指摘List
        inspection_phrases2: 比較対象の定型指摘List

    Returns:
        差分があれば Trueを返す

    """
    sorted_inspection_phrases1 = sorted_inspection_phrases(inspection_phrases1)
    sorted_inspection_phrases2 = sorted_inspection_phrases(inspection_phrases2)

    phrase_ids1 = [e["id"] for e in sorted_inspection_phrases1]
    phrase_ids2 = [e["id"] for e in sorted_inspection_phrases2]

    if phrase_ids1 != phrase_ids2:
        print("定型指摘IDのListに差分あり")
        print(f"set(phrase_ids1) - set(phrase_ids2) = {set(phrase_ids1) - set(phrase_ids2)}")
        print(f"set(phrase_ids2) - set(phrase_ids1) = {set(phrase_ids2) - set(phrase_ids1)}")
        return True

    is_different = False
    for phrase1, phrase2 in zip(sorted_inspection_phrases1, sorted_inspection_phrases2):
        diff_result = list(dictdiffer.diff(phrase1, phrase2))
        if len(diff_result) > 0:
            is_different = True
            print(f"差分のある定型指摘: {phrase1['id']}")
            pprint.pprint(diff_result)

    if not is_different:
        print("定型指摘は同一")

    return is_different





def diff_annotation_specs(project_id1: str, project_id2: str):
    """
    プロジェクト間のアノテーション仕様の差分を表示する。
    Args:
        project_id1: 比較対象のプロジェクトのproject_id
        project_id2: 比較対象のプロジェクトのproject_id

    """

    annotation_specs1, _ = service.api.get_annotation_specs(project_id1)
    annotation_specs2, _ = service.api.get_annotation_specs(project_id2)

    diff_inspection_phrases(annotation_specs1["inspection_phrases"], annotation_specs2["inspection_phrases"])





def validate_args(args):
    return True


def main(args):
    example_utils.load_logging_config(args)

    logger.debug(args)

    if not validate_args(args):
        return

    diff_annotation_specs(args.project_id1, args.project_id2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="プロジェクト間のアノテーション仕様の差分を表示する。"
        "AnnoFab認証情報は`.netrc`に記載すること")

    parser.add_argument('project_id1',
                        type=str,
                        help='比較対象のプロジェクトのproject_id')

    parser.add_argument('project_id2',
                        type=str,
                        help='比較対象のプロジェクトのproject_id')


    example_utils.add_common_arguments_to_parser(parser)

    service = annofabapi.build_from_netrc()
    examples_wrapper = ExamplesWrapper(service)

    try:
        main(parser.parse_args())

    except Exception as e:
        logger.exception(e)
