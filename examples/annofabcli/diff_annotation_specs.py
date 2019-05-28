"""
プロジェクト間のアノテーション仕様の差分を表示する。
"""

import argparse
import copy
import logging
import pprint
from typing import Any, Dict, List  # pylint: disable=unused-import

import dictdiffer

import annofabcli
import annofabapi
from annofabcli.common.utils import AnnofabApiFacade


logger = logging.getLogger(__name__)


def get_label_name_en(label: Dict[str, Any]):
    """label情報から英語名を取得する"""
    label_name_messages = label["label_name"]["messages"]
    return [e["message"] for e in label_name_messages
            if e["lang"] == "en-US"][0]


def sorted_inspection_phrases(phrases: List[Dict[str, Any]]):
    return sorted(phrases, key=lambda e: e["id"])


def create_ignored_label(label: Dict[str, Any]):
    """
    比較対象外のkeyを削除したラベル情報を生成する
    Args:
        label: l

    Returns:

    """
    """比較対象外のkeyを削除したラベル情報を生成する"""
    copied_label = copy.deepcopy(label)
    copied_label.pop("label_id", None)

    additional_data_definitions = copied_label["additional_data_definitions"]
    for additional_data in additional_data_definitions:
        additional_data.pop("additional_data_definition_id", None)
        choices = additional_data["choices"]
        for choice in choices:
            choice.pop("choice_id", None)

    return copied_label


def diff_labels_of_annotation_specs(labels1: List[Dict[str, Any]],
                                    labels2: List[Dict[str, Any]]) -> bool:
    """
    アノテーションラベル情報の差分を表示する。ラベル名(英語)を基準に差分を表示する。
    以下の項目は無視して比較する。
     * label_id
     * additional_data_definition_id
     * choice_id
    Args:
        labels1: 比較対象のラベル情報
        labels2: 比較対象のラベル情報

    Returns:
        差分があれば Trueを返す
    """
    print("=== アノテーションラベル情報の差分を確認 ===")

    label_names1 = [get_label_name_en(e) for e in labels1]
    label_names2 = [get_label_name_en(e) for e in labels2]

    if label_names1 != label_names2:
        print("ラベル名(en)のListに差分あり")
        print(f"label_names1: {label_names1}")
        print(f"label_names2: {label_names2}")
        return True

    is_different = False
    for label1, label2 in zip(labels1, labels2):

        diff_result = list(
            dictdiffer.diff(create_ignored_label(label1),
                            create_ignored_label(label2)))
        if len(diff_result) > 0:
            is_different = True
            print(f"差分のあるラベル情報: {get_label_name_en(label1)}")
            pprint.pprint(diff_result)

    if not is_different:
        print("アノテーションラベル情報は同一")

    return is_different


def diff_inspection_phrases(inspection_phrases1: List[Dict[str, Any]],
                            inspection_phrases2: List[Dict[str, Any]]) -> bool:
    """
    定型指摘の差分を表示する。定型指摘IDを基準に差分を表示する。

    Args:
        inspection_phrases1: 比較対象の定型指摘List
        inspection_phrases2: 比較対象の定型指摘List

    Returns:
        差分があれば Trueを返す

    """
    print("=== 定型指摘の差分を確認 ===")

    # 定型指摘は順番に意味がないので、ソートしたリストを比較する
    sorted_inspection_phrases1 = sorted_inspection_phrases(inspection_phrases1)
    sorted_inspection_phrases2 = sorted_inspection_phrases(inspection_phrases2)

    phrase_ids1 = [e["id"] for e in sorted_inspection_phrases1]
    phrase_ids2 = [e["id"] for e in sorted_inspection_phrases2]

    if phrase_ids1 != phrase_ids2:
        print("定型指摘IDのListに差分あり")
        print(
            f"set(phrase_ids1) - set(phrase_ids2) = {set(phrase_ids1) - set(phrase_ids2)}"
        )
        print(
            f"set(phrase_ids2) - set(phrase_ids1) = {set(phrase_ids2) - set(phrase_ids1)}"
        )
        return True

    is_different = False
    for phrase1, phrase2 in zip(sorted_inspection_phrases1,
                                sorted_inspection_phrases2):
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

    diff_inspection_phrases(annotation_specs1["inspection_phrases"],
                            annotation_specs2["inspection_phrases"])

    diff_labels_of_annotation_specs(annotation_specs1["labels"],
                                    annotation_specs2["labels"])


def validate_args(args):
    return True


def main(args):
    annofabcli.utils.load_logging_config_from_args(args, __file__)

    logger.info(f"args: {args}")

    if not validate_args(args):
        return

    diff_annotation_specs(args.project_id1, args.project_id2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="プロジェクト間のアノテーション仕様の差分を表示する。"
                                     "ただし、label_idなどAnnoFab内で生成されるIDは比較しない。"
                                     "AnnoFab認証情報は`.netrc`に記載すること")

    parser.add_argument('project_id1', type=str, help='比較対象のプロジェクトのproject_id')

    parser.add_argument('project_id2', type=str, help='比較対象のプロジェクトのproject_id')

    annofabcli.utils.add_common_arguments_to_parser(parser)

    service = annofabapi.build_from_netrc()
    examples_wrapper = AnnofabApiFacade(service)

    try:
        main(parser.parse_args())

    except Exception as e:
        logger.exception(e)
