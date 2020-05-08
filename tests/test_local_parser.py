import configparser
import os
import zipfile
from pathlib import Path

import pytest

import annofabapi
import annofabapi.parser
import annofabapi.utils
from annofabapi.dataclass.annotation import FullAnnotation, SimpleAnnotation
from annofabapi.exceptions import AnnotationOuterFileNotFoundError
from annofabapi.parser import (
    FullAnnotationDirParser,
    FullAnnotationZipParser,
    SimpleAnnotationDirParser,
    SimpleAnnotationZipParser,
)

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")
inifile = configparser.ConfigParser()
inifile.read("./pytest.ini", "UTF-8")

test_dir = Path("./tests/data")


class TestSimpleAnnotation:
    def test_simple_annotation_zip(self):
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
            with pytest.raises(AnnotationOuterFileNotFoundError):
                parser.open_outer_file("foo")

    def test_simple_annotation_dir(self):
        dir_path = Path(test_dir / "simple-annotation")
        iter_parser = annofabapi.parser.lazy_parse_simple_annotation_dir(dir_path)

        index = 0
        for parser in iter_parser:
            simple_annotation = parser.parse()
            assert type(simple_annotation) == SimpleAnnotation
            index += 1

        assert index == 2

        parser = SimpleAnnotationDirParser(
            Path(f"{test_dir}/simple-annotation/sample_1/.__tests__data__lenna.png.json")
        )
        assert parser.task_id == "sample_1"
        assert parser.expected_input_data_name == "./tests/data/lenna.png"
        with pytest.raises(AnnotationOuterFileNotFoundError):
            parser.open_outer_file("foo")


class TestSimpleAnnotationV2:
    def test_simple_annotation_zip(self):
        zip_path = Path(test_dir / "simple-annotation-v2.zip")
        iter_parser = annofabapi.parser.lazy_parse_simple_annotation_zip(zip_path)

        index = 0
        for parser in iter_parser:
            simple_annotation = parser.parse()
            assert type(simple_annotation) == SimpleAnnotation
            index += 1

            dict_simple_annotation = parser.load_json()
            assert type(dict_simple_annotation) == dict
            assert "details" in dict_simple_annotation

        assert index == 4

        with zipfile.ZipFile(zip_path) as zip_file:
            parser = SimpleAnnotationZipParser(zip_file, "sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json")
            assert parser.task_id == "sample_1"
            assert parser.input_data_id == "c86205d1-bdd4-4110-ae46-194e661d622b"
            with pytest.raises(AnnotationOuterFileNotFoundError):
                parser.open_outer_file("foo")

    def test_simple_annotation_dir(self):
        dir_path = Path(test_dir / "simple-annotation-v2")
        iter_parser = annofabapi.parser.lazy_parse_simple_annotation_dir(dir_path)

        index = 0
        for parser in iter_parser:
            simple_annotation = parser.parse()
            assert type(simple_annotation) == SimpleAnnotation
            index += 1

        assert index == 4

        parser = SimpleAnnotationDirParser(dir_path / "sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json")
        assert parser.task_id == "sample_1"
        assert parser.input_data_id == "c86205d1-bdd4-4110-ae46-194e661d622b"
        with pytest.raises(AnnotationOuterFileNotFoundError):
            parser.open_outer_file("foo")

    def test_lazy_parse_simple_annotation_zip_by_task(self):
        zip_path = Path(test_dir / "simple-annotation-v2.zip")
        task_parser_list = list(annofabapi.parser.lazy_parse_simple_annotation_zip_by_task(zip_path))

        assert len(task_parser_list) == 2
        assert len([e for e in task_parser_list if e.task_id == "sample_1"]) == 1
        assert len([e for e in task_parser_list if e.task_id == "sample_0"]) == 1

        task_parser = [e for e in task_parser_list if e.task_id == "sample_1"][0]
        parser_list = list(task_parser.lazy_parse())
        assert len(parser_list) == 2
        assert len([e for e in parser_list if e.input_data_id == "c6e1c2ec-6c7c-41c6-9639-4244c2ed2839"]) == 1
        assert len([e for e in parser_list if e.input_data_id == "c86205d1-bdd4-4110-ae46-194e661d622b"]) == 1

    def test_lazy_parse_simple_annotation_dir_by_task(self):
        zip_path = Path(test_dir / "simple-annotation-v2")
        task_parser_list = list(annofabapi.parser.lazy_parse_simple_annotation_dir_by_task(zip_path))

        assert len(task_parser_list) == 2
        assert len([e for e in task_parser_list if e.task_id == "sample_1"]) == 1
        assert len([e for e in task_parser_list if e.task_id == "sample_0"]) == 1

        task_parser = [e for e in task_parser_list if e.task_id == "sample_1"][0]
        parser_list = list(task_parser.lazy_parse())
        assert len(parser_list) == 2
        assert len([e for e in parser_list if e.input_data_id == "c6e1c2ec-6c7c-41c6-9639-4244c2ed2839"]) == 1
        assert len([e for e in parser_list if e.input_data_id == "c86205d1-bdd4-4110-ae46-194e661d622b"]) == 1


class TestFullAnnotation:
    def test_full_annotation_zip(self):
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
            with pytest.raises(AnnotationOuterFileNotFoundError):
                parser.open_outer_file("foo")

    def test_full_annotation_dir(self):
        dir_path = Path(test_dir / "full-annotation")
        iter_parser = annofabapi.parser.lazy_parse_full_annotation_dir(dir_path)

        index = 0
        for parser in iter_parser:
            full_annotation = parser.parse()
            assert type(full_annotation) == FullAnnotation
            index += 1

        assert index == 4

        parser = FullAnnotationDirParser(
            Path(f"{test_dir}/simple-annotation/sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json")
        )
        assert parser.task_id == "sample_1"
        assert parser.input_data_id == "c86205d1-bdd4-4110-ae46-194e661d622b"
        with pytest.raises(AnnotationOuterFileNotFoundError):
            parser.open_outer_file("foo")
