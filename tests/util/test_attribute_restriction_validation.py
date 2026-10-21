import copy
import json
from pathlib import Path

import pytest

from annofabapi.parser import lazy_parse_simple_annotation_zip
from annofabapi.util.attribute_restriction_validation import AttributeRestrictionValidator
from annofabapi.util.attribute_restrictions import Restriction


def message(text):
    return {"messages": [{"lang": "en-US", "message": text}]}


def restriction(attribute_id="note", condition_type="NotEquals", **condition):
    return {"additional_data_definition_id": attribute_id, "condition": {"_type": condition_type, **condition}}


@pytest.fixture
def specs():
    attributes = [
        {"additional_data_definition_id": name, "name": message(name), "type": kind}
        for name, kind in [("note", "comment"), ("unclear", "flag"), ("count", "integer"), ("kind", "choice"), ("link", "link")]
    ]
    attributes[3]["choices"] = [{"choice_id": "choice-1", "name": message("car")}]
    return {
        "labels": [
            {
                "label_id": "object-id",
                "label_name": message("object"),
                "additional_data_definitions": [a["additional_data_definition_id"] for a in attributes],
            },
            {"label_id": "other-id", "label_name": message("other"), "additional_data_definitions": []},
        ],
        "additionals": attributes,
        "restrictions": [restriction(value="")],
    }


def detail(attributes=None, annotation_id="a1", label="object"):
    return {"annotation_id": annotation_id, "label": label, "attributes": attributes or {}}


def evaluate(specs, attributes=None, others=()):
    return AttributeRestrictionValidator(specs).validate_simple_annotation_details([detail(attributes), *others])


@pytest.mark.parametrize(
    "attributes, expected",
    [({}, "violated"), ({"note": None}, "violated"), ({"note": ""}, "violated"), ({"note": " "}, "satisfied"), ({"note": "abc"}, "satisfied")],
)
def test_required(specs, attributes, expected):
    result = evaluate(specs, attributes)[0]
    assert result.status == expected
    assert result.annotation_id == "a1"
    assert result.attribute_id == "note"
    assert result.restriction_index == 0
    assert result.message is None


@pytest.mark.parametrize(
    "attribute_id, value, expected_value, expected",
    [
        ("unclear", True, "true", "satisfied"),
        ("unclear", False, "true", "violated"),
        ("unclear", None, "false", "satisfied"),
        ("unclear", "false", "false", "undetermined"),
        ("count", 0, "0", "satisfied"),
        ("count", "12", "12", "satisfied"),
        ("count", None, "", "satisfied"),
        ("count", True, "1", "undetermined"),
        ("count", 1.5, "1", "undetermined"),
        ("kind", "car", "choice-1", "satisfied"),
        ("kind", "bus", "choice-1", "undetermined"),
        ("kind", None, "", "satisfied"),
        ("note", "abc", "abc", "satisfied"),
        ("note", 1, "1", "undetermined"),
    ],
)
def test_equals_and_not_equals(specs, attribute_id, value, expected_value, expected):
    specs["restrictions"] = [restriction(attribute_id, "Equals", value=expected_value)]
    assert evaluate(specs, {attribute_id: value})[0].status == expected
    specs["restrictions"][0]["condition"]["_type"] = "NotEquals"
    opposite = {"satisfied": "violated", "violated": "satisfied", "undetermined": "undetermined"}
    assert evaluate(specs, {attribute_id: value})[0].status == opposite[expected]


@pytest.mark.parametrize(
    "condition_type, pattern, value, expected",
    [
        ("Matches", "abc", "xabcx", "satisfied"),
        ("Matches", "^abc$", "xabcx", "violated"),
        ("NotMatches", "abc", "xabcx", "violated"),
        ("NotMatches", "abc", "xyz", "satisfied"),
        ("Matches", "^$", None, "satisfied"),
        ("Matches", "[", "x", "undetermined"),
    ],
)
def test_regex(specs, condition_type, pattern, value, expected):
    specs["restrictions"] = [restriction("note", condition_type, value=pattern)]
    assert evaluate(specs, {"note": value})[0].status == expected


def conditional(premise, conclusion):
    return {
        "additional_data_definition_id": conclusion["additional_data_definition_id"],
        "condition": {"_type": "Imply", "premise": premise, "condition": conclusion["condition"]},
    }


