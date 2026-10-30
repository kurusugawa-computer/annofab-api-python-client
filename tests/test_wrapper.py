import io
import warnings
from pathlib import Path
from unittest.mock import patch

import pytest
import requests

from annofabapi.api import AnnofabApi
from annofabapi.credentials import Pat
from annofabapi.wrapper import Wrapper

data_dir = Path("./tests/data")


class TestWrapperUtils:
    def test__get_mime_type(self):
        assert Wrapper._get_mime_type(str(data_dir / "lenna.png")) == "image/png"
        assert Wrapper._get_mime_type("sample.jpg") == "image/jpeg"
        assert Wrapper._get_mime_type("sample.txt") == "text/plain"
        assert Wrapper._get_mime_type("sample") == "application/octet-stream"


@pytest.mark.parametrize("use_deprecated_name", [False, True])
@pytest.mark.parametrize("use_string_path", [False, True])
@pytest.mark.parametrize(
    ("old_name", "new_name", "api_method", "source_file"),
    [
        ("download_annotation_archive", "download_annotation_zip", "get_annotation_archive", "simple-annotation.zip"),
        ("download_project_inputs_url", "download_project_inputs_json", "get_project_inputs_url", "tasks.json"),
        ("download_project_tasks_url", "download_project_tasks_json", "get_project_tasks_url", "tasks.json"),
        ("download_project_comments_url", "download_project_comments_json", "get_project_comments_url", "tasks.json"),
        (
            "download_project_task_history_events_url",
            "download_project_task_history_events_json",
            "get_project_task_history_events_url",
            "tasks.json",
        ),
        ("download_project_task_histories_url", "download_project_task_histories_json", "get_project_task_histories_url", "tasks.json"),
    ],
)
def test_download_file(tmp_path, use_deprecated_name, use_string_path, old_name, new_name, api_method, source_file):
    """新旧のメソッドでファイル保存とURLの返却を維持し、旧名だけ移行を警告する。"""
    api = AnnofabApi(Pat("test-token"))
    wrapper = Wrapper(api)
    url = "https://example.com/download"
    content = (data_dir / source_file).read_bytes() if source_file.endswith(".zip") else b'[{"task_id": "task-1"}]'
    metadata_response = requests.Response()
    metadata_response.status_code = 200
    metadata_response.headers["Location"] = url
    download_response = requests.Response()
    download_response.status_code = 200
    download_response.raw = io.BytesIO(content)
    dest_path = tmp_path / "nested" / source_file
    dest = str(dest_path) if use_string_path else dest_path
    method = getattr(wrapper, old_name if use_deprecated_name else new_name)

    with (
        patch.object(api, api_method, return_value=({"url": url}, metadata_response)),
        patch.object(api, "_execute_http_request", return_value=download_response),
        warnings.catch_warnings(),
    ):
        warnings.simplefilter("error", FutureWarning)
        if use_deprecated_name:
            with pytest.warns(FutureWarning, match=rf"{old_name}.*on or after 2027-04-01.*{new_name}") as warning_records:
                actual_url = method("project-1", dest)
            assert len(warning_records) == 1
            assert warning_records[0].filename == __file__
        else:
            actual_url = method("project-1", dest)

    assert actual_url == url
    assert dest_path.read_bytes() == content


@pytest.mark.parametrize("method_name", ["download_annotation_archive", "download_annotation_zip"])
def test_download_annotation_zip_waits_for_update(tmp_path, method_name):
    """更新中のZIPは、指定された間隔・回数でジョブを確認してからダウンロードする。"""
    api = AnnofabApi(Pat("test-token"))
    wrapper = Wrapper(api)
    url = "https://example.com/annotation.zip"
    conflict = requests.Response()
    conflict.status_code = 409
    conflict._content = b'{"errors": [{"error_code": "WORKER_ALREADY_INVOKED"}]}'
    metadata_response = requests.Response()
    metadata_response.headers["Location"] = url
    content = (data_dir / "simple-annotation.zip").read_bytes()
    download_response = requests.Response()
    download_response.raw = io.BytesIO(content)
    dest_path = tmp_path / "annotation.zip"
    progress = {"job_id": "job-1", "job_status": "progress"}
    succeeded = {"job_id": "job-1", "job_status": "succeeded"}

    with (
        patch.object(api, "get_annotation_archive", side_effect=[requests.HTTPError(response=conflict), ({}, metadata_response)]),
        patch.object(api, "get_project_job", side_effect=[({"list": [progress]}, metadata_response), ({"list": [succeeded]}, metadata_response)]),
        patch.object(api, "_execute_http_request", return_value=download_response),
        patch("annofabapi.wrapper.time.sleep") as sleep,
        warnings.catch_warnings(),
    ):
        warnings.simplefilter("ignore", FutureWarning)
        actual_url = getattr(wrapper, method_name)("project-1", dest_path, job_access_interval=7, max_job_access=2)

    sleep.assert_called_once_with(7)
    assert actual_url == url
    assert dest_path.read_bytes() == content
