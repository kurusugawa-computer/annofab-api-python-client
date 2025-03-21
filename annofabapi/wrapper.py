# pylint: disable=too-many-lines
import copy
import datetime
import functools
import hashlib
import logging
import mimetypes
import time
import urllib
import urllib.parse
import uuid
import warnings
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional, Union

import more_itertools
import requests
from dateutil.relativedelta import relativedelta

from annofabapi import AnnofabApi
from annofabapi.api import _log_error_response, _raise_for_status
from annofabapi.exceptions import AnnofabApiException, CheckSumError
from annofabapi.models import (
    AdditionalDataDefinitionType,
    AdditionalDataDefinitionV1,
    AdditionalDataV1,
    AnnotationDataHoldingType,
    AnnotationDetailV1,
    FullAnnotationData,
    InputData,
    Instruction,
    JobStatus,
    LabelV1,
    MyOrganization,
    Organization,
    OrganizationMember,
    Project,
    ProjectJobInfo,
    ProjectJobType,
    ProjectMember,
    SimpleAnnotationDetail,
    SupplementaryData,
    Task,
    TaskStatus,
)
from annofabapi.parser import SimpleAnnotationDirParser, SimpleAnnotationParser

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
    label_id: dict[str, str]
    additional_data_definition_id: dict[str, str]
    choice_id: dict[ChoiceKey, ChoiceKey]


_JOB_CONCURRENCY_LIMIT = {
    ProjectJobType.COPY_PROJECT: {
        ProjectJobType.GEN_INPUTS,
        ProjectJobType.GEN_TASKS,
        ProjectJobType.DELETE_PROJECT,
        ProjectJobType.MOVE_PROJECT,
    },
    ProjectJobType.GEN_INPUTS: {
        ProjectJobType.COPY_PROJECT,
        ProjectJobType.GEN_INPUTS,
        ProjectJobType.GEN_TASKS,
        ProjectJobType.GEN_INPUTS_LIST,
        ProjectJobType.DELETE_PROJECT,
        ProjectJobType.MOVE_PROJECT,
    },
    ProjectJobType.GEN_TASKS: {
        ProjectJobType.COPY_PROJECT,
        ProjectJobType.GEN_INPUTS,
        ProjectJobType.GEN_TASKS,
        ProjectJobType.GEN_ANNOTATION,
        ProjectJobType.GEN_TASKS_LIST,
        ProjectJobType.DELETE_PROJECT,
        ProjectJobType.MOVE_PROJECT,
    },
    ProjectJobType.GEN_ANNOTATION: {
        ProjectJobType.GEN_TASKS,
        ProjectJobType.GEN_ANNOTATION,
        ProjectJobType.DELETE_PROJECT,
        ProjectJobType.MOVE_PROJECT,
    },
    ProjectJobType.GEN_TASKS_LIST: {
        ProjectJobType.GEN_TASKS,
        ProjectJobType.GEN_TASKS_LIST,
        ProjectJobType.DELETE_PROJECT,
        ProjectJobType.MOVE_PROJECT,
    },
    ProjectJobType.GEN_INPUTS_LIST: {
        ProjectJobType.GEN_INPUTS,
        ProjectJobType.GEN_INPUTS_LIST,
        ProjectJobType.DELETE_PROJECT,
        ProjectJobType.MOVE_PROJECT,
    },
    ProjectJobType.INVOKE_HOOK: {ProjectJobType.DELETE_PROJECT, ProjectJobType.MOVE_PROJECT},
    ProjectJobType.DELETE_PROJECT: set(ProjectJobType),
    ProjectJobType.MOVE_PROJECT: set(ProjectJobType),
}
"""同時に実行できないジョブを表しています。valueに指定されたジョブが1つ以上実行されている場合、keyに指定されたジョブは実行できません。"""


