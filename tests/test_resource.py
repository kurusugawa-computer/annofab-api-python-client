"""
resource.pyのテストコード
"""

import os

import pytest

import annofabapi.exceptions
from annofabapi.credentials import IdPass
from annofabapi.resource import build, build_from_env


class TestBuild:
    # def test_build_from_netrc(self):
    #     # ".netrc"ファイルが存在すること前提
    #     assert isinstance(build_from_netrc(), annofabapi.Resource)

    def test_raise_ValueError(self):
        with pytest.raises(ValueError):
            annofabapi.AnnofabApi(IdPass("test_user", ""))

    def test_build_from_env_raise_CredentialsNotFoundError(self):
        with pytest.raises(annofabapi.exceptions.CredentialsNotFoundError):
            os.environ.pop("ANNOFAB_USER_ID", None)
            os.environ.pop("ANNOFAB_PASSWORD", None)
            os.environ.pop("ANNOFAB_PAT", None)
            build_from_env()

    def test_build_from_env(self):
        os.environ["ANNOFAB_USER_ID"] = "FOO"
        os.environ["ANNOFAB_PASSWORD"] = "BAR"
        assert isinstance(build_from_env(), annofabapi.Resource)

    def test_build(self):
        assert isinstance(build(login_user_id="FOO", login_password="BAR"), annofabapi.Resource)

        with pytest.raises(ValueError):
            build(login_user_id="FOO", login_password=None)

        with pytest.raises(ValueError):
            build(login_user_id=None, login_password="BAR")

        os.environ["ANNOFAB_USER_ID"] = "FOO"
        os.environ["ANNOFAB_PASSWORD"] = "BAR"
        assert isinstance(build(login_user_id=None, login_password=None), annofabapi.Resource)

    def test_build_with_endpoint(self):
        user_id = "test_user"
        password = "password"
        resource = build(user_id, password, endpoint_url="https://localhost:8080")
        assert resource.api.url_prefix == "https://localhost:8080/api/v1"
        assert resource.api2.url_prefix == "https://localhost:8080/api/v2"
        assert resource.api.credentials == IdPass(user_id, password)
