import datetime

from annofabapi.utils import to_iso8601_extension


def test_to_iso8601_extension():
    d = datetime.datetime(2019, 10, 8, 16, 20, 8, 241762)
    assert to_iso8601_extension(d) == "2019-10-08T16:20:08.241+09:00"
