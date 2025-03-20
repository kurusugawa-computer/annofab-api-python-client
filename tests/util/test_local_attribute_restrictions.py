import json
from pathlib import Path

import pytest

from annofabapi.util.annotation_specs import AnnotationSpecsAccessor
from annofabapi.util.attribute_restrictions import AnnotationLink, Checkbox, IntegerTextBox, Selection, StringTextBox, TrackingId

accessor = AnnotationSpecsAccessor(annotation_specs=json.loads(Path("tests/data/util/attribute_restrictions/annotation_specs.json").read_text()))


class Test__Checkbox:
    def test__checked(self):
        actual = Checkbox(accessor, attribute_id="2517f635-2269-4142-8ef4-16312b4cc9f7").checked().generate()
        assert actual == {"additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7", "condition": {"_type": "Equals", "value": "true"}}

    def test__unchecked(self):
        actual = Checkbox(accessor, attribute_name="occluded").unchecked().generate()
        assert actual == {
            "additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7",
            "condition": {"_type": "NotEquals", "value": "true"},
        }

    def test__is_valid_attribute_type(self):
        with pytest.raises(ValueError, match="属性の種類が'tracking'である属性は、クラス'Checkbox'では扱えません。"):
            Checkbox(accessor, attribute_id="d349e76d-b59a-44cd-94b4-713a00b2e84d")


class Test__StringTextBox:
    def test__matches(self):
        actual = StringTextBox(accessor, attribute_name="note").matches("\\w").generate()
        assert actual == {"additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00", "condition": {"_type": "Matches", "value": "\\w"}}

    def test__not_matches(self):
        actual = StringTextBox(accessor, attribute_name="note").not_matches("\\w").generate()
        assert actual == {
            "additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00",
            "condition": {"_type": "NotMatches", "value": "\\w"},
        }

    def test__equals(self):
        actual = StringTextBox(accessor, attribute_name="note").equals("foo").generate()
        assert actual == {"additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00", "condition": {"_type": "Equals", "value": "foo"}}

    def test__not_equals(self):
        actual = StringTextBox(accessor, attribute_name="note").not_equals("foo").generate()
        assert actual == {
            "additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00",
            "condition": {"_type": "NotEquals", "value": "foo"},
        }

    def test__is_empty(self):
        actual = StringTextBox(accessor, attribute_name="note").is_empty().generate()
        assert actual == {"additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00", "condition": {"_type": "Equals", "value": ""}}

    def test__is_not_empty(self):
        actual = StringTextBox(accessor, attribute_name="note").is_not_empty().generate()
        assert actual == {"additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00", "condition": {"_type": "NotEquals", "value": ""}}


class Test__IntegerTextBox:
    def test__equals(self):
        actual = IntegerTextBox(accessor, attribute_name="traffic_lane").equals(10).generate()
        assert actual == {"additional_data_definition_id": "ec27de5d-122c-40e7-89bc-5500e37bae6a", "condition": {"_type": "Equals", "value": "10"}}

    def test__not_matches(self):
        actual = IntegerTextBox(accessor, attribute_name="traffic_lane").not_equals(10).generate()
        assert actual == {"additional_data_definition_id": "ec27de5d-122c-40e7-89bc-5500e37bae6a", "condition": {"_type": "NotEquals", "value": "10"}}


class Test__AnnotationLink:
    def test__has_label(self):
        actual = AnnotationLink(accessor, attribute_name="link_car").has_label(label_names=["car"]).generate()
        assert actual == {
            "additional_data_definition_id": "15ba8b9d-4882-40c2-bb31-ed3f68197c2e",
            "condition": {"_type": "HasLabel", "labels": ["9d6cca8d-3f5a-4808-a6c9-0ae18a478176"]},
        }

        actual = AnnotationLink(accessor, attribute_name="link_car").has_label(label_ids=["9d6cca8d-3f5a-4808-a6c9-0ae18a478176"]).generate()
        assert actual == {
            "additional_data_definition_id": "15ba8b9d-4882-40c2-bb31-ed3f68197c2e",
            "condition": {"_type": "HasLabel", "labels": ["9d6cca8d-3f5a-4808-a6c9-0ae18a478176"]},
        }


class Test__TrackingId:
    def test__equals(self):
        actual = TrackingId(accessor, attribute_name="tracking").equals("foo").generate()
        assert actual == {"additional_data_definition_id": "d349e76d-b59a-44cd-94b4-713a00b2e84d", "condition": {"_type": "Equals", "value": "foo"}}

    def test__not_equals(self):
        actual = TrackingId(accessor, attribute_name="tracking").not_equals("foo").generate()
        assert actual == {
            "additional_data_definition_id": "d349e76d-b59a-44cd-94b4-713a00b2e84d",
            "condition": {"_type": "NotEquals", "value": "foo"},
        }


class Test__Selection:
    def test__has_choice(self):
        actual = Selection(accessor, attribute_name="car_kind").has_choice(choice_name="general_car").generate()
        assert actual == {
            "additional_data_definition_id": "cbb0155f-1631-48e1-8fc3-43c5f254b6f2",
            "condition": {"_type": "Equals", "value": "7512ee39-8073-4e24-9b8c-93d99b76b7d2"},
        }

    def test__not_has_choice(self):
        actual = Selection(accessor, attribute_name="car_kind").not_has_choice(choice_id="7512ee39-8073-4e24-9b8c-93d99b76b7d2").generate()
        assert actual == {
            "additional_data_definition_id": "cbb0155f-1631-48e1-8fc3-43c5f254b6f2",
            "condition": {"_type": "NotEquals", "value": "7512ee39-8073-4e24-9b8c-93d99b76b7d2"},
        }
