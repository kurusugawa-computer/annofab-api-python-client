import pytest

from annofabapi.util.annotation_specs import (
    AnnotationSpecsAccessor,
    AttributeChoice,
    LabelNameHolder,
    Lang,
    NameHolder,
    get_attribute_name_en,
    get_choice,
    get_choice_name_en,
    get_english_message,
    get_label_name_en,
    get_message_with_lang,
)


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
        assert get_message_with_lang(i18n_message, Lang.JA_JP) == "自動車"  # type: ignore[arg-type]
        assert get_message_with_lang(i18n_message, "en-US") == "car"  # type: ignore[arg-type]
        assert get_message_with_lang(i18n_message, Lang.VI_VN) is None  # type: ignore[arg-type]


class Test__get_label_name_en:
    def test__get_label_name_en(self):
        label: LabelNameHolder = {
            "label_name": {"messages": [{"lang": "ja-JP", "message": "自動車"}, {"lang": "en-US", "message": "Car"}]},
        }

        assert get_label_name_en(label) == "Car"

    def test__get_label_name_en__英語メッセージが存在しない場合はValueErrorをスローする(self):
        label: LabelNameHolder = {
            "label_name": {"messages": [{"lang": "ja-JP", "message": "自動車"}]},
        }

        with pytest.raises(ValueError):
            get_label_name_en(label)


class Test__get_attribute_name_en:
    def test__get_attribute_name_en(self):
        attribute: NameHolder = {
            "name": {"messages": [{"lang": "ja-JP", "message": "色"}, {"lang": "en-US", "message": "Color"}]},
        }

        assert get_attribute_name_en(attribute) == "Color"

    def test__get_attribute_name_en__英語メッセージが存在しない場合はValueErrorをスローする(self):
        attribute: NameHolder = {
            "name": {"messages": [{"lang": "ja-JP", "message": "色"}]},
        }

        with pytest.raises(ValueError):
            get_attribute_name_en(attribute)


class Test__get_choice_name_en:
    def test__get_choice_name_en(self):
        choice: NameHolder = {
            "name": {"messages": [{"lang": "ja-JP", "message": "赤"}, {"lang": "en-US", "message": "Red"}]},
        }

        assert get_choice_name_en(choice) == "Red"

    def test__get_choice_name_en__英語メッセージが存在しない場合はValueErrorをスローする(self):
        choice: NameHolder = {
            "name": {"messages": [{"lang": "ja-JP", "message": "赤"}]},
        }

        with pytest.raises(ValueError):
            get_choice_name_en(choice)


class Test__AnnotationSpecsAccessor:
    def setup_method(self):
        self.annotation_specs = {
            "labels": [
                {"label_id": "1", "label_name": {"messages": [{"lang": "en-US", "message": "Car"}]}, "additional_data_definitions": ["1", "2"]},
                {"label_id": "2", "label_name": {"messages": [{"lang": "en-US", "message": "Bike"}]}, "additional_data_definitions": []},
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
        assert get_label_name_en(label) == "Car"

    def test_get_label_by_name(self):
        label = self.accessor.get_label(label_name="Bike")
        assert label["label_id"] == "2"
        assert get_label_name_en(label) == "Bike"

    def test_get_label_not_found(self):
        with pytest.raises(ValueError):
            self.accessor.get_label(label_id="3")

    def test_get_attribute_by_id(self):
        attribute = self.accessor.get_attribute(attribute_id="1")
        assert attribute["additional_data_definition_id"] == "1"
        assert get_attribute_name_en(attribute) == "Color"

    def test_get_attribute_by_name(self):
        attribute = self.accessor.get_attribute(attribute_name="Size")
        assert attribute["additional_data_definition_id"] == "2"
        assert get_attribute_name_en(attribute) == "Size"

    def test_get_attribute_not_found(self):
        with pytest.raises(ValueError):
            self.accessor.get_attribute(attribute_id="3")

    def test_get_attribute_by_id_and_label(self):
        label = self.accessor.get_label(label_id="1")
        attribute = self.accessor.get_attribute(attribute_id="1", label=label)
        assert attribute["additional_data_definition_id"] == "1"
        assert get_attribute_name_en(attribute) == "Color"

    def test_get_attribute_by_id_and_label__not_found(self):
        label = self.accessor.get_label(label_id="2")
        with pytest.raises(ValueError):
            self.accessor.get_attribute(attribute_id="1", label=label)


class Test__get_choice:
    def setup_method(self):
        self.choices: list[AttributeChoice] = [
            {"choice_id": "1", "name": {"messages": [{"lang": "en-US", "message": "Option1"}]}},
            {"choice_id": "2", "name": {"messages": [{"lang": "en-US", "message": "Option2"}]}},
        ]

    def test_get_choice_by_id(self):
        choice = get_choice(self.choices, choice_id="1")
        assert choice["choice_id"] == "1"
        assert get_choice_name_en(choice) == "Option1"

    def test_get_choice_by_name(self):
        choice = get_choice(self.choices, choice_name="Option2")
        assert choice["choice_id"] == "2"
        assert get_choice_name_en(choice) == "Option2"

    def test_get_choice_not_found(self):
        with pytest.raises(ValueError):
            get_choice(self.choices, choice_id="3")

    def test_get_choice_invalid_arguments(self):
        with pytest.raises(ValueError):
            get_choice(self.choices, choice_id="1", choice_name="Option1")

    def test_get_choice_no_arguments(self):
        with pytest.raises(ValueError):
            get_choice(self.choices)