class Wrapper:
    """
    AnnofabApiのラッパー.

    Args:
        api: AnnofabApi Instance

    """

    def __init__(self, api: AnnofabApi) -> None:
        self.api = api

    #########################################
    # Private Method
    #########################################
    @staticmethod
    def _get_mime_type(file_path: str) -> str:
        """
        ファイルパスからMIME Typeを返す。MIME Typeが推測できない場合は、``application/octet-stream`` を返す。

        Args:
            file_path: MIME Typeを取得したいファイルのパス

        Returns:
            ファイルパスから取得したMIME Type

        """
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is not None:
            return content_type

        logger.info(
            "ファイルパス '%s' からMIME Typeを推測できませんでした。MIME Typeは `application/octet-stream' とみなします。",
            file_path,
        )
        return "application/octet-stream"

    @staticmethod
    def _get_all_objects(func_get_list: Callable, limit: int, **kwargs_for_func_get_list) -> list[dict[str, Any]]:
        """
        get_all_XXX関数の共通処理

        Args:
            func_get_list: AnnofabApiのget_XXX関数
            limit: 1ページあたりの取得するデータ件数
            **kwargs_for_func_get_list: `func_get_list`に渡す引数。

        Returns:
            get_XXX関数で取得した情報の一覧

        """
        arg_query_params = kwargs_for_func_get_list.get("query_params")
        copied_query_params = copy.deepcopy(arg_query_params) if arg_query_params is not None else {}

        all_objects: list[dict[str, Any]] = []

        copied_query_params.update({"page": 1, "limit": limit})
        kwargs_for_func_get_list["query_params"] = copied_query_params
        content, _ = func_get_list(**kwargs_for_func_get_list)

        if content["over_limit"]:
            logger.warning(
                "calling %s :: 検索結果が10,000件を超えています。Web APIの都合上10,000件までしか取得できません。",
                func_get_list.__name__,
            )

        all_objects.extend(content["list"])

        while content["page_no"] < content["total_page_no"]:
            next_page_no = content["page_no"] + 1
            copied_query_params.update({"page": next_page_no})
            kwargs_for_func_get_list["query_params"] = copied_query_params
            logger.debug("calling '%s' :: %d/%d steps", func_get_list.__name__, next_page_no, content["total_page_no"])
            content, _ = func_get_list(**kwargs_for_func_get_list)
            all_objects.extend(content["list"])

        return all_objects

    def execute_http_get(self, url: str) -> requests.Response:
        """
        指定したURLに対してHTTP GETを実行します。

        塗りつぶし画像など外部リソースのURLを指定することを想定しています。

        Args:
            url: HTTP GETでアクセスするURL

        Returns:
            URLにアクセスしたときの ``requests.Response`` 情報

        Note:
            ``requests.get`` でアクセスすることとの違いは以下の通りです。

             * ``requests.Session`` 情報を使ってTCPコネクションを再利用しているため、``requests.get`` を使ってダウンロードするよりも、パフォーマンスが向上する可能性があります。
             * 必要に応じてリトライします
             * HTTPステータスコードが4XX,5XXならば、HTTPErrorがスローされます


        """  # noqa: E501
        return self.api._execute_http_request(http_method="get", url=url)

    def download(self, url: str, dest_path: Union[str, Path], *, chunk_size: int = 1024 * 1024 * 500, logger_prefix: str = "") -> None:
        """
        指定したURLからファイルをダウンロードします。

        Args:
            url: ダウンロード対象のURL
            dest_path: 保存先ファイルのパス
            chunk_size: メモリに読み込むバイト数
            logger_prefix: ログメッセージのプレフィックス

        """

        def to_megabyte_string(value: Optional[Union[str, int]]) -> str:
            if value is None:
                return "None"
            megabyte_value = int(value) / (1024 * 1024)
            return f"{megabyte_value:.3f}"

        p = dest_path if isinstance(dest_path, Path) else Path(dest_path)
        with self.api._execute_http_request(http_method="get", url=url, stream=True) as response:
            content_length = response.headers.get("Content-Length")
            last_modified = response.headers.get("Last-Modified")

            # `Last-Modified`をログに出力する理由：
            # ダウンロード対象のファイルがいつ更新されたかが分かるようにするため。
            # ダウンロード対象の全件ファイルは原則AM03:00頃に更新されるが、更新に遅れが生じることがある。
            logger.info("%s :: ダウンロードします。 :: Content-Length='%s', Last-Modified='%s'", logger_prefix, content_length, last_modified)

            p.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, "wb") as f:
                sum_chunk_size = 0
                for chunk in response.iter_content(chunk_size=chunk_size):
                    sum_chunk_size += len(chunk)
                    logger.debug(
                        "%s :: ダウンロード中です。 :: %s / %s MBをダウンロードしました。",
                        logger_prefix,
                        to_megabyte_string(sum_chunk_size),
                        to_megabyte_string(content_length),
                    )
                    f.write(chunk)

            logger.info("%s :: ダウンロードが完了しました。 :: file='%s'", logger_prefix, dest_path)

    #########################################
    # Public Method : Annotation
    #########################################
    def get_editor_annotation_or_none(
        self, project_id: str, task_id: str, input_data_id: str, *, query_params: Optional[dict[str, Any]] = None
    ) -> Optional[dict[str, Any]]:
        """
        アノテーションを取得する。
        存在しない場合(HTTP 404 Error)はNoneを返します。

        Args:
            project_id: プロジェクトID
            task_id: タスクID
            input_data_id: 入力データID

        Returns:
            アノテーション
        """
        content, response = self.api.get_editor_annotation(project_id, task_id, input_data_id, query_params=query_params, raise_for_status=False)

        if response.status_code == requests.codes.not_found:
            return None
        else:
            _log_error_response(logger, response)
            _raise_for_status(response)
            return content

    def download_annotation_archive(self, project_id: str, dest_path: Union[str, Path]) -> str:
        """
        simpleアノテーションZIPをダウンロードする。

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先のファイルパス

        Returns:
            ダウンロード元のURL

        """
        # 2022/01時点でレスポンスのcontent-typeが"text/plain"なので、contentの型がdictにならない。したがって、Locationヘッダを参照する。
        _, response = self.api.get_annotation_archive(project_id)
        url = response.headers["Location"]
        self.download(url, dest_path, logger_prefix=f"project_id='{project_id}', ダウンロード対象のファイル='SimpleアノテーションZIP'")
        return url

    def download_full_annotation_archive(self, project_id: str, dest_path: Union[str, Path]) -> str:
        """
        FullアノテーションZIPをダウンロードする。

        .. deprecated:: X

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先のファイルパス

        Returns:
            ダウンロード元のURL

        """
        warnings.warn(
            "annofabapi.Wrapper.download_full_annotation_archive() is deprecated and will be removed.",
            FutureWarning,
            stacklevel=2,
        )
        # 2022/01時点でレスポンスのcontent-typeが"text/plain"なので、contentの型がdictにならない。したがって、Locationヘッダを参照する。
        _, response = self.api.get_archive_full_with_pro_id(project_id)
        url = response.headers["Location"]
        self.download(url, dest_path, logger_prefix=f"project_id='{project_id}', ダウンロード対象のファイル='FullアノテーションZIP'")
        return url

    def get_all_annotation_list(self, project_id: str, query_params: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """
        すべてのアノテーション情報を取得する。

        Args:
            project_id: プロジェクトID
            query_params: `api.get_annotation_list` メソッドのQuery Parameter

        Returns:l
            すべてのアノテーション一覧
        """
        return self._get_all_objects(self.api.get_annotation_list, limit=200, project_id=project_id, query_params=query_params)

    @staticmethod
    def __replace_annotation_specs_id(detail: dict[str, Any], annotation_specs_relation: AnnotationSpecsRelation) -> Optional[dict[str, Any]]:
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
            new_additional_data_definition_id = annotation_specs_relation.additional_data_definition_id.get(additional_data_definition_id)
            if new_additional_data_definition_id is None:
                continue
            additional_data["additional_data_definition_id"] = new_additional_data_definition_id

            if additional_data["choice"] is not None:
                new_choice = annotation_specs_relation.choice_id.get(ChoiceKey(additional_data_definition_id, additional_data["choice"]))
                additional_data["choice"] = new_choice.choice_id if new_choice is not None else None

            new_additional_data_list.append(additional_data)

        detail["additional_data_list"] = new_additional_data_list
        return detail

    def __to_dest_annotation_detail(
        self,
        dest_project_id: str,
        detail: dict[str, Any],
        account_id: str,
    ) -> dict[str, Any]:
        """
        コピー元の１個のアノテーションを、コピー先用に変換する。
        塗りつぶし画像などの外部アノテーションファイルがある場合、S3にアップロードする。

        Notes:
            annotation_id をUUIDv4で生成すると、アノテーションリンク属性をコピーしたときに対応できないので、暫定的にannotation_idは維持するようにする。

        Raises:
            CheckSumError: アップロードした外部アノテーションファイルのMD5ハッシュ値が、S3にアップロードしたときのレスポンスのETagに一致しない

        """  # noqa: E501
        dest_detail = detail
        dest_detail["account_id"] = account_id
        if detail["data_holding_type"] == AnnotationDataHoldingType.OUTER.value:
            try:
                outer_file_url = detail["url"]
                src_response = self.api._execute_http_request("get", outer_file_url)
                s3_path = self.upload_data_to_s3(dest_project_id, data=src_response.content, content_type=src_response.headers["Content-Type"])
                dest_detail["path"] = s3_path
                dest_detail["url"] = None
                dest_detail["etag"] = None

            except CheckSumError as e:
                message = (
                    f"外部アノテーションファイル {outer_file_url} のレスポンスのMD5ハッシュ値('{e.uploaded_data_hash}')が、"
                    f"AWS S3にアップロードしたときのレスポンスのETag('{e.response_etag}')に一致しませんでした。アップロード時にデータが破損した可能性があります。"  # noqa: E501
                )
                raise CheckSumError(message=message, uploaded_data_hash=e.uploaded_data_hash, response_etag=e.response_etag) from e

        return dest_detail

    def _create_request_body_for_copy_annotation(
        self,
        project_id: str,
        task_id: str,
        input_data_id: str,
        src_details: list[dict[str, Any]],
        account_id: Optional[str] = None,
        annotation_specs_relation: Optional[AnnotationSpecsRelation] = None,
    ) -> dict[str, Any]:
        if account_id is None:
            account_id = self.api.account_id
        dest_details: list[dict[str, Any]] = []

        for src_detail in src_details:
            if annotation_specs_relation is not None:
                tmp_detail = self.__replace_annotation_specs_id(src_detail, annotation_specs_relation)
                if tmp_detail is None:
                    continue
                src_detail = tmp_detail  # noqa: PLW2901

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
        src_annotation_details: list[dict[str, Any]] = src_annotation["details"]

        if len(src_annotation_details) == 0:
            logger.warning("コピー元にアノテーションが１つもないため、アノテーションのコピーをスキップします。:: src='{src}'")
            return False

        old_dest_annotation, _ = self.api.get_editor_annotation(dest.project_id, dest.task_id, dest.input_data_id)
        updated_datetime = old_dest_annotation["updated_datetime"]

        request_body = self._create_request_body_for_copy_annotation(
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

    def __get_label_info_from_label_name(self, label_name: str, annotation_specs_labels: list[LabelV1]) -> Optional[LabelV1]:
        for label in annotation_specs_labels:
            if self.__get_label_name_en(label) == label_name:
                return label
        return None

    def __get_additional_data_from_attribute_name(self, attribute_name: str, label_info: LabelV1) -> Optional[AdditionalDataDefinitionV1]:
        for additional_data in label_info["additional_data_definitions"]:
            if self.__get_additional_data_definition_name_en(additional_data) == attribute_name:
                return additional_data

        return None

    def _get_choice_id_from_name(self, name: str, choices: list[dict[str, Any]]) -> Optional[str]:
        choice_info = more_itertools.first_true(choices, pred=lambda e: self.__get_choice_name_en(e) == name)
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

    def __to_additional_data_list(self, attributes: dict[str, Any], label_info: LabelV1) -> list[AdditionalDataV1]:
        additional_data_list: list[AdditionalDataV1] = []
        for key, value in attributes.items():
            specs_additional_data = self.__get_additional_data_from_attribute_name(key, label_info)
            if specs_additional_data is None:
                logger.warning(
                    "アノテーション仕様の '%s' ラベルに、attribute_name='%s' である属性が存在しません。",
                    self.__get_label_name_en(label_info),
                    key,
                )
                continue

            additional_data = {
                "additional_data_definition_id": specs_additional_data["additional_data_definition_id"],
                "flag": None,
                "integer": None,
                "choice": None,
                "comment": None,
            }
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
                logger.warning(
                    "additional_data_type='%s'が不正です。 :: additional_data_definition_id='%s'",
                    additional_data_type,
                    specs_additional_data["additional_data_definition_id"],
                )
                continue

            additional_data_list.append(additional_data)

        return additional_data_list

    def __to_annotation_detail_for_request(
        self,
        project_id: str,
        parser: SimpleAnnotationParser,
        detail: SimpleAnnotationDetail,
        annotation_specs_labels: list[LabelV1],
    ) -> Optional[AnnotationDetailV1]:
        """
        Request Bodyに渡すDataClassに変換する。塗りつぶし画像があれば、それをS3にアップロードする。

        Args:
            project_id:
            parser:
            detail:

        Returns:

        Raises:
            CheckSumError: アップロードした外部アノテーションファイルのMD5ハッシュ値が、S3にアップロードしたときのレスポンスのETagに一致しない

        """
        label_info = self.__get_label_info_from_label_name(detail["label"], annotation_specs_labels)
        if label_info is None:
            logger.warning("アノテーション仕様に '%s' のラベルが存在しません。 :: project_id='%s'", {detail["label"]}, project_id)
            return None

        additional_data_list: list[AdditionalDataV1] = self.__to_additional_data_list(detail["attributes"], label_info)
        data_holding_type = self.__get_data_holding_type_from_data(detail["data"])

        dest_obj = {
            "label_id": label_info["label_id"],
            "annotation_id": detail["annotation_id"] if detail.get("annotation_id") is not None else str(uuid.uuid4()),
            "account_id": self.api.account_id,
            "data_holding_type": data_holding_type,
            "data": detail["data"],
            "additional_data_list": additional_data_list,
            "is_protected": False,
            "etag": None,
            "url": None,
            "path": None,
            "created_datetime": None,
            "updated_datetime": None,
        }

        if data_holding_type == AnnotationDataHoldingType.OUTER.value:
            data_uri = detail["data"]["data_uri"]
            outer_file_path = f"{parser.task_id}/{parser.input_data_id}/{data_uri}"
            with parser.open_outer_file(data_uri) as f:
                try:
                    s3_path = self.upload_data_to_s3(project_id, f, content_type="image/png")
                    dest_obj["path"] = s3_path

                except CheckSumError as e:
                    message = (
                        f"アップロードした外部アノテーションファイル'{outer_file_path}'のMD5ハッシュ値('{e.uploaded_data_hash}')が、"
                        f"AWS S3にアップロードしたときのレスポンスのETag('{e.response_etag}')に一致しませんでした。アップロード時にデータが破損した可能性があります。"  # noqa: E501
                    )
                    raise CheckSumError(message=message, uploaded_data_hash=e.uploaded_data_hash, response_etag=e.response_etag) from e

        return dest_obj

    def __convert_annotation_specs_labels_v2_to_v1(self, labels_v2: list[dict[str, Any]], additionals_v2: list[dict[str, Any]]) -> list[LabelV1]:
        """アノテーション仕様のV2版からV1版に変換する。V1版の方が扱いやすいので。

        Args:
            labels_v2 (list[dict[str, Any]]): V2版のラベル情報
            additionals_v2 (list[dict[str, Any]]): V2版の属性情報

        Returns:
            list[LabelV1]: V1版のラベル情報
        """

        def get_additional(additional_data_definition_id: str) -> Optional[dict[str, Any]]:
            return more_itertools.first_true(additionals_v2, pred=lambda e: e["additional_data_definition_id"] == additional_data_definition_id)

        def to_label_v1(label_v2: dict[str, Any]) -> LabelV1:
            additional_data_definition_id_list = label_v2["additional_data_definitions"]
            new_additional_data_definitions = []
            for additional_data_definition_id in additional_data_definition_id_list:
                additional = get_additional(additional_data_definition_id)
                if additional is not None:
                    new_additional_data_definitions.append(additional)
                else:
                    raise ValueError(
                        f"additional_data_definition_id='{additional_data_definition_id}' に対応する属性情報が存在しません。"
                        f"label_id='{label_v2['label_id']}', label_name_en='{self.__get_label_name_en(label_v2)}'"
                    )
            label_v2["additional_data_definitions"] = new_additional_data_definitions
            return label_v2

        return [to_label_v1(label_v2) for label_v2 in labels_v2]

    def put_annotation_for_simple_annotation_json(
        self,
        project_id: str,
        task_id: str,
        input_data_id: str,
        simple_annotation_json: str,
        annotation_specs_labels: list[dict[str, Any]],
        annotation_specs_additionals: Optional[list[dict[str, Any]]] = None,
    ) -> bool:
        """
        Annofabからダウンロードしたアノテーションzip配下のJSONと同じフォーマット（Simple Annotation)の内容から、アノテーションを登録する。

        Args:
            project_id:
            task_id:
            input_data_id:
            simple_annotation_json: Annofabからダウンロードしたアノテーションzip配下のJSONのパス
            annotation_specs_labels: アノテーション仕様のラベル情報。annotation_specs_additionalsが指定されている場合はV2版、指定されない場合はV1版。
            annotation_specs_additionals: アノテーション仕様の属性情報（V2版）

        Returns:
            True:アノテーション情報をした。False: 登録するアノテーション情報がなかったため、登録しなかった。

        Notes:
            2021/07以降、引数annotation_specs_labelsはV1版をサポートしなくなる予定です。
        """
        parser = SimpleAnnotationDirParser(Path(simple_annotation_json))
        annotation = parser.load_json()

        details = annotation["details"]
        if len(details) == 0:
            logger.warning(
                "simple_annotation_json='%s'にアノテーション情報は記載されていなかったので、アノテーションの登録処理をスキップします。"
                " :: project_id='%s', task_id='%s', input_data_id='%s'",
                simple_annotation_json,
                project_id,
                task_id,
                input_data_id,
            )
            return False

        request_details: list[dict[str, Any]] = []
        annotation_specs_labels_v1 = (
            self.__convert_annotation_specs_labels_v2_to_v1(annotation_specs_labels, annotation_specs_additionals)
            if annotation_specs_additionals is not None
            else annotation_specs_labels
        )
        for detail in details:
            request_detail = self.__to_annotation_detail_for_request(project_id, parser, detail, annotation_specs_labels_v1)
            if request_detail is not None:
                request_details.append(request_detail)
        if len(request_details) == 0:
            logger.warning(
                "simple_annotation_json='%s'に、登録できるアノテーションはなかったので、アノテーションの登録処理をスキップします。"
                " :: project_id='%s', task_id='%s', input_data_id='%s'",
                simple_annotation_json,
                project_id,
                task_id,
                input_data_id,
            )
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

    @staticmethod
    def __get_label_name_en(label: dict[str, Any]) -> str:
        """label情報から英語名を取得する"""
        label_name_messages = label["label_name"]["messages"]
        return next(e["message"] for e in label_name_messages if e["lang"] == "en-US")

    @staticmethod
    def __get_additional_data_definition_name_en(additional_data_definition: dict[str, Any]) -> str:
        """additional_data_definitionから英語名を取得する"""
        messages = additional_data_definition["name"]["messages"]
        return next(e["message"] for e in messages if e["lang"] == "en-US")

    @staticmethod
    def __get_choice_name_en(choice: dict[str, Any]) -> str:
        """choiceから英語名を取得する"""
        messages = choice["name"]["messages"]
        return next(e["message"] for e in messages if e["lang"] == "en-US")

    def __get_dest_additional(
        self,
        src_additional: dict[str, Any],
        dest_additionals: list[dict[str, Any]],
        src_labels: list[dict[str, Any]],
        dest_labels: list[dict[str, Any]],
        dict_label_id: dict[str, str],
    ) -> Optional[dict[str, Any]]:
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

                    dest_label = more_itertools.first_true(
                        dest_labels,
                        pred=lambda e: e["label_id"] == dest_label_id,  # pylint: disable=cell-var-from-loop  # noqa: B023
                    )
                    if dest_label is None:
                        dest_label_contains_dest_additional = False
                        break
                    if dest_additional["additional_data_definition_id"] not in dest_label["additional_data_definitions"]:
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

        dict_label_id: dict[str, str] = {}
        for src_label in src_annotation_specs["labels"]:
            src_label_name_en = self.__get_label_name_en(src_label)
            dest_label = more_itertools.first_true(
                dest_labels,
                pred=lambda e: self.__get_label_name_en(e) == src_label_name_en,  # pylint: disable=cell-var-from-loop  # noqa: B023
            )
            if dest_label is not None:
                dict_label_id[src_label["label_id"]] = dest_label["label_id"]

        dict_additional_data_definition_id: dict[str, str] = {}
        dict_choice_id: dict[ChoiceKey, ChoiceKey] = {}
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

            dict_additional_data_definition_id[src_additional["additional_data_definition_id"]] = dest_additional["additional_data_definition_id"]

            dest_choices = dest_additional["choices"]
            for src_choice in src_additional["choices"]:
                src_choice_name_en = self.__get_choice_name_en(src_choice)
                dest_choice = more_itertools.first_true(
                    dest_choices,
                    pred=lambda e: self.__get_choice_name_en(e) == src_choice_name_en,  # pylint: disable=cell-var-from-loop  # noqa: B023
                )
                if dest_choice is not None:
                    dict_choice_id[ChoiceKey(src_additional["additional_data_definition_id"], src_choice["choice_id"])] = ChoiceKey(
                        dest_additional["additional_data_definition_id"], dest_choice["choice_id"]
                    )

        return AnnotationSpecsRelation(
            label_id=dict_label_id,
            additional_data_definition_id=dict_additional_data_definition_id,
            choice_id=dict_choice_id,
        )

    #########################################
    # Public Method : Input
    #########################################
    def get_input_data_or_none(self, project_id: str, input_data_id: str) -> Optional[InputData]:
        """
        入力データを取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            project_id:
            input_data_id:

        Returns:
            入力データ
        """
        content, response = self.api.get_input_data(project_id, input_data_id, raise_for_status=False)

        if response.status_code == requests.codes.not_found:
            return None
        else:
            _log_error_response(logger, response)
            _raise_for_status(response)
            return content

    def get_all_input_data_list(self, project_id: str, query_params: Optional[dict[str, Any]] = None) -> list[InputData]:
        """
        すべての入力データを取得する。

        Args:
            project_id: プロジェクトID
            query_params: `api.get_input_data_list` メソッドのQuery Parameter

        Returns:
            入力データ一覧
        """
        return self._get_all_objects(self.api.get_input_data_list, limit=200, project_id=project_id, query_params=query_params)

    def upload_file_to_s3(self, project_id: str, file_path: str, content_type: Optional[str] = None) -> str:
        """
        createTempPath APIを使ってアップロード用のURLとS3パスを取得して、ファイルをアップロードする。

        Args:
            project_id: プロジェクトID
            file_path: アップロードするファイルのパス
            content_type: アップロードするファイルのMIME Type. Noneの場合、ファイルパスから推測する。

        Returns:
            一時データ保存先であるS3パス

        Raises:
            CheckSumError: アップロードしたファイルのMD5ハッシュ値が、S3にアップロードしたときのレスポンスのETagと一致しない

        """

        # content_type を推測
        new_content_type = self._get_mime_type(file_path) if content_type is None else content_type
        with open(file_path, "rb") as f:
            try:
                return self.upload_data_to_s3(project_id, data=f, content_type=new_content_type)
            except CheckSumError as e:
                message = (
                    f"アップロードしたファイル'{file_path}'のMD5ハッシュ値('{e.uploaded_data_hash}')が、"
                    f"AWS S3にアップロードしたときのレスポンスのETag('{e.response_etag}')に一致しませんでした。アップロード時にデータが破損した可能性があります。"  # noqa: E501
                )
                raise CheckSumError(message=message, uploaded_data_hash=e.uploaded_data_hash, response_etag=e.response_etag) from e

    def upload_data_to_s3(self, project_id: str, data: Any, content_type: str) -> str:  # noqa: ANN401
        """
        createTempPath APIを使ってアップロード用のURLとS3パスを取得して、"data" をアップロードする。

        Args:
            project_id: プロジェクトID
            data: アップロード対象のdata. ``open(mode="b")`` 関数の戻り値、またはバイナリ型の値です。 ``requests.put`` メソッドの ``data`` 引数にそのまま渡します。
            content_type: アップロードするfile objectのMIME Type.

        Returns:
            一時データ保存先であるS3パス

        Raises:
            CheckSumError: アップロードしたデータのMD5ハッシュ値が、S3にアップロードしたときのレスポンスのETagと一致しない
        """  # noqa: E501

        def get_md5_value_from_file(fp):  # noqa: ANN001, ANN202
            md5_obj = hashlib.md5()
            while True:
                chunk = fp.read(2048 * md5_obj.block_size)
                if len(chunk) == 0:
                    break
                md5_obj.update(chunk)
            return md5_obj.hexdigest()

        # 一時データ保存先を取得
        content, _ = self.api.create_temp_path(project_id)

        url_parse_result = urllib.parse.urlparse(content["url"])
        query_dict = urllib.parse.parse_qs(url_parse_result.query)

        # URL Queryを除いたURLを取得する
        s3_url = content["url"].split("?")[0]

        # アップロード
        res_put = self.api._execute_http_request(http_method="put", url=s3_url, params=query_dict, data=data, headers={"content-type": content_type})

        # アップロードしたファイルが破損していなかをチェックする
        if hasattr(data, "read"):
            # 読み込み位置を先頭に戻す
            data.seek(0)
            uploaded_data_hash = get_md5_value_from_file(data)
        else:
            uploaded_data_hash = hashlib.md5(data).hexdigest()

        # ETagにはダブルクォートが含まれているため、`str_md5`もそれに合わせる
        response_etag = res_put.headers["ETag"]

        if f'"{uploaded_data_hash}"' != response_etag:
            message = (
                f"アップロードしたデータのMD5ハッシュ値('{uploaded_data_hash}')が、"
                f"AWS S3にアップロードしたときのレスポンスのETag('{response_etag}')に一致しませんでした。アップロード時にデータが破損した可能性があります。"  # noqa: E501
            )
            raise CheckSumError(message=message, uploaded_data_hash=uploaded_data_hash, response_etag=response_etag)

        return content["path"]

    def put_input_data_from_file(
        self,
        project_id: str,
        input_data_id: str,
        file_path: str,
        request_body: Optional[dict[str, Any]] = None,
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
    def _get_statistics_content(self, content: Any, response: requests.Response) -> Optional[Any]:  # noqa: ANN401
        """
        統計情報webapiのレスポンス情報に格納されているURLにアクセスして、統計情報の中身を取得する。
        統計情報webapiのレスポンス'url'にアクセスする。
            response:

        Returns:
            統計情報の中身
        """
        url = content.get("url")
        if url is None:
            # プロジェクト作成直後は contentの中身が空になる
            logger.warning(
                "レスポンスに'url'がないか、または'url'の値がnullです。 :: %s",
                {"http_method": response.request.method, "url": response.request.url},
            )
            return None

        response = self.api._execute_http_request(http_method="get", url=url)
        response.encoding = "utf-8"
        # statistics系のURLLocationヘッダに記載されているURLの中身はJSONであること前提
        return response.json()

    def get_label_statistics(self, project_id: str) -> list[Any]:
        """
        getLabelStatistics APIのLocation headerの中身を返す。

        Args:
            project_id:

        Returns:

        """
        result = self._get_statistics_content(*self.api.get_label_statistics(project_id))
        if result is not None:
            return result
        else:
            return []

    def _get_statistics_daily_xxx(
        self,
        function: Callable[[dict[str, Any]], list[dict[str, Any]]],
        dt_from_date: datetime.date,
        dt_to_date: datetime.date,
    ) -> list[dict[str, Any]]:
        """statistics daily apiの結果を、3ヶ月ごと（webapiの制約の都合）に再帰的に取得する。

        Args:
            function (Callable): 実行する関数
            dt_from_date: 取得する期間の開始日
            dt_to_date: 取得する期間の終了日

        Returns:

        """
        results: list[dict[str, Any]] = []
        # 取得期間が最大3ヶ月になるようにする
        dt_max_to_date = dt_from_date + relativedelta(months=3, days=-1)
        dt_tmp_to_date = min(dt_max_to_date, dt_to_date)

        query_params = {"from": str(dt_from_date), "to": str(dt_tmp_to_date)}
        tmp_result: list[dict[str, Any]] = function(query_params)
        results.extend(tmp_result)

        dt_tmp_from_date = dt_tmp_to_date + datetime.timedelta(days=1)

        if dt_tmp_from_date <= dt_to_date:
            tmp_result = self._get_statistics_daily_xxx(function, dt_from_date=dt_tmp_from_date, dt_to_date=dt_to_date)
            results.extend(tmp_result)

        return results

    def _get_from_and_to_date_for_statistics_webapi(
        self, project_id: str, from_date: Optional[str], to_date: Optional[str]
    ) -> tuple[datetime.date, datetime.date]:
        """statistics webapi用に、`datetime.date`型であるfrom_date, to_dateを取得する。
        `from_date`または`to_date`がNoneならば、`get_statistics_available_dates` APIで取得した統計情報が存在する期間を参照して、`from_date`と`to_date`を決めます。

        Args:
            project_id (str): プロジェクトID。
            from_date (Optional[str]): 取得する統計の区間の開始日(YYYY-MM-DD)。
            to_date (Optional[str]): 取得する統計の区間の終了日(YYYY-MM-DD)。

        Returns:
            tuple[datetime.date, datetime.date]: [description]
        """  # noqa: E501
        if from_date is None or to_date is None:
            dates, _ = self.api.get_statistics_available_dates(project_id)
            assert len(dates) > 0
            if from_date is None:
                from_date = dates[0]["from"]
            if to_date is None:
                to_date = dates[-1]["to"]

        dt_from_date = datetime.datetime.fromisoformat(from_date).date()
        dt_to_date = datetime.datetime.fromisoformat(to_date).date()
        return dt_from_date, dt_to_date

    def get_account_daily_statistics(
        self, project_id: str, *, from_date: Optional[str] = None, to_date: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """指定した期間の ユーザ別タスク集計データ を取得します。

        Args:
            project_id: プロジェクトID
            from_date (Optional[str]): 取得する統計の区間の開始日(YYYY-MM-DD)。Noneの場合は、プロジェクト作成日を開始日とみなします。
            to_date (Optional[str]): 取得する統計の区間の終了日(YYYY-MM-DD)。Noneの場合は、今日の日付を終了日とみなします。

        Returns:
            ユーザ別タスク集計データ
        """

        def decorator(f, project_id: str):  # noqa: ANN001, ANN202
            @functools.wraps(f)
            def wrapper(*args, **kwargs):  # noqa: ANN202
                content, _ = f(project_id, *args, **kwargs)
                return content

            return wrapper

        dt_from_date, dt_to_date = self._get_from_and_to_date_for_statistics_webapi(project_id, from_date=from_date, to_date=to_date)
        func = decorator(self.api.get_account_daily_statistics, project_id)
        result = self._get_statistics_daily_xxx(func, dt_from_date=dt_from_date, dt_to_date=dt_to_date)

        tmp_dict_results = defaultdict(list)
        for elm in result:
            tmp_dict_results[elm["account_id"]].extend(elm["histories"])

        return [{"account_id": k, "histories": v} for k, v in tmp_dict_results.items()]

    def get_inspection_daily_statistics(
        self, project_id: str, *, from_date: Optional[str] = None, to_date: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """
        指定した期間の 検査コメント集計データ を取得します。

        Args:
            project_id: プロジェクトID
            from_date (Optional[str]): 取得する統計の区間の開始日(YYYY-MM-DD)。Noneの場合は、プロジェクト作成日を開始日とみなします。
            to_date (Optional[str]): 取得する統計の区間の終了日(YYYY-MM-DD)。Noneの場合は、今日の日付を終了日とみなします。

        Returns:
            検査コメント集計データ

        """

        def decorator(f, project_id: str):  # noqa: ANN001, ANN202
            @functools.wraps(f)
            def wrapper(*args, **kwargs):  # noqa: ANN202
                content, _ = f(project_id, *args, **kwargs)
                return content

            return wrapper

        dt_from_date, dt_to_date = self._get_from_and_to_date_for_statistics_webapi(project_id, from_date=from_date, to_date=to_date)
        func = decorator(self.api.get_inspection_daily_statistics, project_id)
        return self._get_statistics_daily_xxx(func, dt_from_date=dt_from_date, dt_to_date=dt_to_date)

    def get_phase_daily_statistics(self, project_id: str, *, from_date: Optional[str] = None, to_date: Optional[str] = None) -> list[dict[str, Any]]:
        """指定した期間の フェーズ別タスク集計データ を取得します。

        Args:
            project_id: プロジェクトID
            from_date (Optional[str]): 取得する統計の区間の開始日(YYYY-MM-DD)。Noneの場合は、プロジェクト作成日を開始日とみなします。
            to_date (Optional[str]): 取得する統計の区間の終了日(YYYY-MM-DD)。Noneの場合は、今日の日付を終了日とみなします。

        Returns:
            フェーズ別タスク集計データ

        """

        def decorator(f, project_id: str):  # noqa: ANN001, ANN202
            @functools.wraps(f)
            def wrapper(*args, **kwargs):  # noqa: ANN202
                content, _ = f(project_id, *args, **kwargs)
                return content

            return wrapper

        dt_from_date, dt_to_date = self._get_from_and_to_date_for_statistics_webapi(project_id, from_date=from_date, to_date=to_date)
        func = decorator(self.api.get_phase_daily_statistics, project_id)
        return self._get_statistics_daily_xxx(func, dt_from_date=dt_from_date, dt_to_date=dt_to_date)

    def get_task_daily_statistics(self, project_id: str, *, from_date: Optional[str] = None, to_date: Optional[str] = None) -> list[dict[str, Any]]:
        """指定した期間の タスク集計データ を取得します。

        Args:
            project_id: プロジェクトID
            from_date (Optional[str]): 取得する統計の区間の開始日(YYYY-MM-DD)。Noneの場合は、プロジェクト作成日を開始日とみなします。
            to_date (Optional[str]): 取得する統計の区間の終了日(YYYY-MM-DD)。Noneの場合は、今日の日付を終了日とみなします。

        Returns:
            タスク集計データ

        """

        def decorator(f, project_id: str):  # noqa: ANN001, ANN202
            @functools.wraps(f)
            def wrapper(*args, **kwargs):  # noqa: ANN202
                content, _ = f(project_id, *args, **kwargs)
                return content

            return wrapper

        dt_from_date, dt_to_date = self._get_from_and_to_date_for_statistics_webapi(project_id, from_date=from_date, to_date=to_date)
        func = decorator(self.api.get_task_daily_statistics, project_id)
        return self._get_statistics_daily_xxx(func, dt_from_date=dt_from_date, dt_to_date=dt_to_date)

    def get_worktime_daily_statistics(self, project_id: str, *, from_date: Optional[str] = None, to_date: Optional[str] = None) -> dict[str, Any]:
        """プロジェクト全体のタスク作業時間集計データを取得します。

        Args:
            project_id: プロジェクトID
            from_date (Optional[str]): 取得する統計の区間の開始日(YYYY-MM-DD)。Noneの場合は、プロジェクト作成日を開始日とみなします。
            to_date (Optional[str]): 取得する統計の区間の終了日(YYYY-MM-DD)。Noneの場合は、今日の日付を終了日とみなします。

        Returns:
            プロジェクト全体のタスク作業時間集計データ
        """

        def decorator(f, project_id: str):  # noqa: ANN001, ANN202
            @functools.wraps(f)
            def wrapper(*args, **kwargs):  # noqa: ANN202
                content, _ = f(project_id, *args, **kwargs)
                return content["data_series"]

            return wrapper

        dt_from_date, dt_to_date = self._get_from_and_to_date_for_statistics_webapi(project_id, from_date=from_date, to_date=to_date)
        func = decorator(self.api.get_worktime_daily_statistics, project_id)
        result = self._get_statistics_daily_xxx(func, dt_from_date=dt_from_date, dt_to_date=dt_to_date)
        return {"project_id": project_id, "data_series": result}

    def get_worktime_daily_statistics_by_account(
        self, project_id: str, account_id: str, *, from_date: Optional[str] = None, to_date: Optional[str] = None
    ) -> dict[str, Any]:
        """指定したプロジェクトメンバーのタスク作業時間集計データを取得します。

        Args:
            project_id: プロジェクトID
            account_id: アカウントID
            from_date (Optional[str]): 取得する統計の区間の開始日(YYYY-MM-DD)。Noneの場合は、プロジェクト作成日を開始日とみなします。
            to_date (Optional[str]): 取得する統計の区間の終了日(YYYY-MM-DD)。Noneの場合は、今日の日付を終了日とみなします。

        Returns:
            プロジェクトメンバーのタスク作業時間集計データ
        """

        def decorator(f, project_id: str, account_id: str):  # noqa: ANN001, ANN202
            @functools.wraps(f)
            def wrapper(*args, **kwargs):  # noqa: ANN202
                content, _ = f(project_id, account_id, *args, **kwargs)
                return content["data_series"]

            return wrapper

        dt_from_date, dt_to_date = self._get_from_and_to_date_for_statistics_webapi(project_id, from_date=from_date, to_date=to_date)
        func = decorator(self.api.get_worktime_daily_statistics_by_account, project_id, account_id)
        result = self._get_statistics_daily_xxx(func, dt_from_date=dt_from_date, dt_to_date=dt_to_date)
        return {"project_id": project_id, "account_id": account_id, "data_series": result}

    #########################################
    # Public Method : Supplementary
    #########################################

    def get_supplementary_data_list_or_none(self, project_id: str, input_data_id: str) -> Optional[list[dict[str, Any]]]:
        """
        補助情報一覧を取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            project_id:
            input_data_id:

        Returns:
            補助情報一覧
        """
        content, response = self.api.get_supplementary_data_list(project_id, input_data_id, raise_for_status=False)
        if response.status_code == requests.codes.not_found:
            return None
        else:
            _log_error_response(logger, response)
            _raise_for_status(response)
            return content

    def put_supplementary_data_from_file(
        self,
        project_id: str,
        input_data_id: str,
        supplementary_data_id: str,
        file_path: str,
        request_body: dict[str, Any],
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
        new_content_type = self._get_mime_type(file_path) if content_type is None else content_type

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

        return self.api.put_supplementary_data(project_id, input_data_id, supplementary_data_id, request_body=copied_request_body)[0]

    #########################################
    # Public Method : Inspection
    #########################################

    #########################################
    # Public Method : My
    #########################################
    def get_all_my_organizations(self) -> list[MyOrganization]:
        """
        所属しているすべての組織一覧を取得する

        Returns:
            すべての所属一覧
        """
        # クエリパラメータを指定できないので、そのままAPIを実行する
        content, _ = self.api.get_my_organizations()
        return content["list"]

    #########################################
    # Public Method : Organization
    #########################################
    def get_organization_or_none(self, organization_name: str) -> Optional[Organization]:
        """
        組織情報を取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            organization_name: 組織名

        Returns:
            組織情報
        """
        content, response = self.api.get_organization(organization_name, raise_for_status=False)

        if response.status_code == requests.codes.not_found:
            return None
        else:
            _log_error_response(logger, response)
            _raise_for_status(response)
            return content

    def get_all_projects_of_organization(self, organization_name: str, query_params: Optional[dict[str, Any]] = None) -> list[Project]:
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
    def get_organization_member_or_none(self, organization_name: str, user_id: str) -> Optional[OrganizationMember]:
        """
        組織メンバを取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            organization_name: 組織名
            user_id:

        Returns:
            組織メンバ
        """
        content, response = self.api.get_organization_member(organization_name, user_id, raise_for_status=False)
        if response.status_code == requests.codes.not_found:
            return None
        else:
            _log_error_response(logger, response)
            _raise_for_status(response)
            return content

    def get_all_organization_members(self, organization_name: str) -> list[OrganizationMember]:
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
    def get_project_or_none(self, project_id: str) -> Optional[Project]:
        """
        プロジェクトを取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            project_id:

        Returns:
            プロジェクト
        """
        content, response = self.api.get_project(project_id, raise_for_status=False)
        if response.status_code == requests.codes.not_found:
            return None
        else:
            _log_error_response(logger, response)
            _raise_for_status(response)
            return content

    def download_project_inputs_url(self, project_id: str, dest_path: Union[str, Path]) -> str:
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
        self.download(url, dest_path, logger_prefix=f"project_id='{project_id}', ダウンロード対象のファイル='入力データ全件ファイル'")
        return url

    def download_project_tasks_url(self, project_id: str, dest_path: Union[str, Path]) -> str:
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
        self.download(url, dest_path, logger_prefix=f"project_id='{project_id}', ダウンロード対象のファイル='タスク全件ファイル'")
        return url

    def download_project_inspections_url(self, project_id: str, dest_path: Union[str, Path]) -> str:
        """
        プロジェクトの検査コメント全件ファイルをダウンロードする。
        ファイルの中身はJSON。

        .. deprecated:: 2022-08-23以降に廃止する予定です。検査コメントに関するWebAPIが廃止されるためです。

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先ファイルのパス

        Returns:
            ダウンロード元のURL

        """
        warnings.warn(
            "annofabapi.Wrapper.download_project_inspections_url() is deprecated and will be removed.",
            FutureWarning,
            stacklevel=2,
        )

        content, _ = self.api.get_project_inspections_url(project_id)
        url = content["url"]
        self.download(url, dest_path, logger_prefix=f"project_id='{project_id}', ダウンロード対象のファイル='検査コメント全件ファイル'")
        return url

    def download_project_comments_url(self, project_id: str, dest_path: Union[str, Path]) -> str:
        """
        プロジェクトのコメント全件ファイルをダウンロードする。

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先ファイルのパス

        Returns:
            ダウンロード元のURL

        """

        content, _ = self.api.get_project_comments_url(project_id)
        url = content["url"]
        self.download(url, dest_path, logger_prefix=f"project_id='{project_id}', ダウンロード対象のファイル='コメント全件ファイル'")
        return url

    def download_project_task_history_events_url(self, project_id: str, dest_path: Union[str, Path]) -> str:
        """
        プロジェクトのタスク履歴イベント全件ファイルをダウンロードする。
        ファイルの中身はJSON。

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先ファイルのパス

        Returns:
            ダウンロード元のURL

        """
        with warnings.catch_warnings():
            # `get_project_task_history_events_url`関数は非推奨だが、タスク履歴イベントでしか取得できない情報があるため、annofab-cliなどではよく利用する  # noqa: E501
            # `get_project_task_history_events_url`関数がいつ廃止さるのかは未定なので、`get_project_task_history_events_url`関数実行時の警告を無視する
            warnings.simplefilter("ignore", category=FutureWarning)
            content, _ = self.api.get_project_task_history_events_url(project_id)

        url = content["url"]
        self.download(url, dest_path, logger_prefix=f"project_id='{project_id}', ダウンロード対象のファイル='タスク履歴イベント全件ファイル'")
        return url

    def download_project_task_histories_url(self, project_id: str, dest_path: Union[str, Path]) -> str:
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
        self.download(url, dest_path, logger_prefix=f"project_id='{project_id}', ダウンロード対象のファイル='タスク履歴全件ファイル'")
        return url

    #########################################
    # Public Method : ProjectMember
    #########################################
    def get_project_member_or_none(self, project_id: str, user_id: str) -> Optional[ProjectMember]:
        """
        プロジェクトメンバを取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            project_id:
            user_id:

        Returns:
            プロジェクトメンバ
        """
        content, response = self.api.get_project_member(project_id, user_id, raise_for_status=False)
        if response.status_code == requests.codes.not_found:
            return None
        else:
            _log_error_response(logger, response)
            _raise_for_status(response)
            return content

    def get_all_project_members(self, project_id: str, query_params: Optional[dict[str, Any]] = None) -> list[ProjectMember]:
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

    #########################################
    # Public Method : Task
    #########################################
    def initiate_tasks_generation_by_csv(self, project_id: str, csvfile_path: str) -> dict[str, Any]:
        """
        タスクID,入力データ名,入力データID」を1行毎に指定したCSVを使って、タスクを生成する

        Args:
            project_id: プロジェクトID
            csvfile_path: CSVファイルのパス

        Returns:
            `initiate_tasks_generation` APIのContent
        """
        s3_path = self.upload_file_to_s3(project_id, csvfile_path, "text/csv")

        project_last_updated_datetime = self.api.get_project(project_id)[0]["updated_datetime"]

        request_body = {
            "task_generate_rule": {"_type": "ByInputDataCsv", "csv_data_path": s3_path},
            "project_last_updated_datetime": project_last_updated_datetime,
        }
        return self.api.initiate_tasks_generation(project_id, request_body=request_body)[0]

    def get_task_or_none(self, project_id: str, task_id: str) -> Optional[Task]:
        """
        タスクを取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            project_id:
            task_id:

        Returns:
            タスク
        """
        content, response = self.api.get_task(project_id, task_id, raise_for_status=False)

        if response.status_code == requests.codes.not_found:
            return None
        else:
            _log_error_response(logger, response)
            _raise_for_status(response)
            return content

    def get_task_histories_or_none(self, project_id: str, task_id: str) -> Optional[list[Task]]:
        """
        タスク履歴一覧を取得する。存在しない場合(HTTP 404 Error)はNoneを返す。

        Args:
            project_id:
            task_id:

        Returns:
            タスク履歴一覧
        """
        content, response = self.api.get_task_histories(project_id, task_id, raise_for_status=False)
        if response.status_code == requests.codes.not_found:
            return None
        else:
            _log_error_response(logger, response)
            _raise_for_status(response)
            return content

    def get_all_tasks(self, project_id: str, query_params: Optional[dict[str, Any]] = None) -> list[Task]:
        """
        すべてのタスクを取得する。

        Args:
            project_id: プロジェクトID
            query_params: `api.get_tasks` メソッドに渡すQuery Parameter

        Returns:
            すべてのタスク一覧
        """
        return self._get_all_objects(self.api.get_tasks, limit=200, project_id=project_id, query_params=query_params)

    def change_task_status_to_working(self, project_id: str, task_id: str, *, last_updated_datetime: Optional[str] = None) -> Task:
        """
        タスクのステータスを「作業中」に変更します。

        Notes:
            * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。
            * 現在の状態が未着手(not_started)、休憩中(break)、保留(on_hold)のいずれかであるタスクに対してのみ、この操作を行うことができます。

        Args:
            project_id: プロジェクトID
            task_id: タスクID
            last_updated_datetime: `operate_task` APIのリクエストボディに渡すタスクの最終更新日時。Noneなら`get_task`APIを実行して、タスクの最終更新日時を取得します。

        Returns:
            変更後のタスク
        """  # noqa: E501
        if last_updated_datetime is None:
            task, _ = self.api.get_task(project_id, task_id)
            last_updated_datetime = task["updated_datetime"]
        request_body = {
            "status": TaskStatus.WORKING.value,
            "account_id": self.api.account_id,
            "last_updated_datetime": last_updated_datetime,
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def change_task_status_to_break(self, project_id: str, task_id: str, *, last_updated_datetime: Optional[str] = None) -> Task:
        """
        タスクのステータスを「休憩中」に変更します。

        Notes:
            * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。
            * 現在の状態が作業中(working)のタスクに対してのみ、この操作を行うことができます。

        Args:
            project_id: プロジェクトID
            task_id: タスクID
            last_updated_datetime: `operate_task` APIのリクエストボディに渡すタスクの最終更新日時。Noneなら`get_task`APIを実行して、タスクの最終更新日時を取得します。

        Returns:
            変更後のタスク
        """  # noqa: E501
        if last_updated_datetime is None:
            task, _ = self.api.get_task(project_id, task_id)
            last_updated_datetime = task["updated_datetime"]

        request_body = {
            "status": TaskStatus.BREAK.value,
            "account_id": self.api.account_id,
            "last_updated_datetime": last_updated_datetime,
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def change_task_status_to_on_hold(self, project_id: str, task_id: str, *, last_updated_datetime: Optional[str] = None) -> Task:
        """
        タスクのステータスを「保留」に変更します。

        Notes:
            * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。
            * 現在の状態が作業中(working)のタスクに対してのみ、この操作を行うことができます。

        Args:
            project_id: プロジェクトID
            task_id: タスクID
            last_updated_datetime: `operate_task` APIのリクエストボディに渡すタスクの最終更新日時。Noneなら`get_task`APIを実行して、タスクの最終更新日時を取得します。

        Returns:
            変更後のタスク
        """  # noqa: E501
        if last_updated_datetime is None:
            task, _ = self.api.get_task(project_id, task_id)
            last_updated_datetime = task["updated_datetime"]

        request_body = {
            "status": TaskStatus.ON_HOLD.value,
            "account_id": self.api.account_id,
            "last_updated_datetime": last_updated_datetime,
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def complete_task(self, project_id: str, task_id: str, *, last_updated_datetime: Optional[str] = None) -> Task:
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
            last_updated_datetime: `operate_task` APIのリクエストボディに渡すタスクの最終更新日時。Noneなら`get_task`APIを実行して、タスクの最終更新日時を取得します。

        Returns:
            変更後のタスク
        """  # noqa: E501
        if last_updated_datetime is None:
            task, _ = self.api.get_task(project_id, task_id)
            last_updated_datetime = task["updated_datetime"]

        request_body = {
            "status": TaskStatus.COMPLETE.value,
            "account_id": self.api.account_id,
            "last_updated_datetime": last_updated_datetime,
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def cancel_submitted_task(self, project_id: str, task_id: str, *, last_updated_datetime: Optional[str] = None) -> Task:
        """
        タスクの提出を取り消します。
        「提出されたタスク」とは、以下の状態のタスクのことです。
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
            last_updated_datetime: `operate_task` APIのリクエストボディに渡すタスクの最終更新日時。Noneなら`get_task`APIを実行して、タスクの最終更新日時を取得します。

        Returns:
            変更後のタスク
        """  # noqa: E501
        if last_updated_datetime is None:
            task, _ = self.api.get_task(project_id, task_id)
            last_updated_datetime = task["updated_datetime"]

        request_body = {
            "status": TaskStatus.CANCELLED.value,
            "account_id": self.api.account_id,
            "last_updated_datetime": last_updated_datetime,
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def cancel_completed_task(
        self,
        project_id: str,
        task_id: str,
        operator_account_id: Optional[str],
        *,
        last_updated_datetime: Optional[str] = None,
    ) -> Task:
        """
        タスクの完了状態を取り消します。
        このメソッドを実行すると、タスクの`status`は`not_started`になります。

        Notes:
            `phase`が`acceptance`, `status`が`completed`のタスクを想定しています。
            それ以外のタスクに対して実行してもエラーにはならず、`status`が`not_started`になります。

        Args:
            project_id: プロジェクトID
            task_id: タスクID
            operator_account_id: 受入完了状態を取り消した後の担当者のaccount_id
            last_updated_datetime: `operate_task` APIのリクエストボディに渡すタスクの最終更新日時。Noneなら`get_task`APIを実行して、タスクの最終更新日時を取得します。

        Returns:
            変更後のタスク
        """  # noqa: E501
        if last_updated_datetime is None:
            task, _ = self.api.get_task(project_id, task_id)
            last_updated_datetime = task["updated_datetime"]

        request_body = {
            "status": TaskStatus.NOT_STARTED.value,
            "account_id": operator_account_id,
            "last_updated_datetime": last_updated_datetime,
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def change_task_operator(
        self,
        project_id: str,
        task_id: str,
        operator_account_id: Optional[str],
        *,
        last_updated_datetime: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        タスクの担当者を変更します。

        Notes:
            * プロジェクトオーナー(owner)、もしくは受入担当者(accepter)のみ、この操作を行うことができます。

        Args:
            project_id: プロジェクトID
            task_id: タスクID
            operator_account_id: 新しい担当者のaccount_id。Noneの場合は、担当者を「未割り当て」にします。
            last_updated_datetime: `operate_task` APIのリクエストボディに渡すタスクの最終更新日時。Noneなら`get_task`APIを実行して、タスクの最終更新日時を取得します。

        Returns:
            変更後のタスク

        """  # noqa: E501
        if last_updated_datetime is None:
            task, _ = self.api.get_task(project_id, task_id)
            last_updated_datetime = task["updated_datetime"]

        request_body = {
            "status": TaskStatus.NOT_STARTED.value,
            "account_id": operator_account_id,
            "last_updated_datetime": last_updated_datetime,
        }
        updated_task, _ = self.api.operate_task(project_id, task_id, request_body=request_body)
        return updated_task

    def reject_task(self, project_id: str, task_id: str, *, force: bool = False, last_updated_datetime: Optional[str] = None) -> dict[str, Any]:
        """
        タスクを差し戻します。
        このメソッドを実行すると、`phase`は`annotation`になります。

        Notes:
            * 通常の差し戻しの場合(force=False)
                * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。
                * 現在の状態が作業中(working)のタスクに対してのみ、この操作を行うことができます。
            * 強制差し戻しの場合(force=True)
                * タスクの状態・フェーズを無視して、フェーズを教師付け(annotation)に、状態を未作業(not started)に変更します。
                * この差戻しは、抜取検査・抜取受入のスキップ判定に影響を及ぼしません。

        Args:
            project_id: プロジェクトID
            task_id: タスクID
            force: Trueなら強制差し戻し、Falseなら通常の差し戻しを実施する
            last_updated_datetime: `operate_task` APIのリクエストボディに渡すタスクの最終更新日時。Noneなら`get_task`APIを実行して、タスクの最終更新日時を取得します。

        Returns:
            変更後のタスク

        """  # noqa: E501
        if last_updated_datetime is None:
            task, _ = self.api.get_task(project_id, task_id)
            last_updated_datetime = task["updated_datetime"]

        request_body = {
            "status": TaskStatus.REJECTED.value,
            "account_id": self.api.account_id,
            "last_updated_datetime": last_updated_datetime,
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

    def upload_instruction_image(self, project_id: str, image_id: str, file_path: str, content_type: Optional[str] = None) -> str:
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
        new_content_type = self._get_mime_type(file_path) if content_type is None else content_type

        with open(file_path, "rb") as f:
            return self.upload_data_as_instruction_image(project_id, image_id, data=f, content_type=new_content_type)

    def upload_data_as_instruction_image(self, project_id: str, image_id: str, data: Any, content_type: str) -> str:  # noqa: ANN401
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
        content, _ = self.api.get_instruction_image_url_for_put(project_id, image_id)

        url_parse_result = urllib.parse.urlparse(content["url"])
        query_dict = urllib.parse.parse_qs(url_parse_result.query)

        # URL Queryを除いたURLを取得する
        s3_url = content["url"].split("?")[0]

        # アップロード
        self.api._execute_http_request(http_method="put", url=s3_url, params=query_dict, data=data, headers={"content-type": content_type})
        return content["path"]

    #########################################
    # Public Method : Job
    #########################################
    def delete_all_succeeded_job(self, project_id: str, job_type: ProjectJobType) -> list[ProjectJobInfo]:
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
            if job["job_status"] == JobStatus.SUCCEEDED.value:
                self.api.delete_project_job(project_id, job_type=job_type.value, job_id=job["job_id"])
                deleted_jobs.append(job)

        return deleted_jobs

    def get_all_project_job(self, project_id: str, query_params: Optional[dict[str, Any]] = None) -> list[ProjectJobInfo]:
        """
        すべてのバックグランドジョブを取得する。

        Args:
            project_id: プロジェクトID
            query_params: `api.get_project_job` メソッドに渡すQuery Parameter

        Returns:
            すべてのバックグランドジョブ一覧
        """
        copied_params = copy.deepcopy(query_params) if query_params is not None else {}

        all_jobs: list[dict[str, Any]] = []
        limit = 200
        # クエリパラメタ`page`が未実装なため、`1`を指定する
        copied_params.update({"page": 1, "limit": limit})
        r = self.api.get_project_job(project_id, query_params=copied_params)[0]
        all_jobs.extend(r["list"])
        return all_jobs

    def job_in_progress(self, project_id: str, job_type: ProjectJobType) -> bool:
        """
        ジョブが進行中状態かどうか

        Args:
            project_id: プロジェクトID
            job_type: ジョブ種別

        Returns:
            ジョブが進行中状態ならば ``True`` を返します。それ以外の状態の場合は ``False`` を返します。
            また、``job_type`` であるジョブが存在しない場合は ``False`` を返します。

        """
        job_list = self.api.get_project_job(project_id, query_params={"type": job_type.value})[0]["list"]
        if len(job_list) == 0:
            return False

        job = job_list[0]
        return job["job_status"] == JobStatus.PROGRESS.value

    def wait_for_completion(
        self,
        project_id: str,
        job_type: ProjectJobType,
        job_access_interval: int = 60,
        max_job_access: int = 10,
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
        job_status = self.wait_until_job_finished(project_id, job_type, job_access_interval=job_access_interval, max_job_access=max_job_access)
        if job_status is None:
            # 実行中のジョブが存在しない
            return True

        return job_status == JobStatus.SUCCEEDED

    def wait_until_job_finished(
        self,
        project_id: str,
        job_type: ProjectJobType,
        job_id: Optional[str] = None,
        job_access_interval: int = 60,
        max_job_access: int = 360,
    ) -> Optional[JobStatus]:
        """
        指定したジョブが終了するまで待つ。

        Args:
            project_id: プロジェクトID
            job_type: ジョブ種別
            job_id: ジョブID。Noneの場合は、現在進行中のジョブが終了するまで待つ。
            job_access_interval: ジョブにアクセスする間隔[sec]
            max_job_access: ジョブに最大何回アクセスするか

        Returns:
            指定した時間（アクセス頻度と回数）待った後のジョブのステータスを返す。
            指定したジョブ（job_idがNoneの場合は現在進行中のジョブ）が存在しない場合は、Noneを返す。

        """

        def get_latest_job() -> Optional[ProjectJobInfo]:
            job_list = self.api.get_project_job(project_id, query_params={"type": job_type.value})[0]["list"]
            if len(job_list) > 0:
                return job_list[0]
            else:
                return None

        def get_job_from_job_id(arg_job_id: str) -> Optional[ProjectJobInfo]:
            content, _ = self.api.get_project_job(project_id, query_params={"type": job_type.value})
            job_list = content["list"]
            return more_itertools.first_true(job_list, pred=lambda e: e["job_id"] == arg_job_id)

        job_access_count = 0
        while True:
            if job_id is not None:
                job = get_job_from_job_id(job_id)
            else:
                # 初回のみ
                job = get_latest_job()
                if job is None or job["job_status"] != JobStatus.PROGRESS.value:
                    logger.info(
                        "project_id='%s', job_type='%s' である進行中のジョブは存在しません。",
                        project_id,
                        job_type.value,
                    )
                    return None
                job_id = job["job_id"]

            if job is None:
                logger.info(
                    "project_id='%s', job_id='%s', job_type='%s' のジョブは存在しません。",
                    project_id,
                    job_type.value,
                    job_id,
                )
                return None

            job_access_count += 1

            if job["job_status"] == JobStatus.SUCCEEDED.value:
                logger.info(
                    "project_id='%s', job_id='%s', job_type='%s' のジョブが成功しました。",
                    project_id,
                    job_id,
                    job_type.value,
                )
                return JobStatus.SUCCEEDED

            elif job["job_status"] == JobStatus.FAILED.value:
                logger.info(
                    "project_id='%s', job_id='%s', job_type='%s' のジョブが失敗しました。:: errors='%s'",
                    project_id,
                    job_id,
                    job_type.value,
                    job["errors"],
                )
                return JobStatus.FAILED

            else:  # noqa: PLR5501
                # 進行中
                if job_access_count < max_job_access:
                    logger.info(
                        "project_id='%s', job_id='%s', job_type='%s' のジョブは進行中です。%d 秒間待ちます。",
                        project_id,
                        job_id,
                        job_type.value,
                        job_access_interval,
                    )
                    time.sleep(job_access_interval)
                else:
                    logger.info(
                        "project_id='%s', job_id='%s', job_type='%s' のジョブは %.1f 分以上経過しても、終了しませんでした。",
                        project_id,
                        job["job_id"],
                        job_type.value,
                        job_access_interval * job_access_count / 60,
                    )
                    return JobStatus.PROGRESS

    def can_execute_job(self, project_id: str, job_type: ProjectJobType) -> bool:
        """
        ジョブが実行できる状態か否か。他のジョブが実行中で同時に実行できない場合はFalseを返す。

        Args:
            project_id: プロジェクトID
            job_type: 実行したいジョブの種別

        Returns:
            ジョブが実行できる状態か否か
        """
        job_type_list = _JOB_CONCURRENCY_LIMIT[job_type]

        # 依存する複数のジョブが進行中状態かどうかを確認する
        result_list = [self.job_in_progress(project_id, dependent_job_type) for dependent_job_type in job_type_list]

        # 依存するすべてのジョブが進行中状態なら
        return all(not e for e in result_list)

    def wait_until_job_is_executable(
        self,
        project_id: str,
        job_type: ProjectJobType,
        job_access_interval: int = 60,
        max_job_access: int = 360,
    ) -> bool:
        """
        ジョブが実行可能な状態になるまで待ちます。他のジョブが実行されているときは、他のジョブが終了するまで待ちます。

        Args:
            project_id: プロジェクトID
            job_type: 実行したいジョブの種別
            job_access_interval: ジョブにアクセスする間隔[sec]
            max_job_access: ジョブに最大何回アクセスするか

        Returns:
            指定した時間（アクセス頻度と回数）待った後、ジョブが実行可能な状態かどうか。進行中のジョブが存在する場合は、ジョブが実行不可能。

        """

        job_type_list = _JOB_CONCURRENCY_LIMIT[job_type]

        # `job_type`のジョブと同時に実行できないジョブが終了するまで待ちます。
        # 非同期で実行しない理由：同期的に実行しても、最終的な待ち時間は変わらないため
        result_list = []
        for dependent_job_type in job_type_list:
            result = self.wait_until_job_finished(project_id, dependent_job_type, None, job_access_interval, max_job_access)
            result_list.append(result)

        # 依存するジョブが一つ以上進行中状態なら、Falseを返す
        return all(e != JobStatus.PROGRESS for e in result_list)
