import copy
import json
from pathlib import Path

import pytest

from annofabapi.parser import lazy_parse_simple_annotation_zip
from annofabapi.util.attribute_restriction_validation import AttributeRestrictionValidator, AttributeRestrictionViolation
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


def assert_evaluation(specs, attributes, expected, others=()):
    if expected is None:
        with pytest.raises(ValueError):
            evaluate(specs, attributes, others)
    else:
        actual = evaluate(specs, attributes, others)
        assert actual == ([AttributeRestrictionViolation("a1", specs["restrictions"][0]["additional_data_definition_id"], 0)] if expected else [])


@pytest.mark.parametrize(
    "attributes, expected",
    [({}, True), ({"note": None}, True), ({"note": ""}, True), ({"note": " "}, False), ({"note": "abc"}, False)],
)
def test_required(specs, attributes, expected):
    assert_evaluation(specs, attributes, expected)


@pytest.mark.parametrize(
    "attribute_id, value, expected_value, expected",
    [
        ("unclear", True, "true", False),
        ("unclear", False, "true", True),
        ("unclear", None, "false", False),
        ("unclear", "false", "false", None),
        ("count", 0, "0", False),
        ("count", "12", "12", False),
        ("count", None, "", False),
        ("count", True, "1", None),
        ("count", 1.5, "1", None),
        ("kind", "car", "choice-1", False),
        ("kind", "bus", "choice-1", None),
        ("kind", None, "", False),
        ("note", "abc", "abc", False),
        ("note", 1, "1", None),
    ],
)
def test_equals_and_not_equals(specs, attribute_id, value, expected_value, expected):
    specs["restrictions"] = [restriction(attribute_id, "Equals", value=expected_value)]
    assert_evaluation(specs, {attribute_id: value}, expected)
    specs["restrictions"][0]["condition"]["_type"] = "NotEquals"
    opposite = {False: True, True: False, None: None}
    assert_evaluation(specs, {attribute_id: value}, opposite[expected])


@pytest.mark.parametrize(
    "condition_type, pattern, value, expected",
    [
        ("Matches", "abc", "xabcx", True),
        ("Matches", "abc", "abc", False),
        ("NotMatches", "abc", "abc", True),
        ("Matches", "^abc$", "xabcx", True),
        ("Matches", "abc$", "abc\n", True),
        ("Matches", r"\d", "1", False),
        ("Matches", r"\d", "12", True),
        ("Matches", r"\d", "a", True),
        ("NotMatches", r"\d", "1", True),
        ("NotMatches", r"\d", "12", False),
        ("Matches", "[0-9]", "1", False),
        ("Matches", "[0-9]", "12", True),
        ("Matches", "[0-9]", "a", True),
        ("NotMatches", "abc", "xabcx", False),
        ("NotMatches", "abc", "xyz", False),
        ("Matches", "^$", None, False),
        ("Matches", "[", "x", None),
    ],
)
def test_regex(specs, condition_type, pattern, value, expected):
    specs["restrictions"] = [restriction("note", condition_type, value=pattern)]
    assert_evaluation(specs, {"note": value}, expected)


def conditional(premise, conclusion):
    return {
        "additional_data_definition_id": conclusion["additional_data_definition_id"],
        "condition": {"_type": "Imply", "premise": premise, "condition": conclusion["condition"]},
    }


@pytest.mark.parametrize(
    "unclear, note, expected",
    [
        (True, "", True),
        (True, "ok", False),
        (False, "", False),
        (None, "", False),
        ("bad", "", None),
        ("bad", "ok", None),
    ],
)
def test_imply(specs, unclear, note, expected):
    specs["restrictions"] = [conditional(restriction("unclear", "Equals", value="true"), restriction(value=""))]
    assert_evaluation(specs, {"unclear": unclear, "note": note}, expected)


def test_nested_imply_is_one_result(specs):
    specs["restrictions"] = [
        conditional(restriction("unclear", "Equals", value="true"), conditional(restriction("count", "Equals", value="1"), restriction(value="")))
    ]
    results = evaluate(specs, {"unclear": True, "count": 1})
    assert len(results) == 1
    assert results[0] == AttributeRestrictionViolation("a1", "note", 0)
    assert evaluate(specs, {"unclear": True, "count": 2}) == []


