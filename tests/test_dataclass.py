import configparser
import logging
import os
from distutils.util import strtobool
from pathlib import Path

import annofabapi
import annofabapi.utils
from annofabapi.dataclass.annotation import SimpleAnnotation, SingleAnnotation
from annofabapi.dataclass.annotation_specs import AnnotationSpecs
from annofabapi.dataclass.input import InputData
from annofabapi.dataclass.inspection import Inspection
from annofabapi.dataclass.organization import Organization, OrganizationActivity
from annofabapi.dataclass.organization_member import OrganizationMember
from annofabapi.dataclass.project import Project
from annofabapi.dataclass.project_member import ProjectMember
from annofabapi.dataclass.supplementary import SupplementaryData
from annofabapi.dataclass.task import Task, TaskHistory
from annofabapi.dataclass.job import JobInfo
from tests.utils_for_test import WrapperForTest

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")
inifile = configparser.ConfigParser()
inifile.read('./pytest.ini', 'UTF-8')
project_id = inifile.get('annofab', 'project_id')
task_id = inifile.get('annofab', 'task_id')
input_data_id = inifile.get('annofab', 'input_data_id')
should_execute_job_api: bool = strtobool(inifile.get('annofab', 'should_execute_job_api'))
should_print_log_message: bool = strtobool(inifile.get('annofab', 'should_print_log_message'))

test_dir = Path('./tests/data')

if should_print_log_message:
    logging_formatter = '%(levelname)s : %(asctime)s : %(name)s : %(funcName)s : %(message)s'
    logging.basicConfig(format=logging_formatter)
    logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)

service = annofabapi.build_from_netrc()
test_wrapper = WrapperForTest(service.api)

my_account_id = service.api.get_my_account()[0]['account_id']
organization_name = service.api.get_organization_of_project(project_id)[0]['organization_name']

annofab_user_id = service.api.login_user_id


def test_annotation():
    annotation_list = service.wrapper.get_all_annotation_list(project_id, query_params={'query': {'task_id': task_id}})
    single_annotation = SingleAnnotation.from_dict(annotation_list[0])
    assert type(single_annotation) == SingleAnnotation

    dict_simple_annotation, _ = service.api.get_annotation(project_id, task_id, input_data_id)
    simple_annotation = SimpleAnnotation.from_dict(dict_simple_annotation)
    assert type(simple_annotation) == SimpleAnnotation


def test_annotation_specs():
    dict_annotation_specs, _ = service.api.get_annotation_specs(project_id)
    annotation_specs = AnnotationSpecs.from_dict(dict_annotation_specs)
    assert type(annotation_specs) == AnnotationSpecs


def test_input():
    input_data_list = service.wrapper.get_all_input_data_list(project_id, query_params={'task_id': task_id})
    input_data = InputData.from_dict(input_data_list[0])
    assert type(input_data) == InputData


def test_inspection():
    inspection_list, _ = service.api.get_inspections(project_id, task_id, input_data_id)
    inspection = Inspection.from_dict(inspection_list[0])
    assert type(inspection) == Inspection


def test_job():
    job_list = service.wrapper.get_all_project_job(project_id, query_params={"type": "gen-tasks"})
    job = JobInfo.from_dict(job_list[0])
    assert type(job) == JobInfo


def test_organization():
    dict_organization, _ = service.api.get_organization(organization_name)
    organization = Organization.from_dict(dict_organization)
    assert type(organization) == Organization

    dict_organization_activity, _ = service.api.get_organization_activity(organization_name)
    organization_activity = OrganizationActivity.from_dict(dict_organization_activity)
    assert type(organization_activity) == OrganizationActivity


def test_organization_member():
    dict_organization_member, _ = service.api.get_organization_member(organization_name, annofab_user_id)
    organization_member = OrganizationMember.from_dict(dict_organization_member)
    assert type(organization_member) == OrganizationMember


def test_project():
    dict_project, _ = service.api.get_project(project_id)
    project = Project.from_dict(dict_project)
    assert type(project) == Project


def test_project_member():
    dict_project_member, _ = service.api.get_project_member(project_id, annofab_user_id)
    project_member = ProjectMember.from_dict(dict_project_member)
    assert type(project_member) == ProjectMember


def test_supplementary():
    supplementary_data_list, _ = service.api.get_supplementary_data_list(project_id, input_data_id)
    supplementary_data = SupplementaryData.from_dict(supplementary_data_list[0])
    assert type(supplementary_data) == SupplementaryData


def test_task():
    dict_task, _ = service.api.get_task(project_id, task_id)
    task = Task.from_dict(dict_task)
    assert type(task) == Task

    task_histories, _ = service.api.get_task_histories(project_id, task_id)
    task_history = TaskHistory.from_dict(task_histories[0])
    assert type(task_history) == TaskHistory
