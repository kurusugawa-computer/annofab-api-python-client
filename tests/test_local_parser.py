"""
AnnofabApi2のテストメソッド

"""
import configparser
import os
from pathlib import Path

import annofabapi
import zipfile
import annofabapi.parser
from annofabapi.parser import SimpleAnnotationDirParser, SimpleAnnotationZipParser, FullAnnotationDirParser, FullAnnotationZipParser
import annofabapi.utils
from annofabapi.dataclass.annotation import FullAnnotation, SimpleAnnotation

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

    with zipfile.ZipFile(zip_path) as zip_file:
        parser = SimpleAnnotationZipParser(zip_file, "sample_1/.__tests__data__lenna.png.json")
        assert parser.task_id == "sample_1"
        assert parser.expected_input_data_name == "./tests/data/lenna.png"


def test_simple_annotation_dir():
    dir_path = Path(test_dir / "simple-annotation")
    iter_parser = annofabapi.parser.lazy_parse_simple_annotation_dir(dir_path)

    index = 0
    for parser in iter_parser:
        simple_annotation = parser.parse()
        assert type(simple_annotation) == SimpleAnnotation
        index += 1

    assert index == 2

    parser = SimpleAnnotationDirParser(Path(f"{test_dir}/simple-annotation/sample_1/.__tests__data__lenna.png.json"))
    assert parser.task_id == "sample_1"
    assert parser.expected_input_data_name == "./tests/data/lenna.png"


def test_full_annotation_zip():
    zip_path = Path(test_dir / "full-annotation.zip")
    iter_parser = annofabapi.parser.lazy_parse_full_annotation_zip(zip_path)

    index = 0
    for parser in iter_parser:
        full_annotation = parser.parse()
        assert type(full_annotation) == FullAnnotation
        index += 1

    assert index == 4

    with zipfile.ZipFile(zip_path) as zip_file:
        parser = FullAnnotationZipParser(zip_file, "sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json")
        assert parser.task_id == "sample_1"
        assert parser.input_data_id == "c86205d1-bdd4-4110-ae46-194e661d622b"


def test_full_annotation_dir():
    dir_path = Path(test_dir / "full-annotation")
    iter_parser = annofabapi.parser.lazy_parse_full_annotation_dir(dir_path)

    index = 0
    for parser in iter_parser:
        full_annotation = parser.parse()
        assert type(full_annotation) == FullAnnotation
        index += 1

    assert index == 4

    parser = FullAnnotationDirParser(Path(f"{test_dir}/simple-annotation/sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json"))
    assert parser.task_id == "sample_1"
    assert parser.input_data_id == "c86205d1-bdd4-4110-ae46-194e661d622b"
