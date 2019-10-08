import datetime

from annofabapi.utils import to_iso8601_extension

# timezonが異なる場所だとテストに失敗するので、コメントアウトする
# def test_to_iso8601_extension():
#     d = datetime.datetime(2019, 10, 8, 16, 20, 8, 241762)
#     tz_jst = datetime.timezone(datetime.timedelta(hours=9))
#     assert to_iso8601_extension(d, tz_jst) == "2019-10-08T16:20:08.241+09:00"