@pytest.mark.parametrize(
    "unclear, note, expected",
    [
        (True, "", "violated"),
        (True, "ok", "satisfied"),
        (False, "", "satisfied"),
        (None, "", "satisfied"),
        ("bad", "", "undetermined"),
        ("bad", "ok", "satisfied"),
    ],
)
def test_imply(specs, unclear, note, expected):
    specs["restrictions"] = [conditional(restriction("unclear", "Equals", value="true"), restriction(value=""))]
    assert evaluate(specs, {"unclear": unclear, "note": note})[0].status == expected


def test_nested_imply_is_one_result(specs):
    specs["restrictions"] = [
        conditional(restriction("unclear", "Equals", value="true"), conditional(restriction("count", "Equals", value="1"), restriction(value="")))
    ]
    results = evaluate(specs, {"unclear": True, "count": 1})
    assert len(results) == 1
    assert results[0].status == "violated"
    assert evaluate(specs, {"unclear": True, "count": 2})[0].status == "satisfied"


@pytest.mark.parametrize(
    "value, labels, target_label, expected",
    [
        ("a2", ["object-id"], "object", "satisfied"),
        ("a2", ["object-id"], "other", "violated"),
        ("a2", [], "other", "satisfied"),
        ("", ["object-id"], "other", "satisfied"),
        (None, ["object-id"], "other", "satisfied"),
        ("missing", ["object-id"], "other", "undetermined"),
        ("a2", ["object-id"], "removed", "undetermined"),
    ],
)
def test_has_label(specs, value, labels, target_label, expected):
    specs["restrictions"] = [restriction("link", "HasLabel", labels=labels)]
    results = evaluate(specs, {"link": value}, [detail(annotation_id="a2", label=target_label)])
    assert results[0].status == expected


def test_imply_with_link_premise(specs):
    specs["restrictions"] = [conditional(restriction("link", "HasLabel", labels=["object-id"]), restriction(value=""))]
    assert evaluate(specs, {"link": "a2"}, [detail(annotation_id="a2")])[0].status == "violated"
    assert evaluate(specs, {"link": "a2"}, [detail(annotation_id="a2", label="other")])[0].status == "satisfied"
    assert evaluate(specs, {"link": "missing"})[0].status == "undetermined"


def test_can_input_and_read_only_are_excluded(specs):
    specs["restrictions"] = [
        restriction("note", "CanInput", enable=False),
        conditional(restriction("unclear", "Equals", value="true"), restriction("note", "CanInput", enable=False)),
    ]
    assert evaluate(specs, {"note": "existing", "unclear": True}) == []
    specs["restrictions"] = [restriction(value="")]
    specs["additionals"][0]["read_only"] = True
    assert evaluate(specs) == []


def test_default_is_not_filled(specs):
    specs["additionals"][0]["default"] = "default"
    assert evaluate(specs)[0].status == "violated"


def test_not_applicable_and_empty_input(specs):
    validator = AttributeRestrictionValidator(specs)
    assert validator.validate_simple_annotation_details([detail(label="other")]) == []
    assert validator.validate_simple_annotation_details([]) == []


@pytest.mark.parametrize("condition", [{"_type": "Unknown"}, {"_type": "Equals"}, {"_type": "Equals", "value": False}])
def test_bad_condition_does_not_stop_other_checks(specs, condition):
    specs["restrictions"] = [{"additional_data_definition_id": "note", "condition": condition}, restriction(value="")]
    results = evaluate(specs)
    assert [r.status for r in results] == ["undetermined", "violated"]
    assert results[0].message
    assert [r.restriction_index for r in results] == [0, 1]


def test_unknown_and_ambiguous_names(specs):
    assert AttributeRestrictionValidator(specs).validate_simple_annotation_details([detail(label="removed")])[0].status == "undetermined"
    specs["labels"].append(copy.deepcopy(specs["labels"][0]))
    assert evaluate(specs)[0].status == "undetermined"


def test_ambiguous_attribute_and_choice_names(specs):
    duplicate = copy.deepcopy(specs["additionals"][0])
    duplicate["additional_data_definition_id"] = "duplicate"
    specs["additionals"].append(duplicate)
    specs["labels"][0]["additional_data_definitions"].append("duplicate")
    assert evaluate(specs)[0].status == "undetermined"
    specs["restrictions"] = [restriction("kind", "Equals", value="choice-1")]
    specs["additionals"][3]["choices"].append({"choice_id": "choice-2", "name": message("car")})
    assert evaluate(specs, {"kind": "car"})[0].status == "undetermined"


