"""
AnnofabApi, Wrapperのテストコード

"""

from __future__ import annotations

import configparser

import annofabapi
from annofabapi.pydantic_models.input_data import InputData
from annofabapi.pydantic_models.project import Project
from annofabapi.pydantic_models.project_member import ProjectMember
from annofabapi.pydantic_models.single_annotation import SingleAnnotation
from annofabapi.pydantic_models.task import Task

inifile = configparser.ConfigParser()
inifile.read("./pytest.ini", "UTF-8")

project_id = inifile["annofab"]["project_id"]
task_id = inifile["annofab"]["task_id"]
changed_task_id = inifile["annofab"]["changed_task_id"]


endpoint_url = inifile["annofab"].get("endpoint_url", None)
if endpoint_url is not None:
    service = annofabapi.build(endpoint_url=endpoint_url)
else:
    service = annofabapi.build()


def test_task():
    content, _ = service.api.get_tasks(project_id)
    task = content["list"][0]
    actual = Task.from_dict(task)
    print(actual)


def test_input_data():
    content, _ = service.api.get_input_data_list(project_id)
    input_data = content["list"][0]
    actual = InputData.from_dict(input_data)
    print(actual)


def test_project_member():
    content, _ = service.api.get_project_members(project_id)
    member = content["list"][0]
    actual = ProjectMember.from_dict(member)
    print(actual)


def test_project():
    project, _ = service.api.get_project(project_id)
    actual = Project.from_dict(project)
    print(actual)


def test_single_annotation():
    content, _ = service.api.get_annotation_list(project_id)
    annotation = content["list"][0]
    actual = SingleAnnotation.from_dict(annotation)
    print(actual)
