"""生成されたAPIメソッドの引数に関する回帰テスト。"""

import inspect
from unittest.mock import patch

import pytest
import requests

from annofabapi.api import AnnofabApi
from annofabapi.api2 import AnnofabApi2
from annofabapi.credentials import Pat
from annofabapi.generated_api import AbstractAnnofabApi
from annofabapi.generated_api2 import AbstractAnnofabApi2


@pytest.mark.parametrize("api_class", [AbstractAnnofabApi, AbstractAnnofabApi2])
def test_生成メソッドのリクエスト引数はキーワード専用(api_class):
    for name, method in inspect.getmembers(api_class, inspect.isfunction):
        if name.startswith("_"):
            continue
        for parameter in inspect.signature(method).parameters.values():
            if parameter.name in {"query_params", "header_params", "request_body"}:
                assert parameter.kind == inspect.Parameter.KEYWORD_ONLY, (name, parameter.name)
            elif parameter.name != "kwargs":
                assert parameter.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD, (name, parameter.name)


@pytest.mark.parametrize("version", [1, 2])
def test_リクエスト引数を位置引数で渡すと通信前に失敗する(version):
    api = AnnofabApi(Pat("test-token"))
    target_api = api if version == 1 else AnnofabApi2(api)
    method_name = "put_annotation" if version == 1 else "get_annotation_specs_v2"
    path_args = ("project", "task", "input") if version == 1 else ("project",)

    with patch.object(api.session, "request") as request:
        with pytest.raises(TypeError):
            getattr(target_api, method_name)(*path_args, {"v": "2"})
        request.assert_not_called()


def test_put_annotationのキーワード引数がHTTPリクエストに反映される():
    api = AnnofabApi(Pat("test-token"))
    api.tokens = Pat("test-token")
    response = requests.Response()
    response.status_code = 204
    response.headers["Content-Type"] = "text/plain"
    response._content = b""
    query_params = {"v": "2"}
    request_body: dict[str, dict[str, list[object]]] = {"annotation": {"details": []}}
    header_params = {"X-Test": "test"}

    with patch.object(api.session, "request", return_value=response) as request:
        _, actual_response = api.put_annotation(
            "project", "task", "input", query_params=query_params, header_params=header_params, request_body=request_body
        )

    assert actual_response is response
    assert request.call_count == 1
    assert request.call_args.kwargs["url"].endswith("/projects/project/tasks/task/inputs/input/annotation")
    assert request.call_args.kwargs["params"] == query_params
    assert request.call_args.kwargs["headers"] == header_params
    assert request.call_args.kwargs["json"] == request_body


def test_v2のキーワード引数がHTTPリクエストに反映される():
    api = AnnofabApi(Pat("test-token"))
    api2 = AnnofabApi2(api)
    response = requests.Response()
    response.status_code = 204
    response.headers["Content-Type"] = "text/plain"
    response._content = b""
    query_params = {"v": "3"}

    with patch.object(api.session, "request", return_value=response) as request:
        _, actual_response = api2.get_annotation_specs_v2(project_id="project", query_params=query_params)

    assert actual_response is response
    assert request.call_count == 1
    assert request.call_args.kwargs["url"].endswith("/api/v2/projects/project/annotation-specs")
    assert request.call_args.kwargs["params"] == query_params
