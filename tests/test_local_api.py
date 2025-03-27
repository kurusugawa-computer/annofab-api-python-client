from __future__ import annotations

from typing import Any

import pytest
import requests

from annofabapi.api import _create_request_body_for_logger, my_backoff


class TestMyBackoff:
    @my_backoff
    def requestexception_connectionerror_then_true(self, log: list[Any]):
        if len(log) == 2:
            return True

        e: Exception
        if len(log) == 0:
            e = requests.exceptions.RequestException()
        elif len(log) == 1:
            e = ConnectionError()
        log.append(e)
        raise e

    def test_assert_retry(self):
        log: list[Any] = []
        assert self.requestexception_connectionerror_then_true(log) is True
        assert 2 == len(log)
        print(log)
        assert isinstance(type(log[0]), requests.exceptions.RequestException)
        assert isinstance(type(log[1]), ConnectionError)

    @my_backoff
    def chunkedencodingerror_requestsconnectionerror_then_true(self, log: list[Any]):
        if len(log) == 2:
            return True

        e: Exception
        if len(log) == 0:
            e = requests.exceptions.ChunkedEncodingError()
            log.append(e)
            raise e
        elif len(log) == 1:
            e = requests.exceptions.ConnectionError()
            log.append(e)
            raise e

    def test_assert_retry2(self):
        log: list[Any] = []
        assert self.chunkedencodingerror_requestsconnectionerror_then_true(log) is True
        assert 2 == len(log)
        print(log)
        assert isinstance(type(log[0]), requests.exceptions.ChunkedEncodingError)
        assert isinstance(type(log[1]), requests.exceptions.ConnectionError)

    @my_backoff
    def httperror_then_true(self, log: list[Any]):
        if len(log) == 2:
            return True
        response = requests.Response()
        if len(log) == 0:
            response.status_code = 429
            e = requests.exceptions.HTTPError(response=response)
        elif len(log) == 1:
            response.status_code = 500
            e = requests.exceptions.HTTPError(response=response)
        log.append(e)
        raise e

    def test_assert_retry_with_httperror(self):
        log: list[Any] = []
        assert self.httperror_then_true(log) is True
        assert 2 == len(log)
        print(log)
        assert isinstance(type(log[0]), requests.exceptions.HTTPError)
        assert log[0].response.status_code == 429
        assert isinstance(type(log[1]), requests.exceptions.HTTPError)
        assert log[1].response.status_code == 500

    @my_backoff
    def httperror_with_400(self, log):
        if len(log) == 1:
            return True
        response = requests.Response()
        if len(log) == 0:
            response.status_code = 400
            e = requests.exceptions.HTTPError(response=response)
        log.append(e)
        raise e

    def test_assert_not_retry(self):
        log: list[Any] = []
        with pytest.raises(requests.exceptions.HTTPError):
            self.httperror_with_400(log)
        assert 1 == len(log)


class Test__create_request_body_for_logger:
    def test_data_dict(self):
        actual = _create_request_body_for_logger({"foo": "1", "password": "x", "new_password": "y", "old_password": "z"})
        assert actual == {"foo": "1", "password": "***", "new_password": "***", "old_password": "***"}

    def test_data_dict2(self):
        actual = _create_request_body_for_logger({"foo": "1"})
        assert actual == {"foo": "1"}

    def test_data_list(self):
        actual = _create_request_body_for_logger([{"foo": "1"}])
        assert actual == [{"foo": "1"}]