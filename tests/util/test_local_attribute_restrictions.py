import configparser
from pathlib import Path

import pytest

from annofabapi.util.attribute_restrictions import Checkbox, StringTextBox, IntegerTextBox


class Test__Checkbox:
    def test__checked(self):
        actual = Checkbox("id1").checked().generate()
        assert actual == {"additional_data_definition_id": "id1", "condition": {"_type": "Equals", "value": "true"}}

    def test__unchecked(self):
        actual = Checkbox("id1").unchecked().generate()
        assert actual == {"additional_data_definition_id": "id1", "condition": {"_type": "NotEquals", "value": "true"}}

    def test__unchecked(self):
        actual = Checkbox("id1").unchecked().generate()
        assert actual == {"additional_data_definition_id": "id1", "condition": {"_type": "NotEquals", "value": "true"}}


class Test__StringTextBox:
    def test__matches(self):
        actual = StringTextBox("id1").matches("\\w").generate()
        assert actual == {"additional_data_definition_id": "id1", "condition": {"_type": "Matches", "value": "\\w"}}

    def test__not_matches(self):
        actual = StringTextBox("id1").not_matches("\\w").generate()
        assert actual == {"additional_data_definition_id": "id1", "condition": {"_type": "NotMatches", "value": "\\w"}}


class Test__IntegerTextBox:
    def test__equals(self):
        actual = IntegerTextBox("id1").equals(10).generate()
        assert actual == {"additional_data_definition_id": "id1", "condition": {"_type": "Equals", "value": "10"}}

    def test__not_matches(self):
        actual = IntegerTextBox("id1").not_equals(10).generate()
        assert actual == {"additional_data_definition_id": "id1", "condition": {"_type": "NotEquals", "value": "10"}}

