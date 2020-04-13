# timezonが異なる場所だとテストに失敗するので、コメントアウトする
# def test_to_iso8601_extension():
#     d = datetime.datetime(2019, 10, 8, 16, 20, 8, 241762)
#     tz_jst = datetime.timezone(datetime.timedelta(hours=9))
#     assert to_iso8601_extension(d, tz_jst) == "2019-10-08T16:20:08.241+09:00"

from annofabapi.models import TaskPhase
from annofabapi.utils import (get_number_of_rejections, get_task_history_index_skipped_acceptance,
                              get_task_history_index_skipped_inspection)


class TestTaskHistoryUtils:
    ACCOUNT_ID = "12345678-abcd-1234-abcd-1234abcd5678"

    def test_get_task_history_index_skipped_acceptance_検査0回_受入スキップ(self):
        task_history_list = [{
            "started_datetime": "2020-01-22T09:32:15.284+09:00",
            "ended_datetime": "2020-01-22T09:32:19.628+09:00",
            "accumulated_labor_time_milliseconds": "PT4.344S",
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "started_datetime": "2020-01-22T09:32:19.63+09:00",
            "ended_datetime": "2020-01-22T09:32:19.63+09:00",
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "acceptance",
            "phase_stage": 1,
            "account_id": None
        }]

        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = [1]
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_acceptance_検査0回_受入スキップ後に受入取消(self):
        task_history_list = [{
            "started_datetime": "2020-01-22T09:35:26.13+09:00",
            "ended_datetime": "2020-01-22T09:35:29.745+09:00",
            "accumulated_labor_time_milliseconds": "PT3.615S",
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": "00589ed0-dd63-40db-abb2-dfe5e13c8299"
        }, {
            "started_datetime": "2020-01-22T09:35:29.747+09:00",
            "ended_datetime": "2020-01-22T09:35:29.747+09:00",
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "acceptance",
            "phase_stage": 1,
            "account_id": None
        }, {
            "started_datetime": None,
            "ended_datetime": None,
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "acceptance",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }]

        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = [1]
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_acceptance_検査0回_教師付で提出取消(self):
        task_history_list = [{
            "started_datetime": "2020-01-22T09:36:11.187+09:00",
            "ended_datetime": "2020-01-22T09:36:14.186+09:00",
            "accumulated_labor_time_milliseconds": "PT2.999S",
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "started_datetime": "2020-01-22T09:36:23.86+09:00",
            "ended_datetime": "2020-01-22T09:36:23.86+09:00",
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "acceptance",
            "phase_stage": 1,
            "account_id": None
        }, {
            "started_datetime": None,
            "ended_datetime": None,
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }]
        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_acceptance_検査1回_検査で提出取消(self):
        task_history_list = [{
            "started_datetime": "2020-01-22T09:39:20.492+09:00",
            "ended_datetime": "2020-01-22T09:39:24.911+09:00",
            "accumulated_labor_time_milliseconds": "PT4.419S",
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "started_datetime": "2020-01-22T09:40:04.978+09:00",
            "ended_datetime": "2020-01-22T09:40:08.091+09:00",
            "accumulated_labor_time_milliseconds": "PT3.113S",
            "phase": "inspection",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "started_datetime": "2020-01-22T09:40:15.136+09:00",
            "ended_datetime": "2020-01-22T09:40:15.136+09:00",
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "acceptance",
            "phase_stage": 1,
            "account_id": None
        }, {
            "started_datetime": None,
            "ended_datetime": None,
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "inspection",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }]

        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_inspection_検査1回_検査スキップ(self):
        task_history_list = [{
            "started_datetime": "2020-01-22T09:58:20.063+09:00",
            "ended_datetime": "2020-01-22T09:58:23.749+09:00",
            "accumulated_labor_time_milliseconds": "PT3.686S",
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "started_datetime": "2020-01-22T09:58:23.751+09:00",
            "ended_datetime": "2020-01-22T09:58:23.751+09:00",
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "inspection",
            "phase_stage": 1,
            "account_id": None
        }, {
            "started_datetime": "2020-01-22T09:58:23.753+09:00",
            "ended_datetime": "2020-01-22T09:58:23.753+09:00",
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "acceptance",
            "phase_stage": 1,
            "account_id": None
        }]

        actual = get_task_history_index_skipped_inspection(task_history_list)
        expected = [1]
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_inspection_検査1回_教師付で提出取消(self):
        task_history_list = [{
            "started_datetime": "2020-01-22T10:00:33.832+09:00",
            "ended_datetime": "2020-01-22T10:00:37.381+09:00",
            "accumulated_labor_time_milliseconds": "PT3.549S",
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "started_datetime": "2020-01-22T10:00:45.953+09:00",
            "ended_datetime": "2020-01-22T10:00:45.953+09:00",
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "inspection",
            "phase_stage": 1,
            "account_id": None
        }, {
            "started_datetime": None,
            "ended_datetime": None,
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }]
        actual = get_task_history_index_skipped_inspection(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_inspection_検査1回_教師付で提出取消(self):
        task_history_list = [{
            "started_datetime": "2020-01-22T10:00:33.832+09:00",
            "ended_datetime": "2020-01-22T10:00:37.381+09:00",
            "accumulated_labor_time_milliseconds": "PT3.549S",
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "started_datetime": "2020-01-22T10:00:45.953+09:00",
            "ended_datetime": "2020-01-22T10:00:45.953+09:00",
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "inspection",
            "phase_stage": 1,
            "account_id": None
        }, {
            "started_datetime": None,
            "ended_datetime": None,
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }]
        actual = get_task_history_index_skipped_inspection(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_inspection_検査2回_検査1回目で提出取消(self):
        task_history_list = [{
            "started_datetime": "2019-09-04T16:15:51.505+09:00",
            "ended_datetime": "2019-09-04T16:16:31.597+09:00",
            "accumulated_labor_time_milliseconds": "PT40.092S",
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "started_datetime": "2020-01-22T10:06:18.435+09:00",
            "ended_datetime": "2020-01-22T10:06:21.919+09:00",
            "accumulated_labor_time_milliseconds": "PT3.484S",
            "phase": "inspection",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "started_datetime": "2020-01-22T10:07:38.456+09:00",
            "ended_datetime": "2020-01-22T10:07:38.456+09:00",
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "inspection",
            "phase_stage": 2,
            "account_id": None
        }, {
            "started_datetime": None,
            "ended_datetime": None,
            "accumulated_labor_time_milliseconds": "PT0S",
            "phase": "inspection",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }]
        actual = get_task_history_index_skipped_inspection(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_number_of_rejections_教師付1回目(self):
        task_history_short_list = [{
            "account_id": self.ACCOUNT_ID,
            "phase": "annotation",
            "phase_stage": 1,
            "worked": True
        }]

        actual = get_number_of_rejections(task_history_short_list, TaskPhase.ACCEPTANCE)
        assert actual == 0

    def test_get_number_of_rejections_受入で1回差戻(self):
        task_history_short_list = [
            {
                "account_id": self.ACCOUNT_ID,
                'phase': 'annotation',
                'phase_stage': 1,
                'worked': True
            },
            {
                "account_id": self.ACCOUNT_ID,
                'phase': 'acceptance',
                'phase_stage': 1,
                'worked': True
            },
            {
                "account_id": self.ACCOUNT_ID,
                'phase': 'annotation',
                'phase_stage': 1,
                'worked': True
            },
        ]

        actual = get_number_of_rejections(task_history_short_list, TaskPhase.ACCEPTANCE)
        assert actual == 1

    def test_get_number_of_rejections_検査で1回差戻(self):
        task_history_short_list = [
            {
                "account_id": self.ACCOUNT_ID,
                'phase': 'annotation',
                'phase_stage': 1,
                'worked': True
            },
            {
                "account_id": self.ACCOUNT_ID,
                'phase': 'inspection',
                'phase_stage': 1,
                'worked': True
            },
            {
                "account_id": self.ACCOUNT_ID,
                'phase': 'annotation',
                'phase_stage': 1,
                'worked': True
            },
        ]

        actual = get_number_of_rejections(task_history_short_list, TaskPhase.INSPECTION)
        assert actual == 1

    def test_get_number_of_rejections_検査と受入で1回差戻(self):
        task_history_short_list = [{
            "account_id": self.ACCOUNT_ID,
            "phase": "annotation",
            "phase_stage": 1,
            "worked": True
        }, {
            "account_id": self.ACCOUNT_ID,
            "phase": "inspection",
            "phase_stage": 1,
            "worked": True
        }, {
            "account_id": self.ACCOUNT_ID,
            "phase": "annotation",
            "phase_stage": 1,
            "worked": True
        }, {
            "account_id": self.ACCOUNT_ID,
            "phase": "inspection",
            "phase_stage": 1,
            "worked": True
        }, {
            "account_id": self.ACCOUNT_ID,
            "phase": "acceptance",
            "phase_stage": 1,
            "worked": True
        }, {
            "account_id": self.ACCOUNT_ID,
            "phase": "annotation",
            "phase_stage": 1,
            "worked": True
        }, {
            "account_id": "00589ed0-dd63-40db-abb2-dfe5e13c8299",
            "phase": "inspection",
            "phase_stage": 1,
            "worked": True
        }, {
            "account_id": self.ACCOUNT_ID,
            "phase": "acceptance",
            "phase_stage": 1,
            "worked": True
        }]
        actual_inspection = get_number_of_rejections(task_history_short_list, TaskPhase.INSPECTION)
        assert actual_inspection == 1
        actual_acceptance = get_number_of_rejections(task_history_short_list, TaskPhase.ACCEPTANCE)
        assert actual_acceptance == 1
