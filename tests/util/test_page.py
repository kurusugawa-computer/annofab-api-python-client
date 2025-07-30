"""
page.pyのテストコード
"""

import pytest

from annofabapi.util.page import create_3dpc_editor_url, create_image_editor_url, create_video_editor_url


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
        with pytest.raises(ValueError, match="'input_data_id' must be specified if 'annotation_id' is specified"):
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
        expected = "https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html?p=project1&t=task1/#input1"
        assert result == expected

    def test_with_both_ids(self):
        """input_data_idとannotation_idの両方を指定した場合のテスト"""
        result = create_3dpc_editor_url("project1", "task1", input_data_id="input1", annotation_id="annotation1")
        expected = "https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html?p=project1&t=task1/#input1/annotation1"
        assert result == expected

    def test_annotation_id_without_input_data_id_raises_error(self):
        """annotation_idのみを指定した場合にValueErrorが発生することをテスト"""
        with pytest.raises(ValueError, match="'input_data_id' must be specified if 'annotation_id' is specified"):
            create_3dpc_editor_url("project1", "task1", annotation_id="annotation1")
