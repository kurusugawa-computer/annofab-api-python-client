import pytest

from annofabapi.credentials import IdPass, Pat
from annofabapi.exceptions import CredentialsNotFoundError
from annofabapi.resource import build


class Test引数なしでbuildした時:
    @pytest.fixture(autouse=True)
    def clear_env(self, monkeypatch):
        for name in ("ANNOFAB_USER_ID", "ANNOFAB_PASSWORD", "ANNOFAB_PAT"):
            monkeypatch.delenv(name, raising=False)

    def test_netrcに認証情報があっても環境変数に認証情報がなければエラーになること(self, tmp_path, monkeypatch):
        netrc_path = tmp_path / ".netrc"
        netrc_path.write_text("machine annofab.com login DUMMY_USER_ID password DUMMY_PASSWORD\n", encoding="utf-8")
        netrc_path.chmod(0o600)
        monkeypatch.setenv("HOME", str(tmp_path))
        monkeypatch.setenv("USERPROFILE", str(tmp_path))
        monkeypatch.setenv("NETRC", str(netrc_path))

        with pytest.raises(CredentialsNotFoundError):
            build()

    def test_環境変数ANNOFAB_PATが設定されている場合はredentialsがPatになっていること(self, monkeypatch):
        monkeypatch.setenv("ANNOFAB_PAT", "DUMMY_PAT")
        monkeypatch.setenv("ANNOFAB_USER_ID", "DUMMY_USER_ID")
        monkeypatch.setenv("ANNOFAB_PASSWORD", "DUMMY_PASSWORD")
        resource = build()
        assert isinstance(resource.api.credentials, Pat)
        assert resource.api.credentials.token == "DUMMY_PAT"

    def test_環境変数ANNOFAB_USER_IDとANNOFAB_PASSWORDのみが設定されている場合はredentialsがIdPathになっていること(self, monkeypatch):
        monkeypatch.setenv("ANNOFAB_USER_ID", "DUMMY_USER_ID")
        monkeypatch.setenv("ANNOFAB_PASSWORD", "DUMMY_PASSWORD")
        resource = build()
        assert isinstance(resource.api.credentials, IdPass)
        assert resource.api.credentials.user_id == "DUMMY_USER_ID"
        assert resource.api.credentials.password == "DUMMY_PASSWORD"
