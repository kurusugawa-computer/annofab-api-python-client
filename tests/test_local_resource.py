"""
resource.pyのテストコード
"""
import os

import pytest

import annofabapi
import annofabapi.exceptions
from annofabapi.resource import build_from_netrc_or_env

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")


class TestBuild:
    def test_build_from_netrc(self):
        # ".netrc"ファイルが存在すること前提
        assert isinstance(annofabapi.build_from_netrc(), annofabapi.Resource)

    def test_raise_ValueError(self):
        with pytest.raises(ValueError):
            annofabapi.AnnofabApi("test_user", "")

    def test_build_from_env_raise_AnnofabApiException(self):
        with pytest.raises(annofabapi.exceptions.AnnofabApiException):
            os.environ.pop("ANNOFAB_USER_ID", None)
            os.environ.pop("ANNOFAB_PASSWORD", None)
            annofabapi.build_from_env()

    def test_build_from_env(self):
        os.environ["ANNOFAB_USER_ID"] = "FOO"
        os.environ["ANNOFAB_PASSWORD"] = "BAR"
        assert isinstance(annofabapi.build_from_env(), annofabapi.Resource)

    def test_build_from_netrc_or_env(self):
        os.environ["ANNOFAB_USER_ID"] = "FOO"
        os.environ["ANNOFAB_PASSWORD"] = "BAR"
        assert isinstance(build_from_netrc_or_env(), annofabapi.Resource)

    def test_build_with_endpoint(self):
        resource = annofabapi.build("test_user", "password", "https://localhost:8080")
        assert resource.api.url_prefix == "https://localhost:8080/api/v1"
        assert resource.api2.url_prefix == "https://localhost:8080/api/v2"
