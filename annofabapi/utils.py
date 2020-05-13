"""
Annofab APIのutils

"""
import copy
import datetime
import json
import logging
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import dateutil
import dateutil.tz
import requests
from requests.structures import CaseInsensitiveDict

from annofabapi.models import Task, TaskHistory, TaskHistoryShort, TaskPhase


def _raise_for_status(response: requests.Response) -> None:
    """
    HTTP Status CodeがErrorの場合、``requests.exceptions.HTTPError`` を発生させる。
    そのとき ``response.text`` もHTTPErrorに加えて、HTTPError発生時にエラーの原因が分かるようにする。


    Args:
        response: Response

    Raises:
        requests.exceptions.HTTPError:

    """
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        http_error_msg = f"{e.args[0]} , {response.text}"
        e.args = (http_error_msg,)
        raise e


def raise_for_status(response: requests.Response) -> None:
    """
    HTTP Status CodeがErrorの場合、``requests.exceptions.HTTPError`` を発生させる。
    そのとき ``response.text`` もHTTPErrorに加えて、HTTPError発生時にエラーの原因が分かるようにする。

    .. deprecated:: 2020-05-01 以降廃止予定です。

    Args:
        response: Response

    Raises:
        requests.exceptions.HTTPError:

    """
    warnings.warn("deprecated", DeprecationWarning)
    _raise_for_status(response)


def _log_error_response(arg_logger: logging.Logger, response: requests.Response) -> None:
    """
    HTTP Statusが400以上ならば、loggerにresponse/request情報を出力する


    Args:
        arg_logger: logger
        response: Response

    """
    RequestBodyHeader = Union[Dict[str, Any], CaseInsensitiveDict]

    def mask_key(d: RequestBodyHeader, key: str) -> RequestBodyHeader:
        if key in d:
            d[key] = "***"
        return d

    def mask_password(d: RequestBodyHeader) -> RequestBodyHeader:
        d = mask_key(d, "password")
        d = mask_key(d, "old_password")
        d = mask_key(d, "new_password")
        return d

    if 400 <= response.status_code < 600:
        headers = copy.deepcopy(response.request.headers)

        arg_logger.debug("status_code = %s, response.text = %s", response.status_code, response.text)
        arg_logger.debug("request.url = %s %s", response.request.method, response.request.url)

        # logにAuthorizationを出力しないようにマスクする
        mask_key(headers, "Authorization")
        arg_logger.debug("request.headers = %s", headers)

        # request_bodyのpassword関係をマスクして、logに出力する
        if response.request.body is None or response.request.body == "":
            dict_request_body = {}
        else:
            dict_request_body = json.loads(response.request.body)

        arg_logger.debug("request.body = %s", mask_password(dict_request_body))


def log_error_response(arg_logger: logging.Logger, response: requests.Response) -> None:
    """
    HTTP Statusが400以上ならば、loggerにresponse/request情報を出力する

    .. deprecated:: 2020-05-01 以降廃止予定です。

    Args:
        arg_logger: logger
        response: Response

    """
    warnings.warn("deprecated", DeprecationWarning)
    _log_error_response(arg_logger, response)


