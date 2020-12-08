# pylint: disable=too-many-lines
import copy
import logging
import mimetypes
import time
import urllib
import urllib.parse
import uuid
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import requests

from annofabapi import AnnofabApi
from annofabapi.exceptions import AnnofabApiException
from annofabapi.models import (
    AdditionalData,
    AdditionalDataDefinitionType,
    AdditionalDataDefinitionV1,
    AnnotationDataHoldingType,
    AnnotationDetail,
    AnnotationSpecsV1,
    FullAnnotationData,
    InputData,
    Inspection,
    InspectionStatus,
    Instruction,
    JobInfo,
    JobStatus,
    JobType,
    LabelV1,
    MyOrganization,
    Organization,
    OrganizationMember,
    Project,
    ProjectMember,
    SimpleAnnotationDetail,
    SupplementaryData,
    Task,
    TaskStatus,
)
from annofabapi.parser import SimpleAnnotationDirParser, SimpleAnnotationParser
from annofabapi.utils import _download, _log_error_response, _raise_for_status, allow_404_error, str_now

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TaskFrameKey:
    project_id: str
    task_id: str
    input_data_id: str


@dataclass(frozen=True)
class ChoiceKey:
    additional_data_definition_id: str
    choice_id: str


@dataclass(frozen=True)
class AnnotationSpecsRelation:
    label_id: Dict[str, str]
    additional_data_definition_id: Dict[str, str]
    choice_id: Dict[ChoiceKey, ChoiceKey]


def _first_true(iterable, default=None, pred=None):
    return next(filter(pred, iterable), default)


