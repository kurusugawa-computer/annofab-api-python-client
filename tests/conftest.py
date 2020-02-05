import logging

import pytest


def pytest_addoption(parser):
    parser.addoption("--run_submitting_job", action="store_true", default=False, help="ジョブを投げるテストを実行する。")
    parser.addoption("--print_log_annofabapi", action="store_true", default=False, help="annofabapiモジュールのログを表示する。")


def pytest_configure(config):
    config.addinivalue_line("markers", "submitting_job: mark test with submitting job")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run_submitting_job"):
        return
    skip_slow = pytest.mark.skip(reason="need --sun_submitting_job option to run")
    for item in items:
        if "submitting_job" in item.keywords:
            item.add_marker(skip_slow)


def pytest_cmdline_main(config):
    if config.getoption("--print_log_annofabapi"):
        print("logging")
        logging_formatter = '%(levelname)s : %(asctime)s : %(name)s : %(funcName)s : %(message)s'
        logging.basicConfig(format=logging_formatter)
        logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)
    else:
        print("not logging")
