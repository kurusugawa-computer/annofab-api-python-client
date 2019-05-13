"""
Annofab APIのutils

"""

import datetime
import logging
import os

import dateutil
import requests


def log_error_response(arg_logger: logging.Logger,
                       response: requests.Response):
    """
    HTTP Statusが400以上ならば、loggerにresponse/request情報を出力する
    Args:
        arg_logger: logger
        response: Response
    """

    if 400 <= response.status_code < 600:
        arg_logger.debug(f"response.text = {response.text}")
        arg_logger.debug(f"request.url = {response.request.url}")
        arg_logger.debug(f"request.headers = {response.request.headers}")
        arg_logger.debug(f"request.body = {response.request.body}")


def download(url, dest_path):
    """
    HTTP GETで取得した内容を、ダウンロードする
    Args:
        url: ダウンロード対象のURL
        dest_path: 保存先
    """
    response = requests.get(url)
    response.raise_for_status()

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'wb') as f:
        f.write(response.content)


def str_now():
    """
    現在日時をISO8601 formatで取得する。
    Returns:
        ISO 8601 formatの現在日時
    """
    d = datetime.datetime.now(dateutil.tz.tzlocal())
    return d.isoformat(timespec='milliseconds')
