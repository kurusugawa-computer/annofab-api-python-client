import copy
import json
from pathlib import Path

import pytest

from annofabapi.util.label_field_values import describe_label_field_values


def describe(field_id, value, *, annotation_type="polygon", lang="en"):
    return describe_label_field_values({"annotation_type": annotation_type, "field_values": {field_id: value}}, lang=lang)[0]


@pytest.mark.parametrize("lang", ["ja", "en"])
@pytest.mark.parametrize("rule", ["and", "or", {"_type": "And"}, {"_type": "Or"}])
def test_サイズ制約は違反する条件の論理演算を説明する(rule, lang):
    result = describe("minimum_size_2d", {"_type": "MinimumSize2d", "min_warn_rule": rule, "min_width": 100, "min_height": 200}, lang=lang)
    conjunction = rule in ("and", {"_type": "And"})
    if lang == "ja":
        connector = "かつ" if conjunction else "または"
        expected = f"幅が100ピクセル未満、{connector}高さが200ピクセル未満の場合にサイズ制約の警告を表示します。サイズ制約の警告があっても、タスクの提出・合格は可能です。"
    else:
        condition = (
            "both width is less than 100 pixels and height is less than 200 pixels"
            if conjunction
            else "width is less than 100 pixels or height is less than 200 pixels"
        )
        expected = f"A size warning is shown when {condition}. Size warnings do not prevent task submission or acceptance."
    assert result.is_supported
    assert result.field_id == "minimum_size_2d"
    assert result.text == expected


@pytest.mark.parametrize(
    ("field_id", "value", "annotation_type", "ja", "en"),
    [
        (
            "minimum_area_2d",
            {"_type": "MinimumArea2d", "min_area": 400},
            "polygon",
            "面積が400平方ピクセル未満の場合にサイズ制約の警告を表示します。警告があっても、タスクの提出・合格は可能です。",
            "A size warning is shown when area is less than 400 square pixels. Size warnings do not prevent task submission or acceptance.",
        ),
        (
            "margin_of_error_tolerance",
            {"_type": "MarginOfErrorTolerance", "max_pixel": 5},
            "point",
            "誤差許容範囲は5ピクセルです。画像エディタの許容範囲表示を有効にすると、半径5ピクセルの円を表示します。",
            "The error tolerance is 5 pixels. Enabling tolerance display in the image editor shows a circle with a radius of 5 pixels.",
        ),
        (
            "display_line_direction",
            {"_type": "DisplayLineDirection", "has_direction": True},
            "polyline",
            "ポリラインの向きを表示します。",
            "The polyline direction is displayed.",
        ),
        (
            "display_line_direction",
            {"_type": "DisplayLineDirection", "has_direction": False},
            "polyline",
            "ポリラインの向きを表示しません。",
            "The polyline direction is not displayed.",
        ),
        (
            "vertex_count_min_max",
            {"_type": "VertexCountMinMax", "min": 3, "max": 10},
            "polygon",
            "頂点数の下限は3個です。頂点数の上限は10個です。",
            "The minimum vertex count is 3. The maximum vertex count is 10.",
        ),
        (
            "vertex_count_min_max",
            {"_type": "VertexCountMinMax", "min": None, "max": 20},
            "polyline",
            "頂点数の下限設定はnull（追加の下限制約なし）です。頂点数の上限は20個です。",
            "The vertex-count lower bound is null (no additional lower bound). The maximum vertex count is 20.",
        ),
        (
            "vertex_count_min_max",
            {"_type": "VertexCountMinMax", "min": 2, "max": None},
            "polyline",
            "頂点数の下限は2個です。頂点数の上限設定はnull（追加の上限制約なし）です。",
            "The minimum vertex count is 2. The vertex-count upper bound is null (no additional upper bound).",
        ),
    ],
)
@pytest.mark.parametrize("lang", ["ja", "en"])
def test_標準設定を日本語と英語で説明する(field_id, value, annotation_type, ja, en, lang):
    result = describe(field_id, value, annotation_type=annotation_type, lang=lang)
    assert result.is_supported
    assert result.text == (ja if lang == "ja" else en)


