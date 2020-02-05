import pytest


def pytest_addoption(parser):
    parser.addoption("--run_submitting_job", action="store_true", default=False, help="ジョブを投げるテストを実行する。")


def pytest_configure(config):
    config.addinivalue_line("markers", "submitting_job: mark test with submitting job")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run_submitting_job"):
        return
    skip_slow = pytest.mark.skip(reason="need --sun_submitting_job option to run")
    for item in items:
        if "submitting_job" in item.keywords:
            item.add_marker(skip_slow)
