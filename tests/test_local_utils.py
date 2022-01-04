import pytest
import requests

from annofabapi.models import TaskPhase
from annofabapi.utils import (
    _create_request_body_for_logger,
    get_number_of_rejections,
    get_task_history_index_skipped_acceptance,
    get_task_history_index_skipped_inspection,
    my_backoff,
)


class TestTaskHistoryUtils:
    ACCOUNT_ID = "12345678-abcd-1234-abcd-1234abcd5678"

    def test_get_task_history_index_skipped_acceptance_検査0回_受入スキップ(self):
        task_history_list = [
            {
                "started_datetime": "2020-01-22T09:32:15.284+09:00",
                "ended_datetime": "2020-01-22T09:32:19.628+09:00",
                "accumulated_labor_time_milliseconds": "PT4.344S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "started_datetime": "2020-01-22T09:32:19.63+09:00",
                "ended_datetime": "2020-01-22T09:32:19.63+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "acceptance",
                "phase_stage": 1,
                "account_id": None,
            },
        ]

        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = [1]
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_acceptance_検査0回_受入スキップ後に受入取消(self):
        task_history_list = [
            {
                "started_datetime": "2020-01-22T09:35:26.13+09:00",
                "ended_datetime": "2020-01-22T09:35:29.745+09:00",
                "accumulated_labor_time_milliseconds": "PT3.615S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": "00589ed0-dd63-40db-abb2-dfe5e13c8299",
            },
            {
                "started_datetime": "2020-01-22T09:35:29.747+09:00",
                "ended_datetime": "2020-01-22T09:35:29.747+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "acceptance",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "started_datetime": None,
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "acceptance",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
        ]

        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = [1]
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_acceptance_検査0回_教師付で提出取消(self):
        task_history_list = [
            {
                "started_datetime": "2020-01-22T09:36:11.187+09:00",
                "ended_datetime": "2020-01-22T09:36:14.186+09:00",
                "accumulated_labor_time_milliseconds": "PT2.999S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "started_datetime": "2020-01-22T09:36:23.86+09:00",
                "ended_datetime": "2020-01-22T09:36:23.86+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "acceptance",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "started_datetime": None,
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
        ]
        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_acceptance_検査1回_検査で提出取消(self):
        task_history_list = [
            {
                "started_datetime": "2020-01-22T09:39:20.492+09:00",
                "ended_datetime": "2020-01-22T09:39:24.911+09:00",
                "accumulated_labor_time_milliseconds": "PT4.419S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "started_datetime": "2020-01-22T09:40:04.978+09:00",
                "ended_datetime": "2020-01-22T09:40:08.091+09:00",
                "accumulated_labor_time_milliseconds": "PT3.113S",
                "phase": "inspection",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "started_datetime": "2020-01-22T09:40:15.136+09:00",
                "ended_datetime": "2020-01-22T09:40:15.136+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "acceptance",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "started_datetime": None,
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "inspection",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
        ]

        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_inspection_検査1回_検査スキップ(self):
        task_history_list = [
            {
                "started_datetime": "2020-01-22T09:58:20.063+09:00",
                "ended_datetime": "2020-01-22T09:58:23.749+09:00",
                "accumulated_labor_time_milliseconds": "PT3.686S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "started_datetime": "2020-01-22T09:58:23.751+09:00",
                "ended_datetime": "2020-01-22T09:58:23.751+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "inspection",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "started_datetime": "2020-01-22T09:58:23.753+09:00",
                "ended_datetime": "2020-01-22T09:58:23.753+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "acceptance",
                "phase_stage": 1,
                "account_id": None,
            },
        ]

        actual = get_task_history_index_skipped_inspection(task_history_list)
        expected = [1]
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_inspection_検査1回_教師付で提出取消(self):
        task_history_list = [
            {
                "started_datetime": "2020-01-22T10:00:33.832+09:00",
                "ended_datetime": "2020-01-22T10:00:37.381+09:00",
                "accumulated_labor_time_milliseconds": "PT3.549S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "started_datetime": "2020-01-22T10:00:45.953+09:00",
                "ended_datetime": "2020-01-22T10:00:45.953+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "inspection",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "started_datetime": None,
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
        ]
        actual = get_task_history_index_skipped_inspection(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_inspection_検査2回_検査1回目で提出取消(self):
        task_history_list = [
            {
                "started_datetime": "2019-09-04T16:15:51.505+09:00",
                "ended_datetime": "2019-09-04T16:16:31.597+09:00",
                "accumulated_labor_time_milliseconds": "PT40.092S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "started_datetime": "2020-01-22T10:06:18.435+09:00",
                "ended_datetime": "2020-01-22T10:06:21.919+09:00",
                "accumulated_labor_time_milliseconds": "PT3.484S",
                "phase": "inspection",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "started_datetime": "2020-01-22T10:07:38.456+09:00",
                "ended_datetime": "2020-01-22T10:07:38.456+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "inspection",
                "phase_stage": 2,
                "account_id": None,
            },
            {
                "started_datetime": None,
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "inspection",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
        ]
        actual = get_task_history_index_skipped_inspection(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_number_of_rejections_教師付1回目(self):
        task_history_short_list = [
            {"account_id": self.ACCOUNT_ID, "phase": "annotation", "phase_stage": 1, "worked": True}
        ]

        actual = get_number_of_rejections(task_history_short_list, TaskPhase.ACCEPTANCE)
        assert actual == 0

    def test_get_number_of_rejections_受入で1回差戻(self):
        task_history_short_list = [
            {"account_id": self.ACCOUNT_ID, "phase": "annotation", "phase_stage": 1, "worked": True},
            {"account_id": self.ACCOUNT_ID, "phase": "acceptance", "phase_stage": 1, "worked": True},
            {"account_id": self.ACCOUNT_ID, "phase": "annotation", "phase_stage": 1, "worked": True},
        ]

        actual = get_number_of_rejections(task_history_short_list, TaskPhase.ACCEPTANCE)
        assert actual == 1

    def test_get_number_of_rejections_検査で1回差戻(self):
        task_history_short_list = [
            {"account_id": self.ACCOUNT_ID, "phase": "annotation", "phase_stage": 1, "worked": True},
            {"account_id": self.ACCOUNT_ID, "phase": "inspection", "phase_stage": 1, "worked": True},
            {"account_id": self.ACCOUNT_ID, "phase": "annotation", "phase_stage": 1, "worked": True},
        ]

        actual = get_number_of_rejections(task_history_short_list, TaskPhase.INSPECTION)
        assert actual == 1

    def test_get_number_of_rejections_検査と受入で1回差戻(self):
        task_history_short_list = [
            {"account_id": self.ACCOUNT_ID, "phase": "annotation", "phase_stage": 1, "worked": True},
            {"account_id": self.ACCOUNT_ID, "phase": "inspection", "phase_stage": 1, "worked": True},
            {"account_id": self.ACCOUNT_ID, "phase": "annotation", "phase_stage": 1, "worked": True},
            {"account_id": self.ACCOUNT_ID, "phase": "inspection", "phase_stage": 1, "worked": True},
            {"account_id": self.ACCOUNT_ID, "phase": "acceptance", "phase_stage": 1, "worked": True},
            {"account_id": self.ACCOUNT_ID, "phase": "annotation", "phase_stage": 1, "worked": True},
            {
                "account_id": "00589ed0-dd63-40db-abb2-dfe5e13c8299",
                "phase": "inspection",
                "phase_stage": 1,
                "worked": True,
            },
            {"account_id": self.ACCOUNT_ID, "phase": "acceptance", "phase_stage": 1, "worked": True},
        ]
        actual_inspection = get_number_of_rejections(task_history_short_list, TaskPhase.INSPECTION)
        assert actual_inspection == 1
        actual_acceptance = get_number_of_rejections(task_history_short_list, TaskPhase.ACCEPTANCE)
        assert actual_acceptance == 1


class TestTaskHistoryUtils2:
    ACCOUNT_ID = "12345678-abcd-1234-abcd-1234abcd5678"

    def test_get_task_history_index_skipped_acceptance_検査0回_受入スキップ(self):
        task_history_list = [
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_01",
                "task_history_id": "d7301dc0-cd8b-4228-8b68-bf7924a02caa",
                "started_datetime": "2020-12-09T02:17:42.257+09:00",
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_01",
                "task_history_id": "a3d81516-8c7d-4d0a-a0ea-1696770a9643",
                "started_datetime": "2020-12-09T16:21:33.39+09:00",
                "ended_datetime": "2020-12-09T16:21:36.302+09:00",
                "accumulated_labor_time_milliseconds": "PT2.912S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_01",
                "task_history_id": "32601981-d8be-4125-9f7e-7e37e34c3fc6",
                "started_datetime": "2020-12-09T16:21:36.304+09:00",
                "ended_datetime": "2020-12-09T16:21:36.304+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "acceptance",
                "phase_stage": 1,
                "account_id": None,
            },
        ]

        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = [2]
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_acceptance_検査0回_受入スキップ後に受入取消(self):
        task_history_list = [
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_01",
                "task_history_id": "d7301dc0-cd8b-4228-8b68-bf7924a02caa",
                "started_datetime": "2020-12-09T02:17:42.257+09:00",
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_01",
                "task_history_id": "a3d81516-8c7d-4d0a-a0ea-1696770a9643",
                "started_datetime": "2020-12-09T16:21:33.39+09:00",
                "ended_datetime": "2020-12-09T16:21:36.302+09:00",
                "accumulated_labor_time_milliseconds": "PT2.912S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_01",
                "task_history_id": "32601981-d8be-4125-9f7e-7e37e34c3fc6",
                "started_datetime": "2020-12-09T16:21:36.304+09:00",
                "ended_datetime": "2020-12-09T16:21:36.304+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "acceptance",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_01",
                "task_history_id": "2ed27cc3-7a85-4f7f-9b28-bbde585ac564",
                "started_datetime": None,
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "acceptance",
                "phase_stage": 1,
                "account_id": None,
            },
        ]

        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = [2]
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_acceptance_検査0回_教師付で提出取消(self):
        task_history_list = [
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_27",
                "task_history_id": "8d8d92fc-322d-442a-b29b-a9a4481753bf",
                "started_datetime": "2020-12-09T02:17:42.257+09:00",
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_27",
                "task_history_id": "a9af5492-82a6-426a-b1c2-25e7704f9078",
                "started_datetime": "2020-12-09T17:13:55.714+09:00",
                "ended_datetime": "2020-12-09T17:14:24.351+09:00",
                "accumulated_labor_time_milliseconds": "PT28.637S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_27",
                "task_history_id": "86e72703-606b-48d8-8e8b-0d3087637762",
                "started_datetime": "2020-12-09T17:14:35.434+09:00",
                "ended_datetime": "2020-12-09T17:14:35.434+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "acceptance",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_27",
                "task_history_id": "457a7860-19c4-4fbb-82d8-1b86fa95b0db",
                "started_datetime": None,
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
        ]

        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_acceptance_検査1回_検査で提出取消(self):
        task_history_list = [
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_30",
                "task_history_id": "fdae87b7-0fdb-46d3-8e31-cb030eb001f7",
                "started_datetime": "2020-12-09T02:17:42.257+09:00",
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_30",
                "task_history_id": "8c68ca72-2e50-4a98-9408-1e008525f550",
                "started_datetime": "2020-12-09T17:20:20.826+09:00",
                "ended_datetime": "2020-12-09T17:20:30.137+09:00",
                "accumulated_labor_time_milliseconds": "PT9.311S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_30",
                "task_history_id": "9b265f61-3a29-4998-b586-e38e7493d786",
                "started_datetime": "2020-12-09T17:20:30.138+09:00",
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "inspection",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_30",
                "task_history_id": "f3a0af42-e31f-4517-a7b6-cb738d886675",
                "started_datetime": "2020-12-09T17:20:43.612+09:00",
                "ended_datetime": "2020-12-09T17:20:47.843+09:00",
                "accumulated_labor_time_milliseconds": "PT4.231S",
                "phase": "inspection",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_30",
                "task_history_id": "799039ea-f18a-4864-af57-764d243fb404",
                "started_datetime": "2020-12-09T17:20:54.664+09:00",
                "ended_datetime": "2020-12-09T17:20:54.664+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "acceptance",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_30",
                "task_history_id": "4cd94d07-9b6e-4a32-b282-4ebd07ff3e78",
                "started_datetime": None,
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "inspection",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
        ]

        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_inspection_検査1回_検査スキップ(self):
        task_history_list = [
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_16",
                "task_history_id": "e1065cd3-6138-43ec-bb52-99da2e677a13",
                "started_datetime": "2020-12-09T02:17:42.257+09:00",
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_16",
                "task_history_id": "58dad703-0f37-4ead-b9d3-c50435dc9d7a",
                "started_datetime": "2020-12-09T16:20:11.705+09:00",
                "ended_datetime": "2020-12-09T16:20:20.44+09:00",
                "accumulated_labor_time_milliseconds": "PT8.735S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_16",
                "task_history_id": "dec1b973-3403-428f-a2ab-9d6abc1c4151",
                "started_datetime": "2020-12-09T16:20:20.442+09:00",
                "ended_datetime": "2020-12-09T16:20:20.442+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "inspection",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_16",
                "task_history_id": "09ead8bd-e979-46f3-986a-cae04c485312",
                "started_datetime": "2020-12-09T16:20:20.444+09:00",
                "ended_datetime": "2020-12-09T16:20:20.444+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "acceptance",
                "phase_stage": 1,
                "account_id": None,
            },
        ]

        actual = get_task_history_index_skipped_inspection(task_history_list)
        expected = [2]
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_inspection_検査1回_教師付で提出取消(self):
        task_history_list = [
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_29",
                "task_history_id": "f0152033-4cc0-4b4b-97c3-3133bf7411a0",
                "started_datetime": "2020-12-09T02:17:42.257+09:00",
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_29",
                "task_history_id": "64e4e22d-8023-4120-b2cf-34d9b6625d52",
                "started_datetime": "2020-12-09T17:27:46.972+09:00",
                "ended_datetime": "2020-12-09T17:27:51.86+09:00",
                "accumulated_labor_time_milliseconds": "PT4.888S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_29",
                "task_history_id": "4a904f0a-646c-40d7-a0f6-7ce8b1c11934",
                "started_datetime": "2020-12-09T17:27:58.352+09:00",
                "ended_datetime": "2020-12-09T17:27:58.352+09:00",
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "inspection",
                "phase_stage": 1,
                "account_id": None,
            },
            {
                "project_id": "58a2a621-7d4b-41e7-927b-cdc570c1114a",
                "task_id": "testt_29",
                "task_history_id": "af3e3455-02a7-4e4d-a6df-e05833b6052a",
                "started_datetime": None,
                "ended_datetime": None,
                "accumulated_labor_time_milliseconds": "PT0S",
                "phase": "annotation",
                "phase_stage": 1,
                "account_id": self.ACCOUNT_ID,
            },
        ]
        actual = get_task_history_index_skipped_inspection(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])


class TestMyBackoff:
    @my_backoff
    def requestexception_connectionerror_then_true(self, log):
        if len(log) == 2:
            return True

        if len(log) == 0:
            e = requests.exceptions.RequestException()
        elif len(log) == 1:
            e = ConnectionError()
        log.append(e)
        raise e

    def test_assert_retry(self):
        log = []
        assert self.requestexception_connectionerror_then_true(log) is True
        assert 2 == len(log)
        print(log)
        assert type(log[0]) == requests.exceptions.RequestException
        assert type(log[1]) == ConnectionError

    @my_backoff
    def chunkedencodingerror_requestsconnectionerror_then_true(self, log):
        if len(log) == 2:
            return True
        if len(log) == 0:
            e = requests.exceptions.ChunkedEncodingError()
            log.append(e)
            raise e
        elif len(log) == 1:
            e = requests.exceptions.ConnectionError()
            log.append(e)
            raise e

    def test_assert_retry2(self):
        log = []
        assert self.chunkedencodingerror_requestsconnectionerror_then_true(log) is True
        assert 2 == len(log)
        print(log)
        assert type(log[0]) == requests.exceptions.ChunkedEncodingError
        assert type(log[1]) == requests.exceptions.ConnectionError

    @my_backoff
    def httperror_then_true(self, log):
        if len(log) == 2:
            return True
        response = requests.Response()
        if len(log) == 0:
            response.status_code = 429
            e = requests.exceptions.HTTPError(response=response)
        elif len(log) == 1:
            response.status_code = 500
            e = requests.exceptions.HTTPError(response=response)
        log.append(e)
        raise e

    def test_assert_retry_with_httperror(self):
        log = []
        assert self.httperror_then_true(log) is True
        assert 2 == len(log)
        print(log)
        assert type(log[0]) == requests.exceptions.HTTPError
        assert log[0].response.status_code == 429
        assert type(log[1]) == requests.exceptions.HTTPError
        assert log[1].response.status_code == 500

    @my_backoff
    def httperror_with_400(self, log):
        if len(log) == 1:
            return True
        response = requests.Response()
        if len(log) == 0:
            response.status_code = 400
            e = requests.exceptions.HTTPError(response=response)
        log.append(e)
        raise e

    def test_assert_not_retry(self):
        log = []
        with pytest.raises(requests.exceptions.HTTPError):
            self.httperror_with_400(log)
        assert 1 == len(log)


class Test__create_request_body_for_logger:
    def test_data_dict(self):
        actual = _create_request_body_for_logger({"foo": "1", "password": "x", "new_password": "y", "old_password": "z"})
        assert actual == {"foo": "1", "password": "***", "new_password": "***", "old_password": "***"}

    def test_data_dict2(self):
        actual = _create_request_body_for_logger({"foo": "1"})
        assert actual == {"foo": "1"}

    def test_data_list(self):
        actual = _create_request_body_for_logger([{"foo": "1"}])
        assert actual == [{"foo": "1"}]
