"""
AnnofabApi2のテストメソッド

"""

import configparser

import annofabapi
from tests.utils_for_test import WrapperForTest

inifile = configparser.ConfigParser()
inifile.read("./pytest.ini", "UTF-8")
project_id = inifile["annofab"]["project_id"]

test_dir = "./tests/data"
out_dir = "./tests/out"

endpoint_url = inifile["annofab"].get("endpoint_url", None)
if endpoint_url is not None:
    service = annofabapi.build(endpoint_url=endpoint_url)
else:
    service = annofabapi.build()

test_wrapper = WrapperForTest(service.api)


def test_project():
    content, _ = service.api2.get_project_cache_v2(project_id)
    assert type(content) == dict  # noqa: E721
