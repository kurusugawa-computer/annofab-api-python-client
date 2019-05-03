"""
Annofab WebAPIに対応する関数
注意：このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照
"""

import base64
import logging
import os
import json

import requests
import mimetypes
import functools
import backoff
import warnings

from annofabapi.exceptions import AnnofabApiException
from typing import Dict, List, Any, Optional, Union, Tuple

logger = logging.getLogger(__name__)


def my_backoff(function):
    """
    HTTP Status Codeが429 or 5XXのときはリトライする. 最大5分間リトライする。
    """

    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        def fatal_code(e):
            """Too many Request以外の4XXはretryしない"""
            code = e.response.status_code
            return code != 429 and code < 500

        return backoff.on_exception(backoff.expo, requests.exceptions.RequestException,
                                    jitter=backoff.full_jitter,
                                    max_time=300,
                                    giveup=fatal_code)(function)(*args, **kwargs)

    return wrapped


class AnnofabApi:
    """
    Annofab APIと一対一で対応する関数の定義
    """

    def __init__(self, login_user_id: str, login_password: str):
        """
        Args:
            login_user_id: AnnoFabにログインするときのユーザID
            login_password: AnnoFabにログインするときのパスワード
        """

        if not login_user_id or not login_password:
            raise ValueError("login_user_id or login_password is empty.")

        self.login_user_id = login_user_id
        self.login_password = login_password
        self.session = requests.Session()

    #: アクセスするURL
    URL_PREFIX = "https://annofab.com/api/v1"

    #: login, refresh_tokenで取得したtoken情報
    token_dict: Optional[Dict[str, Any]] = None

    class __MyToken:
        """
        requestsモジュールのauthに渡す情報。
        http://docs.python-requests.org/en/master/user/advanced/#custom-authentication
        """

        def __init__(self, id_token: str):
            self.id_token = id_token

        def __call__(self, req):
            req.headers['Authorization'] = self.id_token
            return req

    #########################################
    # Private Method
    #########################################
    @staticmethod
    def _log_error_response(response):
        logger.error(f"response.text = {response.text}")
        logger.error(f"request.url = {response.request.url}")
        logger.error(f"request.headers = {response.request.headers}")
        logger.error(f"request.body = {response.request.body}")

    def _create_kwargs(self, params: Dict[str, Any], headers: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        requestsモジュールのget,...メソッドに渡すkwargsを生成する。
        Args:
            params: クエリパラメタに設定する情報
            headers: リクエストヘッダに設定する情報

        Returns:
            kwargs情報

        """

        # query_param
        new_params = {}
        if params is not None:
            for key, value in params.items():
                if type(value) in [list, dict]:
                    new_params[key] = json.dumps(value)
                else:
                    new_params[key] = value

        kwargs: Dict[str, Any] = {
            'params': new_params,
            'headers': headers,
        }
        if self.token_dict is not None:
            kwargs.update({
                'auth': self.__MyToken(self.token_dict['id_token'])
            })

        return kwargs

    @my_backoff
    def _request_wrapper(self,
                         http_method: str,
                         url_path: str,
                         query_params: Optional[Dict[str, Any]] = None,
                         header_params: Optional[Dict[str, Any]] = None,
                         request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:
        """
        HTTP　Requestを投げて、Reponseを返す。
        Args:
            http_method:
            url_path:
            query_params:
            header_params:
            request_body:

        Returns:
            Tuple[content, Response]. contentはcontent_typeにより型が変わる。
            application/jsonならDict型, text/*ならばstr型, それ以外ならばbite型。

        """

        def execute_request():
            if http_method == 'GET':
                return self.session.get(url, **kwargs)

            elif http_method == 'DELETE':
                return self.session.delete(url, **kwargs)

            elif http_method == 'PUT':
                return self.session.put(url, **kwargs)

            elif http_method == 'POST':
                return self.session.post(url, **kwargs)

            elif http_method == 'OPTIONS':
                return self.session.options(url, **kwargs)

            elif http_method == 'HEAD':
                return self.session.head(url, **kwargs)

            else:
                raise AnnofabApiException("HTTP Method '{http_method}' is not supported")

        url = f'{self.URL_PREFIX}{url_path}'
        kwargs = self._create_kwargs(query_params, header_params)
        if request_body is not None:
            if type(request_body) == dict or type(request_body) == list:
                kwargs.update({'json': request_body})

            elif type(request_body) == str:
                kwargs.update({'data': request_body.encode("utf-8")})

            else:
                kwargs.update({'data': request_body})

        # HTTP Requestを投げる
        response = execute_request()

        # Unauthoraized Errorならば、ログイン後に再度実行する
        if response.status_code == requests.codes.unauthorized:
            logger.debug(response.text)
            self.login()
            return self._request_wrapper(http_method, url_path, query_params, header_params, request_body)

        if response.status_code != requests.codes.ok:
            self._log_error_response(response)

        response.encoding = 'utf-8'
        response.raise_for_status()

        content_type = response.headers['Content-Type']
        if content_type == 'application/json':
            content = response.json() if len(response.content) != 0 else {}

        elif content_type.find('text/') >= 0:
            content = response.text

        else:
            content = response.content

        return content, response

    #########################################
    # Public Method : Login
    #########################################
    @my_backoff
    def login(self) -> Tuple[Dict[str, Any], requests.Response]:
        """
        ログイン
        Returns:
            token情報

        """
        logger.debug("Call Login API")
        login_info = {'user_id': self.login_user_id, 'password': self.login_password}

        url = f"{self.URL_PREFIX}/login"
        response = self.session.post(url, json=login_info)
        response.raise_for_status()

        json_obj = response.json()
        self.token_dict = json_obj["token"]
        return json_obj, response

    def logout(self) -> Optional[Tuple[Dict[str, Any], requests.Response]]:
        """
        ログアウト
        すでにログアウトされているときは何もしない
        """

        if self.token_dict is None:
            logger.info("You are not logged in.")
            return None

        request_body = self.token_dict
        content, response = self._request_wrapper('POST', '/logout', request_body=request_body)
        self.token_dict = None
        return content, response

    def refresh_token(self) -> Optional[Tuple[Dict[str, Any], requests.Response]]:
        """
        トークン リフレッシュ
        すでにログアウトされているときは何もしない
        """

        if self.token_dict is None:
            logger.info("You are not logged in.")
            return None

        request_body = {'refresh_token': self.token_dict['refresh_token']}
        content, response = self._request_wrapper('POST', '/refresh-token', request_body=request_body)
        self.token_dict = content
        return content, response


    #########################################
    # Public Method : AfAccountApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def change_password(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """パスワード変更  # noqa: E501
        Args:
            request_body (Any): Request Body
                change_password_request (ChangePasswordRequest):  (required)

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            Everyone, 
        """
        url_path = f'/change-password'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def confirm_reset_email(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """メールアドレスstep2（確定）  # noqa: E501
        [受け取った確認コード](#operation/initiateResetEmail)を使い、メールアドレスを変更します。   # noqa: E501
        Args:
            request_body (Any): Request Body
                confirm_reset_email_request (ConfirmResetEmailRequest):  (required)

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            EveryoneRequestBody, 
        """
        url_path = f'/confirm-reset-email'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def confirm_reset_password(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """パスワードリセットstep3（新しいパスワードに変更）  # noqa: E501
        新しいパスワードに変更します。 本人確認のため、[パスワードリセットを要求](#operation/resetPassoword)で受信したメールに記載された検証コードを使用します。  パスワードリセットプロセスの最終ステップです。   # noqa: E501
        Args:
            request_body (Any): Request Body
                confirm_reset_password_request (ConfirmResetPasswordRequest):  (required)

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            EveryoneRequestBody, 
        """
        url_path = f'/confirm-reset-password'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def confirm_signup(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """サインアップstep2（確定）  # noqa: E501
        Args:
            request_body (Any): Request Body
                confirm_sign_up_request (ConfirmSignUpRequest):  (required)

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            EveryoneRequestBody, 
        """
        url_path = f'/confirm-sign-up'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def confirm_verify_email(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """メールアドレス検証step2（確定）  # noqa: E501
        [受け取った確認コード](#operation/verifyEmail)を使い、メールアドレスが有効であることを確認します。   # noqa: E501
        Args:
            request_body (Any): Request Body
                confirm_verify_email_request (ConfirmVerifyEmailRequest):  (required)

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            Everyone, 
        """
        url_path = f'/confirm-verify-email'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def initiate_password_reset(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """パスワードリセットstep1（開始）  # noqa: E501
        パスワードリセットプロセスを開始します。  このAPIを実行した後、後続の[古いパスワードを無効化](#operation/resetPassoword)を実行するまでは、古いパスワードでログインできます。   # noqa: E501
        Args:
            request_body (Any): Request Body
                password_reset_request (PasswordResetRequest):  (required)

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            EveryoneRequestBody, 
        """
        url_path = f'/request-password-reset'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def initiate_reset_email(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """メールアドレスリセットstep1（開始）  # noqa: E501
        メールアドレス変更プロセスを開始します。  本人からの要求かどうかを検証するための確認コードがメールで送付されます。   # noqa: E501
        Args:
            request_body (Any): Request Body
                reset_email_request (ResetEmailRequest):  (required)

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            Everyone, 
        """
        url_path = f'/reset-email'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def initiate_signup(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """サインアップstep1（開始）  # noqa: E501
        Args:
            request_body (Any): Request Body
                sign_up_request (SignUpRequest):  (required)

        Returns:
            Tuple[Message, requests.Response]

        """
        url_path = f'/sign-up'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def initiate_verify_email(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """メールアドレス検証step1（開始）  # noqa: E501
        メールアドレスが有効かどうかの確認プロセスを開始します。  本人からの要求かどうかを検証するための確認コードがメールで送付されます。   # noqa: E501
        Args:
            request_body (Any): Request Body
                verify_email_request (VerifyEmailRequest):  (required)

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            Everyone, 
        """
        url_path = f'/verify-email'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def reset_password(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """パスワードリセットstep2（古いパスワードを無効化）  # noqa: E501
        古いパスワードを無効化し、パスワードリセットに必要な確認コードをメールで送付します。 本人確認のため、[パスワードリセットを要求](#operation/initiatePasswordReset)して取得したトークンを使用します。  後続の[新しいパスワードに変更](#operation/confirmResetPassoword)を実行することで、新しいパスワードに変更できます。   # noqa: E501
        Args:
            request_body (Any): Request Body
                reset_password_request (ResetPasswordRequest):  (required)

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            EveryoneRequestBody, 
        """
        url_path = f'/reset-password'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfAnnotationApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def batch_update_annotations(self, project_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """アノテーション一括更新  # noqa: E501
        複数のアノテーションを一括更新します。  リクエストボディは、1個以上の「操作」オブジェクトを含むJSON配列になります。 操作オブジェクトには、「更新」と「削除」の2通りがあり、それぞれJSONオブジェクト構造が異なります。 これら操作オブジェクトを複数含めることで、1リクエストで複数の更新や削除ができます。  **現時点で、このAPIは複数のアノテーションを修正するためのもので、新しいアノテーションを作成することはできません**。 新しいアノテーションを更新や削除の対象に指定した場合、無視されます。  既に作成済みのアノテーションのうち、リクエストボディの配列に含まれないアノテーションは更新されません。  更新対象のアノテーションのうち、属性配列に含まれない属性は更新されません。  更新対象のアノテーションのラベルを変更する場合、変更後のラベルに含まれない属性は削除されます。  複数の操作のうち、1つでも失敗するとAPIのレスポンス全体としては失敗になります。 成功した部分までは反映されます。  受入が完了しているタスクのアノテーション更新を含む場合、オーナー以上の権限が必要になります。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            request_body (Any): Request Body
                one_of_batch_annotation_request_item_put_batch_annotation_request_item_delete (list[OneOfBatchAnnotationRequestItemPutBatchAnnotationRequestItemDelete]):  (required)

        Returns:
            Tuple[list[SingleAnnotation], requests.Response]

        Authorizations:
            ProjectAccepter, 
        """
        url_path = f'/projects/{project_id}/annotations'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_annotation(self, project_id, task_id, input_data_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク-入力データのSimpleアノテーション一括取得  # noqa: E501
        指定したタスク - 入力データにつけられたアノテーションを一括で取得します。 simple版のアノテーションJSONは、機械学習の一般的な利用で扱いやすい構造になっています。  プロジェクト全体のアノテーションを一括で取得する場合は、[getAnnotationArchive](#operation/getAnnotationArchive) を使用できます。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)
            input_data_id (str):  入力データID (required)

        Returns:
            Tuple[SimpleAnnotation, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/tasks/{task_id}/inputs/{input_data_id}/annotation/simple'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_annotation_archive(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """simpleアノテーションZIP取得  # noqa: E501
        プロジェクト内のアノテーション（simple版）をZIPにまとめて、一括で取得します。  simple版のアノテーションJSONは、機械学習の一般的な利用で扱いやすい構造になっています。  取得できるZIPファイルの構造は以下のとおりです。  * ファイル名: af-annotation-{プロジェクトID}-{更新日時: yyyyMMdd-hhmmss}.zip * 内容: /   * {タスクID}/     * {入力データ名}.json       * アノテーションJSONデータ (詳細は 200レスポンス を参照)     * {入力データ名}/ (塗りつぶしアノテーション時のみ)       * combined/         * {ラベル名} (ラベルごとに結合した塗りつぶしのPNG画像)       * {アノテーションデータID} (塗りつぶしのPNG画像)  IDが異なる入力データで {入力データ名}が一致するときは、重複ファイル名には {入力データ名__入力データID} のように接尾辞がつきます。 AnnoFabの画像アップロード機能を使うとこのようなケースは発生しませんが、[入力データ更新API](#operation/putInputData)で入力名を重複させると発生します。 入力名の重複を解消してアノテーションZIPを再作成すれば、接尾辞を解消できます。  特定のタスクのsimpleアノテーションを取得したい場合は、[getAnnotation](#operation/getAnnotation) を使用できます。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[SimpleAnnotation, requests.Response]

        Authorizations:
            ProjectDataUser, 
        """
        url_path = f'/projects/{project_id}/archive/simple'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_annotation_list(self, project_id, query_params: Optional[Dict[str, Any]]=None, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """アノテーション一括取得  # noqa: E501
        指定したタスク-入力データにつけられたアノテーションを一括で取得します。  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                page (int):  検索結果のうち、取得したいページの番号(1始まり）
                limit (int):  1ページあたりの取得するデータ件数
                query (AnnotationQuery):  絞り込み条件。[AnnotationQuery](#/components/schemas/AnnotationQuery)** をURIエンコードしたもの。 
                sort (str):  ソート順の指定。 使用可能キーはtask_id, input_data_id, detail.annotation_id, detail.account_id, detail.label_id, detail.data_holding_type, detail.created_datetime, detail.updated_datetimeのいずれかです。降順指定時は先頭に-(ハイフン)を付与します。 複数指定時は,(カンマ)区切りで列挙します。複数キーを列挙した場合は、先頭から優先順位を割り振られます。 

        Returns:
            Tuple[InlineResponse2006, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/annotations'
        http_method = 'GET'
        keyword_params = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_archive_full_with_pro_id(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """fullアノテーションZIP取得  # noqa: E501
        **このAPIは廃止予定です。fullアノテーションZIPにある情報で、simpleアノテーションZIPにも欲しいものがあれば、ご連絡ください。**  プロジェクト内のアノテーション（full版）がまとめられたZIPを取得します。  full版のアノテーションJSONデータは、画像やアノテーションやアノテーション作成者など管理用の詳細情報が付随しています。機械学習での一般的な利用には、[詳細情報を省いた扱いやすい構造の simple版](#operation/getAnnotationArchive) を推奨します。  取得できるZIPファイルの構造は以下のとおりです。  * ファイル名: af-annotation-{プロジェクトID}-{更新日時: yyyyMMdd-hhmmss}.zip * 内容: /   * {タスクID}/     * {入力データID}.json       * アノテーションJSONデータ (詳細は 200レスポンス を参照)     * {入力データID}/ (塗りつぶしアノテーション時のみ)       * combined/         * {ラベルID} (ラベルごとに結合した塗りつぶしのPNG画像)       * {アノテーションデータID} (塗りつぶしのPNG画像)   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[FullAnnotation, requests.Response]

        Authorizations:
            ProjectDataUser, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/projects/{project_id}/archive/full'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_outer_with_pro_id_tas_id_inp_dat_id_ann_id(self, project_id, task_id, input_data_id, annotation_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """【エディタ用】外部ファイル形式のアノテーション取得  # noqa: E501
        このAPIが返すアノテーションは、エディタ用です。 機械学習などで利用する成果物としてのアノテーションを取得するには、以下をご利用いただけます。  * [getAnnotation](#operation/getAnnotation): 特定のタスク - 入力データのアノテーション取得 * [getAnnotationArchive](#operation/getAnnotationArchive): プロジェクト全体のアノテーション（ZIP）   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)
            input_data_id (str):  入力データID (required)
            annotation_id (str):  アノテーションID (required)

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/projects/{project_id}/tasks/{task_id}/inputs/{input_data_id}/annotation/{annotation_id}/outer'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def post_annotation_archive_update(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """アノテーションZIP更新開始  # noqa: E501
        プロジェクト内のアノテーションZIP（simple版とfull版の両方）の更新を開始します。 ZIPの更新は、データ量に応じて数分〜数十分かかります。  ZIPは日本時間AM03:00ごろに自動更新されます。 本APIを用いると、自動更新を待たずに更新を要求できます。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            ProjectDataUser, 
        """
        url_path = f'/projects/{project_id}/archive/update'
        http_method = 'POST'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def put_annotation(self, project_id, task_id, input_data_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク-入力データのアノテーション更新  # noqa: E501
        「過去に誰にも割り当てられていないタスクに含まれる入力データ」に限り、プロジェクトオーナーであればアノテーションを更新できます。 この挙動は、[AnnoFab外部で作成されたアノテーションをインポート](/docs/tutorial/tutorial-ex-importing-annotation.html) する目的にも利用できます。  １度でも誰かに割り当てられたタスクは、タスクの現在の担当者であればアノテーションを更新できます。 タスクの現在の担当者でない場合、エラーになります。 この制限は、アノテーション作業中の予期せぬ同時編集を防ぐためです。  `is_protected`（保護） を `true` にすることで、アノテーションをアノテーションエディタ上での削除から保護できます。 属性の変更もさせたくない場合は、アノテーション仕様で特定の属性を読取専用にすることで保護できます。保護は、  * 外部からインポートしたアノテーション * 別プロジェクトからコピーしたアノテーション  などを誤って削除したくないときに便利です。 `is_protected`は、プロジェクトオーナーのみ変更可能です。  なお、本APIでは `is_protected` によらず、更新や削除が可能です。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)
            input_data_id (str):  入力データID (required)
            request_body (Any): Request Body
                annotation (Annotation):  (required)

        Returns:
            Tuple[Annotation, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/tasks/{task_id}/inputs/{input_data_id}/annotation'
        http_method = 'PUT'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfAnnotationSpecsApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def get_annotation_specs(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """アノテーション仕様取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[AnnotationSpecs, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/annotation-specs'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def put_annotation_specs(self, project_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """アノテーション仕様更新  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            request_body (Any): Request Body
                annotation_specs_request (AnnotationSpecsRequest):  (required)

        Returns:
            Tuple[AnnotationSpecs, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/annotation-specs'
        http_method = 'PUT'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfDeprecatedApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def permanent_redirect1(self, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """所属プロジェクト一括取得  # noqa: E501
        [/my/projects](#operation/getMyProjects)にリダイレクトされます。   # noqa: E501
        Args:

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            Everyone, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/projects'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def permanent_redirect2(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """自分のプロジェクトメンバー取得  # noqa: E501
        [/my/projects/{project_id}/member](#operation/getMyMemberInProject) にリダイレクトされます。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/projects/{project_id}/my-member'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def permanent_redirect3(self, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """自分のアカウント取得  # noqa: E501
        [/my/account](#operation/getMyAccount) にリダイレクトされます。   # noqa: E501
        Args:

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            Everyone, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/accounts/my'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def permanent_redirect4(self, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """自分のアカウント情報更新  # noqa: E501
        [/my/account](#operation/putMyAccount) にリダイレクトされます。   # noqa: E501
        Args:

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            Everyone, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/accounts/my'
        http_method = 'PUT'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def permanent_redirect5(self, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """アカウント削除step1  # noqa: E501
        [/my/account/delete-request](#operation/initiateMyAccountDelete) にリダイレクトされます。   # noqa: E501
        Args:

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            Everyone, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/accounts/my/delete-request'
        http_method = 'POST'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def permanent_redirect6(self, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """アカウント削除step2（確定）  # noqa: E501
        [/my/account/delete-request/confirm](#operation/confirmMyAccountDelete) にリダイレクトされます。   # noqa: E501
        Args:

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            EveryoneRequestBody, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/accounts/my/delete-request/confirm'
        http_method = 'POST'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfInputApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def batch_update_inputs(self, project_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """入力データ一括更新  # noqa: E501
        入力データを一括更新します。  リクエストボディは、1個以上の「操作」オブジェクトを含むJSON配列になります。 操作オブジェクトには、現在「削除」の1通りのみがあります。 これら操作オブジェクトを複数含めることで、1リクエストで複数の削除ができます。  複数の操作のうち、1つでも失敗するとAPIのレスポンス全体としては失敗になります。 成功した部分までは反映されます。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            request_body (Any): Request Body
                one_of_batch_input_data_request_item_delete (list[OneOfBatchInputDataRequestItemDelete]):  (required)

        Returns:
            Tuple[list[InputData], requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/inputs'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def create_temp_path(self, project_id, header_params: Optional[Dict[str, Any]]=None, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """一時データ保存先取得  # noqa: E501
        「複数の入力データを圧縮したZIPファイル」や「4MBを超える画像」などをAnnoFabに一時的に保存するための、URLと登録用データパスを発行します。  このAPIと他のAPIを以下に示すように使うことで、ZIPファイルなどをAFにアップロードできます。   1. 本APIを実行して、URLを取得する。   * `curl -X POST -H 'Content-Type: CONTENT_TYPE_HERE' 'https://annofab.com/api/v1/projects/（プロジェクトID）/create-temp-path` 2. 1で取得したURLに、一時保存したいファイルをPUTする。   * `curl -X PUT -H \"Content-Type: CONTENT_TYPE_HERE' --data-binary @/hoge.zip 'https://（発行されたURL）'` 3. 1で取得した登録用データパスを [入力データ登録API](#operation/putInputData)のリクエストボディ `input_data_path` に指定する。   * `curl -X PUT -H 'Content-Type: text/json\" -d '{\"input_data_name\":\"...\", \"input_data_path\":\"(登録用データパス)\" }' '/projects/{project_id}/inputs/{input_data_id}'`  ここで、1と2で `CONTENT_TYPE_HERE` は必ず一致しなければいけません。 ZIPファイルの場合は `application/zip` 、画像ファイルの場合は `image/png` など、適切な Content-Type を指定します。  登録するファイルはどのような内容であれ、アップロードから24時間経過すると削除されます。 したがって、ZIP圧縮した入力データを登録する場合は、URL発行から24時間以内に完了してください。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            header_params (Dict[str, Any]): Header Parameters
                content_type (str):  アップロードしたいファイルの Content-Type を指定します。 

        Returns:
            Tuple[DataPath, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/create-temp-path'
        http_method = 'POST'
        keyword_params = {
            'header_params': header_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def delete_input_data(self, project_id, input_data_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """入力データ削除  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            input_data_id (str):  入力データID (required)

        Returns:
            Tuple[InputData, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/inputs/{input_data_id}'
        http_method = 'DELETE'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_input_data(self, project_id, input_data_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """入力データ取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            input_data_id (str):  入力データID (required)

        Returns:
            Tuple[InputData, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/inputs/{input_data_id}'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_input_data_list(self, project_id, query_params: Optional[Dict[str, Any]]=None, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """入力データ一括取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                input_data_id (str):  入力データIDでの部分一致検索で使用。1文字以上あれば使用します。
                input_data_name (str):  入力データ名での部分一致検索で使用。1文字以上あれば使用します。
                input_data_path (str):  入力データパスでの部分一致検索で使用。1文字以上あれば使用します。
                task_id (str):  入力データが紐づくタスクIDの部分一致検索で使用。1文字以上あれば使用します。条件に合致した先頭100件のタスクに使われている入力データを検索します。
                _from (str):  更新日時での範囲検索で使用
                to (str):  更新日時での範囲検索で使用
                page (int):  検索結果のうち、取得したいページの番号(1始まり）
                limit (int):  1ページあたりの取得するデータ件数

        Returns:
            Tuple[InlineResponse2007, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/inputs'
        http_method = 'GET'
        keyword_params = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_signed_url_of_input_data(self, project_id, input_data_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """実体参照用認証済みURL取得  # noqa: E501
        入力データの実体（画像や動画などのファイルそのもの）にアクセスするための、認証済み一時URLを取得します。  取得したURLは、1時間で失効し、アクセスできなくなります。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            input_data_id (str):  入力データID (required)

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/projects/{project_id}/inputs/{input_data_id}/data'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def put_input_data(self, project_id, input_data_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """入力データ更新   # noqa: E501
        入力データ（画像プロジェクトなら画像、動画プロジェクトなら動画や時系列データ）を登録します。  画像プロジェクトの場合、複数の画像ファイルをZIPでまとめてアップロードできます。ZIPは最大5GB、UTF-8エンコーディングのみ対応しています。<br> アノテーション作業生産性を高めるため、画像は「長辺4096px以内」かつ「4MB以内」になるよう圧縮されます。<br> 作成されるアノテーションは、元の解像度でつけた場合相当に自動で復元されます。  動画プロジェクトの場合、複数の動画ファイルをZIPでまとめてアップロードできます。ZIPは最大5GB、UTF-8エンコーディングのみ対応しています。<br> また、複数のストリーミング形式の動画をアップロードすることもできます。<br> この場合はZIP形式必須で、同一のZIPファイル内にm3u8ファイルとtsファイルを両方含めてください。<br> なお、このm3u8ファイルに記述された相対パスでtsファイルが参照可能である必要があります。  ### ディレクトリ例 ```   hoge.zip/     hoge.ts     fuga/       foo.m3u8(hoge.ts, fuga/foo1.ts, fuga/foo2.tsを参照)       foo1.ts       foo2.ts     piyo1/       piyo2/         bar.ts       bar.m3u8(hoge.ts, piyo1/piyo2/bar.tsを参照) ```  4MBを超えるファイルの登録には、[アップロード用一時データ保存先作成API](#operation/createTempPath) を組み合わせて使用します。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            input_data_id (str):  入力データID (required)
            request_body (Any): Request Body
                input_data_request (InputDataRequest):  (required)

        Returns:
            Tuple[InputData, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/inputs/{input_data_id}'
        http_method = 'PUT'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfInspectionApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def batch_update_inspections(self, project_id, task_id, input_data_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """検査コメント一括更新  # noqa: E501
        検査コメントを一括更新します。 タスクの現在の担当者でない場合、409エラーになります。  リクエストボディは、1個以上の「操作」オブジェクトを含むJSON配列になります。 操作オブジェクトには、「更新（作成含む）」と「削除」の2通りがあり、それぞれJSONオブジェクト構造が異なります。 これら操作オブジェクトを複数含めることで、1リクエストで複数の更新や削除ができます。  既に作成済みの検査コメントのうち、リクエストボディの配列に含まれないものは更新されません。  複数の操作のうち、1つでも失敗するとAPIのレスポンス全体としては失敗になります。 成功した部分までは反映されます。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)
            input_data_id (str):  入力データID (required)
            request_body (Any): Request Body
                one_of_batch_inspection_request_item_put_batch_inspection_request_item_delete (list[OneOfBatchInspectionRequestItemPutBatchInspectionRequestItemDelete]):  (required)

        Returns:
            Tuple[list[Inspection], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/tasks/{task_id}/inputs/{input_data_id}/inspections'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_inspections(self, project_id, task_id, input_data_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """検査コメント一括取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)
            input_data_id (str):  入力データID (required)

        Returns:
            Tuple[list[Inspection], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/tasks/{task_id}/inputs/{input_data_id}/inspections'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfInstructionApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def delete_instruction_image(self, project_id, image_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """作業ガイドの画像削除  # noqa: E501
        プロジェクトの作業ガイドの画像を削除します。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            image_id (str):  作業ガイド画像ID (required)

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            ProjectAccepter, ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/instruction-images/{image_id}'
        http_method = 'DELETE'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_instruction(self, project_id, query_params: Optional[Dict[str, Any]]=None, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """作業ガイドの取得  # noqa: E501
        指定された版の作業ガイドのHTMLを取得します。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                history_id (str):  取得する版の履歴ID (required)

        Returns:
            Tuple[str, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/instruction'
        http_method = 'GET'
        keyword_params = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_instruction_history(self, project_id, query_params: Optional[Dict[str, Any]]=None, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """作業ガイドの編集履歴の取得  # noqa: E501
        プロジェクトの作業ガイドの編集履歴を取得します。 取得される編集履歴は日付の新しい順にソートされます。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                limit (int):  取得する編集履歴の件数

        Returns:
            Tuple[list[InstructionHistory], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/instruction-history'
        http_method = 'GET'
        keyword_params = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_instruction_image_url_for_put(self, project_id, image_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """作業ガイドの画像登録・更新用URL取得  # noqa: E501
        プロジェクトの作業ガイドの画像を登録するためのput先URLを取得します。  リクエストヘッダには、登録する画像に応じた適切な Content-Type を指定してください。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            image_id (str):  作業ガイド画像ID (required)

        Returns:
            Tuple[DataPath, requests.Response]

        Authorizations:
            ProjectAccepter, ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/instruction-images/{image_id}/put-url'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_instruction_images(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """作業ガイドの画像一覧の取得  # noqa: E501
        プロジェクトの作業ガイドの画像一覧を取得します。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[list[InstructionImage], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/instruction-images'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def put_instruction(self, project_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """作業ガイドの更新  # noqa: E501
        作業ガイドのHTMLを更新します。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            request_body (Any): Request Body
                body (str):  (required)

        Returns:
            Tuple[InstructionHistory, requests.Response]

        Authorizations:
            ProjectAccepter, ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/instruction'
        http_method = 'PUT'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfJobApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def delete_project_job(self, project_id, job_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """ZIPアップロードジョブエラー削除  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            job_id (str):  ジョブID (required)

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/jobs/gen-inputs/{job_id}'
        http_method = 'DELETE'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_project_job(self, project_id, query_params: Optional[Dict[str, Any]]=None, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """バックグラウンドジョブ取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                type (str):  取得するジョブ種別 (required)
                page (int):  検索結果のうち、取得したいページの番号(1始まり)  現在は未実装のパラメータです。(今後対応予定) 
                limit (int):  1ページあたりの取得するデータ件数  現在は未実装のパラメータです。(今後対応予定) 
                exclusive_start_created_datetime (str):  取得するデータの直前の作成日時

        Returns:
            Tuple[list[JobInfo], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/jobs'
        http_method = 'GET'
        keyword_params = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfMyApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def confirm_my_account_delete(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """アカウント削除step2（確定）  # noqa: E501
        [受け取った確認コード](#operation/initiateMyAccountDelete)を使い、アカウントを削除します。   # noqa: E501
        Args:
            request_body (Any): Request Body
                confirm_account_delete_request (ConfirmAccountDeleteRequest):  (required)

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            EveryoneRequestBody, 
        """
        url_path = f'/my/account/delete-request/confirm'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_my_account(self, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """自分のアカウント取得  # noqa: E501
        Args:

        Returns:
            Tuple[MyAccount, requests.Response]

        Authorizations:
            Everyone, 
        """
        url_path = f'/my/account'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_my_member_in_project(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """自分のプロジェクトメンバー取得  # noqa: E501
        備考: システム管理者が自身が所属しないプロジェクトに対して実行した場合、オーナーであるというダミーのプロジェクトメンバー情報が取得できます。ダミーには更新日は含まれません。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[ProjectMember, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/my/projects/{project_id}/member'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_my_organizations(self, query_params: Optional[Dict[str, Any]]=None, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """所属組織一括取得  # noqa: E501
        Args:
            query_params (Dict[str, Any]): Query Parameters
                page (int):  表示するページ番号  現在は未実装のパラメータです。(今後対応予定) 
                limit (int):  1ページあたりの取得するデータ件数  現在は未実装のパラメータです。(今後対応予定) 

        Returns:
            Tuple[InlineResponse200, requests.Response]

        Authorizations:
            AllOrganizationMember, 
        """
        url_path = f'/my/organizations'
        http_method = 'GET'
        keyword_params = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_my_project_members(self, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """自分のプロジェクトメンバー情報一括取得  # noqa: E501
        Args:

        Returns:
            Tuple[list[ProjectMember], requests.Response]

        Authorizations:
            Everyone, 
        """
        url_path = f'/my/project-members'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_my_projects(self, query_params: Optional[Dict[str, Any]]=None, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """所属プロジェクト一括取得  # noqa: E501
        自身が所属するプロジェクトを一括で取得します。   # noqa: E501
        Args:
            query_params (Dict[str, Any]): Query Parameters
                exclusive_start_id (str):  取得するデータの直前のプロジェクトID
                page (int):  表示するページ番号  現在は未実装のパラメータです。(今後対応予定) 
                limit (int):  1ページあたりの取得するデータ件数  現在は未実装のパラメータです。(今後対応予定) 

        Returns:
            Tuple[InlineResponse2003, requests.Response]

        Authorizations:
            Everyone, 
        """
        url_path = f'/my/projects'
        http_method = 'GET'
        keyword_params = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def initiate_my_account_delete(self, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """アカウント削除step1  # noqa: E501
        アカウント削除プロセスを開始します。  本人からの要求かどうかを検証するための確認コードがメールで送付されます。   # noqa: E501
        Args:

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            Everyone, 
        """
        url_path = f'/my/account/delete-request'
        http_method = 'POST'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def put_my_account(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """自分のアカウント情報更新  # noqa: E501
        Args:
            request_body (Any): Request Body
                put_my_account_request (PutMyAccountRequest):  (required)

        Returns:
            Tuple[MyAccount, requests.Response]

        Authorizations:
            Everyone, 
        """
        url_path = f'/my/account'
        http_method = 'PUT'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def update_organization(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """組織名変更  # noqa: E501
        同じ name の組織が既に存在する場合は失敗(400)します。   # noqa: E501
        Args:
            request_body (Any): Request Body
                put_organization_name_request (PutOrganizationNameRequest):  (required)

        Returns:
            Tuple[Organization, requests.Response]

        Authorizations:
            OrganizationOwner, 
        """
        url_path = f'/my/organizations'
        http_method = 'PUT'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfOrganizationApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def create_new_organization(self, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """組織新規作成  # noqa: E501
        同じ name の組織が既に存在する場合は失敗（400）します。   # noqa: E501
        Args:
            request_body (Any): Request Body
                organization_registration_request (OrganizationRegistrationRequest):  (required)

        Returns:
            Tuple[Organization, requests.Response]

        Authorizations:
            Everyone, 
        """
        url_path = f'/organizations'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_organization(self, organization_name, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """組織情報取得  # noqa: E501
        Args:
            organization_name (str):  組織名 (required)

        Returns:
            Tuple[Organization, requests.Response]

        Authorizations:
            AllOrganizationMember, 
        """
        url_path = f'/organizations/{organization_name}'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_organization_activity(self, organization_name, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """組織活動サマリー取得  # noqa: E501
        Args:
            organization_name (str):  組織名 (required)

        Returns:
            Tuple[OrganizationActivity, requests.Response]

        Authorizations:
            AllOrganizationMember, 
        """
        url_path = f'/organizations/{organization_name}/activity'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_projects_of_organization(self, organization_name, query_params: Optional[Dict[str, Any]]=None, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """組織配下プロジェクト一括取得  # noqa: E501
        指定した組織のプロジェクトを一括で取得します。   # noqa: E501
        Args:
            organization_name (str):  組織名 (required)
            query_params (Dict[str, Any]): Query Parameters
                page (int):  表示するページ番号  現在は未実装のパラメータです。(今後対応予定) 
                limit (int):  1ページあたりの取得するデータ件数  現在は未実装のパラメータです。(今後対応予定) 

        Returns:
            Tuple[InlineResponse2001, requests.Response]

        Authorizations:
            AllOrganizationMember, 
        """
        url_path = f'/organizations/{organization_name}/projects'
        http_method = 'GET'
        keyword_params = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def permanent_redirect7(self, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """所属組織一括取得  # noqa: E501
        [/my/organizations](#operation/getMyOrganizations) にリダイレクトされます。   # noqa: E501
        Args:

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            AllOrganizationMember, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/organizations'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def permanent_redirect8(self, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """組織名変更  # noqa: E501
        [/my/organizations](#operation/updateOrganization) にリダイレクトされます。   # noqa: E501
        Args:

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            OrganizationOwner, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/organizations'
        http_method = 'PUT'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfOrganizationMemberApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def accept_organization_invitation(self, organization_name, user_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """組織への招待受諾  # noqa: E501
        組織への招待を受諾し、組織へのメンバー登録を完了します。  [組織招待API](#operation/postInviteOrganizationMember)で送信されたメールに記載されているトークンが必要です。   # noqa: E501
        Args:
            organization_name (str):  組織名 (required)
            user_id (str):  ユーザ名 (required)
            request_body (Any): Request Body
                accept_organization_invitation_request (AcceptOrganizationInvitationRequest):  (required)

        Returns:
            Tuple[Message, requests.Response]

        Authorizations:
            EveryoneRequestBody, 
        """
        url_path = f'/organizations/{organization_name}/members/{user_id}/invitation/accept'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def delete_organization_member(self, organization_name, user_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """組織メンバー削除  # noqa: E501
        指定したメンバーを指定した組織から削除します。  組織の管理者が実行する場合、組織のオーナーは削除できません。(権限エラーになります)   # noqa: E501
        Args:
            organization_name (str):  組織名 (required)
            user_id (str):  ユーザID (required)

        Returns:
            Tuple[OrganizationMember, requests.Response]

        Authorizations:
            OrganizationAdministrator, 
        """
        url_path = f'/organizations/{organization_name}/members/{user_id}'
        http_method = 'DELETE'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_organization_member(self, organization_name, user_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """組織メンバー取得  # noqa: E501
        指定したユーザーが指定した組織にどのようなロールで参加しているかを取得します。   # noqa: E501
        Args:
            organization_name (str):  組織名 (required)
            user_id (str):  ユーザID (required)

        Returns:
            Tuple[OrganizationMember, requests.Response]

        Authorizations:
            AllOrganizationMember, 
        """
        url_path = f'/organizations/{organization_name}/members/{user_id}'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_organization_members(self, organization_name, query_params: Optional[Dict[str, Any]]=None, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """組織メンバー一括取得  # noqa: E501
        脱退したメンバーは含まれません。   # noqa: E501
        Args:
            organization_name (str):  組織名 (required)
            query_params (Dict[str, Any]): Query Parameters
                page (int):  ページ番号
                limit (int):  1ページあたりの取得するデータ件数

        Returns:
            Tuple[InlineResponse2002, requests.Response]

        Authorizations:
            AllOrganizationMember, 
        """
        url_path = f'/organizations/{organization_name}/members'
        http_method = 'GET'
        keyword_params = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def invite_organization_member(self, organization_name, user_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """組織への招待送信  # noqa: E501
        指定したユーザーに、組織への招待（メール）を送信します。  組織の管理者が実行する場合、リクエストボディ内の `role` には `contributor` を指定してください。(それ以外の値を指定した場合エラーとなります)   # noqa: E501
        Args:
            organization_name (str):  組織名 (required)
            user_id (str):  ユーザ名 (required)
            request_body (Any): Request Body
                invite_organization_member_request (InviteOrganizationMemberRequest):  (required)

        Returns:
            Tuple[OrganizationMember, requests.Response]

        Authorizations:
            OrganizationAdministrator, 
        """
        url_path = f'/organizations/{organization_name}/members/{user_id}/invitation'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def update_organization_member_role(self, organization_name, user_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """組織メンバーのロール更新  # noqa: E501
        Args:
            organization_name (str):  組織名 (required)
            user_id (str):  ユーザID (required)
            request_body (Any): Request Body
                put_organization_member_role_request (PutOrganizationMemberRoleRequest):  (required)

        Returns:
            Tuple[OrganizationMember, requests.Response]

        Authorizations:
            OrganizationOwner, 
        """
        url_path = f'/organizations/{organization_name}/members/{user_id}/role'
        http_method = 'PUT'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfProjectApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def delete_project(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """プロジェクト削除  # noqa: E501
        プロジェクトを完全に削除します。 アノテーション仕様、タスク、入力データ、アノテーションなど、プロジェクト配下のリソースがすべて削除されます。  削除されたプロジェクトは元に戻せません。 完了したプロジェクトは削除せず、プロジェクト状態を「停止中」に変更するのをおすすめします。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[Project, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}'
        http_method = 'DELETE'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_organization_of_project(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """プロジェクトの所属組織取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[Organization, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/organization'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_project(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """プロジェクト取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[Project, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def initiate_project_copy(self, project_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """プロジェクト複製  # noqa: E501
        プロジェクトのアノテーション仕様やメンバーを引き継いで、別のプロジェクトを作成します。 設定により、アノテーションやタスクも引き継がせる事が可能です。  このAPIを利用するには、プロジェクトを登録する組織の[OrganizationAdministrator](#section/Authentication/OrganizationAdministrator) かつ コピー元プロジェクトの [ProjectOwner](#section/Authentication/ProjectOwner) である必要があります。   # noqa: E501
        Args:
            project_id (str):  コピー元となるプロジェクトID (required)
            request_body (Any): Request Body
                project_copy_request (ProjectCopyRequest):  (required)

        Returns:
            Tuple[Project, requests.Response]

        Authorizations:
            OrganizationAdministrator, ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/copy'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def put_project(self, project_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """プロジェクト作成/更新  # noqa: E501
        プロジェクトを新規作成または更新します。  ### 新規作成する場合 ユーザーは、作成するプロジェクトをひもづける組織の [OrganizationAdministrator](#section/Authentication/OrganizationAdministrator) である必要があります。  ### 更新する場合 ユーザーは、更新するプロジェクトの [ProjectOwner](#section/Authentication/ProjectOwner) である必要があります。 また所属組織を変更する場合は、新しくひもづける組織の [OrganizationAdministrator](#section/Authentication/OrganizationAdministrator) である必要があります。  なお、プロジェクト状態を「停止中」にした場合、アノテーションZIPやタスク進捗状況などの集計情報は自動更新されなくなります。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            request_body (Any): Request Body
                put_project_request (PutProjectRequest):  (required)

        Returns:
            Tuple[Project, requests.Response]

        Authorizations:
            OrganizationAdministrator, ProjectOwner, 
        """
        url_path = f'/projects/{project_id}'
        http_method = 'PUT'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfProjectMemberApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def get_project_member(self, project_id, user_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """プロジェクトメンバー取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            user_id (str):  アカウントのユーザID. RESTクライアントユーザが指定しやすいように、Cognitoのaccount_idではなくuser_idとしている。 (required)

        Returns:
            Tuple[list[ProjectMember], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/members/{user_id}'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_project_members(self, project_id, query_params: Optional[Dict[str, Any]]=None, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """プロジェクトメンバー一括取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                page (str):  ページ番号
                limit (int):  1ページあたりの取得するデータ件数

        Returns:
            Tuple[InlineResponse2004, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/members'
        http_method = 'GET'
        keyword_params = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def put_project_member(self, project_id, user_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """プロジェクトメンバー作成/更新  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            user_id (str):  アカウントのユーザID. RESTクライアントユーザが指定しやすいように、Cognitoのaccount_idではなくuser_idとしている。 (required)
            request_body (Any): Request Body
                project_member_request (ProjectMemberRequest):  (required)

        Returns:
            Tuple[ProjectMember, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/members/{user_id}'
        http_method = 'PUT'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfStatisticsApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def get_account_statistics(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """ユーザー別タスク集計取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[list[ProjectAccountStatistics], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/statistics/accounts'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_inspection_statistics(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """検査コメント集計取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[list[InspectionStatistics], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/statistics/inspections'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_label_statistics(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """ラベル別アノテーション数集計取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[list[LabelStatistics], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/statistics/labels'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_task_phase_statistics(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """フェーズ別タスク集計取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[list[TaskPhaseStatistics], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/statistics/task-phases'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_task_statistics(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク集計取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[list[ProjectTaskStatisticsHistory], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/statistics/tasks'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_worktime_statistics(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク作業時間集計取得  # noqa: E501
        ヒストグラムは最終日のby_tasks、by_inputsでのみ返却する。 アカウント毎の集計のby_tasks、by_inputsには、最終日であってもヒストグラムを返却しない。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[list[WorktimeStatistics], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/statistics/worktimes'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfSupplementaryApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def delete_supplementary_data(self, project_id, input_data_id, supplementary_data_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """補助情報削除  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            input_data_id (str):  入力データID (required)
            supplementary_data_id (str):  補助情報ID (required)

        Returns:
            Tuple[, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/inputs/{input_data_id}/supplementary-data/{supplementary_data_id}'
        http_method = 'DELETE'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_supplementary_data_list(self, project_id, input_data_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """補助情報一括取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            input_data_id (str):  入力データID (required)

        Returns:
            Tuple[list[SupplementaryData], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/inputs/{input_data_id}/supplementary-data'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def put_supplementary_data(self, project_id, input_data_id, supplementary_data_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """補助情報作成/更新  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            input_data_id (str):  入力データID (required)
            supplementary_data_id (str):  補助情報ID (required)
            request_body (Any): Request Body
                supplementary_data_request (SupplementaryDataRequest):  (required)

        Returns:
            Tuple[SupplementaryData, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/inputs/{input_data_id}/supplementary-data/{supplementary_data_id}'
        http_method = 'PUT'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfTaskApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def batch_update_tasks(self, project_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク一括更新  # noqa: E501
        タスクを一括更新します。  リクエストボディは、1個以上の「操作」オブジェクトを含むJSON配列になります。 操作オブジェクトには、現在「削除」の1通りのみがあります。 これら操作オブジェクトを複数含めることで、1リクエストで複数の削除ができます。  複数の操作のうち、1つでも失敗するとAPIのレスポンス全体としては失敗になります。 成功した部分までは反映されます。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            request_body (Any): Request Body
                one_of_batch_task_request_item_delete (list[OneOfBatchTaskRequestItemDelete]):  (required)

        Returns:
            Tuple[list[Task], requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/tasks'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def delete_task(self, project_id, task_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク削除  # noqa: E501
        不要になったタスクや、間違って投入したタスクを削除します。教師データなどは削除せず残すので、あとから復元することも可能です。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)

        Returns:
            Tuple[Task, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/tasks/{task_id}'
        http_method = 'DELETE'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_histories_with_pro_id_tas_id_tas_his_id(self, project_id, task_id, task_history_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク履歴取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)
            task_history_id (str):  タスク履歴ID (required)

        Returns:
            Tuple[list[TaskHistory], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/projects/{project_id}/tasks/{task_id}/histories/{task_history_id}'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_history_events_with_pro_id_tas_id(self, project_id, task_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク履歴イベント取得  # noqa: E501
        作業時間を計算したタスク履歴ではなく、その元となったタスク履歴イベントを一括で取得します。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)

        Returns:
            Tuple[list[TaskHistoryEvent], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/projects/{project_id}/tasks/{task_id}/history-events'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_task(self, project_id, task_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク取得  # noqa: E501
        個々のタスクの情報を取得します。  タスクを割り当てる場合は、[タスク割当](#operation/startTask)を使います。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)

        Returns:
            Tuple[Task, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/tasks/{task_id}'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_task_histories(self, project_id, task_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク履歴一括取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)

        Returns:
            Tuple[list[TaskHistory], requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/tasks/{task_id}/histories'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_task_validation(self, project_id, task_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク自動検査  # noqa: E501
        指定したタスクの自動検査で見つかった警告やエラーを一括で取得します。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)

        Returns:
            Tuple[TaskValidation, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/tasks/{task_id}/validation'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_tasks(self, project_id, query_params: Optional[Dict[str, Any]]=None, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク一括取得  # noqa: E501
        プロジェクトに含まれる複数のタスクをまとめて取得します。  検索条件を指定することで、特定のユーザが担当するタスクなどを絞り込むことができます。  パフォーマンスのため、結果はページング形式で返ります。全件取得したい場合は、レスポンスを見て、ページ移動してください。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            query_params (Dict[str, Any]): Query Parameters
                page (int):  検索結果のうち、取得したいページの番号(1始まり）
                limit (int):  1ページあたりの取得するデータ件数
                task_id (str):  タスクIDでの部分一致検索で使用。1文字以上あれば使用します。利便性のため、大文字小文字は区別しません
                phase (str):  絞り込み条件となるフェーズ名。未指定時は全フェーズ
                status (str):  絞り込み条件となる状態名。未指定時は全ステータス。
                account_id (str):  絞り込み条件となる作業中のアカウントID。未指定時は全アカウント
                no_user (str):  未割り当てのタスクを絞り込む時に、キーのみ指定する（値不要）。
                previous_account_id (str):  そのタスクをこれまでに担当したことのあるユーザー（現在の担当者含む）のアカウントID。未指定時は全ユーザ
                previous_phase (TaskPhase):  そのタスクがこれまでに遷移したことのあるフェーズ名（現在のフェーズ含む）。未指定時は全フェーズ
                rejected_only (str):  差し戻されたタスクだけを絞り込む時に、キーのみ指定します（値は無視されます）。
                auto_accepted_only (str):  「抜取検査の対象外となり、自動受入されたタスク」だけを絞り込む時に、キーのみ指定します（値は無視されます）。
                sort (str):  ソート順の指定。 使用可能キーはtask_id、updated_datetime、number_of_rejections、phase、status、account_idのいずれかです。降順指定時は先頭に-(ハイフン)を付与します。 複数指定時は,(カンマ)区切りで列挙します。複数キーを列挙した場合は、先頭から優先順位を割り振られます。 

        Returns:
            Tuple[InlineResponse2005, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/tasks'
        http_method = 'GET'
        keyword_params = {
            'query_params': query_params,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_tasks_inputs_with_pro_id(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """【非推奨】タスク-入力データ一括取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[TasksInputs, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        warnings.warn("deprecated", DeprecationWarning)
        url_path = f'/projects/{project_id}/tasks-inputs'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def initiate_tasks_generation(self, project_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク一括作成  # noqa: E501
        典型的なタスク作成ルールにもとづいた、一括作成を行うAPIです。  タスク作成ルールは、リクエストペイロードの `task_generate_rule` フィールドで指定できます。<br> `ByCount` を指定した場合、1つのタスクに割りあてる入力データの個数を指定してタスクを生成します。この作成ルールは、画像を同じ枚数均等にタスクに割り振りたい場合に便利です。<br> `ByDirectory` を指定した場合、入力データ名をファイルパスに見立て、ディレクトリ単位でタスクを生成します。この作成ルールは、動画などから切り出した画像をディレクトリ別に格納し、、その動画（ディレクトリ）の単位でタスクを作りたい場合に便利です。 `ByInputDataCsv` を指定した場合、入力データを各タスクに割り振ったCSVへのS3パスを指定してタスクを生成できます。この作成ルールは特定のデータの組み合わせを持ったタスクを作成したい場合に便利です。<br>   #### ByDirectory: ディレクトリ単位でのタスク一括生成の使い方 例えば、次のような `input_data_name_` の入力データが登録されているとします。  * a.zip/dir1/image1.png * a.zip/dir1/image2.png * a.zip/dir1/subdir/image3.png * a.zip/dir1/subdir/image4.png * a.zip/dir1/subdir/image5.png * b.zip/dir2/subdir1/image6.png * b.zip/dir2/subdir1/image7.png * b.zip/dir2/subdir1/image8.png * b.zip/dir2/subdir2/image9.png * b.zip/dir2/subdir2/image10.png  ここで、`input_data_name_prefix`フィールド に `a.zip` を指定すると、次の2タスクが生成されます。  1. タスク: `{task_id_prefix}_a.zip_dir1`   * a.zip/dir1/image1.png   * a.zip/dir1/image2.png 2. タスク: `{task_id_prefix}_a.zip_dir1_subdir`   * a.zip/dir1/subdir/image3.png   * a.zip/dir1/subdir/image4.png   * a.zip/dir1/subdir/image5.png  次に、`input_data_name_prefix` に `b.zip/dir2` を指定すると、次の2タスクが生成されます。  1. タスク: `{task_id_prefix}_b.zip_dir2_subdir1`   * b.zip/dir2/subdir1/image6.png   * b.zip/dir2/subdir1/image7.png   * b.zip/dir2/subdir1/image8.png 2. タスク: `{task_id_prefix}_b.zip_dir2_subdir2`   * b.zip/dir2/subdir2/image9.png   * b.zip/dir2/subdir2/image10.png  `input_data_name_prefix` が未指定の時は、全ディレクトリごとにタスクが作成されます。つまり次のように4つのタスクが生成されます。  1. タスク: `{task_id_prefix}_a.zip_dir1`   * a.zip/dir1/image1.png   * a.zip/dir1/image2.png 2. タスク: `{task_id_prefix}_a.zip_dir1_subdir`   * a.zip/dir1/subdir/image3.png   * a.zip/dir1/subdir/image4.png   * a.zip/dir1/subdir/image5.png 3. タスク: `{task_id_prefix}_b.zip_dir2_subdir1`   * b.zip/dir2/subdir1/image6.png   * b.zip/dir2/subdir1/image7.png   * b.zip/dir2/subdir1/image8.png 4. タスク: `{task_id_prefix}_b.zip_dir2_subdir2`   * b.zip/dir2/subdir2/image9.png   * b.zip/dir2/subdir2/image10.png  画像プロジェクトの場合、タスクに割り当てられる「ディレクトリ内の入力データ」の順序は、名前の昇順となります。<br> 動画プロジェクトの場合、タスクに割り当てられる「ディレクトリ内の入力データ」の順序は、動画の入力データが先頭に来るようにソートされたうえで、名前の昇順となります。  **注意:** `ByDirectory`では、入力データ名がファイルパス形式になっていない入力データはタスクの作成対象になりません。 例えば、`foo/bar.png` はタスクの作成対象になりますが、ディレクトリを含まない`bar.png` や、最後がディレクトリになっている`foo/bar.png/` は対象になりません。  **注意:** 動画プロジェクトの場合、ディレクトリに含まれる動画の入力データは一つに制限してください。 これが守られない場合、作成されたタスクで動画を再生できない場合があります。  #### ByInputDataCsv: CSVによるタスク一括生成の使い方 以下のように「タスク番号,入力データ名,入力データID」を1行毎に指定したCSVを作成します。  ``` 1,a001.jpg,ca0cb2f9-fec5-49b4-98df-dc34490f9785 1,a002.jpg,5ac1987e-ca7c-42a0-9c19-b5b23a41836b 1,centinel.jpg,81d6407b-2172-4fa8-8525-2e43c49267ee 2,b001.jpg,4f2ae4d0-7a38-4f9a-be6f-170ba76aba73 2,b002.jpg,45ac5852-f20c-4938-9ee9-cc0274401df7 2,centinel.jpg,81d6407b-2172-4fa8-8525-2e43c49267ee 3,c001.jpg,3260c7a0-4820-424d-a26e-db7e91dbc139 3,centinel.jpg,81d6407b-2172-4fa8-8525-2e43c49267ee ``` CSVのエンコーディングは UTF-8(BOM付き)、UTF-8(BOMなし)、UTF-16(BOM付きLE) のいずれかのみ対応しています。  **注意:** 動画プロジェクトの場合、一つのタスクに含まれる動画の入力データは一つに制限し、動画の入力データの位置は先頭にしてください。 これが守られない場合、作成されたタスクで動画を再生できない場合があります。  [createTempPath](#operation/createTempPath) APIを使ってアップロード用のURLとS3パスを取得してCSVをアップロードした上で`csv_data_path` フィールドに取得したS3パスを記述します。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            request_body (Any): Request Body
                task_generate_request (TaskGenerateRequest):  (required)

        Returns:
            Tuple[Project, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/generate-tasks'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def operate_task(self, project_id, task_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク状態変更  # noqa: E501
        タスクの状態、もしくはタスクの担当者を変更することができます。  #### ユースケースごとの使い方  * タスクを作業中(working)にしたい場合   * 制約     * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。     * 現在の状態が未着手(not_started)、休憩中(break)、保留(on_hold)のいずれかであるタスクに対してのみ、この操作を行うことができます。   * リクエストボディのJSONサンプル     * ```{ status: \"working\", account_id: \"自身(現在のタスク担当者)のアカウントID\", last_updated_datetime: \"2018-08-14T19:01:51.775+09:00\"}``` * タスクを休憩中にしたい場合   * 制約     * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。     * 現在の状態が作業中(working)のタスクに対してのみ、この操作を行うことができます。   * リクエストボディのJSONサンプル     * ```{ status: \"break\", account_id: \"自身(現在のタスク担当者)のアカウントID\", last_updated_datetime: \"2018-08-14T19:01:51.775+09:00\"}``` * タスクを保留(on_hold)にしたい場合   * 制約     * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。     * 現在の状態が作業中(working)のタスクに対してのみ、この操作を行うことができます。   * リクエストボディのJSONサンプル     * ```{ status: \"on_hold\", account_id: \"自身(現在のタスク担当者)のアカウントID\", last_updated_datetime: \"2018-08-14T19:01:51.775+09:00\"}``` * タスクを提出(complete)したい場合   * 制約     * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。     * 現在の状態が作業中(working)のタスクに対してのみ、この操作を行うことができます。   * リクエストボディのJSONサンプル     * ```{ status: \"complete\", account_id: \"自身(現在のタスク担当者)のアカウントID\", last_updated_datetime: \"2018-08-14T19:01:51.775+09:00\"}``` * タスクの提出を取消し(cancelled)したい場合   * 制約     * タスクを提出したユーザーのみ、この操作を行うことができます。     * タスク提出後に検査/受入(抜取含む)等の作業が一切行われていない場合のみ、この操作を行うことができます。     * 現在の状態が未着手(not_started)のタスクに対してのみ、この操作を行うことができます。     * 現在のフェーズが検査(inspection)、もしくは受入(acceptance)のタスクに対してのみ、この操作を行うことができます。   * リクエストボディのJSONサンプル     * ```{ status: \"cancelled\", account_id: \"自身(タスク提出者)のアカウントID\", last_updated_datetime: \"2018-08-14T19:01:51.775+09:00\"}``` * タスクを差戻し(rejected)したい場合   * 制約     * 現在タスクを担当しているユーザーのみ、この操作を行うことができます。     * 現在の状態が作業中(working)のタスクに対してのみ、この操作を行うことができます。     * 現在のフェーズが検査(inspection)、もしくは受入(acceptance)のタスクに対してのみ、この操作を行うことができます。   * リクエストボディのJSONサンプル     * ```{ status: \"rejected\", account_id: \"自身(現在のタスク担当者)のアカウントID\", last_updated_datetime: \"2018-08-14T19:01:51.775+09:00\"}``` * タスクの受入完了を取り消したい場合   * 制約     * プロジェクトオーナー(owner)のみ、この操作を行うことができます。     * 現在の状態が完了(completed)のタスクに対してのみ、この操作を行うことができます。     * 現在のフェーズが受入(acceptance)のタスクに対してのみ、この操作を行うことができます。   * リクエストボディのJSONサンプル     * ```{ status: \"not_started\", account_id: \"再度受入を担当させたいアカウントID\", last_updated_datetime: \"2018-08-14T19:01:51.775+09:00\"}``` * タスクの担当者を変更したい場合   * 制約     * プロジェクトオーナー(owner)、もしくは受入担当者(accepter)のみ、この操作を行うことができます。   * リクエストボディのJSONサンプル     * ```{ status: \"not_started\", account_id: \"現在のフェーズを担当できるアカウントID\", last_updated_datetime: \"2018-08-14T19:01:51.775+09:00\"}``` * タスクの担当者を未割当てにしたい場合   * 制約     * プロジェクトオーナー(owner)、もしくは受入担当者(accepter)のみ、この操作を行うことができます。   * リクエストボディのJSONサンプル     * ```{ status: \"not_started\", last_updated_datetime: \"2018-08-14T19:01:51.775+09:00\"}```   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)
            request_body (Any): Request Body
                task_operation (TaskOperation):  (required)

        Returns:
            Tuple[Task, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/tasks/{task_id}/operate'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def put_task(self, project_id, task_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク作成/更新  # noqa: E501
        1つのタスクを作成または更新します。 複数のタスクを一括生成する場合は、効率のよい[一括作成API](#operation/initiateTasksGeneration)を検討してください。  このAPIで変更できるのは、タスクの入力データ（`input_data_list`）のみです。タスクに割り当てた画像や動画などの入力データを差し替えることができます。  タスクの担当者やステータスを変更するには、[タスク割当](#operation/startTask)や[タスクの状態遷移](#operation/operateTask)を使用します。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            task_id (str):  タスクID (required)
            request_body (Any): Request Body
                task_request (TaskRequest):  (required)

        Returns:
            Tuple[Task, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/tasks/{task_id}'
        http_method = 'PUT'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def start_task(self, project_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """タスク割当  # noqa: E501
        タスクの割当を要求します。  個々のタスクの情報を取得する場合は、[タスク取得](#operation/getTask)を使います。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            request_body (Any): Request Body
                task_start (TaskStart):  (required)

        Returns:
            Tuple[Task, requests.Response]

        Authorizations:
            AllProjectMember, 
        """
        url_path = f'/projects/{project_id}/start-task'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)


    #########################################
    # Public Method : AfWebhookApi
    # NOTE: This method is auto generated by OpenAPI Generator
    #########################################

    def delete_webhook(self, project_id, webhook_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """プロジェクトのWebhookを削除  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            webhook_id (str):  WebhookID (required)

        Returns:
            Tuple[Webhook, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/webhooks/{webhook_id}'
        http_method = 'DELETE'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def get_webhooks(self, project_id, ) -> Tuple[Any, requests.Response]:  # noqa: E501
        """プロジェクトのWebhookをすべて取得  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)

        Returns:
            Tuple[list[Webhook], requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/webhooks'
        http_method = 'GET'
        keyword_params = {
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def put_webhook(self, project_id, webhook_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """プロジェクトのWebhookを更新  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            webhook_id (str):  WebhookID (required)
            request_body (Any): Request Body
                webhook (Webhook):  (required)

        Returns:
            Tuple[Webhook, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/webhooks/{webhook_id}'
        http_method = 'PUT'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)

    def test_webhook(self, project_id, webhook_id, request_body: Optional[Any] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """プロジェクトのWebhookをテスト実行  # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            webhook_id (str):  WebhookID (required)
            request_body (Any): Request Body
                webhook_test_request (WebhookTestRequest):  (required)

        Returns:
            Tuple[WebhookTestResponse, requests.Response]

        Authorizations:
            ProjectOwner, 
        """
        url_path = f'/projects/{project_id}/webhooks/{webhook_id}/test'
        http_method = 'POST'
        keyword_params = {
            'request_body': request_body,
        }
        return self._request_wrapper(http_method, url_path, **keyword_params)