def test_duplicate_ids_and_missing_input_fields(specs):
    validator = AttributeRestrictionValidator(specs)
    with pytest.raises(ValueError):
        validator.validate_simple_annotation_details([detail(), detail()])
    with pytest.raises(KeyError):
        validator.validate_simple_annotation_details([{"annotation_id": "a1", "label": "object"}])


def test_reusable_validator_and_spec_snapshot(specs):
    validator = AttributeRestrictionValidator(specs)
    specs["restrictions"].clear()
    assert validator.validate_simple_annotation_details(iter([detail()]))[0].status == "violated"
    assert validator.validate_simple_annotation_details([detail({"note": "ok"})])[0].status == "satisfied"


def test_real_spec_and_existing_restriction_model():
    specs = json.loads(Path("tests/data/util/attribute_restrictions/annotation_specs.json").read_text())
    specs["restrictions"] = [Restriction.from_dict(r).to_dict() for r in specs["restrictions"]]
    validator = AttributeRestrictionValidator(specs)
    results = validator.validate_simple_annotation_details([detail(label="car"), detail(annotation_id="a2", label="number_plate")])
    assert {r.status for r in results} == {"satisfied", "violated"}


def test_zip_parser_integration(specs):
    specs["labels"][0]["label_name"] = message("climatic")
    validator = AttributeRestrictionValidator(specs)
    results = [
        result
        for parser in lazy_parse_simple_annotation_zip(Path("tests/data/simple-annotation.zip"))
        for result in validator.validate_simple_annotation_details(parser.load_json()["details"])
    ]
    assert any(r.status == "violated" for r in results)


@pytest.mark.parametrize(
    "attribute_type, value, expected_value", [("text", "abc", "abc"), ("tracking", "track-1", "track-1"), ("select", "car", "choice-1")]
)
def test_other_attribute_types(specs, attribute_type, value, expected_value):
    attribute = specs["additionals"][3] if attribute_type == "select" else specs["additionals"][0]
    attribute["type"] = attribute_type
    attribute_id = attribute["additional_data_definition_id"]
    specs["restrictions"] = [restriction(attribute_id, "Equals", value=expected_value)]
    assert evaluate(specs, {attribute_id: value})[0].status == "satisfied"


def test_false_premise_does_not_evaluate_bad_conclusion(specs):
    specs["restrictions"] = [conditional(restriction("unclear", "Equals", value="true"), restriction("note", "Matches", value="["))]
    assert evaluate(specs, {"unclear": False})[0].status == "satisfied"
    assert evaluate(specs, {"unclear": True})[0].status == "undetermined"


def test_unknown_attribute_and_unsupported_type(specs):
    specs["restrictions"] = [restriction("missing", value=""), restriction(value="")]
    specs["additionals"][0]["type"] = "future-type"
    assert [r.status for r in evaluate(specs)] == ["undetermined", "undetermined"]


def test_premise_attribute_not_on_label(specs):
    specs["labels"][0]["additional_data_definitions"].remove("unclear")
    specs["restrictions"] = [conditional(restriction("unclear", "Equals", value="true"), restriction(value=""))]
    assert evaluate(specs)[0].status == "undetermined"


def test_nested_premise(specs):
    premise = conditional(restriction("unclear", "Equals", value="true"), restriction("count", "Equals", value="1"))
    specs["restrictions"] = [conditional(premise, restriction(value=""))]
    assert evaluate(specs, {"unclear": True, "count": 1})[0].status == "violated"
    assert evaluate(specs, {"unclear": True, "count": 2})[0].status == "satisfied"


@pytest.mark.parametrize("condition_type", ["Matches", "NotMatches"])
@pytest.mark.parametrize("pattern", ["a{4294967296}", "(?:" * 1000 + "a" + ")" * 1000], ids=["overflow", "recursion"])
def test_regex_error_does_not_stop_other_checks(specs, condition_type, pattern):
    specs["restrictions"] = [restriction("note", condition_type, value=pattern), restriction(value="")]
    results = evaluate(specs, {"note": "abc"})
    assert [r.status for r in results] == ["undetermined", "satisfied"]
    assert results[0].message
