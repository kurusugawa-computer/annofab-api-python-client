import json
from pathlib import Path

import pytest

from annofabapi.util.annotation_specs import AnnotationSpecsAccessor
from annofabapi.util.attribute_restrictions import (
    AnnotationLink,
    AttributeRestrictionCatalogItem,
    AttributeFactory,
    Checkbox,
    IntegerTextbox,
    Restriction,
    RestrictionAst,
    Selection,
    StringTextbox,
    TrackingId,
    get_attribute_restriction_catalog,
)

accessor = AnnotationSpecsAccessor(annotation_specs=json.loads(Path("tests/data/util/attribute_restrictions/annotation_specs.json").read_text()))


class Test__Checkbox:
    def test__checked(self):
        actual = Checkbox(accessor, attribute_id="2517f635-2269-4142-8ef4-16312b4cc9f7").checked().to_dict()
        assert actual == {"additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7", "condition": {"_type": "Equals", "value": "true"}}

    def test__unchecked(self):
        actual = Checkbox(accessor, attribute_name="occluded").unchecked().to_dict()
        assert actual == {
            "additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7",
            "condition": {"_type": "NotEquals", "value": "true"},
        }

    def test__is_valid_attribute_type(self):
        with pytest.raises(ValueError, match="属性の種類が'tracking'である属性は、クラス'Checkbox'では扱えません。"):
            Checkbox(accessor, attribute_id="d349e76d-b59a-44cd-94b4-713a00b2e84d")


class Test__StringTextBox:
    def test__matches(self):
        actual = StringTextbox(accessor, attribute_name="note").matches("\\w").to_dict()
        assert actual == {"additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00", "condition": {"_type": "Matches", "value": "\\w"}}

    def test__not_matches(self):
        actual = StringTextbox(accessor, attribute_name="note").not_matches("\\w").to_dict()
        assert actual == {
            "additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00",
            "condition": {"_type": "NotMatches", "value": "\\w"},
        }

    def test__equals(self):
        actual = StringTextbox(accessor, attribute_name="note").equals("foo").to_dict()
        assert actual == {"additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00", "condition": {"_type": "Equals", "value": "foo"}}

    def test__not_equals(self):
        actual = StringTextbox(accessor, attribute_name="note").not_equals("foo").to_dict()
        assert actual == {
            "additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00",
            "condition": {"_type": "NotEquals", "value": "foo"},
        }

    def test__is_empty(self):
        actual = StringTextbox(accessor, attribute_name="note").is_empty().to_dict()
        assert actual == {"additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00", "condition": {"_type": "Equals", "value": ""}}

    def test__is_not_empty(self):
        actual = StringTextbox(accessor, attribute_name="note").is_not_empty().to_dict()
        assert actual == {"additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00", "condition": {"_type": "NotEquals", "value": ""}}


class Test__IntegerTextBox:
    def test__equals(self):
        actual = IntegerTextbox(accessor, attribute_name="traffic_lane").equals(10).to_dict()
        assert actual == {"additional_data_definition_id": "ec27de5d-122c-40e7-89bc-5500e37bae6a", "condition": {"_type": "Equals", "value": "10"}}

    def test__not_equals(self):
        actual = IntegerTextbox(accessor, attribute_name="traffic_lane").not_equals(10).to_dict()
        assert actual == {"additional_data_definition_id": "ec27de5d-122c-40e7-89bc-5500e37bae6a", "condition": {"_type": "NotEquals", "value": "10"}}


class Test__AnnotationLink:
    def test__has_label(self):
        actual = AnnotationLink(accessor, attribute_name="link_car").has_label(label_names=["car"]).to_dict()
        assert actual == {
            "additional_data_definition_id": "15ba8b9d-4882-40c2-bb31-ed3f68197c2e",
            "condition": {"_type": "HasLabel", "labels": ["9d6cca8d-3f5a-4808-a6c9-0ae18a478176"]},
        }

        actual = AnnotationLink(accessor, attribute_name="link_car").has_label(label_ids=["9d6cca8d-3f5a-4808-a6c9-0ae18a478176"]).to_dict()
        assert actual == {
            "additional_data_definition_id": "15ba8b9d-4882-40c2-bb31-ed3f68197c2e",
            "condition": {"_type": "HasLabel", "labels": ["9d6cca8d-3f5a-4808-a6c9-0ae18a478176"]},
        }


