# timezonが異なる場所だとテストに失敗するので、コメントアウトする
# def test_to_iso8601_extension():
#     d = datetime.datetime(2019, 10, 8, 16, 20, 8, 241762)
#     tz_jst = datetime.timezone(datetime.timedelta(hours=9))
#     assert to_iso8601_extension(d, tz_jst) == "2019-10-08T16:20:08.241+09:00"

from annofabapi.utils import get_task_history_index_skipped_acceptance, get_task_history_index_skipped_inspection


class TestTaskHistoryUtils:
    ACCOUNT_ID = "12345678-abcd-1234-abcd-1234abcd5678"

    def test_get_task_history_index_skipped_acceptance(self):
        task_history_list = [{
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "phase": "acceptance",
            "phase_stage": 1,
            "account_id": None
        }]

        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = [1]
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_acceptance_提出取消は対象外(self):
        task_history_list = [{
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "phase": "acceptance",
            "phase_stage": 1,
            "account_id": None
        }, {
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }]
        actual = get_task_history_index_skipped_acceptance(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_inspection(self):
        task_history_list = [{
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "phase": "inspection",
            "phase_stage": 1,
            "account_id": None
        }, {
            "phase": "acceptance",
            "phase_stage": 1,
            "account_id": None
        }]

        actual = get_task_history_index_skipped_inspection(task_history_list)
        expected = [1]
        assert all([a == b for a, b in zip(actual, expected)])

    def test_get_task_history_index_skipped_inspection_提出取消は対象外(self):
        task_history_list = [{
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }, {
            "phase": "inspection",
            "phase_stage": 1,
            "account_id": None
        }, {
            "phase": "annotation",
            "phase_stage": 1,
            "account_id": self.ACCOUNT_ID
        }]
        actual = get_task_history_index_skipped_inspection(task_history_list)
        expected = []
        assert all([a == b for a, b in zip(actual, expected)])
