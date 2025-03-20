import json
from pathlib import Path

import pytest

from annofabapi.util.annotation_specs import AnnotationSpecsAccessor
from annofabapi.util.attribute_restrictions import Checkbox, IntegerTextBox, StringTextBox

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
        actual = StringTextBox(accessor, attribute_id="id1").matches("\\w").generate()
        assert actual == {"additional_data_definition_id": "id1", "condition": {"_type": "Matches", "value": "\\w"}}

    def test__not_matches(self):
        actual = StringTextBox(accessor, attribute_id="id1").not_matches("\\w").generate()
        assert actual == {"additional_data_definition_id": "id1", "condition": {"_type": "NotMatches", "value": "\\w"}}


class Test__IntegerTextBox:
    def test__equals(self):
        actual = IntegerTextBox(accessor, attribute_id="id1").equals(10).generate()
        assert actual == {"additional_data_definition_id": "id1", "condition": {"_type": "Equals", "value": "10"}}

    def test__not_matches(self):
        actual = IntegerTextBox(accessor, attribute_id="id1").not_equals(10).generate()
        assert actual == {"additional_data_definition_id": "id1", "condition": {"_type": "NotEquals", "value": "10"}}