@pytest.mark.parametrize("lang", ["ja", "en"])
@pytest.mark.parametrize("position", ["omitted", None, [0, 30]])
def test_矩形挿入はサイズと位置を説明する(position, lang):
    value = {"_type": "MinimumSize2dWithDefaultInsertPosition", "min_warn_rule": {"_type": "Or"}, "min_width": 20, "min_height": 40}
    if position != "omitted":
        value["position_for_minimum_bounding_box_insertion"] = position
    result = describe("minimum_size_2d_with_default_insert_position", value, annotation_type="bounding_box", lang=lang)
    assert result.is_supported
    if isinstance(position, list):
        assert "(x=0, y=30)" in result.text
        assert ("幅20・高さ40ピクセル" if lang == "ja" else "20 by 40 pixel") in result.text
    else:
        assert ("表示範囲の中央" if lang == "ja" else "center of the visible canvas") in result.text
        assert (("省略" if lang == "ja" else "omitted") if position == "omitted" else "null") in result.text


@pytest.mark.parametrize("lang", ["ja", "en"])
def test_作図機能はfalseも明示し省略とは区別する(lang):
    value = {
        "_type": "AnnotationEditorFeature",
        "append": True,
        "erase": False,
        "freehand": True,
        "rectangle_fill": False,
        "polygon_fill": True,
        "fill_near": False,
    }
    result = describe("annotation_editor_feature", value, annotation_type="segmentation_v2", lang=lang)
    assert result.is_supported
    if lang == "ja":
        assert (
            result.text
            == "作図機能「追記」は使用できます。作図機能「消しゴム」は使用できません。作図機能「フリーハンド」は使用できます。作図機能「矩形」は使用できません。作図機能「自由形状」は使用できます。作図機能「近似色塗りつぶし」は使用できません。"
        )
    else:
        assert (
            result.text
            == "The append drawing feature is available. The eraser drawing feature is unavailable. The freehand drawing feature is available. The rectangle fill drawing feature is unavailable. The polygon fill drawing feature is available. The similar-color fill drawing feature is unavailable."
        )
    del value["erase"]
    assert not describe("annotation_editor_feature", value, annotation_type="segmentation_v2", lang=lang).is_supported


@pytest.mark.parametrize("value", [None, False, {}, [], 5, "false"])
@pytest.mark.parametrize("lang", ["ja", "en"])
def test_未対応の値を無効とは推測しない(value, lang):
    result = describe("display_line_direction", value, annotation_type="polyline", lang=lang)
    assert not result.is_supported
    assert ("解釈できません" if lang == "ja" else "Cannot interpret") in result.text
    assert json.dumps({"display_line_direction": value}, ensure_ascii=False) in result.text


@pytest.mark.parametrize(
    ("field_id", "value", "annotation_type"),
    [
        ("new_field", {"_type": "MarginOfErrorTolerance", "max_pixel": 5}, "polygon"),
        ("display_line_direction", {"_type": "NewType", "has_direction": True}, "polyline"),
        ("display_line_direction", {"has_direction": True}, "polyline"),
        ("display_line_direction", {"_type": "DisplayLineDirection", "has_direction": None}, "polyline"),
        ("display_line_direction", {"_type": "DisplayLineDirection", "has_direction": 0}, "polyline"),
        ("display_line_direction", {"_type": "DisplayLineDirection", "has_direction": False, "new": {"mode": 3}}, "polyline"),
        ("display_line_direction", {"_type": "DisplayLineDirection", "has_direction": True}, "polygon"),
        ("margin_of_error_tolerance", {"_type": "MarginOfErrorTolerance", "max_pixel": 5}, "user_bounding_box"),
        ("margin_of_error_tolerance", {"_type": "MarginOfErrorTolerance", "max_pixel": 5}, "range"),
        ("margin_of_error_tolerance", {"_type": "MarginOfErrorTolerance", "max_pixel": 5}, "classification"),
        ("margin_of_error_tolerance", {"_type": "MarginOfErrorTolerance", "max_pixel": -1}, "point"),
        ("margin_of_error_tolerance", {"_type": "MarginOfErrorTolerance", "max_pixel": True}, "point"),
        ("margin_of_error_tolerance", {"_type": "MarginOfErrorTolerance", "max_pixel": 1.5}, "point"),
        ("vertex_count_min_max", {"_type": "VertexCountMinMax", "min": 10, "max": 3}, "polygon"),
        ("vertex_count_min_max", {"_type": "VertexCountMinMax", "min": 2, "max": 3}, "polygon"),
        ("vertex_count_min_max", {"_type": "VertexCountMinMax", "min": True, "max": 3}, "polyline"),
        ("vertex_count_min_max", {"_type": "VertexCountMinMax", "min": 2}, "polyline"),
        ("minimum_area_2d", {"_type": "MinimumArea2d", "min_area": 0}, "polygon"),
        ("minimum_area_2d", {"_type": "MinimumArea2d", "min_area": 5, "extra": True}, "polygon"),
        ("custom", {"_type": "OneBooleanFieldValue", "value": False}, "user_custom"),
        ("custom", {"_type": "EmptyFieldValue"}, "user_custom"),
    ],
)
@pytest.mark.parametrize("lang", ["ja", "en"])
def test_不明な設定や適用条件は元のキーと値を残す(field_id, value, annotation_type, lang):
    result = describe(field_id, value, annotation_type=annotation_type, lang=lang)
    assert not result.is_supported
    assert result.field_id == field_id
    assert json.dumps({field_id: value}, ensure_ascii=False) in result.text


