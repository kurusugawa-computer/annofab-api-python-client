import configparser
import os
import zipfile
from pathlib import Path

import pytest

import annofabapi
import annofabapi.parser
import annofabapi.utils
from annofabapi.dataclass.annotation import FullAnnotation, FullAnnotationDataPoints, SimpleAnnotation
from annofabapi.exceptions import AnnotationOuterFileNotFoundError
from annofabapi.parser import (
    FullAnnotationDirParser,
    FullAnnotationZipParser,
    SimpleAnnotationDirParser,
    SimpleAnnotationDirParserByTask,
    SimpleAnnotationZipParser,
    SimpleAnnotationZipParserByTask,
)

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")
inifile = configparser.ConfigParser()
inifile.read("./pytest.ini", "UTF-8")

test_dir = Path("./tests/data")


class TestSimpleAnnotationParser:
    def test_SimpleAnnotationZipParser(self):
        zip_path = Path(test_dir / "simple-annotation.zip")
        with zipfile.ZipFile(zip_path) as zip_file:
            parser = SimpleAnnotationZipParser(zip_file, "sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json")
            assert parser.task_id == "sample_1"
            assert parser.input_data_id == "c86205d1-bdd4-4110-ae46-194e661d622b"
            assert parser.json_file_path == "sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json"

            with parser.open_outer_file("e2a1fbe3-fa8e-413c-be31-882f12ef62b9") as f:
                data = f.read()
                assert len(data) > 0

            with pytest.raises(AnnotationOuterFileNotFoundError):
                parser.open_outer_file("foo")

    def convert_deitail_data(self, dict_data):
        if dict_data["_type"] == "Points":
            dict_data["type"] = dict_data["_type"]
            return FullAnnotationDataPoints.from_dict(dict_data)
        else:
            return dict_data

    def test_parse_for_zip(self):
        zip_path = Path(test_dir / "simple-annotation.zip")
        with zipfile.ZipFile(zip_path) as zip_file:
            parser = SimpleAnnotationZipParser(zip_file, "sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json")

            simple_annotation = parser.parse()
            assert type(simple_annotation.details[0].data) == dict

            simple_annotation2 = parser.parse(self.convert_deitail_data)
            assert type(simple_annotation2.details[0].data) == FullAnnotationDataPoints

    def test_SimpleAnnotationDirParser(self):
        dir_path = Path(test_dir / "simple-annotation")

        parser = SimpleAnnotationDirParser(dir_path / "sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json")
        assert parser.task_id == "sample_1"
        assert parser.input_data_id == "c86205d1-bdd4-4110-ae46-194e661d622b"
        assert parser.json_file_path == str(dir_path / "sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json")

        with parser.open_outer_file("e2a1fbe3-fa8e-413c-be31-882f12ef62b9") as f:
            data = f.read()
            assert len(data) > 0

        with pytest.raises(AnnotationOuterFileNotFoundError):
            with parser.open_outer_file("foo"):
                pass


class TestSimpleAnnotationParserByTask:
    def test_SimpleAnnotationDirParserByTask(self):
        annotation_dir = test_dir / "simple-annotation"
        task_parser = SimpleAnnotationDirParserByTask(annotation_dir / "sample_1")
        assert task_parser.task_id == "sample_1"
        json_file_path_list = task_parser.json_file_path_list
        assert str(annotation_dir / "sample_1/c6e1c2ec-6c7c-41c6-9639-4244c2ed2839.json") in json_file_path_list
        assert str(annotation_dir / "sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json") in json_file_path_list

        input_data_parser = task_parser.get_parser(
            str(annotation_dir / "sample_1/c6e1c2ec-6c7c-41c6-9639-4244c2ed2839.json")
        )
        assert input_data_parser.input_data_id == "c6e1c2ec-6c7c-41c6-9639-4244c2ed2839"
        assert input_data_parser.json_file_path == str(
            test_dir / "simple-annotation/sample_1/c6e1c2ec-6c7c-41c6-9639-4244c2ed2839.json"
        )

    def test_SimpleAnnotationZipParserByTask(self):
        with zipfile.ZipFile(test_dir / "simple-annotation.zip") as zip_file:
            task_parser = SimpleAnnotationZipParserByTask(zip_file, "sample_1")

            assert task_parser.task_id == "sample_1"
            json_file_path_list = task_parser.json_file_path_list
            assert "sample_1/c6e1c2ec-6c7c-41c6-9639-4244c2ed2839.json" in json_file_path_list
            assert "sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json" in json_file_path_list

            input_data_parser = task_parser.get_parser("sample_1/c6e1c2ec-6c7c-41c6-9639-4244c2ed2839.json")
            assert input_data_parser.input_data_id == "c6e1c2ec-6c7c-41c6-9639-4244c2ed2839"
            assert input_data_parser.json_file_path == str("sample_1/c6e1c2ec-6c7c-41c6-9639-4244c2ed2839.json")


class TestSimpleAnnotation:
    def test_simple_annotation_zip(self):
        zip_path = Path(test_dir / "simple-annotation.zip")
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

    def test_simple_annotation_dir(self):
        dir_path = Path(test_dir / "simple-annotation")
        iter_parser = annofabapi.parser.lazy_parse_simple_annotation_dir(dir_path)

        index = 0
        for parser in iter_parser:
            simple_annotation = parser.parse()
            assert type(simple_annotation) == SimpleAnnotation
            index += 1

            dict_simple_annotation = parser.load_json()
            assert type(dict_simple_annotation) == dict
            assert "details" in dict_simple_annotation

        assert index == 4

    def test_lazy_parse_simple_annotation_zip_by_task(self):
        zip_path = Path(test_dir / "simple-annotation.zip")
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
        zip_path = Path(test_dir / "simple-annotation")
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

            dict_simple_annotation = parser.load_json()
            assert type(dict_simple_annotation) == dict
            assert "details" in dict_simple_annotation

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

        parser_full = FullAnnotationDirParser(
            Path(f"{test_dir}/full-annotation/sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json")
        )
        assert parser_full.task_id == "sample_1"
        assert parser_full.input_data_id == "c86205d1-bdd4-4110-ae46-194e661d622b"

        dict_simple_annotation = parser_full.load_json()
        assert type(dict_simple_annotation) == dict
        assert "details" in dict_simple_annotation

        with pytest.raises(AnnotationOuterFileNotFoundError):
            parser_full.open_outer_file("foo")

    def convert_deitail_data(self, dict_data):
        if dict_data["_type"] == "Points":
            dict_data["type"] = dict_data["_type"]
            return FullAnnotationDataPoints.from_dict(dict_data)
        else:
            return dict_data

    def test_parse_for_zip(self):
        zip_path = Path(test_dir / "full-annotation.zip")
        with zipfile.ZipFile(zip_path) as zip_file:
            parser = FullAnnotationZipParser(zip_file, "sample_1/c86205d1-bdd4-4110-ae46-194e661d622b.json")

            full_annotation = parser.parse()
            assert type(full_annotation.details[0].data) == dict

            full_annotation2 = parser.parse(self.convert_deitail_data)
            assert type(full_annotation2.details[0].data) == FullAnnotationDataPoints
