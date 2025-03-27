import os

import pytest

from annofabapi.credentials import IdPass, Pat
from annofabapi.resource import build


class Test引数なしでbuildした時:
    @pytest.fixture(autouse=True)
    def clear_env(self):
        os.environ.pop("ANNOFAB_USER_ID", None)
        os.environ.pop("ANNOFAB_PASSWORD", None)
        os.environ.pop("ANNOFAB_PAT", None)
        yield

    def test_環境変数ANNOFAB_PATが設定されている場合はredentialsがPatになっていること(self):
        os.environ["ANNOFAB_PAT"] = "DUMMY_PAT"
        os.environ["ANNOFAB_USER_ID"] = "DUMMY_USER_ID"
        os.environ["ANNOFAB_PASSWORD"] = "DUMMY_PASSWORD"
        resource = build()
        assert isinstance(resource.api.credentials, Pat)
        assert resource.api.credentials.token == "DUMMY_PAT"

    def test_環境変数ANNOFAB_USER_IDとANNOFAB_PASSWORDのみが設定されている場合はredentialsがIdPathになっていること(self):
        os.environ["ANNOFAB_USER_ID"] = "DUMMY_USER_ID"
        os.environ["ANNOFAB_PASSWORD"] = "DUMMY_PASSWORD"
        resource = build()
        assert isinstance(resource.api.credentials, IdPass)
        assert resource.api.credentials.user_id == "DUMMY_USER_ID"
        assert resource.api.credentials.password == "DUMMY_PASSWORD"
