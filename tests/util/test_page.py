"""
page.pyのテストコード
"""

import pytest

from annofabapi.util.page import (
    create_3dpc_editor_url,
    create_image_editor_url,
    create_project_url,
    create_video_editor_url,
    parse_3dpc_editor_url,
    parse_image_editor_url,
    parse_project_url,
    parse_task_url,
    parse_video_editor_url,
)


class TestCreateProjectUrl:
    """create_project_url関数のテストクラス"""

    def test_basic_url(self):
        result = create_project_url("project1")
        assert result == "https://annofab.com/projects/project1"


class TestCreateVideoEditorUrl:
    """create_video_editor_url関数のテストクラス"""

    def test_basic_url(self):
        """基本的なURLの生成をテスト"""
        result = create_video_editor_url("project1", "task1")
        expected = "https://annofab.com/projects/project1/tasks/task1/timeline"
        assert result == expected

    def test_with_annotation_id(self):
        """annotation_idを指定した場合のテスト"""
        result = create_video_editor_url("project1", "task1", annotation_id="annotation1")
        expected = "https://annofab.com/projects/project1/tasks/task1/timeline?#annotation1"
        assert result == expected

    def test_with_seek_seconds(self):
        """seek_secondsを指定した場合のテスト"""
        result = create_video_editor_url("project1", "task1", seek_seconds=5.5)
        expected = "https://annofab.com/projects/project1/tasks/task1/timeline?#/5.5"
        assert result == expected

    def test_with_both_params(self):
        """annotation_idとseek_secondsの両方を指定した場合のテスト"""
        result = create_video_editor_url("project1", "task1", annotation_id="annotation1", seek_seconds=10.5)
        expected = "https://annofab.com/projects/project1/tasks/task1/timeline?#annotation1/10.5"
        assert result == expected


class TestCreateImageEditorUrl:
    """create_image_editor_url関数のテストクラス"""

    def test_basic_url(self):
        """基本的なURLの生成をテスト"""
        result = create_image_editor_url("project1", "task1")
        expected = "https://annofab.com/projects/project1/tasks/task1/editor"
        assert result == expected

    def test_with_input_data_id(self):
        """input_data_idを指定した場合のテスト"""
        result = create_image_editor_url("project1", "task1", input_data_id="input1")
        expected = "https://annofab.com/projects/project1/tasks/task1/editor?#input1"
        assert result == expected

    def test_with_both_ids(self):
        """input_data_idとannotation_idの両方を指定した場合のテスト"""
        result = create_image_editor_url("project1", "task1", input_data_id="input1", annotation_id="annotation1")
        expected = "https://annofab.com/projects/project1/tasks/task1/editor?#input1/annotation1"
        assert result == expected

    def test_annotation_id_without_input_data_id_raises_error(self):
        """annotation_idのみを指定した場合にValueErrorが発生することをテスト"""
        with pytest.raises(ValueError):
            create_image_editor_url("project1", "task1", annotation_id="annotation1")


class TestCreate3dpcEditorUrl:
    """create_3dpc_editor_url関数のテストクラス"""

    def test_basic_url(self):
        """基本的なURLの生成をテスト"""
        result = create_3dpc_editor_url("project1", "task1")
        expected = "https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html?p=project1&t=task1"
        assert result == expected

    def test_with_custom_base_url(self):
        """カスタムのbase_urlを指定した場合のテスト"""
        custom_base_url = "https://custom.example.com/3d-editor/index.html"
        result = create_3dpc_editor_url("project1", "task1", base_url=custom_base_url)
        expected = "https://custom.example.com/3d-editor/index.html?p=project1&t=task1"
        assert result == expected

    def test_with_input_data_id(self):
        """input_data_idを指定した場合のテスト"""
        result = create_3dpc_editor_url("project1", "task1", input_data_id="input1")
        expected = "https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html?p=project1&t=task1#/input1"
        assert result == expected

    def test_with_both_ids(self):
        """input_data_idとannotation_idの両方を指定した場合のテスト"""
        result = create_3dpc_editor_url("project1", "task1", input_data_id="input1", annotation_id="annotation1")
        expected = "https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html?p=project1&t=task1#/input1/annotation1"
        assert result == expected

    def test_annotation_id_without_input_data_id_raises_error(self):
        """annotation_idのみを指定した場合にValueErrorが発生することをテスト"""
        with pytest.raises(ValueError):
            create_3dpc_editor_url("project1", "task1", annotation_id="annotation1")


