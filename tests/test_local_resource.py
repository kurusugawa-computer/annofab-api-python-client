"""
resource.pyのテストコード
"""
import os

import pytest

import annofabapi
import annofabapi.exceptions

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")


def test_build():
    assert isinstance(annofabapi.build_from_netrc(), annofabapi.Resource)

    with pytest.raises(ValueError):
        annofabapi.AnnofabApi("test_user", "")

    with pytest.raises(annofabapi.exceptions.AnnofabApiException):
        os.environ.pop('ANNOFAB_USER_ID', None)
        os.environ.pop('ANNOFAB_PASSWORD', None)
        annofabapi.build_from_env()

    os.environ['ANNOFAB_USER_ID'] = 'FOO'
    os.environ['ANNOFAB_PASSWORD'] = 'BAR'
    assert isinstance(annofabapi.build_from_env(), annofabapi.Resource)
