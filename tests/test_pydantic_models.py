import configparser
import json

import pytest

import annofabapi
from annofabapi.pydantic_models.annotation_specs_v3 import AnnotationSpecsV3
from annofabapi.pydantic_models.input_data import InputData
from annofabapi.pydantic_models.my_organization import MyOrganization
from annofabapi.pydantic_models.project import Project
from annofabapi.pydantic_models.project_member import ProjectMember
from annofabapi.pydantic_models.simple_annotation import SimpleAnnotation
from annofabapi.pydantic_models.single_annotation import SingleAnnotation
from annofabapi.pydantic_models.task import Task

# webapiにアクセスするテストモジュール
pytestmark = pytest.mark.access_webapi

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


# 良く利用するモデルのみテストする
# Errorが発生しないことを確認する


def test__Task():
    content, _ = service.api.get_tasks(project_id)
    task = content["list"][0]
    Task.from_dict(task)


def test__InputData():
    content, _ = service.api.get_input_data_list(project_id)
    input_data = content["list"][0]
    InputData.from_dict(input_data)


def test__ProjectMember():
    content, _ = service.api.get_project_members(project_id)
    member = content["list"][0]
    ProjectMember.from_dict(member)


def test__Project():
    project, _ = service.api.get_project(project_id)
    Project.from_dict(project)


def test_SingleAnnotation():
    content, _ = service.api.get_annotation_list(project_id, query_params={"v": "2"})
    annotation = content["list"][0]
    SingleAnnotation.from_dict(annotation)


def test_AnnotationSpecsV3():
    content, _ = service.api.get_annotation_specs(project_id, query_params={"v": "3"})
    AnnotationSpecsV3.from_dict(content)


def test__SimpleAnnotation():
    with open("tests/data/simple-annotation/sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json") as f:
        content = json.load(f)
    SimpleAnnotation.from_dict(content)


def test__MyOrganization():
    organizations, _ = service.api.get_my_organizations()
    MyOrganization.from_dict(organizations["list"][0])