@pytest.mark.parametrize(
    "value, labels, target_label, expected",
    [
        ("a2", ["object-id"], "object", False),
        ("a2", ["object-id"], "other", True),
        ("a2", [], "other", False),
        ("", ["object-id"], "other", False),
        (None, ["object-id"], "other", False),
        ("missing", ["object-id"], "other", None),
        ("a2", ["object-id"], "removed", None),
    ],
)
def test_has_label(specs, value, labels, target_label, expected):
    specs["restrictions"] = [restriction("link", "HasLabel", labels=labels)]
    assert_evaluation(specs, {"link": value}, expected, [detail(annotation_id="a2", label=target_label)])


def test_imply_with_link_premise(specs):
    specs["restrictions"] = [conditional(restriction("link", "HasLabel", labels=["object-id"]), restriction(value=""))]
    assert_evaluation(specs, {"link": "a2"}, True, [detail({"note": "ok"}, annotation_id="a2")])
    assert_evaluation(specs, {"link": "a2"}, False, [detail(annotation_id="a2", label="other")])
    assert_evaluation(specs, {"link": "missing"}, None)


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
    assert evaluate(specs) == [AttributeRestrictionViolation("a1", "note", 0)]


def test_not_applicable_and_empty_input(specs):
    validator = AttributeRestrictionValidator(specs)
    assert validator.validate_simple_annotation_details([detail(label="other")]) == []
    assert validator.validate_simple_annotation_details([]) == []


@pytest.mark.parametrize("condition", [{"_type": "Unknown"}, {"_type": "Equals"}, {"_type": "Equals", "value": False}])
def test_bad_condition_raises(specs, condition):
    specs["restrictions"] = [{"additional_data_definition_id": "note", "condition": condition}, restriction(value="")]
    with pytest.raises(ValueError):
        evaluate(specs)


def test_unknown_and_ambiguous_label_names(specs):
    with pytest.raises(ValueError):
        AttributeRestrictionValidator(specs).validate_simple_annotation_details([detail(label="removed")])
    duplicate = copy.deepcopy(specs["labels"][0])
    duplicate["label_id"] = "duplicate-label"
    specs["labels"].append(duplicate)
    with pytest.raises(ValueError):
        evaluate(specs)


def test_ambiguous_attribute_names_on_same_label(specs):
    duplicate = copy.deepcopy(specs["additionals"][0])
    duplicate["additional_data_definition_id"] = "duplicate"
    specs["additionals"].append(duplicate)
    specs["labels"][0]["additional_data_definitions"].append("duplicate")
    with pytest.raises(ValueError):
        evaluate(specs, {"note": "ok"})


def test_same_attribute_name_on_different_labels(specs):
    duplicate = copy.deepcopy(specs["additionals"][0])
    duplicate["additional_data_definition_id"] = "other-note"
    specs["additionals"].append(duplicate)
    specs["labels"][1]["additional_data_definitions"].append("other-note")
    specs["restrictions"].append(restriction("other-note", value=""))
    annotations = [detail(), detail(annotation_id="a2", label="other")]
    assert AttributeRestrictionValidator(specs).validate_simple_annotation_details(annotations) == [
        AttributeRestrictionViolation("a1", "note", 0),
        AttributeRestrictionViolation("a2", "other-note", 1),
    ]


def test_ambiguous_choice_names(specs):
    specs["restrictions"] = [restriction("kind", "Equals", value="choice-1")]
    specs["additionals"][3]["choices"].append({"choice_id": "choice-2", "name": message("car")})
    with pytest.raises(ValueError):
        evaluate(specs, {"kind": "car"})


def test_duplicate_ids_and_missing_input_fields(specs):
    validator = AttributeRestrictionValidator(specs)
    with pytest.raises(ValueError):
        validator.validate_simple_annotation_details([detail(), detail()])
    with pytest.raises(KeyError):
        validator.validate_simple_annotation_details([{"annotation_id": "a1", "label": "object"}])


def test_reusable_validator_and_spec_snapshot(specs):
    validator = AttributeRestrictionValidator(specs)
    specs["restrictions"].clear()
    assert validator.validate_simple_annotation_details(iter([detail()])) == [AttributeRestrictionViolation("a1", "note", 0)]
    assert validator.validate_simple_annotation_details([detail({"note": "ok"})]) == []


