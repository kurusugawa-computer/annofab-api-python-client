# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace
"""
AbstractAnnofabApi2のヘッダ部分

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照
"""

import abc
import warnings  # pylint: disable=unused-import
from typing import Any, Dict, List, Optional, Tuple, Union  # pylint: disable=unused-import

import requests

import annofabapi  # pylint: disable=unused-import


class AbstractAnnofabApi2(abc.ABC):
    """
    AnnofabApi2クラスの抽象クラス
    """
    @abc.abstractmethod
    def _request_wrapper(self, http_method: str, url_path: str, query_params: Optional[Dict[str, Any]] = None,
                         header_params: Optional[Dict[str, Any]] = None,
                         request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:
        pass

    #########################################
    # Public Method : AfAnnotationSpecsV2Api
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def get_annotation_specs_v2(self, project_id: str, query_params: Optional[Dict[str, Any]] = None,
                                **kwargs) -> Tuple[Any, requests.Response]:
        """アノテーション仕様取得


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature



        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                cache (str):  CACHE TIMESTAMP 
                history_id (str):  過去のアノテーション仕様を取得する場合、[アノテーション仕様履歴取得](#operation/getAnnotationSpecsHistories)APIで取得した `history_id` の値を指定します。 未指定時は最新のアノテーション仕様を取得します。 
                v (str):  取得するアノテーション仕様のフォーマットバージョンを指定します。 

        Returns:
            Tuple[OneOfAnnotationSpecsV1AnnotationSpecsV2, requests.Response]


        """
        url_path = f'/projects/{project_id}/annotation-specs'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    #########################################
    # Public Method : AfOrganizationV2Api
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def get_organization_by_name_v2(self, organization_name: str, query_params: Optional[Dict[str, Any]] = None,
                                    **kwargs) -> Tuple[Any, requests.Response]:
        """組織情報取得


        authorizations: AllOrganizationMember



        Args:
            organization_name (str):  組織名 (required)
            query_params (Dict[str, Any]): Query Parameters
                cache (str):  CACHE TIMESTAMP 

        Returns:
            Tuple[Organization, requests.Response]


        """
        url_path = f'/organizations-by-name/{organization_name}'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_organization_cache_by_name_v2(self, organization_name: str, **kwargs) -> Tuple[Any, requests.Response]:
        """キャッシュレコード


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature



        Args:
            organization_name (str):  組織名 (required)

        Returns:
            Tuple[OrganizationCacheRecord, requests.Response]


        """
        url_path = f'/organizations-by-name/{organization_name}/cache'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {}
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_organization_cache_v2(self, organization_id: str, **kwargs) -> Tuple[Any, requests.Response]:
        """キャッシュレコード


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature



        Args:
            organization_id (str):  組織ID (required)

        Returns:
            Tuple[OrganizationCacheRecord, requests.Response]


        """
        url_path = f'/organizations/{organization_id}/cache'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {}
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_organization_v2(self, organization_id: str, query_params: Optional[Dict[str, Any]] = None,
                            **kwargs) -> Tuple[Any, requests.Response]:
        """組織情報取得


        authorizations: AllOrganizationMember



        Args:
            organization_id (str):  組織ID (required)
            query_params (Dict[str, Any]): Query Parameters
                cache (str):  CACHE TIMESTAMP 

        Returns:
            Tuple[Organization, requests.Response]


        """
        url_path = f'/organizations/{organization_id}'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_project_task_count_v2(self, organization_id: str, project_id: str,
                                  **kwargs) -> Tuple[Any, requests.Response]:
        """プロジェクトのタスク件数取得


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature



        Args:
            organization_id (str):  組織ID (required)
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[ProjectTaskCounts, requests.Response]


        """
        url_path = f'/organizations/{organization_id}/projects/{project_id}/task-counts'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {}
        return self._request_wrapper(http_method, url_path, **keyword_params)

    #########################################
    # Public Method : AfProjectMemberV2Api
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def get_project_member_v2(self, project_id: str, user_id: str, query_params: Optional[Dict[str, Any]] = None,
                              **kwargs) -> Tuple[Any, requests.Response]:
        """プロジェクトメンバー取得


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature



        Args:
            project_id (str):  プロジェクトID (required)
            user_id (str):  アカウントのユーザID. RESTクライアントユーザが指定しやすいように、Cognitoのaccount_idではなくuser_idとしている。 (required)
            query_params (Dict[str, Any]): Query Parameters
                cache (str):  CACHE TIMESTAMP 

        Returns:
            Tuple[List[ProjectMember], requests.Response]


        """
        url_path = f'/projects/{project_id}/members/{user_id}'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_project_members_v2(self, project_id: str, query_params: Optional[Dict[str, Any]] = None,
                               **kwargs) -> Tuple[Any, requests.Response]:
        """プロジェクトメンバー一括取得


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature



        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                include_inactive_member (str):  脱退したプロジェクトメンバーも取得する時に、キーのみ指定します（値は無視されます）。
                cache (str):  CACHE TIMESTAMP 

        Returns:
            Tuple[InlineResponse200, requests.Response]


        """
        url_path = f'/projects/{project_id}/members'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    #########################################
    # Public Method : AfProjectV2Api
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def get_project_cache_v2(self, project_id: str, **kwargs) -> Tuple[Any, requests.Response]:
        """キャッシュレコード


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature



        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[ProjectCacheRecord, requests.Response]


        """
        url_path = f'/projects/{project_id}/cache'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {}
        return self._request_wrapper(http_method, url_path, **keyword_params)

    #########################################
    # Public Method : AfStatisticsV2Api
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def get_account_statistics_v2(self, project_id: str, query_params: Optional[Dict[str, Any]] = None,
                                  **kwargs) -> Tuple[Any, requests.Response]:
        """ユーザー別タスク集計取得


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature



        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                cache (str):  CACHE TIMESTAMP 

        Returns:
            Tuple[List[ProjectAccountStatistics], requests.Response]


        """
        url_path = f'/projects/{project_id}/statistics/accounts'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_inspection_statistics_v2(self, project_id: str, query_params: Optional[Dict[str, Any]] = None,
                                     **kwargs) -> Tuple[Any, requests.Response]:
        """検査コメント集計取得


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature



        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                cache (str):  CACHE TIMESTAMP 

        Returns:
            Tuple[List[InspectionStatistics], requests.Response]


        """
        url_path = f'/projects/{project_id}/statistics/inspections'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_label_statistics_v2(self, project_id: str, query_params: Optional[Dict[str, Any]] = None,
                                **kwargs) -> Tuple[Any, requests.Response]:
        """ラベル別アノテーション数集計取得


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature



        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                cache (str):  CACHE TIMESTAMP 

        Returns:
            Tuple[List[LabelStatistics], requests.Response]


        """
        url_path = f'/projects/{project_id}/statistics/labels'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_task_phase_statistics_v2(self, project_id: str, query_params: Optional[Dict[str, Any]] = None,
                                     **kwargs) -> Tuple[Any, requests.Response]:
        """フェーズ別タスク集計取得


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature



        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                cache (str):  CACHE TIMESTAMP 

        Returns:
            Tuple[List[TaskPhaseStatistics], requests.Response]


        """
        url_path = f'/projects/{project_id}/statistics/task-phases'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_task_statistics_v2(self, project_id: str, query_params: Optional[Dict[str, Any]] = None,
                               **kwargs) -> Tuple[Any, requests.Response]:
        """タスク集計取得


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature



        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                cache (str):  CACHE TIMESTAMP 

        Returns:
            Tuple[List[ProjectTaskStatisticsHistory], requests.Response]


        """
        url_path = f'/projects/{project_id}/statistics/tasks'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_worktime_statistics_v2(self, project_id: str, query_params: Optional[Dict[str, Any]] = None,
                                   **kwargs) -> Tuple[Any, requests.Response]:
        """タスク作業時間集計取得


        authorizations: SignedCookieKeyPairId, SignedCookiePolicy, SignedCookieSignature


        ヒストグラムは最終日のby_tasks、by_inputsでのみ返却する。 アカウント毎の集計のby_tasks、by_inputsには、最終日であってもヒストグラムを返却しない。 

        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                cache (str):  CACHE TIMESTAMP 

        Returns:
            Tuple[List[WorktimeStatistics], requests.Response]


        """
        url_path = f'/projects/{project_id}/statistics/worktimes'
        http_method = 'GET'
        keyword_params: Dict[str, Any] = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)
