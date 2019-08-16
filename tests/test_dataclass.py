"""
AnnofabApi2のテストメソッド

"""
import configparser
import datetime
import logging
import os
import time
import uuid
from distutils.util import strtobool

import annofabapi
import annofabapi.utils
from annofabapi.dataclass.task import Task, TaskHistory
from annofabapi.dataclass.input import InputData
from tests.utils_for_test import WrapperForTest, create_csv_for_task

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")
inifile = configparser.ConfigParser()
inifile.read('./pytest.ini', 'UTF-8')
project_id = inifile.get('annofab', 'project_id')
task_id = inifile.get('annofab', 'task_id')
should_execute_job_api: bool = strtobool(inifile.get('annofab', 'should_execute_job_api'))
should_print_log_message: bool = strtobool(inifile.get('annofab', 'should_print_log_message'))

test_dir = './tests/data'
out_dir = './tests/out'

if should_print_log_message:
    logging_formatter = '%(levelname)s : %(asctime)s : %(name)s : %(funcName)s : %(message)s'
    logging.basicConfig(format=logging_formatter)
    logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)

service = annofabapi.build_from_netrc()
test_wrapper = WrapperForTest(service.api)

my_account_id = service.api.get_my_account()[0]['account_id']
organization_name = service.api.get_organization_of_project(project_id)[0]['organization_name']

annofab_user_id = service.api.login_user_id

def test_input():
    input_data_list = service.wrapper.get_all_input_data_list(project_id, query_params={'task_id':task_id})
    input_data = InputData.from_dict(input_data_list[0])
    print(input_data)
    assert type(input_data) == InputData


def test_task():
    dict_task, _ = service.api.get_task(project_id, task_id)
    task = Task.from_dict(dict_task)
    assert type(task) == Task

    task_histories, _ = service.api.get_task_histories(project_id, task_id)
    task_history = TaskHistory.from_dict(task_histories[0])
    print(task_history)
    assert type(task_history) == TaskHistory
