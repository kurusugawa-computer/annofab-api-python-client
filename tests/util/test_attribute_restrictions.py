import copy
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from annofabapi.pydantic_models.additional_data_definition_type import AdditionalDataDefinitionType
from annofabapi.util.annotation_specs import AnnotationSpecsAccessor, get_english_message
from annofabapi.util.attribute_restrictions import (
    AnnotationLink,
    AttributeFactory,
    AttributeRestrictionCatalogItem,
    Checkbox,
    IntegerTextbox,
    Restriction,
    RestrictionAst,
    RestrictionAstType,
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
        with pytest.raises(ValueError):
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

    def test__create(self):
        actual = self.factory.create(AdditionalDataDefinitionType.TEXT, attribute_name="note")

        assert isinstance(actual, StringTextbox)
        assert actual.attribute_id == "9b05648d-1e16-4ea2-ab79-48907f5eed00"


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

        actual = Restriction.from_dict(restriction_dict)

        assert actual.to_dict() == restriction_dict

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
            }
        )

        actual = restriction.to_ast(accessor.annotation_specs)

        assert actual == RestrictionAst(
            type=RestrictionAstType.IMPLY,
            premise=RestrictionAst(type=RestrictionAstType.CHECKED, attribute_name="occluded"),
            conclusion=RestrictionAst(type=RestrictionAstType.IS_NOT_EMPTY, attribute_name="note"),
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
            }
        )

        actual = restriction.to_human_readable(accessor.annotation_specs)

        assert actual == "If 'occluded' is checked, 'note' is not empty."

    def test__to_human_readable__右側にネストしたimplyは条件をまとめる(self):
        restriction = Restriction.from_dict(
            {
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
        )

        actual = restriction.to_human_readable(accessor.annotation_specs)

        assert actual == "If 'occluded' is checked and 'traffic_lane' is 2, 'note' is not empty."

    def test__from_dict__妥当性検証せずに復元する(self):
        restriction_dict = {
            "additional_data_definition_id": "d349e76d-b59a-44cd-94b4-713a00b2e84d",
            "condition": {"_type": "Matches", "value": "\\d+"},
        }

        actual = Restriction.from_dict(restriction_dict)

        assert actual.to_dict() == restriction_dict

    def test__to_ast__tracking_id属性にmatchesは指定できない(self):
        restriction_dict = {
            "additional_data_definition_id": "d349e76d-b59a-44cd-94b4-713a00b2e84d",
            "condition": {"_type": "Matches", "value": "\\d+"},
        }
        restriction = Restriction.from_dict(restriction_dict)

        with pytest.raises(ValueError):
            restriction.to_ast(accessor.annotation_specs)

    def test__to_ast__integer属性に整数以外の値は指定できない(self):
        restriction_dict = {
            "additional_data_definition_id": "ec27de5d-122c-40e7-89bc-5500e37bae6a",
            "condition": {"_type": "Equals", "value": "foo"},
        }
        restriction = Restriction.from_dict(restriction_dict)

        with pytest.raises(ValueError):
            restriction.to_ast(accessor.annotation_specs)

    def test__from_dict__can_input_true(self):
        restriction_dict = {
            "additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7",
            "condition": {"_type": "CanInput", "enable": True},
        }
        restriction = Restriction.from_dict(restriction_dict)

        assert restriction.to_dict() == restriction_dict
        assert restriction.to_ast(accessor.annotation_specs) == RestrictionAst(
            type=RestrictionAstType.CAN_INPUT,
            attribute_name="occluded",
            enable=True,
        )

    def test__from_ast(self):
        ast = RestrictionAst(
            type=RestrictionAstType.IMPLY,
            premise=RestrictionAst(type=RestrictionAstType.CHECKED, attribute_name="occluded"),
            conclusion=RestrictionAst(type=RestrictionAstType.HAS_CHOICE, attribute_name="car_kind", choice_name="general_car"),
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
    def test__model_dump(self):
        ast = RestrictionAst(
            type=RestrictionAstType.IMPLY,
            premise=RestrictionAst(type=RestrictionAstType.CHECKED, attribute_name="occluded"),
            conclusion=RestrictionAst(type=RestrictionAstType.IS_NOT_EMPTY, attribute_name="note"),
        )

        assert ast.model_dump(mode="python", exclude_none=True) == {
            "type": "imply",
            "premise": {"type": "checked", "attribute_name": "occluded"},
            "conclusion": {"type": "is_not_empty", "attribute_name": "note"},
        }

    def test__model_validate(self):
        actual = RestrictionAst.model_validate(
            {
                "type": "imply",
                "premise": {"type": "checked", "attribute_name": "occluded"},
                "conclusion": {"type": "has_choice", "attribute_name": "car_kind", "choice_name": "general_car"},
            }
        )

        assert actual == RestrictionAst(
            type=RestrictionAstType.IMPLY,
            premise=RestrictionAst(type=RestrictionAstType.CHECKED, attribute_name="occluded"),
            conclusion=RestrictionAst(type=RestrictionAstType.HAS_CHOICE, attribute_name="car_kind", choice_name="general_car"),
        )
        assert actual.type is RestrictionAstType.IMPLY

    def test__to_restriction(self):
        ast = RestrictionAst(type=RestrictionAstType.MATCHES_STRING, attribute_name="note", value="[abc]+")

        actual = ast.to_restriction(accessor.annotation_specs)

        assert actual.to_dict() == {
            "additional_data_definition_id": "9b05648d-1e16-4ea2-ab79-48907f5eed00",
            "condition": {"_type": "Matches", "value": "[abc]+"},
        }

    def test__to_restriction__trackingにはmatches_stringを指定できない(self):
        ast = RestrictionAst(type=RestrictionAstType.MATCHES_STRING, attribute_name="tracking", value="foo")

        with pytest.raises(ValueError):
            ast.to_restriction(accessor.annotation_specs)

    def test__to_human_readable(self):
        ast = RestrictionAst(type=RestrictionAstType.HAS_LABEL, attribute_name="link_car", label_names=["car", "number_plate"])

        actual = ast.to_human_readable()

        assert actual == "'link_car' has labels 'car', 'number_plate'"

    def test__invalid_fields(self):
        with pytest.raises(ValidationError):
            RestrictionAst(type=RestrictionAstType.EQUALS_STRING, attribute_name="note")

    def test__invalid_field_type(self):
        with pytest.raises(ValidationError):
            RestrictionAst(type=RestrictionAstType.EQUALS_STRING, attribute_name="note", value=1)

    def test__model_json_schema(self):
        actual = RestrictionAst.model_json_schema()
        properties = actual["$defs"]["RestrictionAst"]["properties"]

        assert properties["type"]["description"] == "ASTノードの種類です。"
        assert properties["attribute_name"]["description"] == "対象属性の名前です。"
        assert properties["premise"]["description"] == "`imply` ノードの前提です。"


class Test__get_attribute_restriction_catalog:
    def test__catalog(self):
        actual = get_attribute_restriction_catalog(accessor.annotation_specs)

        assert all(isinstance(item, AttributeRestrictionCatalogItem) for item in actual)
        assert isinstance(actual[0].allowed_ast_types[0], RestrictionAstType)
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

    def test__複数link属性でも同じラベル一覧を返す(self):
        annotation_specs = copy.deepcopy(accessor.annotation_specs)
        expected_label_names = [get_english_message(label["label_name"]) for label in annotation_specs["labels"]]
        link_attribute = next(attribute for attribute in annotation_specs["additionals"] if attribute["type"] == "link")
        copied_link_attribute = copy.deepcopy(link_attribute)
        copied_link_attribute["additional_data_definition_id"] = "dummy-link-id"
        copied_link_attribute["name"]["messages"][0]["message"] = "link_car_2"
        copied_link_attribute["name"]["messages"][1]["message"] = "リンク_車両2"
        copied_link_attribute["name"]["messages"][2]["message"] = "link_car_2"
        annotation_specs["additionals"].append(copied_link_attribute)

        actual = get_attribute_restriction_catalog(annotation_specs)

        link_items = [item for item in actual if item.attribute_type == AdditionalDataDefinitionType.LINK]
        assert len(link_items) == 2
        assert link_items[0].label_names == expected_label_names
        assert link_items[1].label_names == expected_label_names

    def test__catalog_model_json_schema(self):
        actual = AttributeRestrictionCatalogItem.model_json_schema()

        assert (
            actual["properties"]["attribute_name"]["description"]
            == "アノテーション仕様に定義された属性名です。LLMはこの名前を使って属性を参照します。"
        )
        assert (
            actual["properties"]["allowed_ast_types"]["description"]
            == "この属性で利用できる意味ベースAST種別の一覧です。LLMはこの一覧に含まれないAST種別を使ってはいけません。"
        )
        assert (
            actual["properties"]["choice_names"]["description"] == "choice/select 属性で利用できる選択肢名の一覧です。それ以外の属性では null です。"
        )