class Wrapper:
    """
    AnnofabApiのラッパー.

    Args:
        api: AnnofabApi Instance

    """

    def __init__(self, api: AnnofabApi):
        self.api = api

    #########################################
    # Private Method
    #########################################
    @staticmethod
    def _get_content_type(file_path: str, content_type: Optional[str] = None) -> str:
        """
        ファイルパスからContent-Typeを取得する。

        Args:
            file_path: アップロードするファイルのパス
            content_type: アップロードするファイルのMIME Type. Noneの場合、ファイルパスから推測する。

        Returns:
            APIに渡すContent-Type

        Raises:
            AnnofabApiException: Content-Typeを取得できなかった

        """

        if content_type is None:
            new_content_type = mimetypes.guess_type(file_path)[0]
            if new_content_type is None:
                logger.info("mimetypes.guess_type function can't guess type. file_path = %s", file_path)
                new_content_type = content_type

        else:
            new_content_type = content_type

        if new_content_type is None:
            raise AnnofabApiException("content_type is none")

        return new_content_type

    @staticmethod
    def _get_all_objects(func_get_list: Callable, limit: int, **kwargs_for_func_get_list) -> List[Dict[str, Any]]:
        """
        get_all_XXX関数の共通処理

        Args:ｃ
            func_get_list: AnnofabApiのget_XXX関数
            limit: 1ページあたりの取得するデータ件数
            **kwargs_for_func_get_list: `func_get_list`に渡す引数。

        Returns:
            get_XXX関数で取得した情報の一覧

        """
        arg_query_params = kwargs_for_func_get_list.get("query_params")
        copied_query_params = copy.deepcopy(arg_query_params) if arg_query_params is not None else {}

        all_objects: List[Dict[str, Any]] = []

        copied_query_params.update({"page": 1, "limit": limit})
        kwargs_for_func_get_list["query_params"] = copied_query_params
        content, _ = func_get_list(**kwargs_for_func_get_list)

        logger.debug("%s %d 件 取得します。", func_get_list.__name__, content.get("total_count"))
        if content.get("over_limit"):
            logger.warning("検索結果が10,000件を超えてますが、Web APIの都合上10,000件までしか取得できません。")

        all_objects.extend(content["list"])

        while content["page_no"] < content["total_page_no"]:
            next_page_no = content["page_no"] + 1
            copied_query_params.update({"page": next_page_no})
            kwargs_for_func_get_list["query_params"] = copied_query_params
            content, _ = func_get_list(**kwargs_for_func_get_list)
            all_objects.extend(content["list"])
            logger.debug("%s %d / %d page", func_get_list.__name__, content["page_no"], content["total_page_no"])

        return all_objects

    #########################################
    # Public Method : Annotation
    #########################################
    def download_annotation_archive(self, project_id: str, dest_path: str, v2: bool = False) -> str:
        """
        simpleアノテーションZIPをダウンロードする。

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先のファイルパス
            v2:  互換性を保つために残している引数。2020-10-31以降に廃止する。

        Returns:
            ダウンロード元のURL

        """
        query_params = None
        if v2:
            query_params = {"v2": True}
            logger.warning("メソッド引数`v2`は2020-10-31以降に廃止します。")

        _, response = self.api.get_annotation_archive(project_id, query_params=query_params)
        url = response.headers["Location"]
        response2 = _download(url, dest_path)
        logger.debug(f"type=simple_annotation, Last-Modified={response2.headers.get('Last-Modified')}")
        return url

    def download_full_annotation_archive(self, project_id: str, dest_path: str) -> str:
        """
        FullアノテーションZIPをダウンロードする。

        .. deprecated:: X

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先のファイルパス

        Returns:
            ダウンロード元のURL

        """
        warnings.warn("deprecated", DeprecationWarning)
        _, response = self.api.get_archive_full_with_pro_id(project_id)
        url = response.headers["Location"]
        response2 = _download(url, dest_path)
        logger.debug(f"type=full_annotation, Last-Modified={response2.headers.get('Last-Modified')}")
        return url

    def get_all_annotation_list(
        self, project_id: str, query_params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        すべてのアノテーション情報を取得する。

        Args:
            project_id: プロジェクトID
            query_params: `api.get_annotation_list` メソッドのQuery Parameter

        Returns:l
            すべてのアノテーション一覧
        """
        return self._get_all_objects(
            self.api.get_annotation_list, limit=200, project_id=project_id, query_params=query_params
        )

    @staticmethod
    def __create_annotation_id(detail: Dict[str, Any]) -> str:
        if detail["data_holding_type"] == AnnotationDataHoldingType.INNER.value and detail["data"] is None:
            # annotation_typeがclassificationのときは、label_idとannotation_idを一致させる必要がある。
            return detail["label_id"]
        else:
            return str(uuid.uuid4())

    @staticmethod
    def __replace_annotation_specs_id(
        detail: Dict[str, Any], annotation_specs_relation: AnnotationSpecsRelation
    ) -> Optional[Dict[str, Any]]:
        """
        アノテーション仕様関係のIDを、新しいIDに置換する。

        Args:
            detail: (IN/OUT) １個のアノテーション詳細情報

        Returns:
            IDを置換した後のアノテーション詳細情報.
        """
        label_id = detail["label_id"]

        new_label_id = annotation_specs_relation.label_id.get(label_id)
        if new_label_id is None:
            return None
        else:
            detail["label_id"] = new_label_id

        additional_data_list = detail["additional_data_list"]
        new_additional_data_list = []
        for additional_data in additional_data_list:
            additional_data_definition_id = additional_data["additional_data_definition_id"]
            new_additional_data_definition_id = annotation_specs_relation.additional_data_definition_id.get(
                additional_data_definition_id
            )
            if new_additional_data_definition_id is None:
                continue
            additional_data["additional_data_definition_id"] = new_additional_data_definition_id

            if additional_data["choice"] is not None:
                new_choice = annotation_specs_relation.choice_id.get(
                    ChoiceKey(additional_data_definition_id, additional_data["choice"])
                )
                additional_data["choice"] = new_choice.choice_id if new_choice is not None else None

            new_additional_data_list.append(additional_data)

        detail["additional_data_list"] = new_additional_data_list
        return detail

    def __to_dest_annotation_detail(
        self,
        dest_project_id: str,
        detail: Dict[str, Any],
        account_id: str,
    ) -> Dict[str, Any]:
        """
        コピー元の１個のアノテーションを、コピー先用に変換する。
        塗りつぶし画像の場合、S3にアップロードする。

        Notes:
            annotation_id をUUIDv4で生成すると、アノテーションリンク属性をコピーしたときに対応できないので、暫定的にannotation_idは維持するようにする。
        """
        dest_detail = detail
        dest_detail["account_id"] = account_id
        if detail["data_holding_type"] == AnnotationDataHoldingType.OUTER.value:
            outer_file_url = detail["url"]
            src_response = self.api.session.get(outer_file_url)
            s3_path = self.upload_data_to_s3(
                dest_project_id, data=src_response.content, content_type=src_response.headers["Content-Type"]
            )
            logger.debug("%s に塗りつぶし画像をアップロードしました。", s3_path)
            dest_detail["path"] = s3_path
            dest_detail["url"] = None
            dest_detail["etag"] = None

        return dest_detail

    def __create_request_body_for_copy_annotation(
        self,
        project_id: str,
        task_id: str,
        input_data_id: str,
        src_details: List[Dict[str, Any]],
        account_id: str,
        annotation_specs_relation: Optional[AnnotationSpecsRelation] = None,
    ) -> Dict[str, Any]:
        dest_details: List[Dict[str, Any]] = []

        for src_detail in src_details:
            if annotation_specs_relation is not None:
                tmp_detail = self.__replace_annotation_specs_id(src_detail, annotation_specs_relation)
                if tmp_detail is None:
                    continue
                src_detail = tmp_detail

            dest_detail = self.__to_dest_annotation_detail(project_id, src_detail, account_id=account_id)
            dest_details.append(dest_detail)

        request_body = {
            "project_id": project_id,
            "task_id": task_id,
            "input_data_id": input_data_id,
            "details": dest_details,
        }
        return request_body

    def copy_annotation(
        self,
        src: TaskFrameKey,
        dest: TaskFrameKey,
        account_id: Optional[str] = None,
        annotation_specs_relation: Optional[AnnotationSpecsRelation] = None,
    ) -> bool:
        """
        アノテーションをコピーする。

        Args:
            src: コピー元のTaskFrame情報
            dest: コピー先のTaskFrame情報
            account_id: アノテーションを登録するユーザのアカウントID。Noneの場合、自分自身のアカウントIDで登録する。
            annotation_specs_relation: アノテーション仕様間の紐付け情報。``get_annotation_specs_relation`` メソッドで紐付け情報を取得できる。
                Noneの場合、コピー元のアノテーション仕様のID情報（ラベルID、属性ID、選択肢ID）を変換せずに、アノテーションをコピーします。

        Returns:
            アノテーションのコピー実施したかどうか

        """
        src_annotation, _ = self.api.get_editor_annotation(src.project_id, src.task_id, src.input_data_id)
        src_annotation_details: List[Dict[str, Any]] = src_annotation["details"]

        if len(src_annotation_details) == 0:
            logger.debug("コピー元にアノテーションが１つもないため、アノテーションのコピーをスキップします。")
            return False

        old_dest_annotation, _ = self.api.get_editor_annotation(dest.project_id, dest.task_id, dest.input_data_id)
        updated_datetime = old_dest_annotation["updated_datetime"]

        request_body = self.__create_request_body_for_copy_annotation(
            dest.project_id,
            dest.task_id,
            dest.input_data_id,
            src_details=src_annotation_details,
            account_id=account_id if account_id is not None else self.api.account_id,
            annotation_specs_relation=annotation_specs_relation,
        )
        request_body["updated_datetime"] = updated_datetime
        self.api.put_annotation(dest.project_id, dest.task_id, dest.input_data_id, request_body=request_body)
        return True

    def __get_label_info_from_label_name(
        self, label_name: str, annotation_specs_labels: List[LabelV1]
    ) -> Optional[LabelV1]:
        for label in annotation_specs_labels:
            if self.__get_label_name_en(label) == label_name:
                return label
        return None

    def __get_additional_data_from_attribute_name(
        self, attribute_name: str, label_info: LabelV1
    ) -> Optional[AdditionalDataDefinitionV1]:
        for additional_data in label_info["additional_data_definitions"]:
            if self.__get_additional_data_definition_name_en(additional_data) == attribute_name:
                return additional_data

        return None

    def _get_choice_id_from_name(self, name: str, choices: List[Dict[str, Any]]) -> Optional[str]:
        choice_info = _first_true(choices, pred=lambda e: self.__get_choice_name_en(e) == name)
        if choice_info is not None:
            return choice_info["choice_id"]
        else:
            return None

    @staticmethod
    def __get_data_holding_type_from_data(data: FullAnnotationData) -> str:
        if data["_type"] in ["Segmentation", "SegmentationV2"]:
            return AnnotationDataHoldingType.OUTER.value
        else:
            return AnnotationDataHoldingType.INNER.value

    @staticmethod
    def _create_annotation_id(data: FullAnnotationData, label_id: str) -> str:
        if data["_type"] == "Classification":
            return label_id
        else:
            return str(uuid.uuid4())

    def __to_additional_data_list(self, attributes: Dict[str, Any], label_info: LabelV1) -> List[AdditionalData]:
        additional_data_list: List[AdditionalData] = []
        for key, value in attributes.items():
            specs_additional_data = self.__get_additional_data_from_attribute_name(key, label_info)
            if specs_additional_data is None:
                logger.warning(f"アノテーション仕様に attribute_name='{key}' の属性が存在しません。")
                continue

            additional_data = dict(
                additional_data_definition_id=specs_additional_data["additional_data_definition_id"],
                flag=None,
                integer=None,
                choice=None,
                comment=None,
            )
            additional_data_type = specs_additional_data["type"]
            if additional_data_type == AdditionalDataDefinitionType.FLAG.value:
                additional_data["flag"] = value
            elif additional_data_type == AdditionalDataDefinitionType.INTEGER.value:
                additional_data["integer"] = value
            elif additional_data_type in [
                AdditionalDataDefinitionType.TEXT.value,
                AdditionalDataDefinitionType.COMMENT.value,
                AdditionalDataDefinitionType.TRACKING.value,
                AdditionalDataDefinitionType.LINK.value,
            ]:
                additional_data["comment"] = value
            elif additional_data_type in [
                AdditionalDataDefinitionType.CHOICE.value,
                AdditionalDataDefinitionType.SELECT.value,
            ]:
                additional_data["choice"] = self._get_choice_id_from_name(value, specs_additional_data["choices"])
            else:
                logger.warning(f"additional_data_type={additional_data_type}が不正です。")
                continue

            additional_data_list.append(additional_data)

        return additional_data_list

    def __to_annotation_detail_for_request(
        self,
        project_id: str,
        parser: SimpleAnnotationParser,
        detail: SimpleAnnotationDetail,
        annotation_specs_labels: List[LabelV1],
    ) -> Optional[AnnotationDetail]:
        """
        Request Bodyに渡すDataClassに変換する。塗りつぶし画像があれば、それをS3にアップロードする。

        Args:
            project_id:
            parser:
            detail:

        Returns:

        """
        label_info = self.__get_label_info_from_label_name(detail["label"], annotation_specs_labels)
        if label_info is None:
            logger.warning(f"アノテーション仕様に '{detail['label']}' のラベルが存在しません。")
            return None

        additional_data_list: List[AdditionalData] = self.__to_additional_data_list(detail["attributes"], label_info)
        data_holding_type = self.__get_data_holding_type_from_data(detail["data"])

        dest_obj = dict(
            label_id=label_info["label_id"],
            annotation_id=detail["annotation_id"] if detail.get("annotation_id") is not None else str(uuid.uuid4()),
            account_id=self.api.account_id,
            data_holding_type=data_holding_type,
            data=detail["data"],
            additional_data_list=additional_data_list,
            is_protected=False,
            etag=None,
            url=None,
            path=None,
            created_datetime=None,
            updated_datetime=None,
        )

        if data_holding_type == AnnotationDataHoldingType.OUTER.value:
            data_uri = detail["data"]["data_uri"]
            with parser.open_outer_file(data_uri) as f:
                s3_path = self.upload_data_to_s3(project_id, f, content_type="image/png")
                dest_obj["path"] = s3_path
                logger.debug(f"{parser.task_id}/{parser.input_data_id}/{data_uri} をS3にアップロードしました。")

        return dest_obj

    def put_annotation_for_simple_annotation_json(
        self,
        project_id: str,
        task_id: str,
        input_data_id: str,
        simple_annotation_json: str,
        annotation_specs_labels: List[LabelV1],
    ) -> bool:
        """
        AnnoFabからダウンロードしたアノテーションzip配下のJSONと同じフォーマット（Simple Annotation)の内容から、アノテーションを登録する。

        Args:
            project_id:
            task_id:
            input_data_id:
            simple_annotation_json:

        Returns:
            True:アノテーション情報をした。False: 登録するアノテーション情報がなかったため、登録しなかった。
        """
        parser = SimpleAnnotationDirParser(Path(simple_annotation_json))
        annotation = parser.load_json()

        details = annotation["details"]
        if len(details) == 0:
            logger.warning(f"simple_annotation_json='{simple_annotation_json}'にアノテーション情報は記載されていなかったので、スキップします。")
            return False

        request_details: List[Dict[str, Any]] = []
        for detail in details:
            request_detail = self.__to_annotation_detail_for_request(
                project_id, parser, detail, annotation_specs_labels
            )
            if request_detail is not None:
                request_details.append(request_detail)
        if len(request_details) == 0:
            logger.warning(f"simple_annotation_json='{simple_annotation_json}'に、登録できるアノテーションはなかったので、スキップします。")
            return False

        old_annotation, _ = self.api.get_editor_annotation(project_id, task_id, input_data_id)
        updated_datetime = old_annotation["updated_datetime"] if old_annotation is not None else None

        request_body = {
            "project_id": project_id,
            "task_id": task_id,
            "input_data_id": input_data_id,
            "details": request_details,
            "updated_datetime": updated_datetime,
        }
        self.api.put_annotation(project_id, task_id, input_data_id, request_body=request_body)
        return True

    #########################################
    # Public Method : AnnotationSpecs
    #########################################
    def copy_annotation_specs(
        self, src_project_id: str, dest_project_id: str, comment: Optional[str] = None
    ) -> AnnotationSpecsV1:
        """
        アノテーション仕様を、別のプロジェクトにコピーする。

        Note:
            誤って実行しないようにすること

        Args:
            src_project_id: コピー元のproject_id
            dest_project_id: コピー先のproject_id
            comment: アノテーション仕様を保存するときのコメント。Noneならば、コピーした旨を記載する。

        Returns:
            put_annotation_specsのContent
        """
        src_annotation_specs = self.api.get_annotation_specs(src_project_id)[0]

        if comment is None:
            comment = f"Copied the annotation specification of project {src_project_id} on {str_now()}"

        request_body = {
            "labels": src_annotation_specs["labels"],
            "inspection_phrases": src_annotation_specs["inspection_phrases"],
            "comment": comment,
        }
        return self.api.put_annotation_specs(dest_project_id, request_body=request_body)[0]

    @staticmethod
    def __get_label_name_en(label: Dict[str, Any]) -> str:
        """label情報から英語名を取得する"""
        label_name_messages = label["label_name"]["messages"]
        return [e["message"] for e in label_name_messages if e["lang"] == "en-US"][0]

    @staticmethod
    def __get_additional_data_definition_name_en(additional_data_definition: Dict[str, Any]) -> str:
        """additional_data_definitionから英語名を取得する"""
        messages = additional_data_definition["name"]["messages"]
        return [e["message"] for e in messages if e["lang"] == "en-US"][0]

    @staticmethod
    def __get_choice_name_en(choice: Dict[str, Any]) -> str:
        """choiceから英語名を取得する"""
        messages = choice["name"]["messages"]
        return [e["message"] for e in messages if e["lang"] == "en-US"][0]

    def __get_dest_additional(
        self,
        src_additional: Dict[str, Any],
        dest_additionals: List[Dict[str, Any]],
        src_labels: List[Dict[str, Any]],
        dest_labels: List[Dict[str, Any]],
        dict_label_id: Dict[str, str],
    ) -> Optional[Dict[str, Any]]:
        src_additional_name_en = self.__get_additional_data_definition_name_en(src_additional)
        for dest_additional in dest_additionals:
            if src_additional_name_en != self.__get_additional_data_definition_name_en(dest_additional):
                continue

            dest_label_contains_dest_additional = True
            for src_label in src_labels:
                if src_additional["additional_data_definition_id"] in src_label["additional_data_definitions"]:
                    dest_label_id = dict_label_id.get(src_label["label_id"])
                    if dest_label_id is None:
                        dest_label_contains_dest_additional = False
                        break

                    dest_label = _first_true(dest_labels, pred=lambda e, f=dest_label_id: e["label_id"] == f)
                    if dest_label is None:
                        dest_label_contains_dest_additional = False
                        break
                    if (
                        dest_additional["additional_data_definition_id"]
                        not in dest_label["additional_data_definitions"]
                    ):
                        dest_label_contains_dest_additional = False
                        break

            if dest_label_contains_dest_additional:
                return dest_additional

        return None

    def get_annotation_specs_relation(self, src_project_id: str, dest_project_id: str) -> AnnotationSpecsRelation:
        """
        プロジェクト間のアノテーション仕様の紐付け情報を取得する。
        ラベル、属性、選択肢の英語名で紐付ける。
        ただし、属性は、参照されるラベルが一致していることも判定する。
        紐付け先がない場合は無視する。

        Args:
            src_project_id: 紐付け元のプロジェクトID
            dest_project_id: 紐付け先のプロジェクトID

        Returns:
            アノテーション仕様の紐付け情報

        """
        src_annotation_specs, _ = self.api.get_annotation_specs(src_project_id, query_params={"v": "2"})
        dest_annotation_specs, _ = self.api.get_annotation_specs(dest_project_id, query_params={"v": "2"})
        dest_labels = dest_annotation_specs["labels"]
        dest_additionals = dest_annotation_specs["additionals"]

        dict_label_id: Dict[str, str] = {}
        for src_label in src_annotation_specs["labels"]:
            src_label_name_en = self.__get_label_name_en(src_label)
            dest_label = _first_true(dest_labels, pred=lambda e, f=src_label_name_en: self.__get_label_name_en(e) == f)
            if dest_label is not None:
                dict_label_id[src_label["label_id"]] = dest_label["label_id"]

        dict_additional_data_definition_id: Dict[str, str] = {}
        dict_choice_id: Dict[ChoiceKey, ChoiceKey] = {}
        for src_additional in src_annotation_specs["additionals"]:
            dest_additional = self.__get_dest_additional(
                src_additional=src_additional,
                dest_additionals=dest_additionals,
                src_labels=src_annotation_specs["labels"],
                dest_labels=dest_labels,
                dict_label_id=dict_label_id,
            )
            if dest_additional is None:
                continue

            dict_additional_data_definition_id[src_additional["additional_data_definition_id"]] = dest_additional[
                "additional_data_definition_id"
            ]

            dest_choices = dest_additional["choices"]
            for src_choice in src_additional["choices"]:
                src_choice_name_en = self.__get_choice_name_en(src_choice)
                dest_choice = _first_true(
                    dest_choices, pred=lambda e, f=src_choice_name_en: self.__get_choice_name_en(e) == f
                )
                if dest_choice is not None:
                    dict_choice_id[
                        ChoiceKey(src_additional["additional_data_definition_id"], src_choice["choice_id"])
                    ] = ChoiceKey(dest_additional["additional_data_definition_id"], dest_choice["choice_id"])

        return AnnotationSpecsRelation(
            label_id=dict_label_id,
            additional_data_definition_id=dict_additional_data_definition_id,
            choice_id=dict_choice_id,
        )

    #########################################
    # Public Method : Input
    #########################################
    @allow_404_error
    def get_input_data_or_none(self, project_id: str, input_data_id: str) -> Optional[InputData]:
        """
        入力データを取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            project_id:
            input_data_id:

        Returns:
            入力データ
        """
        input_data, _ = self.api.get_input_data(project_id, input_data_id)
        return input_data

    def get_all_input_data_list(
        self, project_id: str, query_params: Optional[Dict[str, Any]] = None
    ) -> List[InputData]:
        """
        すべての入力データを取得する。

        Args:
            project_id: プロジェクトID
            query_params: `api.get_input_data_list` メソッドのQuery Parameter

        Returns:
            入力データ一覧
        """
        return self._get_all_objects(
            self.api.get_input_data_list, limit=200, project_id=project_id, query_params=query_params
        )

    def upload_file_to_s3(self, project_id: str, file_path: str, content_type: Optional[str] = None) -> str:
        """
        createTempPath APIを使ってアップロード用のURLとS3パスを取得して、ファイルをアップロードする。

        Args:
            project_id: プロジェクトID
            file_path: アップロードするファイルのパス
            content_type: アップロードするファイルのMIME Type. Noneの場合、ファイルパスから推測する。

        Returns:
            一時データ保存先であるS3パス
        """

        # content_type を推測
        new_content_type = self._get_content_type(file_path, content_type)
        with open(file_path, "rb") as f:
            return self.upload_data_to_s3(project_id, data=f, content_type=new_content_type)

    def upload_data_to_s3(self, project_id: str, data: Any, content_type: str) -> str:
        """
        createTempPath APIを使ってアップロード用のURLとS3パスを取得して、"data" をアップロードする。

        Args:
            project_id: プロジェクトID
            data: アップロード対象のdata. ``requests.put`` メソッドの ``data`` 引数にそのまま渡す。
            content_type: アップロードするfile objectのMIME Type.

        Returns:
            一時データ保存先であるS3パス
        """
        # 一時データ保存先を取得
        content = self.api.create_temp_path(project_id, header_params={"content-type": content_type})[0]

        url_parse_result = urllib.parse.urlparse(content["url"])
        query_dict = urllib.parse.parse_qs(url_parse_result.query)

        # URL Queryを除いたURLを取得する
        s3_url = content["url"].split("?")[0]

        # アップロード
        res_put = self.api.session.put(s3_url, params=query_dict, data=data, headers={"content-type": content_type})

        _log_error_response(logger, res_put)
        _raise_for_status(res_put)
        return content["path"]

    def put_input_data_from_file(
        self,
        project_id: str,
        input_data_id: str,
        file_path: str,
        request_body: Optional[Dict[str, Any]] = None,
        content_type: Optional[str] = None,
    ) -> InputData:
        """
        ファイル（画像データ、動画データ、 zipファイル）を入力データとして登録する。


        Args:
            project_id: プロジェクトID
            input_data_id: 入力データID
            file_path: アップロードするファイルのパス
            request_body: `put_input_data` に渡すrequest body. Keyに`input_data_name` がなければ、ファイルパスが設定される。
            content_type: アップロードするファイルのMIME Type. Noneの場合、ファイルパスから推測する。

        Returns:
            `put_input_data` のcontent

        """

        s3_path = self.upload_file_to_s3(project_id, file_path, content_type)

        copied_request_body = copy.deepcopy(request_body) if request_body is not None else {}

        copied_request_body.update({"input_data_path": s3_path})
        if "input_data_name" not in copied_request_body:
            copied_request_body["input_data_name"] = file_path

        return self.api.put_input_data(project_id, input_data_id, request_body=copied_request_body)[0]

    #########################################
    # Public Method : Statistics
    #########################################
    def _request_location_header_url(self, response: requests.Response) -> Any:
        """
        Location headerに記載されているURLの中身を返す。

        Args:
            response:

        Returns:
            Location headerに記載されているURLの中身

        """
        url = response.headers["Location"]

        response = self.api.session.get(url)
        _log_error_response(logger, response)

        response.encoding = "utf-8"
        _raise_for_status(response)
        content = self.api._response_to_content(response)
        return content

    def get_task_statistics(self, project_id: str) -> List[Any]:
        """
        getTaskStatistics APIのLocation headerの中身を返す。

        Args:
            project_id:  プロジェクトID

        Returns:


        """
        _, response = self.api.get_task_statistics(project_id)
        return self._request_location_header_url(response)

    def get_account_statistics(self, project_id: str) -> List[Any]:
        """
        getAccountStatistics APIのLocation headerの中身を返す。

        Args:
            project_id:

        Returns:

        """
        _, response = self.api.get_account_statistics(project_id)
        return self._request_location_header_url(response)

    def get_inspection_statistics(self, project_id: str) -> List[Any]:
        """
        getInspectionStatistics APIのLocation headerの中身を返す。

        Args:
            project_id:

        Returns:

        """
        _, response = self.api.get_inspection_statistics(project_id)
        return self._request_location_header_url(response)

    def get_task_phase_statistics(self, project_id: str) -> List[Any]:
        """
        getTaskPhaseStatistics APIのLocation headerの中身を返す。

        Args:
            project_id:

        Returns:

        """
        _, response = self.api.get_task_phase_statistics(project_id)
        return self._request_location_header_url(response)

    def get_label_statistics(self, project_id: str) -> List[Any]:
        """
        getLabelStatistics APIのLocation headerの中身を返す。

        Args:
            project_id:

        Returns:

        """
        _, response = self.api.get_label_statistics(project_id)
        return self._request_location_header_url(response)

    def get_worktime_statistics(self, project_id: str) -> List[Any]:
        """
        タスク作業時間集計取得.
        Location Headerに記載されたURLのレスポンスをJSON形式で返す。

        Args:
            project_id:  プロジェクトID

        Returns:
            タスク作業時間集計

        """
        _, response = self.api.get_worktime_statistics(project_id)
        return self._request_location_header_url(response)

    #########################################
    # Public Method : Supplementary
    #########################################
    def put_supplementary_data_from_file(
        self,
        project_id,
        input_data_id: str,
        supplementary_data_id: str,
        file_path: str,
        request_body: Dict[str, Any],
        content_type: Optional[str] = None,
    ) -> SupplementaryData:
        """
        補助情報ファイルをアップロードする

        Args:
            project_id: プロジェクトID
            input_data_id: 入力データID
            supplementary_data_id: 補助情報ID
            file_path: アップロードするファイル(text , image)
            request_body: `put_supplementary_data` に渡すRequest Body.
                `supplementary_data_name` , `supplementary_data_type` は指定されていなければ、ファイルパスから取得した情報が設定される。
            content_type: アップロードするファイルのMIME Type. Noneの場合、ファイルパスから推測する。

        Returns:
            put_supplementary_data のレスポンス

        """

        # content_type を推測
        new_content_type = self._get_content_type(file_path, content_type)

        # S3にファイルアップロード
        s3_path = self.upload_file_to_s3(project_id, file_path, new_content_type)

        copied_request_body = copy.deepcopy(request_body) if request_body is not None else {}

        copied_request_body["supplementary_data_path"] = s3_path

        if "supplementary_data_name" not in copied_request_body:
            copied_request_body["supplementary_data_name"] = file_path

        if "supplementary_data_type" not in copied_request_body:
            if new_content_type.startswith("image"):
                supplementary_data_type = "image"
            elif new_content_type.startswith("text"):
                supplementary_data_type = "text"
            else:
                raise AnnofabApiException(f"File type not supported. Content-Type={new_content_type}")
            copied_request_body["supplementary_data_type"] = supplementary_data_type

        return self.api.put_supplementary_data(
            project_id, input_data_id, supplementary_data_id, request_body=copied_request_body
        )[0]

    #########################################
    # Public Method : Inspection
    #########################################
    def update_status_of_inspections(
        self,
        project_id: str,
        task_id: str,
        input_data_id: str,
        filter_inspection: Callable[[Inspection], bool],
        inspection_status: InspectionStatus,
        updated_datetime: Optional[str] = None,
    ) -> List[Inspection]:
        """
        検査コメント（返信コメント以外）のstatusを変更する。

        Args:
            project_id: プロジェクトID
            task_id: タスクID
            input_data_id: 入力データID
            filter_inspection: 変更対象の検査コメントを絞り込む条件
            inspection_status: 検査コメントのstatus
            updated_datetime: 検査コメントの更新日時。タスクの更新日時以降を指定する必要があります。Noneの場合、現在時刻を指定します。

        Returns:
            `batch_update_inspections` メソッドのcontent
        """

        def not_reply_comment(arg_inspection: Inspection) -> bool:
            """返信コメントでないならTrueをかえす"""
            return arg_inspection["parent_inspection_id"] is None

        def search_updated_inspections(arg_inspection: Inspection) -> bool:
            """変更対象の検査コメントを探す"""
            return filter_inspection(arg_inspection) and not_reply_comment(arg_inspection)

        inspections, _ = self.api.get_inspections(project_id, task_id, input_data_id)

        target_inspections = [e for e in inspections if search_updated_inspections(e)]

        if updated_datetime is None:
            updated_datetime = str_now()
        for inspection in target_inspections:
            inspection["status"] = inspection_status.value
            inspection["updated_datetime"] = updated_datetime

        req_inspection = [{"data": e, "_type": "Put"} for e in target_inspections]
        content = self.api.batch_update_inspections(project_id, task_id, input_data_id, req_inspection)[0]
        return content

    #########################################
    # Public Method : My
    #########################################
    def get_all_my_organizations(self) -> List[MyOrganization]:
        """
        所属しているすべての組織一覧を取得する

        Returns:
            すべての所属一覧
        """
        return self._get_all_objects(self.api.get_my_organizations, limit=200)

    #########################################
    # Public Method : Organization
    #########################################
    @allow_404_error
    def get_organization_or_none(self, organization_name: str) -> Optional[Organization]:
        """
        組織情報を取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            organization_name: 組織名

        Returns:
            組織情報
        """
        content, _ = self.api.get_organization(organization_name)
        return content

    def get_all_projects_of_organization(
        self, organization_name: str, query_params: Optional[Dict[str, Any]] = None
    ) -> List[Project]:
        """
        組織配下のすべてのプロジェクト一覧を取得する

        Args:
            organization_name: 組織名
            query_params: `api.get_projects_of_organization` メソッドに渡すQuery Parameter

        Returns:
            すべてのプロジェクト一覧
        """
        return self._get_all_objects(
            self.api.get_projects_of_organization,
            limit=200,
            organization_name=organization_name,
            query_params=query_params,
        )

    #########################################
    # Public Method : OrganizationMember
    #########################################
    @allow_404_error
    def get_organization_member_or_none(self, organization_name: str, user_id: str) -> Optional[OrganizationMember]:
        """
        組織メンバを取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            organization_name: 組織名
            user_id:

        Returns:
            組織メンバ
        """
        content, _ = self.api.get_organization_member(organization_name, user_id)
        return content

    def get_all_organization_members(self, organization_name: str) -> List[OrganizationMember]:
        """
        すべての組織メンバ一覧を取得する

        Args:
            organization_name: 組織名

        Returns:
            すべての組織メンバ一覧
        """

        # ページングされないので、そのままAPIを実行する
        content, _ = self.api.get_organization_members(organization_name)
        return content["list"]

    #########################################
    # Public Method : Project
    #########################################
    @allow_404_error
    def get_project_or_none(self, project_id: str) -> Optional[Project]:
        """
        プロジェクトを取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            project_id:

        Returns:
            プロジェクト
        """
        content, _ = self.api.get_project(project_id)
        return content

    def download_project_inputs_url(self, project_id: str, dest_path: str) -> str:
        """
        プロジェクトの入力データ全件ファイルをダウンロードする。
        ファイルの中身はJSON。

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先ファイルのパス

        Returns:
            ダウンロード元のURL

        """
        content, _ = self.api.get_project_inputs_url(project_id)
        url = content["url"]
        response2 = _download(url, dest_path)
        logger.debug(f"type=input_data, Last-Modified={response2.headers.get('Last-Modified')}")
        return url

    def download_project_tasks_url(self, project_id: str, dest_path: str) -> str:
        """
        プロジェクトのタスク全件ファイルをダウンロードする。
        ファイルの中身はJSON。

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先ファイルのパス

        Returns:
            ダウンロード元のURL

        """

        content, _ = self.api.get_project_tasks_url(project_id)
        url = content["url"]
        response2 = _download(url, dest_path)
        logger.debug(f"type=task, Last-Modified={response2.headers.get('Last-Modified')}")
        return url

    def download_project_inspections_url(self, project_id: str, dest_path: str) -> str:
        """
        プロジェクトの検査コメント全件ファイルをダウンロードする。
        ファイルの中身はJSON。

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先ファイルのパス

        Returns:
            ダウンロード元のURL

        """

        content, _ = self.api.get_project_inspections_url(project_id)
        url = content["url"]
        response2 = _download(url, dest_path)
        logger.debug(f"type=inspection_comment, Last-Modified={response2.headers.get('Last-Modified')}")
        return url

    def download_project_task_history_events_url(self, project_id: str, dest_path: str) -> str:
        """
        プロジェクトのタスク履歴イベント全件ファイルをダウンロードする。
        ファイルの中身はJSON。

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先ファイルのパス

        Returns:
            ダウンロード元のURL

        """

        content, _ = self.api.get_project_task_history_events_url(project_id)
        url = content["url"]
        response2 = _download(url, dest_path)
        logger.debug(f"type=task_history_event, Last-Modified={response2.headers.get('Last-Modified')}")
        return url

    def download_project_task_histories_url(self, project_id: str, dest_path: str) -> str:
        """
        プロジェクトのタスク履歴全件ファイルをダウンロードする。
        ファイルの中身はJSON。

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先ファイルのパス

        Returns:
            ダウンロード元のURL

        """

        content, _ = self.api.get_project_task_histories_url(project_id)
        url = content["url"]
        response2 = _download(url, dest_path)
        logger.debug(f"type=task_history, Last-Modified={response2.headers.get('Last-Modified')}")
        return url

    #########################################
    # Public Method : ProjectMember
    #########################################
    @allow_404_error
    def get_project_member_or_none(self, project_id: str, user_id: str) -> Optional[ProjectMember]:
        """
        プロジェクトメンバを取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            project_id:
            user_id:

        Returns:
            プロジェクトメンバ
        """
        content, _ = self.api.get_project_member(project_id, user_id)
        return content

    def get_all_project_members(
        self, project_id: str, query_params: Optional[Dict[str, Any]] = None
    ) -> List[ProjectMember]:
        """
        すべてのプロジェクトメンバを取得する.

        Args:
            project_id: プロジェクトID
            query_params: `api.get_project_members` メソッドのQuery Parameter

        Returns:
            すべてのプロジェクトメンバ一覧
        """
        # ページングされないので、そのままAPIを実行する
        content, _ = self.api.get_project_members(project_id, query_params=query_params)
        return content["list"]

    def put_project_members(self, project_id, project_members: List[Dict[str, Any]]) -> List[ProjectMember]:
        """
        複数のプロジェクトメンバを追加/更新/削除する.

        .. deprecated:: 2020-01-01

        Args:
            project_id: プロジェクトID
            project_members: 追加/更新するメンバのList. `user_id` , `member_status` , `member_role` をKeyに持つこと

        Returns:
            `putProjectMember` APIのContentのList

        """
        warnings.warn("deprecated: 2021-01-01以降に廃止します。", DeprecationWarning)

        # 追加/更新前のプロジェクトメンバ
        dest_project_members = self.get_all_project_members(project_id)

        updated_project_members = []
        # プロジェクトメンバを追加/更新する
        for member in project_members:
            dest_member = [e for e in dest_project_members if e["user_id"] == member["user_id"]]
            last_updated_datetime = dest_member[0]["updated_datetime"] if len(dest_member) > 0 else None

            request_body = {
                "member_status": member["member_status"],
                "member_role": member["member_role"],
                "sampling_inspection_rate": member.get("sampling_inspection_rate"),
                "sampling_acceptance_rate": member.get("sampling_acceptance_rate"),
                "last_updated_datetime": last_updated_datetime,
            }
            updated_project_member = self.api.put_project_member(
                project_id, member["user_id"], request_body=request_body
            )[0]
            updated_project_members.append(updated_project_member)

            command_name = "追加" if last_updated_datetime is None else "更新"
            logger.debug(
                "プロジェクトメンバの'%s' 完了." " project_id=%s, user_id=%s, " "last_updated_datetime=%s",
                command_name,
                project_id,
                member["user_id"],
                last_updated_datetime,
            )

        return updated_project_members

    def assign_role_to_project_members(
        self, project_id: str, user_id_list: List[str], member_role: str
    ) -> List[ProjectMember]:
        """
        複数のプロジェクトメンバに1つのロールを割り当てる。

        .. deprecated:: 2020-01-01

        Note:
            誤って実行しないようにすること

        Args:
            project_id: プロジェクトID
            user_id_list: 追加/更新するメンバのuser_idのList
            member_role: 割り当てるロール.

        Returns:
            `putProjectMember` APIのContentのList

        """
        warnings.warn("deprecated: 2021-01-01以降に廃止します。", DeprecationWarning)

        project_members = []
        for user_id in user_id_list:
            member = {"user_id": user_id, "member_status": "active", "member_role": member_role}
            project_members.append(member)

        return self.put_project_members(project_id, project_members)

    def drop_role_to_project_members(self, project_id, user_id_list: List[str]) -> List[ProjectMember]:
        """
        複数のプロジェクトメンバを、プロジェクトから脱退させる

        .. deprecated:: 2020-01-01

        Note:
            誤って実行しないようにすること

        Args:
            project_id: プロジェクトID
            user_id_list: 脱退させるメンバのuser_idのList

        Returns:
            `putProjectMember` APIのContentのList
        """
        warnings.warn("deprecated: 2021-01-01以降に廃止します。", DeprecationWarning)

        project_members = []
        for user_id in user_id_list:
            member = {
                "user_id": user_id,
                "member_status": "inactive",
                "member_role": "worker",  # 何か指定しないとエラーになったため、指定する
            }
            project_members.append(member)

        return self.put_project_members(project_id, project_members)

    def copy_project_members(
        self, src_project_id: str, dest_project_id: str, delete_dest: bool = False
    ) -> List[ProjectMember]:
        """
        プロジェクトメンバを、別のプロジェクトにコピーする。

        .. deprecated:: 2020-01-01

        Note:
            誤って実行しないようにすること

        Args:
            src_project_id: コピー元のproject_id
            dest_project_id: コピー先のproject_id
            delete_dest: Trueならばコピー先にしか存在しないプロジェクトメンバを削除する。

        Returns:
            `putProjectMember` APIのContentのList

        """
        warnings.warn("deprecated: 2021-01-01以降に廃止します。", DeprecationWarning)

        src_project_members = self.get_all_project_members(src_project_id)
        dest_project_members = self.get_all_project_members(dest_project_id)

        if delete_dest:
            # コピー先にしかいないメンバを削除する
            src_account_ids = [e["account_id"] for e in src_project_members]
            deleted_dest_members = [e for e in dest_project_members if e["account_id"] not in src_account_ids]

            def to_inactive(arg_member):
                arg_member["member_status"] = "inactive"
                return arg_member

            deleted_dest_members = list(map(to_inactive, deleted_dest_members))
            return self.put_project_members(dest_project_id, src_project_members + deleted_dest_members)

        else:
            return self.put_project_members(dest_project_id, src_project_members)

    #########################################
    # Public Method : Task
    #########################################
    def initiate_tasks_generation_by_csv(
        self, project_id: str, csvfile_path: str, query_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        タスクID,入力データ名,入力データID」を1行毎に指定したCSVを使って、タスクを生成する

        Args:
            project_id: プロジェクトID
            csvfile_path: CSVファイルのパス
            query_params: `initiate_tasks_generation` メソッドに渡す`query_params`

        Returns:
            `initiate_tasks_generation` APIのContent
        """
        s3_path = self.upload_file_to_s3(project_id, csvfile_path, "text/csv")

        project_last_updated_datetime = self.api.get_project(project_id)[0]["updated_datetime"]

        request_body = {
            "task_generate_rule": {"_type": "ByInputDataCsv", "csv_data_path": s3_path},
            "project_last_updated_datetime": project_last_updated_datetime,
        }
        return self.api.initiate_tasks_generation(project_id, request_body=request_body, query_params=query_params)[0]

    @allow_404_error
    def get_task_or_none(self, project_id: str, task_id: str) -> Optional[Task]:
        """
        タスクを取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            project_id:
            task_id:

        Returns:
            タスク
        """
        content, _ = self.api.get_task(project_id, task_id)
        return content

    def get_all_tasks(self, project_id: str, query_params: Optional[Dict[str, Any]] = None) -> List[Task]:
        """
        すべてのタスクを取得する。

        Args:
            project_id: プロジェクトID
            query_params: `api.get_tasks` メソッドに渡すQuery Parameter

        Returns:
            すべてのタスク一覧
        """
        return self._get_all_objects(self.api.get_tasks, limit=200, project_id=project_id, query_params=query_params)

    def change_task_status_to_working(self, project_id: str, task_id: str) -> Task:
        """
        タスクのステータスを「作業中」に変更します。

        Notes:
            * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。
            * 現在の状態が未着手(not_started)、休憩中(break)、保留(on_hold)のいずれかであるタスクに対してのみ、この操作を行うことができます。

        Args:
            project_id: プロジェクトID
            task_id: タスクID

        Returns:
            変更後のタスク
        """
        task, _ = self.api.get_task(project_id, task_id)
        request_body = {
            "status": TaskStatus.WORKING.value,
            "account_id": self.api.account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def change_task_status_to_break(self, project_id: str, task_id: str) -> Task:
        """
        タスクのステータスを「休憩中」に変更します。

        Notes:
            * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。
            * 現在の状態が作業中(working)のタスクに対してのみ、この操作を行うことができます。

        Args:
            project_id: プロジェクトID
            task_id: タスクID

        Returns:
            変更後のタスク
        """
        task, _ = self.api.get_task(project_id, task_id)
        request_body = {
            "status": TaskStatus.BREAK.value,
            "account_id": self.api.account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def change_task_status_to_on_hold(self, project_id: str, task_id: str) -> Task:
        """
        タスクのステータスを「保留」に変更します。

        Notes:
            * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。
            * 現在の状態が作業中(working)のタスクに対してのみ、この操作を行うことができます。

        Args:
            project_id: プロジェクトID
            task_id: タスクID

        Returns:
            変更後のタスク
        """
        task, _ = self.api.get_task(project_id, task_id)
        request_body = {
            "status": TaskStatus.ON_HOLD.value,
            "account_id": self.api.account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def complete_task(self, project_id: str, task_id: str) -> Task:
        """
        今のフェーズを完了させ、 次のフェーズに遷移させます。
        教師付フェーズのときはタスクを提出します。
        検査／受入フェーズのときは、タスクを合格にします。


        Notes:
            * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。
            * 現在の状態が作業中(working)のタスクに対してのみ、この操作を行うことができます。

        Args:
            project_id: プロジェクトID
            task_id: タスクID

        Returns:
            変更後のタスク
        """
        task, _ = self.api.get_task(project_id, task_id)
        request_body = {
            "status": TaskStatus.COMPLETE.value,
            "account_id": self.api.account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def cancel_submitted_task(self, project_id: str, task_id: str) -> Task:
        """
        タスクの提出を取り消します。
        「提出されたタスク」とは以下の状態になっています。
        * 教師付フェーズで「提出」ボタンを押して、検査/受入フェーズへ遷移したタスク
        * 検査フェーズから「合格」ボタンを押して、受入フェーズへ遷移したタスク

        Notes:
            * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。
            * タスク提出後に検査/受入(抜取含む)等の作業が一切行われていない場合のみ、この操作を行うことができます。
            * 現在の状態が未着手(not_started)のタスクに対してのみ、この操作を行うことができます。
            * 現在のフェーズが検査(inspection)、もしくは受入(acceptance)のタスクに対してのみ、この操作を行うことができます。

        Args:
            project_id: プロジェクトID
            task_id: タスクID

        Returns:
            変更後のタスク
        """
        task, _ = self.api.get_task(project_id, task_id)
        request_body = {
            "status": TaskStatus.CANCELLED.value,
            "account_id": self.api.account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def cancel_completed_task(self, project_id: str, task_id: str, operator_account_id: Optional[str] = None) -> Task:
        """
        タスクの受入完了状態を取り消す。

        Args:
            project_id: プロジェクトID
            task_id: タスクID
            operator_account_id: 受入完了状態を取り消した後の担当者のaccount_id

        Returns:
            変更後のタスク
        """

        task, _ = self.api.get_task(project_id, task_id)

        request_body = {
            "status": TaskStatus.NOT_STARTED.value,
            "account_id": operator_account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def change_task_operator(
        self, project_id: str, task_id: str, operator_account_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        タスクの担当者を変更します。

        Notes:
            * プロジェクトオーナー(owner)、もしくは受入担当者(accepter)のみ、この操作を行うことができます。

        Args:
            project_id: プロジェクトID
            task_id: タスクID
            operator_account_id: 新しい担当者のaccount_id。Noneの場合は、担当者を「未割り当て」にします。

        Returns:
            変更後のタスク

        """
        task, _ = self.api.get_task(project_id, task_id)

        request_body = {
            "status": TaskStatus.NOT_STARTED.value,
            "account_id": operator_account_id,
            "last_updated_datetime": task["updated_datetime"],
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def reject_task(self, project_id: str, task_id: str, force: bool = False) -> Dict[str, Any]:
        """
        タスクを差し戻します。
        * 通常の差し戻しの場合、タスクの担当者は未割り当てになります。
        * 強制差し戻しの場合、タスクの担当者は直前の教師付フェーズの担当者になります。

        Notes:
            * 通常の差し戻しの場合
                * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。
                * 現在の状態が作業中(working)のタスクに対してのみ、この操作を行うことができます。
                * 現在のフェーズが検査(inspection)、もしくは受入(acceptance)のタスクに対してのみ、この操作を行うことができます。
            * 強制差し戻しの場合
                * タスクの状態・フェーズを無視して、フェーズを教師付け(annotation)に、状態を未作業(not started)に変更します。
                * タスクの担当者としては、直前の教師付け(annotation)フェーズの担当者を割り当てます。
                * この差戻しは、抜取検査・抜取受入のスキップ判定に影響を及ぼしません。

        Args:
            project_id: プロジェクトID
            task_id: タスクID
            force: Trueなら強制差し戻し、Falseなら通常の差し戻しを実施する

        Returns:
            変更後のタスク

        """

        task, _ = self.api.get_task(project_id, task_id)

        request_body = {
            "status": TaskStatus.REJECTED.value,
            "account_id": self.api.account_id,
            "last_updated_datetime": task["updated_datetime"],
            "force": force,
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    #########################################
    # Public Method : Instruction
    #########################################
    def get_latest_instruction(self, project_id: str) -> Optional[Instruction]:
        """
        最新の作業ガイドの取得.

        Args:
            project_id: プロジェクトID

        Returns:
            作業ガイド情報。作業ガイドが登録されいてない場合はNone。
        """
        histories = self.api.get_instruction_history(project_id)[0]
        if len(histories) == 0:
            return None

        latest_history_id = histories[0]["history_id"]
        return self.api.get_instruction(project_id, {"history_id": latest_history_id})[0]

    def upload_instruction_image(
        self, project_id: str, image_id: str, file_path: str, content_type: Optional[str] = None
    ) -> str:
        """
        作業ガイドの画像をアップロードする。

        Args:
            project_id: プロジェクトID
            image_id: 作業ガイド画像ID
            file_path: アップロードするファイル
            content_type: アップロードするファイルのMIME Type. Noneの場合、ファイルパスから推測する。

        Returns:
            一時データ保存先であるS3パス
        """
        new_content_type = self._get_content_type(file_path, content_type)
        with open(file_path, "rb") as f:
            return self.upload_data_as_instruction_image(project_id, image_id, data=f, content_type=new_content_type)

    def upload_data_as_instruction_image(self, project_id: str, image_id: str, data: Any, content_type: str) -> str:
        """
        data を作業ガイドの画像としてアップロードする。

        Args:
            project_id: プロジェクトID
            image_id: 作業ガイド画像ID
            data: アップロード対象のdata. ``requests.put`` メソッドの ``data`` 引数にそのまま渡す。
            content_type: アップロードするファイルのMIME Type.

        Returns:
            一時データ保存先であるS3パス
        """
        # 作業ガイド登録用/更新用のURLを取得
        content = self.api.get_instruction_image_url_for_put(
            project_id, image_id, header_params={"content-type": content_type}
        )[0]

        url_parse_result = urllib.parse.urlparse(content["url"])
        query_dict = urllib.parse.parse_qs(url_parse_result.query)

        # URL Queryを除いたURLを取得する
        s3_url = content["url"].split("?")[0]

        # アップロード
        res_put = self.api.session.put(s3_url, params=query_dict, data=data, headers={"content-type": content_type})
        _log_error_response(logger, res_put)
        _raise_for_status(res_put)
        return content["path"]

    #########################################
    # Public Method : Job
    #########################################
    def delete_all_succeeded_job(self, project_id: str, job_type: JobType) -> List[JobInfo]:
        """
        成功したジョブをすべて削除する

        Args:
            project_id: プロジェクトID
            job_type: ジョブ種別

        Returns:
            削除したジョブの一覧
        """

        jobs = self.get_all_project_job(project_id, {"type": job_type.value})
        deleted_jobs = []
        for job in jobs:
            if job["job_status"] == "succeeded":
                logger.debug("job_id=%s のジョブを削除します。", job["job_id"])
                self.api.delete_project_job(project_id, job_type=job_type.value, job_id=job["job_id"])
                deleted_jobs.append(job)

        return deleted_jobs

    def get_all_project_job(self, project_id: str, query_params: Dict[str, Any]) -> List[JobInfo]:
        """
        すべてのバックグランドジョブを取得する。

        Args:
            project_id: プロジェクトID
            query_params: `api.get_project_job` メソッドに渡すQuery Parameter

        Returns:
            すべてのバックグランドジョブ一覧
        """
        copied_params = copy.deepcopy(query_params) if query_params is not None else {}

        all_jobs: List[Dict[str, Any]] = []
        limit = 200
        # クエリパラメタ`page`が未実装なため、`1`を指定する
        copied_params.update({"page": 1, "limit": limit})
        r = self.api.get_project_job(project_id, query_params=copied_params)[0]
        all_jobs.extend(r["list"])
        return all_jobs

    def job_in_progress(self, project_id: str, job_type: JobType) -> bool:
        """
        ジョブが進行中かどうか

        Args:
            project_id: プロジェクトID
            job_type: ジョブ種別

        Returns:
            ジョブが進行中かどうか

        """
        job_list = self.api.get_project_job(project_id, query_params={"type": job_type.value})[0]["list"]
        if len(job_list) == 0:
            return False

        job = job_list[0]
        return job["job_status"] == JobStatus.PROGRESS.value

    def wait_for_completion(
        self, project_id: str, job_type: JobType, job_access_interval: int = 60, max_job_access: int = 10
    ) -> bool:
        """
        ジョブが完了するまで待つ。

        Args:
            project_id: プロジェクトID
            job_type: 取得するジョブ種別
            job_access_interval: ジョブにアクセスする間隔[sec]
            max_job_access: ジョブに最大何回アクセスするか

        Returns:
            Trueならば、ジョブが成功した or 実行中のジョブがない。
            Falseならば、ジョブが失敗 or ``max_job_access`` 回アクセスしても、ジョブが完了しなかった。

        """

        def get_latest_job() -> Optional[JobInfo]:
            job_list = self.api.get_project_job(project_id, query_params={"type": job_type.value})[0]["list"]
            if len(job_list) > 0:
                return job_list[0]
            else:
                return None

        job_access_count = 0
        while True:
            job = get_latest_job()
            if job is None:
                logger.debug("ジョブは存在しませんでした。")
                return True
            else:
                if job_access_count == 0 and job["job_status"] != "progress":
                    logger.debug("進行中のジョブはありませんでした。")
                    return True

            job_access_count += 1

            if job["job_status"] == "succeeded":
                logger.debug("job_id = %s のジョブが成功しました。", job["job_id"])
                return True

            elif job["job_status"] == "failed":
                logger.info("job_id = %s のジョブが失敗しました。", job["job_id"])
                return False

            else:
                # 進行中
                if job_access_count < max_job_access:
                    logger.debug("job_id = %s のジョブが進行中です。%d 秒間待ちます。", job["job_id"], job_access_interval)
                    time.sleep(job_access_interval)
                else:
                    logger.debug("job_id = %s のジョブに %d 回アクセスしましたが、完了しませんでした。", job["job_id"], job_access_count)
                    return False

    #########################################
    # Public Method : Labor Control
    #########################################
    @staticmethod
    def _get_actual_worktime_hour_from_labor(labor: Dict[str, Any]) -> Optional[float]:
        working_time_by_user = labor["values"]["working_time_by_user"]
        if working_time_by_user is None:
            return None

        actual_worktime = working_time_by_user.get("results")
        if actual_worktime is None:
            return None
        else:
            return actual_worktime / 3600 / 1000

    @staticmethod
    def _get_plan_worktime_hour_from_labor(labor: Dict[str, Any]) -> Optional[float]:
        working_time_by_user = labor["values"]["working_time_by_user"]
        if working_time_by_user is None:
            return None

        actual_worktime = working_time_by_user.get("plans")
        if actual_worktime is None:
            return None
        else:
            return actual_worktime / 3600 / 1000

    @staticmethod
    def _get_working_description_from_labor(labor: Dict[str, Any]) -> Optional[str]:
        working_time_by_user = labor["values"]["working_time_by_user"]
        if working_time_by_user is None:
            return None
        return working_time_by_user.get("description")

    def get_labor_control_worktime(
        self,
        organization_id: Optional[str] = None,
        project_id: Optional[str] = None,
        account_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        実績作業時間(actual_worktime)と予定作業時間(plan_worktime)を扱いやすいフォーマットで取得する。
        ただし、organization_id または project_id のいずれかを指定する必要がある。

        Args:
            organization_id: 絞り込み対象の組織ID
            project_id: 絞り込み対象のプロジェクトID
            account_id: 絞り込み対象のアカウントID
            from_date: 絞り込み対象の開始日（YYYY-MM-DD）
            to_date: 絞り込み対象の終了日（YYYY-MM-DD）

        Returns:
            労務管理情報
                * organization_id
                * project_id
                * account_id
                * date
                * actual_worktime：実績作業時間[hour]
                * plan_worktime：予定作業時間[hour]
                * working_description：実績に関するコメント
        """

        def _to_new_data(labor: Dict[str, Any]) -> Dict[str, Any]:
            labor["actual_worktime"] = self._get_actual_worktime_hour_from_labor(labor)
            labor["plan_worktime"] = self._get_plan_worktime_hour_from_labor(labor)
            labor["working_description"] = self._get_working_description_from_labor(labor)
            labor.pop("values", None)
            return labor

        if organization_id is None and project_id is None:
            raise ValueError("one of the arguments organization_id project_id is required")

        query_params = {
            "organization_id": organization_id,
            "project_id": project_id,
            "account_id": account_id,
            "from": from_date,
            "to": to_date,
        }
        labor_list, _ = self.api.get_labor_control(query_params)
        return [_to_new_data(e) for e in labor_list]

    def get_labor_control_availability(
        self, account_id: str, from_date: Optional[str] = None, to_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        労務管理の予定稼働時間を取得する。

        Args:
            account_id: 絞り込み対象のアカウントID
            from_date: 絞り込み対象の開始日（YYYY-MM-DD）
            to_date: 絞り込み対象の終了日（YYYY-MM-DD）

        Returns:
            予定稼働時間情報
                * account_id
                * date
                * availability：予定稼働時間[hour]
        """

        def _to_new_data(labor: Dict[str, Any]) -> Dict[str, Any]:
            labor["availability"] = self._get_plan_worktime_hour_from_labor(labor)
            labor.pop("values", None)
            return labor

        query_params = {
            "organization_id": "___plannedWorktime___",
            "account_id": account_id,
            "from": from_date,
            "to": to_date,
        }
        labor_list, _ = self.api.get_labor_control(query_params)
        return [_to_new_data(e) for e in labor_list]
