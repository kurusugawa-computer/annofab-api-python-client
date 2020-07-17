import logging

import pytest


def pytest_addoption(parser):
    parser.addoption("--run_submitting_job", action="store_true", default=False, help="ジョブを投げるテストを実行する。")
    parser.addoption("--run_side_effect", action="store_true", default=False, help="副作用のあるテストを実行する。")
    parser.addoption("--print_log_annofabapi", action="store_true", default=False, help="annofabapiモジュールのログを表示する。")


def pytest_configure(config):
    config.addinivalue_line("markers", "submitting_job: mark test with submitting job")
    config.addinivalue_line("markers", "side_effect: mark test with side effect")


def pytest_collection_modifyitems(config, items):
    run_submitting_job = config.getoption("--run_submitting_job")
    run_side_effect = config.getoption("--run_side_effect")

    skip_slow_submitting_job = pytest.mark.skip(reason="need --run_submitting_job option to run")
    skip_slow_side_effect = pytest.mark.skip(reason="need --run_side_effect option to run")
    for item in items:
        if not run_submitting_job and "submitting_job" in item.keywords:
            item.add_marker(skip_slow_submitting_job)
        if not run_side_effect and "side_effect" in item.keywords:
            item.add_marker(skip_slow_side_effect)


def pytest_cmdline_main(config):
    if config.getoption("--print_log_annofabapi"):
        logging_formatter = "%(levelname)s : %(asctime)s : %(name)s : %(funcName)s : %(message)s"
        logging.basicConfig(format=logging_formatter)
        logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)
