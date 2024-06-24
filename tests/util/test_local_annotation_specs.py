import configparser
from pathlib import Path

import pytest

from annofabapi.util.annotation_specs import Lang, get_english_message, get_message_with_lang

inifile = configparser.ConfigParser()
inifile.read("./pytest.ini", "UTF-8")

test_dir = Path("./tests/data")


class Test__get_english_message:
    def test__get_english_message(self):
        i18n_message = {
            "messages": [{"lang": "ja-JP", "message": "自動車"}, {"lang": "en-US", "message": "car"}],
            "default_lang": "ja-JP",
        }
        assert get_english_message(i18n_message) == "car"

    def test__get_english_message__英語メッセージが存在しない場合はValueErrorをスローする(self):
        i18n_message = {
            "messages": [{"lang": "ja-JP", "message": "自動車"}],
            "default_lang": "ja-JP",
        }
        with pytest.raises(ValueError):
            get_english_message(i18n_message)


class Test__get_message_with_lang:
    def test__get_message_with_lang(self):
        i18n_message = {
            "messages": [{"lang": "ja-JP", "message": "自動車"}, {"lang": "en-US", "message": "car"}],
            "default_lang": "ja-JP",
        }
        assert get_message_with_lang(i18n_message, Lang.JA_JP) == "自動車"
        assert get_message_with_lang(i18n_message, "en-US") == "car"
        assert get_message_with_lang(i18n_message, Lang.VI_VN) is None
