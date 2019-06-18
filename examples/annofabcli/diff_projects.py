"""
プロジェクト間の差分を表示する。
"""

import argparse
import copy
import logging
import pprint
from typing import Any, Dict, List  # pylint: disable=unused-import

import annofabapi
import annofabcli
import dictdiffer
from annofabcli.common.utils import AnnofabApiFacade

logger = logging.getLogger(__name__)


def sorted_inspection_phrases(phrases: List[Dict[str, Any]]):
    return sorted(phrases, key=lambda e: e["id"])


def sorted_project_members(project_members: List[Dict[str, Any]]):
    return sorted(project_members, key=lambda e: e["user_id"])


def create_ignored_label(label: Dict[str, Any]):
    """
    比較対象外のkeyを削除したラベル情報を生成する
    """
    
    copied_label = copy.deepcopy(label)
    copied_label.pop("label_id", None)

    additional_data_definitions = copied_label["additional_data_definitions"]
    for additional_data in additional_data_definitions:
        additional_data.pop("additional_data_definition_id", None)
        choices = additional_data["choices"]
        for choice in choices:
            choice.pop("choice_id", None)

    return copied_label


class DiffProjecs:
    """
    プロジェクト間の差分を表示する
    """

    def __init__(self, service: annofabapi.Resource, facade: AnnofabApiFacade):
        self.service = service
        self.facade = facade

    def diff_project_members(self, project_id1: str, project_id2: str):
        """
        プロジェクト間のプロジェクトメンバの差分を表示する。
        Args:
            project_id1: 比較対象のプロジェクトのproject_id
            project_id2: 比較対象のプロジェクトのproject_id

        Returns:
            差分があれば Trueを返す

        """
        print("=== プロジェクトメンバの差分 ===")

        project_members1 = self.service.wrapper.get_all_project_members(
            project_id1)
        project_members2 = self.service.wrapper.get_all_project_members(
            project_id2)

        # プロジェクトメンバは順番に意味がないので、ソートしたリストを比較する
        sorted_members1 = sorted_project_members(project_members1)
        sorted_members2 = sorted_project_members(project_members2)

        user_ids1 = [e["user_id"] for e in sorted_members1]
        user_ids2 = [e["user_id"] for e in sorted_members2]

        if user_ids1 != user_ids2:
            print("user_idのListに差分あり")
            print(
                f"set(user_ids1) - set(user_ids2) = {set(user_ids1) - set(user_ids2)}"
            )
            print(
                f"set(user_ids2) - set(user_ids1) = {set(user_ids2) - set(user_ids1)}"
            )
            return True

        is_different = False
        for member1, member2 in zip(sorted_members1, sorted_members2):
            ignored_key = {
                "updated_datetime", "created_datetime", "project_id"
            }
            diff_result = list(
                dictdiffer.diff(member1, member2, ignore=ignored_key))
            if len(diff_result) > 0:
                is_different = True
                print(f"差分のあるuser_id: {member1['user_id']}")
                pprint.pprint(diff_result)

        if not is_different:
            print("プロジェクトメンバは同一")

        return is_different

    def diff_labels_of_annotation_specs(self, labels1: List[Dict[str, Any]],
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
        print("=== アノテーションラベル情報の差分 ===")

        label_names1 = [self.facade.get_label_name_en(e) for e in labels1]
        label_names2 = [self.facade.get_label_name_en(e) for e in labels2]

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
                print(f"差分のあるラベル情報: {self.facade.get_label_name_en(label1)}")
                pprint.pprint(diff_result)

        if not is_different:
            print("アノテーションラベル情報は同一")

        return is_different

    def diff_inspection_phrases(self,
                                inspection_phrases1: List[Dict[str, Any]],
                                inspection_phrases2: List[Dict[str, Any]]
                                ) -> bool:
        """
        定型指摘の差分を表示する。定型指摘IDを基準に差分を表示する。

        Args:
            inspection_phrases1: 比較対象の定型指摘List
            inspection_phrases2: 比較対象の定型指摘List

        Returns:
            差分があれば Trueを返す

        """
        print("=== 定型指摘の差分 ===")

        # 定型指摘は順番に意味がないので、ソートしたリストを比較する
        sorted_inspection_phrases1 = sorted_inspection_phrases(
            inspection_phrases1)
        sorted_inspection_phrases2 = sorted_inspection_phrases(
            inspection_phrases2)

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

    def diff_annotation_specs(self, project_id1: str, project_id2: str,
                              diff_targets: List[str]):
        """
        プロジェクト間のアノテーション仕様の差分を表示する。
        Args:
            project_id1: 比較対象のプロジェクトのproject_id
            project_id2: 比較対象のプロジェクトのproject_id
            diff_targets: 比較対象の項目

        """

        annotation_specs1, _ = self.service.api.get_annotation_specs(
            project_id1)
        annotation_specs2, _ = self.service.api.get_annotation_specs(
            project_id2)

        if "inspection_phrases" in diff_targets:
            self.diff_inspection_phrases(
                annotation_specs1["inspection_phrases"],
                annotation_specs2["inspection_phrases"])

        if "annotation_labels" in diff_targets:
            self.diff_labels_of_annotation_specs(annotation_specs1["labels"],
                                                 annotation_specs2["labels"])

    def diff_project_settingss(self, project_id1: str, project_id2: str):
        """
        プロジェクト間のプロジェクト設定の差分を表示する。
        Args:
            project_id1: 比較対象のプロジェクトのproject_id
            project_id2: 比較対象のプロジェクトのproject_id


        Returns:
            差分があれば Trueを返す

        """
        print("=== プロジェクト設定の差分 ===")

        config1 = self.service.api.get_project(project_id1)[0]["configuration"]
        config2 = self.service.api.get_project(project_id2)[0]["configuration"]

        # ignored_key = {"updated_datetime", "created_datetime", "project_id"}
        diff_result = list(dictdiffer.diff(config1, config2))
        if len(diff_result) > 0:
            print("プロジェクト設定に差分あり")
            pprint.pprint(diff_result)
            return True
        else:
            print("プロジェクト設定は同一")
            return False

    def main(self, args):
        annofabcli.utils.load_logging_config_from_args(args, __file__)

        logger.info(f"args: {args}")

        project_id1 = args.project_id1
        project_id2 = args.project_id2
        project_title1 = self.facade.get_project_title(project_id1)
        project_title2 = self.facade.get_project_title(project_id2)

        print(
            f"=== {project_title1}({project_id1}) と {project_title2}({project_id1}) の差分を表示"
        )

        diff_targets = args.target
        if "members" in diff_targets:
            self.diff_project_members(project_id1, project_id2)

        if "settings" in diff_targets:
            self.diff_project_settingss(project_id1, project_id2)

        if "annotation_labels" in diff_targets or "inspection_phrases" in diff_targets:
            self.diff_annotation_specs(project_id1, project_id2, diff_targets)


def parse_args(parser: argparse.ArgumentParser):
    parser.add_argument('project_id1', type=str, help='比較対象のプロジェクトのproject_id')

    parser.add_argument('project_id2', type=str, help='比較対象のプロジェクトのproject_id')

    parser.add_argument('--target',
                        type=str,
                        nargs="+",
                        choices=[
                            "annotation_labels", "inspection_phrases",
                            "members", "settings"
                        ],
                        default=[
                            "annotation_labels", "inspection_phrases",
                            "members", "settings"
                        ],
                        help='比較する項目。指定しなければ全項目を比較する。'
                        'annotation_labels: アノテーション仕様のラベル情報, '
                        'inspection_phrases: 定型指摘,'
                        'members: プロジェクトメンバ,'
                        'settings: プロジェクト設定,')

    parser.set_defaults(subcommand_func=main)


def main(args):
    try:
        service = annofabapi.build_from_netrc()
        facade = AnnofabApiFacade(service)

        DiffProjecs(service, facade).main(args)

    except Exception as e:
        logger.exception(e)