@pytest.mark.parametrize(
    "change",
    [
        {"min_warn_rule": None},
        {"min_warn_rule": "none"},
        {"min_warn_rule": {}},
        {"min_warn_rule": {"_type": "Or", "unknown": True}},
        {"min_warn_rule": {"_type": "Xor"}},
        {"min_width": False},
        {"min_height": -1},
        {"new": "value"},
        {"position_for_minimum_bounding_box_insertion": {}},
        {"position_for_minimum_bounding_box_insertion": [1]},
        {"position_for_minimum_bounding_box_insertion": [1, 2, 3]},
        {"position_for_minimum_bounding_box_insertion": [True, 2]},
    ],
)
def test_最小サイズの未知の項目も黙って省略しない(change):
    value = {"_type": "MinimumSize2dWithDefaultInsertPosition", "min_warn_rule": "or", "min_width": 20, "min_height": 40} | change
    result = describe("minimum_size_2d_with_default_insert_position", value, annotation_type="bounding_box")
    assert not result.is_supported
    assert json.dumps({"minimum_size_2d_with_default_insert_position": value}) in result.text
    assert "A size warning" not in result.text


def test_ゼロの幅高さや許容誤差を省略とは区別する():
    assert describe("margin_of_error_tolerance", {"_type": "MarginOfErrorTolerance", "max_pixel": 0}).is_supported
    result = describe("minimum_size_2d", {"_type": "MinimumSize2d", "min_warn_rule": "and", "min_width": 0, "min_height": 0})
    assert result.is_supported
    assert "0 pixels" in result.text


@pytest.mark.parametrize("fields", [None, False, [], "invalid"])
def test_field_valuesコンテナ自体も不明なら説明に残す(fields):
    result = describe_label_field_values({"annotation_type": "point", "field_values": fields})
    assert len(result) == 1
    assert result[0].field_id == "field_values"
    assert not result[0].is_supported
    assert json.dumps({"field_values": fields}) in result[0].text


def test_省略した設定の既定値を補完しない():
    assert describe_label_field_values({"annotation_type": "polygon"}) == []
    assert describe_label_field_values({"annotation_type": "polygon", "field_values": {}}) == []


def test_設定の組み合わせは順序を保ち入力を変更しない():
    label = {
        "annotation_type": "polyline",
        "field_values": {
            "vertex_count_min_max": {"_type": "VertexCountMinMax", "min": None, "max": None},
            "unknown": {"_type": "Unknown", "値": False},
            "display_line_direction": {"_type": "DisplayLineDirection", "has_direction": False},
        },
    }
    original = copy.deepcopy(label)
    results = describe_label_field_values(label)
    assert [result.field_id for result in results] == ["vertex_count_min_max", "unknown", "display_line_direction"]
    assert [result.is_supported for result in results] == [True, False, True]
    assert label == original


def test_既存の実レスポンス例を両言語で解釈できる():
    specs_path = Path(__file__).parents[1] / "data/util/attribute_restrictions/annotation_specs.json"
    specs = json.loads(specs_path.read_text())
    for label in specs["labels"]:
        for lang in ("ja", "en"):
            results = describe_label_field_values(label, lang=lang)
            assert len(results) == len(label["field_values"])
            assert all(result.is_supported for result in results)


def test_未対応の言語はエラーにする():
    with pytest.raises(ValueError):
        describe_label_field_values({"annotation_type": "point"}, lang="fr")  # type: ignore[arg-type]


def test_アノテーション種類は必須():
    with pytest.raises(KeyError):
        describe_label_field_values({"field_values": {}})