class TestParseProjectUrl:
    @pytest.mark.parametrize("suffix", ["", "/", "/tasks", "/tasks/t1/editor?version=preview#i1/a1", "?q=1#fragment"])
    def test_project_screens(self, suffix):
        result = parse_project_url(f"https://annofab.com/projects/p1{suffix}")
        assert result.project_id == "p1"

    def test_round_trip(self):
        assert parse_project_url(create_project_url("p1")).project_id == "p1"

    @pytest.mark.parametrize(
        "url",
        [
            "",
            "/projects/p1",
            "http://annofab.com/projects/p1",
            "https://example.com/projects/p1",
            "https://annofab.com.example.com/projects/p1",
            "https://annofab.com@evil.example/projects/p1",
            "https://annofab.com/",
            "https://annofab.com/projects",
            "https://annofab.com/projects/",
            "https://annofab.com/projects/?project=p1",
            "https://annofab.com/other/p1",
        ],
    )
    def test_invalid_url(self, url):
        with pytest.raises(ValueError):
            parse_project_url(url)


class TestParseTaskUrl:
    @pytest.mark.parametrize("suffix", ["", "/", "/histories", "/editor?version=preview#i1/a1", "/timeline?#a1/3.3", "?q=1#fragment"])
    def test_task_screens(self, suffix):
        result = parse_task_url(f"https://annofab.com/projects/p1/tasks/t1{suffix}")
        assert (result.project_id, result.task_id) == ("p1", "t1")

    def test_percent_decoding(self):
        result = parse_task_url("https://annofab.com/projects/p%201/tasks/task%2F1")
        assert (result.project_id, result.task_id) == ("p 1", "task/1")

    @pytest.mark.parametrize(
        "path",
        ["/projects/p1", "/projects/p1/tasks", "/projects/p1/tasks/", "/projects/p1/tasks/?t=t1", "/projects/p1/other/t1", "/projects//tasks/t1"],
    )
    def test_missing_task_id(self, path):
        with pytest.raises(ValueError):
            parse_task_url(f"https://annofab.com{path}")


class TestParseImageEditorUrl:
    def test_preview_url(self):
        result = parse_image_editor_url(
            "https://annofab.com/projects/58a2a621-7d4b-41e7-927b-cdc570c1114a/tasks/20250327_01/editor"
            "?version=preview#b5353063-6b08-4fc6-94be-25354a006453/05da5c25-4ed8-4ff4-99c3-5313d964c775"
        )
        assert result.project_id == "58a2a621-7d4b-41e7-927b-cdc570c1114a"
        assert result.task_id == "20250327_01"
        assert result.input_data_id == "b5353063-6b08-4fc6-94be-25354a006453"
        assert result.annotation_id == "05da5c25-4ed8-4ff4-99c3-5313d964c775"

    @pytest.mark.parametrize(("input_data_id", "annotation_id"), [(None, None), ("i1", None), ("i1", "a1")])
    def test_round_trip(self, input_data_id, annotation_id):
        result = parse_image_editor_url(create_image_editor_url("p1", "t1", input_data_id=input_data_id, annotation_id=annotation_id))
        assert (result.project_id, result.task_id, result.input_data_id, result.annotation_id) == ("p1", "t1", input_data_id, annotation_id)

    def test_percent_decoding_and_trailing_slash(self):
        result = parse_image_editor_url("https://annofab.com/projects/p1/tasks/t1/editor/?version=preview#input%2F1/a%201")
        assert (result.input_data_id, result.annotation_id) == ("input/1", "a 1")

    @pytest.mark.parametrize("suffix", ["/histories#i1/a1", "/editor/other", "/editor#/a1", "/editor#i1/", "/editor#i1/a1/other"])
    def test_invalid_url(self, suffix):
        with pytest.raises(ValueError):
            parse_image_editor_url(f"https://annofab.com/projects/p1/tasks/t1{suffix}")


