"""
resource.pyのテストコード
"""
import os

import pytest

import annofabapi

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")


def test_build():
    assert isinstance(annofabapi.build_from_netrc(), annofabapi.Resource)

    with pytest.raises(ValueError):
        annofabapi.AnnofabApi("test_user", "")