class Test__TrackingId:
    def test__equals(self):
        actual = TrackingId(accessor, attribute_name="tracking").equals("foo").to_dict()
        assert actual == {"additional_data_definition_id": "d349e76d-b59a-44cd-94b4-713a00b2e84d", "condition": {"_type": "Equals", "value": "foo"}}

    def test__not_equals(self):
        actual = TrackingId(accessor, attribute_name="tracking").not_equals("foo").to_dict()
        assert actual == {
            "additional_data_definition_id": "d349e76d-b59a-44cd-94b4-713a00b2e84d",
            "condition": {"_type": "NotEquals", "value": "foo"},
        }


class Test__Selection:
    def test__has_choice(self):
        actual = Selection(accessor, attribute_name="car_kind").has_choice(choice_name="general_car").to_dict()
        assert actual == {
            "additional_data_definition_id": "cbb0155f-1631-48e1-8fc3-43c5f254b6f2",
            "condition": {"_type": "Equals", "value": "7512ee39-8073-4e24-9b8c-93d99b76b7d2"},
        }

    def test__not_has_choice(self):
        actual = Selection(accessor, attribute_name="car_kind").not_has_choice(choice_id="7512ee39-8073-4e24-9b8c-93d99b76b7d2").to_dict()
        assert actual == {
            "additional_data_definition_id": "cbb0155f-1631-48e1-8fc3-43c5f254b6f2",
            "condition": {"_type": "NotEquals", "value": "7512ee39-8073-4e24-9b8c-93d99b76b7d2"},
        }


class Test__imply:
    def test__occludedチェックボックスがONならばnoteテキストボックスは空ではない(self):
        condition = Checkbox(accessor, attribute_name="occluded").checked().imply(StringTextbox(accessor, attribute_name="note").is_not_empty())
        actual = condition.to_dict()
        assert actual == {
            "additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00",
            "condition": {
                "_type": "Imply",
                "premise": {
                    "additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7",
                    "condition": {"_type": "Equals", "value": "true"},
                },
                "condition": {"_type": "NotEquals", "value": ""},
            },
        }

    def test__occludedチェックボックスがONかつtraffic_laneが2ならばnoteテキストボックスは空ではない(self):
        condition = (
            Checkbox(accessor, attribute_name="occluded")
            .checked()
            .imply(
                IntegerTextbox(accessor, attribute_name="traffic_lane").equals(2).imply(StringTextbox(accessor, attribute_name="note").is_not_empty())
            )
        )
        actual = condition.to_dict()
        assert actual == {
            "additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00",
            "condition": {
                "_type": "Imply",
                "premise": {
                    "additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7",
                    "condition": {"_type": "Equals", "value": "true"},
                },
                "condition": {
                    "_type": "Imply",
                    "premise": {
                        "additional_data_definition_id": "ec27de5d-122c-40e7-89bc-5500e37bae6a",
                        "condition": {"_type": "Equals", "value": "2"},
                    },
                    "condition": {"_type": "NotEquals", "value": ""},
                },
            },
        }

    def test__implyメソッドの戻りに対してimplyメソッドを実行するとNotImplementedErrorが発生する(self):
        with pytest.raises(NotImplementedError):
            Checkbox(accessor, attribute_name="occluded").checked().imply(IntegerTextbox(accessor, attribute_name="traffic_lane").equals(2)).imply(
                StringTextbox(accessor, attribute_name="note").is_not_empty()
            )


class Test__AttributeFactory:
    def setup_method(self):
        self.annotation_specs = json.loads(Path("tests/data/util/attribute_restrictions/annotation_specs.json").read_text())
        self.factory = AttributeFactory(self.annotation_specs)

    def test__checkbox(self):
        checkbox = self.factory.checkbox(attribute_name="occluded")
        assert isinstance(checkbox, Checkbox)
        assert checkbox.attribute_id == "2517f635-2269-4142-8ef4-16312b4cc9f7"

    def test__string_textbox(self):
        string_textbox = self.factory.string_textbox(attribute_name="note")
        assert isinstance(string_textbox, StringTextbox)
        assert string_textbox.attribute_id == "9b05648d-1e16-4ea2-ab79-48907f5eed00"

    def test__integer_textbox(self):
        integer_textbox = self.factory.integer_textbox(attribute_name="traffic_lane")
        assert isinstance(integer_textbox, IntegerTextbox)
        assert integer_textbox.attribute_id == "ec27de5d-122c-40e7-89bc-5500e37bae6a"

    def test__annotation_link(self):
        annotation_link = self.factory.annotation_link(attribute_name="link_car")
        assert isinstance(annotation_link, AnnotationLink)
        assert annotation_link.attribute_id == "15ba8b9d-4882-40c2-bb31-ed3f68197c2e"

    def test__tracking_id(self):
        tracking_id = self.factory.tracking_id(attribute_name="tracking")
        assert isinstance(tracking_id, TrackingId)
        assert tracking_id.attribute_id == "d349e76d-b59a-44cd-94b4-713a00b2e84d"

    def test__selection(self):
        selection = self.factory.selection(attribute_name="car_kind")
        assert isinstance(selection, Selection)
        assert selection.attribute_id == "cbb0155f-1631-48e1-8fc3-43c5f254b6f2"