class TestParseVideoEditorUrl:
    @pytest.mark.parametrize(("annotation_id", "seek_seconds"), [(None, None), ("a1", None), (None, 3.3), ("a1", 3.3), ("a1", 0.0)])
    def test_round_trip(self, annotation_id, seek_seconds):
        result = parse_video_editor_url(create_video_editor_url("p1", "t1", annotation_id=annotation_id, seek_seconds=seek_seconds))
        assert (result.project_id, result.task_id, result.annotation_id, result.seek_seconds) == ("p1", "t1", annotation_id, seek_seconds)

    def test_percent_decoding_and_preview(self):
        result = parse_video_editor_url("https://annofab.com/projects/p1/tasks/t1/timeline/?version=preview#a%2F1/3%2E3")
        assert (result.annotation_id, result.seek_seconds) == ("a/1", 3.3)

    @pytest.mark.parametrize(
        "suffix",
        [
            "/editor",
            "/timeline/other",
            "/timeline#a1/",
            "/timeline#a1/invalid",
            "/timeline#a1/-1",
            "/timeline#a1/nan",
            "/timeline#a1/inf",
            "/timeline#a1/1/2",
        ],
    )
    def test_invalid_url(self, suffix):
        with pytest.raises(ValueError):
            parse_video_editor_url(f"https://annofab.com/projects/p1/tasks/t1{suffix}")


class TestParse3dpcEditorUrl:
    @pytest.mark.parametrize(("input_data_id", "annotation_id"), [(None, None), ("i1", None), ("i1", "a1")])
    @pytest.mark.parametrize(
        "base_url", ["https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html", "https://custom.example.com/3d-editor/index.html"]
    )
    def test_round_trip(self, input_data_id, annotation_id, base_url):
        url = create_3dpc_editor_url("p1", "t1", input_data_id=input_data_id, annotation_id=annotation_id, base_url=base_url)
        result = parse_3dpc_editor_url(url, base_url=base_url)
        assert (result.project_id, result.task_id, result.input_data_id, result.annotation_id) == ("p1", "t1", input_data_id, annotation_id)

    def test_default_base_url(self):
        result = parse_3dpc_editor_url(create_3dpc_editor_url("p1", "t1"))
        assert (result.project_id, result.task_id, result.input_data_id, result.annotation_id) == ("p1", "t1", None, None)

    def test_percent_decoding(self):
        result = parse_3dpc_editor_url(
            "https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html?p=p%201&t=t%2F1&version=preview#/i%2F1/a%201"
        )
        assert (result.project_id, result.task_id, result.input_data_id, result.annotation_id) == ("p 1", "t/1", "i/1", "a 1")

    @pytest.mark.parametrize(
        "suffix",
        [
            "",
            "?p=p1",
            "?t=t1",
            "?p=&t=t1",
            "?p=p1&t=",
            "?p=p1&p=p2&t=t1",
            "?p=p1&t=t1&t=t2",
            "?p=p1&t=t1#i1/a1",
            "?p=p1&t=t1#//a1",
            "?p=p1&t=t1#/i1/",
            "?p=p1&t=t1#/i1/a1/extra",
        ],
    )
    def test_invalid_url(self, suffix):
        with pytest.raises(ValueError):
            parse_3dpc_editor_url(f"https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html{suffix}")

    @pytest.mark.parametrize("url", ["https://evil.example/index.html?p=p1&t=t1", "https://d2rljy8mjgrfyd.cloudfront.net/other?p=p1&t=t1"])
    def test_wrong_editor(self, url):
        with pytest.raises(ValueError):
            parse_3dpc_editor_url(url)

    @pytest.mark.parametrize(
        "base_url", ["/editor", "ftp://example.com/editor", "https://example.com/editor?foo=bar", "https://example.com/editor#fragment"]
    )
    def test_invalid_base_url(self, base_url):
        with pytest.raises(ValueError):
            parse_3dpc_editor_url("https://example.com/editor?p=p1&t=t1", base_url=base_url)