def test_real_spec_and_existing_restriction_model():
    specs = json.loads(Path("tests/data/util/attribute_restrictions/annotation_specs.json").read_text())
    specs["restrictions"] = [Restriction.from_dict(r).to_dict() for r in specs["restrictions"]]
    validator = AttributeRestrictionValidator(specs)
    results = validator.validate_simple_annotation_details([detail(label="car"), detail(annotation_id="a2", label="number_plate")])
    assert results == [AttributeRestrictionViolation("a1", specs["restrictions"][1]["additional_data_definition_id"], 1)]


def test_zip_parser_integration(specs):
    annotations = [parser.load_json() for parser in lazy_parse_simple_annotation_zip(Path("tests/data/simple-annotation.zip"))]
    label_names = sorted({item["label"] for annotation in annotations for item in annotation["details"]})
    specs["labels"] = [
        {"label_id": f"label-{index}", "label_name": message(name), "additional_data_definitions": ["note"] if name == "climatic" else []}
        for index, name in enumerate(label_names)
    ]
    validator = AttributeRestrictionValidator(specs)
    results = [result for annotation in annotations for result in validator.validate_simple_annotation_details(annotation["details"])]
    assert results
    assert all(r.attribute_id == "note" and r.restriction_index == 0 for r in results)


@pytest.mark.parametrize(
    "attribute_type, value, expected_value", [("text", "abc", "abc"), ("tracking", "track-1", "track-1"), ("select", "car", "choice-1")]
)
def test_other_attribute_types(specs, attribute_type, value, expected_value):
    attribute = specs["additionals"][3] if attribute_type == "select" else specs["additionals"][0]
    attribute["type"] = attribute_type
    attribute_id = attribute["additional_data_definition_id"]
    specs["restrictions"] = [restriction(attribute_id, "Equals", value=expected_value)]
    assert evaluate(specs, {attribute_id: value}) == []


def test_false_premise_does_not_evaluate_bad_conclusion(specs):
    specs["restrictions"] = [conditional(restriction("unclear", "Equals", value="true"), restriction("note", "Matches", value="["))]
    assert evaluate(specs, {"unclear": False}) == []
    assert_evaluation(specs, {"unclear": True}, None)


def test_unknown_attribute_and_unsupported_type(specs):
    specs["restrictions"] = [restriction("missing", value=""), restriction(value="")]
    specs["additionals"][0]["type"] = "future-type"
    with pytest.raises(ValueError):
        evaluate(specs)
    specs["restrictions"] = [restriction(value="")]
    with pytest.raises(ValueError):
        evaluate(specs)


def test_premise_attribute_not_on_label(specs):
    specs["labels"][0]["additional_data_definitions"].remove("unclear")
    specs["restrictions"] = [conditional(restriction("unclear", "Equals", value="true"), restriction(value=""))]
    assert_evaluation(specs, {}, None)


def test_nested_premise(specs):
    premise = conditional(restriction("unclear", "Equals", value="true"), restriction("count", "Equals", value="1"))
    specs["restrictions"] = [conditional(premise, restriction(value=""))]
    assert evaluate(specs, {"unclear": True, "count": 1}) == [AttributeRestrictionViolation("a1", "note", 0)]
    assert evaluate(specs, {"unclear": True, "count": 2}) == []


@pytest.mark.parametrize("condition_type", ["Matches", "NotMatches"])
@pytest.mark.parametrize("pattern", ["a{4294967296}", "(?:" * 1000 + "a" + ")" * 1000], ids=["overflow", "recursion"])
def test_regex_error_raises(specs, condition_type, pattern):
    specs["restrictions"] = [restriction("note", condition_type, value=pattern), restriction(value="")]
    with pytest.raises(ValueError):
        evaluate(specs, {"note": "abc"})


def test_no_restrictions_returns_empty(specs):
    specs["restrictions"] = []
    assert evaluate(specs) == []


def test_multiple_violations_preserve_order_and_conclusion_attribute(specs):
    specs["restrictions"] = [restriction(value=""), conditional(restriction("unclear", "Equals", value="true"), restriction(value=""))]
    annotations = [detail({"unclear": True}), detail({"note": "ok"}, annotation_id="a2"), detail(annotation_id="a3")]
    assert AttributeRestrictionValidator(specs).validate_simple_annotation_details(annotations) == [
        AttributeRestrictionViolation("a1", "note", 0),
        AttributeRestrictionViolation("a1", "note", 1),
        AttributeRestrictionViolation("a3", "note", 0),
    ]
