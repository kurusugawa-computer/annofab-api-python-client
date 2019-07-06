"""
Annofab APIのutils

"""

import datetime
import logging
from pathlib import Path

import dateutil
import dateutil.tz
import requests


def raise_for_status(response: requests.Response):
    """
    HTTP Status CodeがErrorの場合、`requests.exceptions.HTTPError`を発生させる。
    そのとき`response.text`もHTTPErrorに加えて、HTTPError発生時にエラーの原因が分かるようにする。

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


def log_error_response(arg_logger: logging.Logger, response: requests.Response):
    """
    HTTP Statusが400以上ならば、loggerにresponse/request情報を出力する

    Args:
        arg_logger: logger
        response: Response

    """

    if 400 <= response.status_code < 600:
        arg_logger.debug(f"status_code = {response.status_code}, response.text = {response.text}")
        arg_logger.debug(f"request.url = {response.request.method}  {response.request.url}")
        arg_logger.debug(f"request.headers = {response.request.headers}")
        arg_logger.debug(f"request.body = {response.request.body}")


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
    現在日時をISO8601 formatで取得する。



    Returns:
        ISO 8601 formatの現在日時

    """
    d = datetime.datetime.now(dateutil.tz.tzlocal())
    return d.isoformat(timespec='milliseconds')
