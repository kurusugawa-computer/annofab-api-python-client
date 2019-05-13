"""
resource.pyのテストコード
"""
import configparser
import datetime
import logging
import os
import time
import uuid

import annofabapi

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")


def test_build():
    assert isinstance(annofabapi.build_from_netrc(), annofabapi.Resource)
