import copy
import logging
import mimetypes
import urllib
import urllib.parse
from typing import Any, Callable, Dict, List, Optional, Tuple  # pylint: disable=unused-import

import annofabapi.utils
from annofabapi import AnnofabApi
from annofabapi.exceptions import AnnofabApiException
from annofabapi.typing import (AnnotationSpecs, InputData, Inspection, OrganizationMember, Project, ProjectJob,
                               ProjectMember, SupplementaryData, Task)

logger = logging.getLogger(__name__)


class Wrapper:
    """
    AnnofabApiのラッパー.
    """

    def __init__(self, api: AnnofabApi):
        """
        Args:
            api: AnnofabApi Instance
        """
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

        """

        if content_type is None:
            new_content_type = mimetypes.guess_type(file_path)[0]
            if new_content_type is None:
                logger.info(f"mimetypes.guess_type function can't guess type. file_path = {file_path}")
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
        Args:
            func_get_list: AnnofabApiのget_XXX関数
            limit: 1ページあたりの取得するデータ件数
            **kwargs_for_func_get_list: `func_get_list`に渡す引数。

        Returns:
            get_XXX関数で取得した情報の一覧

        """
        arg_query_params = kwargs_for_func_get_list['query_params']
        copied_query_params = copy.deepcopy(arg_query_params) if arg_query_params is not None else {}

        all_objects: List[Dict[str, Any]] = []

        copied_query_params.update({"page": 1, "limit": limit})
        kwargs_for_func_get_list['query_params'] = copied_query_params
        content, _ = func_get_list(**kwargs_for_func_get_list)

        all_objects.extend(content["list"])

        while content["page_no"] < content["total_page_no"]:
            next_page_no = content["page_no"] + 1
            copied_query_params.update({"page": next_page_no})
            kwargs_for_func_get_list['query_params'] = copied_query_params
            content, _ = func_get_list(**kwargs_for_func_get_list)
            all_objects.extend(content["list"])
            logger.debug(f"{func_get_list.__name__} {content['page_no']} / {content['total_page_no']} page")

        return all_objects

    #########################################
    # Public Method : AfAnnotationApi
    #########################################
    def download_annotation_archive(self, project_id: str, dest_path: str) -> str:
        """
        simpleアノテーションZIPをダウンロードする。

        Args:
            project_id: プロジェクトID
            dest_path: ダウンロード先のファイルパス

        Returns:
            ダウンロード元のURL

        """

        _, response = self.api.get_annotation_archive(project_id)
        url = response.headers['Location']
        annofabapi.utils.download(url, dest_path)
        return url

    def get_all_annotation_list(self, project_id: str,
                                query_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        すべてのアノテーション情報を取得する。
        Args:
            project_id: プロジェクトID
            query_params: `api.get_annotation_list` メソッドのQuery Parameter

        Returns:
            すべてのアノテーション一覧
        """
        return self._get_all_objects(self.api.get_annotation_list, limit=200, project_id=project_id,
                                     query_params=query_params)

    #########################################
    # Public Method : AfAnnotationSpecsApi
    #########################################
    def copy_annotation_specs(self, src_project_id: str, dest_project_id: str) -> AnnotationSpecs:
        """
        アノテーション仕様を、別のプロジェクトにコピーする。
        【注意】誤って実行しないようにすること

        Args:
            src_project_id: コピー元のproject_id
            dest_project_id: コピー先のproject_id

        Returns:
            put_annotation_specsのContent
        """
        src_annotation_specs = self.api.get_annotation_specs(src_project_id)[0]
        dest_annotation_specs = self.api.get_annotation_specs(dest_project_id)[0]

        request_body = {
            "labels": src_annotation_specs["labels"],
            "inspection_phrases": src_annotation_specs["inspection_phrases"],
            "updated_datetime": dest_annotation_specs["updated_datetime"],
        }
        return self.api.put_annotation_specs(dest_project_id, request_body=request_body)[0]

    #########################################
    # Public Method : AfInputApi
    #########################################
    def get_all_input_data_list(self, project_id: str,
                                query_params: Optional[Dict[str, Any]] = None) -> List[InputData]:
        """
        すべての入力データを取得する。

        Args:
            project_id: プロジェクトID
            query_params: `api.get_input_data_list` メソッドのQuery Parameter

        Returns:
            入力データ一覧
        """
        return self._get_all_objects(self.api.get_input_data_list, limit=200, project_id=project_id,
                                     query_params=query_params)

    def upload_file_to_s3(self, project_id: str, file_path: str, content_type: Optional[str] = None) -> str:
        """
        createTempPath APIを使ってアップロード用のURLとS3パスを取得して、ファイルをアップロードする。

        Args:
            project_id: プロジェクトID
            file_path: アップロードするファイルのパス
            content_type: アップロードするファイルのMIME Type. Noneの場合、ファイルパスから推測する。

        Returns:
            AnnoFabに登録するときのpath
        """

        # content_type を推測
        new_content_type = self._get_content_type(file_path, content_type)

        # 一時データ保存先を取得
        content = self.api.create_temp_path(project_id, header_params={'content-type': new_content_type})[0]

        url_parse_result = urllib.parse.urlparse(content["url"])
        query_dict = urllib.parse.parse_qs(url_parse_result.query)

        # URL Queryを除いたURLを取得する
        s3_url = content["url"].split("?")[0]

        # アップロード
        with open(file_path, 'rb') as f:
            res_put = self.api.session.put(s3_url, params=query_dict, data=f,
                                           headers={'content-type': new_content_type})

        annofabapi.utils.log_error_response(logger, res_put)
        annofabapi.utils.raise_for_status(res_put)
        return content["path"]

    def put_input_data_from_file(self, project_id: str, input_data_id: str, file_path: str,
                                 request_body: Optional[Dict[str, Any]] = None,
                                 content_type: Optional[str] = None) -> InputData:
        """
        ファイル（画像 or zip）を入力データとして登録する。
        zipファイルを指定した場合は、登録が完了した後「ZIPアップロードジョブエラー削除」(delete_project_job)を実施する必要がある。

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
    # Public Method : AfSupplementaryApi
    #########################################
    def put_supplementary_data_from_file(self, project_id, input_data_id: str, supplementary_data_id: str,
                                         file_path: str, request_body: Dict[str, Any],
                                         content_type: Optional[str] = None) -> SupplementaryData:
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

        if 'supplementary_data_name' not in copied_request_body:
            copied_request_body['supplementary_data_name'] = file_path

        if 'supplementary_data_type' not in copied_request_body:
            if new_content_type.startswith('image'):
                supplementary_data_type = 'image'
            elif new_content_type.startswith('text'):
                supplementary_data_type = 'text'
            else:
                raise AnnofabApiException(f"File type not supported. Content-Type={new_content_type}")
            copied_request_body['supplementary_data_type'] = supplementary_data_type

        return self.api.put_supplementary_data(project_id, input_data_id, supplementary_data_id,
                                               request_body=copied_request_body)[0]

    #########################################
    # Public Method : AfInspection
    #########################################
    def update_status_of_inspections(self, project_id: str, task_id: str, input_data_id: str,
                                     filter_inspection: Callable[[Inspection], bool],
                                     inspection_status: str) -> List[Inspection]:
        """
        検査コメント（返信コメント以外）のstatusを変更する。

        Args:
            project_id: プロジェクトID
            task_id: タスクID
            input_data_id: 入力データID
            filter_inspection: 変更対象の検査コメントを絞り込む条件
            inspection_status: 検査コメントのstatus

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

        for inspection in target_inspections:
            inspection["status"] = inspection_status
            if inspection["updated_datetime"] is None:
                inspection["updated_datetime"] = inspection["created_datetime"]

        req_inspection = [{"data": e, "_type": "Put"} for e in target_inspections]
        content = self.api.batch_update_inspections(project_id, task_id, input_data_id, req_inspection)[0]
        return content

    #########################################
    # Public Method : AfOrganizationApi
    #########################################
    def get_all_projects_of_organization(self, organization_name: str,
                                         query_params: Optional[Dict[str, Any]] = None) -> List[Project]:
        """
        組織配下のすべてのプロジェクト一覧を取得する
        Args:
            organization_name: 組織名
            query_params: `api.get_projects_of_organization` メソッドに渡すQuery Parameter

        Returns:
            すべてのプロジェクト一覧
        """
        return self._get_all_objects(self.api.get_projects_of_organization, limit=200,
                                     organization_name=organization_name, query_params=query_params)

    #########################################
    # Public Method : AfOrganizationMemberApi
    #########################################
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
    # Public Method : AfProjectApi
    #########################################
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
        annofabapi.utils.download(url, dest_path)
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
        annofabapi.utils.download(url, dest_path)
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
        annofabapi.utils.download(url, dest_path)
        return url

    #########################################
    # Public Method : AfProjectMemberApi
    #########################################
    def get_all_project_members(self, project_id: str,
                                query_params: Optional[Dict[str, Any]] = None) -> List[ProjectMember]:
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
        【注意】誤って実行しないようにすること

        Args:
            project_id: プロジェクトID
            project_members: 追加/更新するメンバのList. `user_id` , `member_status` , `member_role` をKeyに持つこと

        Returns:
            `putProjectMember` APIのContentのList

        """

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
                "last_updated_datetime": last_updated_datetime,
            }
            updated_project_member = self.api.put_project_member(project_id, member["user_id"],
                                                                 request_body=request_body)[0]
            updated_project_members.append(updated_project_member)

            logger.debug(f"プロジェクトメンバの{'追加' if last_updated_datetime is None else '更新'} 完了."
                         f" project_id={project_id}, user_id={member['user_id']}, "
                         f"last_updated_datetime={last_updated_datetime}")

        return updated_project_members

    def assign_role_to_project_members(self, project_id: str, user_id_list: List[str],
                                       member_role: str) -> List[ProjectMember]:
        """
        複数のプロジェクトメンバに1つのロールを割り当てる。
        【注意】誤って実行しないようにすること

        Args:
            project_id: プロジェクトID
            user_id_list: 追加/更新するメンバのuser_idのList
            member_role: 割り当てるロール.

        Returns:
            `putProjectMember` APIのContentのList

        """

        project_members = []
        for user_id in user_id_list:
            member = {'user_id': user_id, 'member_status': 'active', 'member_role': member_role}
            project_members.append(member)

        return self.put_project_members(project_id, project_members)

    def drop_role_to_project_members(self, project_id, user_id_list: List[str]) -> List[ProjectMember]:
        """
        複数のプロジェクトメンバを、プロジェクトから脱退させる
        【注意】誤って実行しないようにすること

        Args:
            project_id: プロジェクトID
            user_id_list: 脱退させるメンバのuser_idのList

        Returns:
            `putProjectMember` APIのContentのList
        """

        project_members = []
        for user_id in user_id_list:
            member = {
                'user_id': user_id,
                'member_status': 'inactive',
                'member_role': 'worker'  # 何か指定しないとエラーになったため、指定する
            }
            project_members.append(member)

        return self.put_project_members(project_id, project_members)

    def copy_project_members(self, src_project_id: str, dest_project_id: str,
                             delete_dest: bool = False) -> List[ProjectMember]:
        """
        プロジェクトメンバを、別のプロジェクトにコピーする。
        【注意】誤って実行しないようにすること

        Args:
            src_project_id: コピー元のproject_id
            dest_project_id: コピー先のproject_id
            delete_dest: Trueならばコピー先にしか存在しないプロジェクトメンバを削除する。

        Returns:
            `putProjectMember` APIのContentのList

        """
        src_project_members = self.get_all_project_members(src_project_id)
        dest_project_members = self.get_all_project_members(dest_project_id)

        if delete_dest:
            # コピー先にしかいないメンバを削除する
            src_account_ids = [e["account_id"] for e in src_project_members]
            deleted_dest_members = [e for e in dest_project_members if e["account_id"] not in src_account_ids]

            def to_inactive(arg_member):
                arg_member['member_status'] = 'inactive'
                return arg_member

            deleted_dest_members = list(map(to_inactive, deleted_dest_members))
            return self.put_project_members(dest_project_id, src_project_members + deleted_dest_members)

        else:
            return self.put_project_members(dest_project_id, src_project_members)

    #########################################
    # Public Method : AfTaskApi
    #########################################
    def initiate_tasks_generation_by_csv(self, project_id: str, csvfile_path: str,
                                         task_id_prefix: str) -> Dict[str, Any]:
        """
        CSV Fileでタスクを生成する

        Args:
            project_id: プロジェクトID
            csvfile_path: CSVファイルのパス
            task_id_prefix: 生成するタスクIDのプレフィックス

        Returns:
            `initiate_tasks_generation` APIのContent
        """
        s3_path = self.upload_file_to_s3(project_id, csvfile_path, "text/csv")

        project_last_updated_datetime = self.api.get_project(project_id)[0]['updated_datetime']

        request_body = {
            'task_generate_rule': {
                '_type': 'ByInputDataCsv',
                'csv_data_path': s3_path,
            },
            'task_id_prefix': task_id_prefix,
            'project_last_updated_datetime': project_last_updated_datetime
        }
        return self.api.initiate_tasks_generation(project_id, request_body=request_body)[0]

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

    #########################################
    # Public Method : AfInstructionApi
    #########################################
    def get_latest_instruction(self, project_id: str) -> str:
        """
        最新の作業ガイドの取得.
        ガイドが設定されていない場合は空文字を返す。

        Args:
            project_id: プロジェクトID

        Returns:
            作業ガイドのHTML
        """
        histories = self.api.get_instruction_history(project_id)[0]
        if len(histories) == 0:
            return ''

        latest_history_id = histories[0]['history_id']
        return self.api.get_instruction(project_id, latest_history_id)[0]

    def upload_instruction_image(self, project_id: str, image_id: str, file_path: str,
                                 content_type: Optional[str] = None) -> str:
        """
        作業ガイドの画像をアップロードする。image_idはUUIDv4

        Args:
            project_id: プロジェクトID
            image_id: 作業ガイド画像ID
            file_path: アップロードするファイル
            content_type: アップロードするファイルのMIME Type. Noneの場合、ファイルパスから推測する。

        Returns:
            AnnoFabに登録するときのpath
        """

        # content_type を推測
        new_content_type = self._get_content_type(file_path, content_type)

        # 作業ガイド登録用/更新用のURLを取得
        content = self.api.get_instruction_image_url_for_put(project_id, image_id,
                                                             header_params={'content-type': new_content_type})[0]

        url_parse_result = urllib.parse.urlparse(content["url"])
        query_dict = urllib.parse.parse_qs(url_parse_result.query)

        # URL Queryを除いたURLを取得する
        s3_url = content["url"].split("?")[0]

        # アップロード
        with open(file_path, 'rb') as f:
            res_put = self.api.session.put(s3_url, params=query_dict, data=f,
                                           headers={'content-type': new_content_type})
        annofabapi.utils.log_error_response(logger, res_put)
        annofabapi.utils.raise_for_status(res_put)
        return content["path"]

    #########################################
    # Public Method : AfJobApi
    #########################################
    def delete_all_succeeded_job(self, project_id: str, job_type: str) -> List[ProjectJob]:
        """
        成功したジョブをすべて削除する

        Args:
            project_id: プロジェクトID
            job_type: ジョブ種別("copy-project" "gen-inputs" "gen-tasks" "gen-annotation")

        Returns:
            削除したジョブの一覧
        """

        jobs = self.get_all_project_job(project_id, {'type': job_type})
        deleted_jobs = []
        for job in jobs:
            if job['job_status'] == 'succeeded':
                self.api.delete_project_job(project_id, job['job_id'])
                deleted_jobs.append(job)

        return deleted_jobs

    def get_all_project_job(self, project_id: str, query_params: Dict[str, Any]) -> List[ProjectJob]:
        """
        すべてのバックグランドジョブを取得する。
        2019/01時点でAPIが未実装のため、このメソッドも未実装。

        Args:
            project_id: プロジェクトID
            query_params: `api.get_project_job` メソッドに渡すQuery Parameter

        Returns:
            すべてのバックグランドジョブ一覧
        """

        # return self._get_all_objects(self.api.get_project_job,
        #                              limit=200,
        #                              project_id=project_id, query_params=query_params)
        #
        copied_params = copy.deepcopy(query_params) if query_params is not None else {}

        all_jobs: List[Dict[str, Any]] = []
        limit = 200
        copied_params.update({"page": 1, "limit": limit})
        r = self.api.get_project_job(project_id, query_params=copied_params)[0]
        all_jobs.extend(r["list"])
        return all_jobs
