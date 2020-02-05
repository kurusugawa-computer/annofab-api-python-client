"""
AnnofabApi2のテストメソッド

"""
import configparser
import os

import annofabapi
import annofabapi.utils
from tests.utils_for_test import WrapperForTest

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")
inifile = configparser.ConfigParser()
inifile.read('./pytest.ini', 'UTF-8')
project_id = inifile.get('annofab', 'project_id')

test_dir = './tests/data'
out_dir = './tests/out'

service = annofabapi.build_from_netrc()
test_wrapper = WrapperForTest(service.api)

my_account_id = service.api.get_my_account()[0]['account_id']
organization_name = service.api.get_organization_of_project(project_id)[0]['organization_name']

annofab_user_id = service.api.login_user_id


def test_project():
    assert type(service.api2.get_project_cache_v2(project_id))
