"""
AnnofabApi2のテストメソッド

"""
import configparser
import datetime
import json
import logging
import os
import time
import uuid
from distutils.util import strtobool
from pathlib import Path

import annofabapi
import annofabapi.utils
from annofabapi.dataclass.annotation import FullAnnotation, SimpleAnnotation, SingleAnnotation
from annofabapi.dataclass.annotation_specs import AnnotationSpecs
from annofabapi.dataclass.input import InputData
from annofabapi.dataclass.inspection import Inspection
from annofabapi.dataclass.organization import Organization, OrganizationActivity
from annofabapi.dataclass.organization_member import OrganizationMember
from annofabapi.dataclass.project import Project
from annofabapi.dataclass.project_member import ProjectMember
from annofabapi.dataclass.supplementary import SupplementaryData
from annofabapi.dataclass.task import Task, TaskHistory
from tests.utils_for_test import WrapperForTest, create_csv_for_task

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")
inifile = configparser.ConfigParser()
inifile.read('./pytest.ini', 'UTF-8')

test_dir = Path('./tests/data')


def test_annotation():
    simple_annotaion_json = test_dir / "simple-annotation.json"
    with simple_annotaion_json.open() as f:
        dict_full_annotation = json.load(f)
    simple_annotion = SimpleAnnotation.from_dict(dict_full_annotation)
    assert type(simple_annotion) == SimpleAnnotation

    full_annotaion_json = test_dir / "full-annotation.json"
    with full_annotaion_json.open() as f:
        dict_full_annotation = json.load(f)
    full_annotion = FullAnnotation.from_dict(dict_full_annotation)
    assert type(full_annotion) == FullAnnotation


def test_annotation_specs():
    annotaion_specs_json = test_dir / "annotation-specs.json"
    with annotaion_specs_json.open() as f:
        dict_annotation_specs = json.load(f)
    annotation_specs = AnnotationSpecs.from_dict(dict_annotation_specs)
    assert type(annotation_specs) == AnnotationSpecs


def test_input():
    input_data_json = test_dir / "input-data.json"
    with input_data_json.open() as f:
        dict_input_data = json.load(f)
    input_data = InputData.from_dict(dict_input_data)
    assert type(input_data) == InputData


def test_inspection():
    inspection_json = test_dir / "inspection.json"
    with inspection_json.open() as f:
        dict_inspection = json.load(f)
    inspection = Inspection.from_dict(dict_inspection)
    assert type(inspection) == Inspection


def test_organization():
    organization_activity_json = test_dir / "organization.json"
    with organization_activity_json.open() as f:
        dict_organization = json.load(f)
    organization = Organization.from_dict(dict_organization)
    assert type(organization) == Organization

    organization_activity_json = test_dir / "organization-activity.json"
    with organization_activity_json.open() as f:
        dict_organization_activity = json.load(f)
    organization_activity = OrganizationActivity.from_dict(dict_organization_activity)
    assert type(organization_activity) == OrganizationActivity


def test_organization_member():
    organization_member_json = test_dir / "organization-member.json"
    with organization_member_json.open() as f:
        dict_organization_member = json.load(f)
    organization_member = OrganizationMember.from_dict(dict_organization_member)
    assert type(organization_member) == OrganizationMember


def test_project():
    project_json = test_dir / "project.json"
    with project_json.open() as f:
        dict_project = json.load(f)
    project = Project.from_dict(dict_project)
    assert type(project) == Project


def test_project_member():
    project_member_json = test_dir / "project-member.json"
    with project_member_json.open() as f:
        dict_project_member = json.load(f)
    project_member = ProjectMember.from_dict(dict_project_member)
    assert type(project_member) == ProjectMember


def test_supplementary():
    supplementary_data_json = test_dir / "supplementary-data.json"
    with supplementary_data_json.open() as f:
        dict_supplementary_data = json.load(f)
    supplementary_data = SupplementaryData.from_dict(dict_supplementary_data)
    assert type(supplementary_data) == SupplementaryData


def test_task():
    task_json = test_dir / "task.json"
    with task_json.open() as f:
        dict_task = json.load(f)
    task = Task.from_dict(dict_task)
    assert type(task) == Task

    task_history_json = test_dir / "task-history.json"
    with task_history_json.open() as f:
        dict_task_history = json.load(f)
    task_history = TaskHistory.from_dict(dict_task_history)
    assert type(task_history) == TaskHistory