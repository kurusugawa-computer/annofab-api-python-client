import configparser
from pathlib import Path

import pytest

from annofabapi.util.annotation_specs import AnnotationSpecsAccessor, Lang, get_choice, get_english_message, get_message_with_lang

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


class Test__AnnotationSpecsAccessor:
    def setup_method(self):
        self.annotation_specs = {
            "labels": [
                {"label_id": "1", "label_name": {"messages": [{"lang": "en-US", "message": "Car"}]}},
                {"label_id": "2", "label_name": {"messages": [{"lang": "en-US", "message": "Bike"}]}},
            ],
            "additionals": [
                {"additional_data_definition_id": "1", "name": {"messages": [{"lang": "en-US", "message": "Color"}]}},
                {"additional_data_definition_id": "2", "name": {"messages": [{"lang": "en-US", "message": "Size"}]}},
            ],
        }
        self.accessor = AnnotationSpecsAccessor(self.annotation_specs)

    def test_get_label_by_id(self):
        label = self.accessor.get_label(label_id="1")
        assert label["label_id"] == "1"
        assert get_english_message(label["label_name"]) == "Car"

    def test_get_label_by_name(self):
        label = self.accessor.get_label(label_name="Bike")
        assert label["label_id"] == "2"
        assert get_english_message(label["label_name"]) == "Bike"

    def test_get_label_not_found(self):
        with pytest.raises(ValueError):
            self.accessor.get_label(label_id="3")

    def test_get_attribute_by_id(self):
        attribute = self.accessor.get_attribute(attribute_id="1")
        assert attribute["additional_data_definition_id"] == "1"
        assert get_english_message(attribute["name"]) == "Color"

    def test_get_attribute_by_name(self):
        attribute = self.accessor.get_attribute(attribute_name="Size")
        assert attribute["additional_data_definition_id"] == "2"
        assert get_english_message(attribute["name"]) == "Size"

    def test_get_attribute_not_found(self):
        with pytest.raises(ValueError):
            self.accessor.get_attribute(attribute_id="3")


class Test__get_choice:
    def setup_method(self):
        self.choices = [
            {"choice_id": "1", "name": {"messages": [{"lang": "en-US", "message": "Option1"}]}},
            {"choice_id": "2", "name": {"messages": [{"lang": "en-US", "message": "Option2"}]}},
        ]

    def test_get_choice_by_id(self):
        choice = get_choice(self.choices, choice_id="1")
        assert choice["choice_id"] == "1"
        assert get_english_message(choice["name"]) == "Option1"

    def test_get_choice_by_name(self):
        choice = get_choice(self.choices, choice_name="Option2")
        assert choice["choice_id"] == "2"
        assert get_english_message(choice["name"]) == "Option2"

    def test_get_choice_not_found(self):
        with pytest.raises(ValueError):
            get_choice(self.choices, choice_id="3")

    def test_get_choice_invalid_arguments(self):
        with pytest.raises(ValueError):
            get_choice(self.choices, choice_id="1", choice_name="Option1")

    def test_get_choice_no_arguments(self):
        with pytest.raises(ValueError):
            get_choice(self.choices)