class Test__Restriction:
    def test__from_dict(self):
        restriction_dict = {
            "additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00",
            "condition": {
                "_type": "Imply",
                "premise": {
                    "additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7",
                    "condition": {"_type": "Equals", "value": "true"},
                },
                "condition": {"_type": "NotEquals", "value": ""},
            },
        }

        actual = Restriction.from_dict(restriction_dict, annotation_specs=accessor.annotation_specs)

        assert actual.to_dict() == restriction_dict

    def test__to_python_expr(self):
        restriction_dict = {
            "additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00",
            "condition": {
                "_type": "Imply",
                "premise": {
                    "additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7",
                    "condition": {"_type": "Equals", "value": "true"},
                },
                "condition": {"_type": "NotEquals", "value": ""},
            },
        }
        restriction = Restriction.from_dict(restriction_dict, annotation_specs=accessor.annotation_specs)

        actual = restriction.to_python_expr(accessor.annotation_specs)

        assert actual == "fac.checkbox(attribute_name='occluded').checked().imply(fac.string_textbox(attribute_name='note').is_not_empty())"

    def test__to_python_expr__selection(self):
        restriction = Restriction.from_dict(
            {
                "additional_data_definition_id": "cbb0155f-1631-48e1-8fc3-43c5f254b6f2",
                "condition": {"_type": "NotEquals", "value": "7512ee39-8073-4e24-9b8c-93d99b76b7d2"},
            },
            annotation_specs=accessor.annotation_specs,
        )

        actual = restriction.to_python_expr(accessor.annotation_specs)

        assert actual == "fac.selection(attribute_name='car_kind').not_has_choice(choice_name='general_car')"

    def test__to_ast(self):
        restriction = Restriction.from_dict(
            {
                "additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00",
                "condition": {
                    "_type": "Imply",
                    "premise": {
                        "additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7",
                        "condition": {"_type": "Equals", "value": "true"},
                    },
                    "condition": {"_type": "NotEquals", "value": ""},
                },
            },
            annotation_specs=accessor.annotation_specs,
        )

        actual = restriction.to_ast(accessor.annotation_specs)

        assert actual == RestrictionAst(
            type="imply",
            premise=RestrictionAst(type="checked", attribute_name="occluded"),
            conclusion=RestrictionAst(type="is_not_empty", attribute_name="note"),
        )

    def test__to_human_readable(self):
        restriction = Restriction.from_dict(
            {
                "additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00",
                "condition": {
                    "_type": "Imply",
                    "premise": {
                        "additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7",
                        "condition": {"_type": "Equals", "value": "true"},
                    },
                    "condition": {"_type": "NotEquals", "value": ""},
                },
            },
            annotation_specs=accessor.annotation_specs,
        )

        actual = restriction.to_human_readable(accessor.annotation_specs)

        assert actual == "'note' DOES NOT EQUAL '' IF 'occluded' EQUALS 'true'"

    def test__from_dict__annotation_specsを指定しない場合は妥当性検証しない(self):
        restriction_dict = {
            "additional_data_definition_id": "d349e76d-b59a-44cd-94b4-713a00b2e84d",
            "condition": {"_type": "Matches", "value": "\\d+"},
        }

        actual = Restriction.from_dict(restriction_dict)

        assert actual.to_dict() == restriction_dict

    def test__from_dict__tracking_id属性にmatchesは指定できない(self):
        restriction_dict = {
            "additional_data_definition_id": "d349e76d-b59a-44cd-94b4-713a00b2e84d",
            "condition": {"_type": "Matches", "value": "\\d+"},
        }

        with pytest.raises(ValueError, match="属性'tracking'\\(type='tracking'\\)では制約'Matches'を利用できません。"):
            Restriction.from_dict(restriction_dict, annotation_specs=accessor.annotation_specs)

    def test__from_dict__integer属性に整数以外の値は指定できない(self):
        restriction_dict = {
            "additional_data_definition_id": "ec27de5d-122c-40e7-89bc-5500e37bae6a",
            "condition": {"_type": "Equals", "value": "foo"},
        }

        with pytest.raises(ValueError, match="整数属性には整数値を指定してください。"):
            Restriction.from_dict(restriction_dict, annotation_specs=accessor.annotation_specs)

    def test__from_dict__can_input_true(self):
        restriction_dict = {
            "additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7",
            "condition": {"_type": "CanInput", "enable": True},
        }
        restriction = Restriction.from_dict(restriction_dict, annotation_specs=accessor.annotation_specs)

        assert restriction.to_dict() == restriction_dict
        assert restriction.to_python_expr(accessor.annotation_specs) == "fac.checkbox(attribute_name='occluded').enabled()"

    def test__from_ast(self):
        ast = RestrictionAst(
            type="imply",
            premise=RestrictionAst(type="checked", attribute_name="occluded"),
            conclusion=RestrictionAst(type="has_choice", attribute_name="car_kind", choice_name="general_car"),
        )

        actual = Restriction.from_ast(ast, accessor.annotation_specs)

        assert actual.to_dict() == {
            "additional_data_definition_id": "cbb0155f-1631-48e1-8fc3-43c5f254b6f2",
            "condition": {
                "_type": "Imply",
                "premise": {
                    "additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7",
                    "condition": {"_type": "Equals", "value": "true"},
                },
                "condition": {"_type": "Equals", "value": "7512ee39-8073-4e24-9b8c-93d99b76b7d2"},
            },
        }


