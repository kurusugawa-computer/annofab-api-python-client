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
import annofabapi.parser
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


def test_simple_annotation_zip():
    zip_path = Path(test_dir / "simple-annotation.zip")
    iter_parser = annofabapi.parser.lazy_parse_simple_annotation_zip(zip_path)

    index = 0
    for parser in iter_parser:
        simple_annotation = parser.parse()
        assert type(simple_annotation) == SimpleAnnotation
        index += 1

    assert index == 2


def test_simple_annotation_dir():
    dir_path = Path(test_dir / "simple-annotation")
    iter_parser = annofabapi.parser.lazy_parse_simple_annotation_dir(dir_path)

    index = 0
    for parser in iter_parser:
        simple_annotation = parser.parse()
        assert type(simple_annotation) == SimpleAnnotation
        index += 1

    assert index == 2


def test_full_annotation_zip():
    zip_path = Path(test_dir / "full-annotation.zip")
    iter_parser = annofabapi.parser.lazy_parse_full_annotation_zip(zip_path)

    index = 0
    for parser in iter_parser:
        full_annotation = parser.parse()
        assert type(full_annotation) == FullAnnotation
        index += 1

    assert index == 4


def test_full_annotation_dir():
    dir_path = Path(test_dir / "full-annotation")
    iter_parser = annofabapi.parser.lazy_parse_full_annotation_dir(dir_path)

    index = 0
    for parser in iter_parser:
        full_annotation = parser.parse()
        assert type(full_annotation) == FullAnnotation
        index += 1

    assert index == 4
