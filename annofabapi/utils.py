"""
Annofab APIのutils

"""

import copy
import datetime
import logging
from pathlib import Path
from typing import Optional

import dateutil
import dateutil.tz
import requests


def raise_for_status(response: requests.Response):
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
        e.args = (http_error_msg, )
        raise e


def log_error_response(arg_logger: logging.Logger, response: requests.Response):
    """
    HTTP Statusが400以上ならば、loggerにresponse/request情報を出力する

    Args:
        arg_logger: logger
        response: Response

    """

    if 400 <= response.status_code < 600:
        headers = copy.deepcopy(response.request.headers)
        if "Authorization" in headers:
            # logにAuthorizationを出力しないようにマスクする
            headers["Authorization"] = "***"

        arg_logger.debug(f"status_code = %s, response.text = %s", response.status_code, response.text)
        arg_logger.debug(f"request.url = %s %s", response.request.method, response.request.url)
        arg_logger.debug("request.headers = %s", headers)
        arg_logger.debug("request.body = %s", response.request.body)


def download(url: str, dest_path: str):
    """
    HTTP GETで取得した内容をファイルに保存する（ダウンロードする）

    Args:
        url: ダウンロード対象のURL
        dest_path: 保存先ファイルのパス

    """
    response = requests.get(url)
    raise_for_status(response)

    p = Path(dest_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, 'wb') as f:
        f.write(response.content)


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
    return d.isoformat(timespec='milliseconds')


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