class Test__RestrictionAst:
    def test__to_dict(self):
        ast = RestrictionAst(
            type="imply",
            premise=RestrictionAst(type="checked", attribute_name="occluded"),
            conclusion=RestrictionAst(type="is_not_empty", attribute_name="note"),
        )

        assert ast.to_dict() == {
            "type": "imply",
            "premise": {"type": "checked", "attribute_name": "occluded"},
            "conclusion": {"type": "is_not_empty", "attribute_name": "note"},
        }

    def test__from_dict(self):
        actual = RestrictionAst.from_dict(
            {
                "type": "imply",
                "premise": {"type": "checked", "attribute_name": "occluded"},
                "conclusion": {"type": "has_choice", "attribute_name": "car_kind", "choice_name": "general_car"},
            }
        )

        assert actual == RestrictionAst(
            type="imply",
            premise=RestrictionAst(type="checked", attribute_name="occluded"),
            conclusion=RestrictionAst(type="has_choice", attribute_name="car_kind", choice_name="general_car"),
        )

    def test__to_restriction(self):
        ast = RestrictionAst(type="matches_string", attribute_name="note", value="[abc]+")

        actual = ast.to_restriction(accessor.annotation_specs)

        assert actual.to_dict() == {
            "additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00",
            "condition": {"_type": "Matches", "value": "[abc]+"},
        }

    def test__to_restriction__trackingにはmatches_stringを指定できない(self):
        ast = RestrictionAst(type="matches_string", attribute_name="tracking", value="foo")

        with pytest.raises(ValueError, match="属性'tracking'\\(type='tracking'\\)ではAST種別'matches_string'を利用できません。"):
            ast.to_restriction(accessor.annotation_specs)

    def test__to_human_readable(self):
        ast = RestrictionAst(type="has_label", attribute_name="link_car", label_names=["car", "number_plate"])

        actual = ast.to_human_readable()

        assert actual == "'link_car' HAS LABEL 'car', 'number_plate'"

    def test__invalid_fields(self):
        with pytest.raises(ValueError, match="required=.*attribute_name.*value"):
            RestrictionAst(type="equals_string", attribute_name="note")


class Test__get_attribute_restriction_catalog:
    def test__catalog(self):
        actual = get_attribute_restriction_catalog(accessor.annotation_specs)

        assert all(isinstance(item, AttributeRestrictionCatalogItem) for item in actual)
        assert {
            "attribute_name": "tracking",
            "attribute_type": "tracking",
            "allowed_ast_types": ["can_input", "is_empty", "is_not_empty", "equals_string", "not_equals_string"],
            "choice_names": None,
            "label_names": None,
        } in [item.model_dump() for item in actual]
        assert {
            "attribute_name": "car_kind",
            "attribute_type": "choice",
            "allowed_ast_types": ["can_input", "is_empty", "is_not_empty", "has_choice", "not_has_choice"],
            "choice_names": ["general_car", "emergency_vehicle", "construction_vehicle"],
            "label_names": None,
        } in [item.model_dump() for item in actual]

    def test__catalog_model_json_schema(self):
        actual = AttributeRestrictionCatalogItem.model_json_schema()

        assert actual["properties"]["attribute_name"]["description"] == "Attribute name in annotation specs. LLM should refer to attributes by this name."
        assert (
            actual["properties"]["allowed_ast_types"]["description"]
            == "Semantic AST node types that are allowed for this attribute. LLM must not use AST types outside this list."
        )
        assert actual["properties"]["choice_names"]["description"] == "Available choice names for choice/select attributes. Null for non-choice attributes."