def _download(url: str, dest_path: str) -> None:
    """
    HTTP GETで取得した内容をファイルに保存する（ダウンロードする）


    Args:
        url: ダウンロード対象のURL
        dest_path: 保存先ファイルのパス

    """
    response = requests.get(url)
    _raise_for_status(response)

    p = Path(dest_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(response.content)


def download(url: str, dest_path: str) -> None:
    """
    HTTP GETで取得した内容をファイルに保存する（ダウンロードする）

    .. deprecated:: 2020-05-01 以降廃止予定です。

    Args:
        url: ダウンロード対象のURL
        dest_path: 保存先ファイルのパス

    """
    warnings.warn("deprecated", DeprecationWarning)
    _download(url, dest_path)


def str_now() -> str:
    """
    現在日時をISO8601 拡張形式で取得する。

    Returns:
        ISO 8601 formatの現在日時

    """
    return to_iso8601_extension(datetime.datetime.now())


def to_iso8601_extension(d: datetime.datetime, tz: Optional[datetime.tzinfo] = None) -> str:
    """
    datetime.datetimeを、ISO8601 拡張形式のstringに変換する。
    ``2019-05-08T10:00:00.000+09:00``

    Args:
        d: datetimeオブジェクト
        tz: タイムゾーンオブジェクト。Noneの場合、ローカルのタイムゾーンを設定する。

    Returns:
        ISO 8601 拡張形式の日時
    """
    if tz is None:
        tz = dateutil.tz.tzlocal()
    d = d.astimezone(tz)
    return d.isoformat(timespec="milliseconds")


def allow_404_error(function):
    """
    Not Found Error(404)を無視(許容)して、処理する。Not Foundのとき戻りはNoneになる。
    リソースの存在確認などに利用する。
    try-exceptを行う。また404 Errorが発生したときのエラーログを無効化する
    """

    def wrapped(*args, **kwargs):
        annofabapi_logger_level = logging.getLogger("annofabapi").level
        backoff_logger_level = logging.getLogger("backoff").level

        try:
            # 不要なログが出力されないようにする
            logging.getLogger("annofabapi").setLevel(level=logging.INFO)
            logging.getLogger("backoff").setLevel(level=logging.CRITICAL)

            return function(*args, **kwargs)

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == requests.codes.not_found:
                return None
            else:
                raise e
        finally:
            # ロガーの設定を元に戻す
            logging.getLogger("annofabapi").setLevel(level=annofabapi_logger_level)
            logging.getLogger("backoff").setLevel(level=backoff_logger_level)

    return wrapped


def get_task_history_index_skipped_acceptance(task_history_list: List[TaskHistory]) -> List[int]:
    """
    受入がスキップされたタスク履歴のインデックス番号（0始まり）を返す。
​
    Args:
        task_history_list: タスク履歴List
​
    Returns:
        受入フェーズがスキップされた履歴のインデックス番号（0始まり）。受入がスキップされていない場合は空リストを返す。
    """
    index_list = []
    for index, history in enumerate(task_history_list):
        if not (
            TaskPhase(history["phase"]) == TaskPhase.ACCEPTANCE
            and history["account_id"] is None
            and history["accumulated_labor_time_milliseconds"] == "PT0S"
            and history["started_datetime"] is not None
            and history["ended_datetime"] is not None
        ):
            continue

        if index + 1 < len(task_history_list):
            # 直後の履歴あり
            next_history = task_history_list[index + 1]
            if TaskPhase(next_history["phase"]) in [TaskPhase.ANNOTATION, TaskPhase.INSPECTION]:
                # 教師付フェーズ or 検査フェーズでの提出取消（直後が前段のフェーズ）
                pass
            else:
                # 受入スキップ
                index_list.append(index)
        else:
            # 直後の履歴がない
            index_list.append(index)

    return index_list


def get_task_history_index_skipped_inspection(task_history_list: List[TaskHistory]) -> List[int]:
    """
    検査フェーズがスキップされたタスク履歴のインデックス番号（0始まり）を返す。
​
    Args:
        task_history_list: タスク履歴List
​
    Returns:
        検査フェーズがスキップされた履歴のインデックス番号（0始まり）。検査がスキップされていない場合は空リストを返す。
    """
    index_list = []
    for index, history in enumerate(task_history_list):
        if not (
            TaskPhase(history["phase"]) == TaskPhase.INSPECTION
            and history["account_id"] is None
            and history["accumulated_labor_time_milliseconds"] == "PT0S"
            and history["started_datetime"] is not None
            and history["ended_datetime"] is not None
        ):
            continue

        if index + 1 < len(task_history_list):
            # 直後の履歴あり
            next_history = task_history_list[index + 1]
            if TaskPhase(next_history["phase"]) in [TaskPhase.ANNOTATION, TaskPhase.INSPECTION]:
                # 教師付フェーズ or 検査フェーズでの提出取消（直後が前段のフェーズ）
                pass
            else:
                # 検査スキップ
                index_list.append(index)
        else:
            # 直後の履歴がない
            index_list.append(index)

    return index_list


def get_number_of_rejections(task_histories: List[TaskHistoryShort], phase: TaskPhase, phase_stage: int = 1) -> int:
    """
    タスク履歴から、指定されたタスクフェーズでの差し戻し回数を取得する。

    Args:
        task_histories: タスク履歴
        phase: どのフェーズで差し戻されたか(TaskPhase.INSPECTIONかTaskPhase.ACCEPTANCE)
        phase_stage: どのフェーズステージで差し戻されたか。デフォルトは1。

    Returns:
        差し戻し回数
    """
    if phase not in [TaskPhase.INSPECTION, TaskPhase.ACCEPTANCE]:
        raise ValueError("引数'phase'には、'TaskPhase.INSPECTION'か'TaskPhase.ACCEPTANCE'を指定してください。")

    rejections_by_phase = 0
    for i, history in enumerate(task_histories):
        if not (history["phase"] == phase.value and history["phase_stage"] == phase_stage and history["worked"]):
            continue

        if i + 1 < len(task_histories) and task_histories[i + 1]["phase"] == TaskPhase.ANNOTATION.value:
            rejections_by_phase += 1

    return rejections_by_phase


def can_put_annotation(task: Task, my_account_id: str) -> bool:
    """
    対象タスクが、`put_annotation` APIで、アノテーションを更新できる状態かどうか。
    過去に担当者が割り当たっている場合、または現在の担当者自分自身の場合は、アノテーションを更新できる。

    Args:
        task: 対象タスク
        my_account_id: 自分（ログインしているユーザ）のアカウントID

    Returns:
        Trueならば、タスクの状態を変更せずに`put_annotation` APIを実行できる。
    """
    # ログインユーザはプロジェクトオーナであること前提
    return len(task["histories_by_phase"]) == 0 or task["account_id"] == my_account_id
