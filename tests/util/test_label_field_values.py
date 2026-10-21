import copy
import json
from pathlib import Path

import pytest

from annofabapi.util.label_field_values import describe_label_field_values


def describe(field_id, value, *, annotation_type="polygon", lang="en"):
    return describe_label_field_values({"annotation_type": annotation_type, "field_values": {field_id: value}}, lang=lang)[0]


@pytest.mark.parametrize("lang", ["ja", "en"])
@pytest.mark.parametrize("rule", ["and", "or", {"_type": "And"}, {"_type": "Or"}])
def test_最小サイズはAndOrを制約の充足条件に変換する(rule, lang):
    result = describe("minimum_size_2d", {"_type": "MinimumSize2d", "min_warn_rule": rule, "min_width": 100, "min_height": 200}, lang=lang)
    conjunction = rule in ("and", {"_type": "And"})
    if lang == "ja":
        connector = "または" if conjunction else "かつ"
        expected = f"最小サイズ制約は、幅100ピクセル以上、{connector}高さ200ピクセル以上です。"
    else:
        connector = "or" if conjunction else "and"
        expected = f"Minimum size: width of at least 100 pixels {connector} height of at least 200 pixels."
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
            "最小面積は400平方ピクセルです。",
            "The minimum area is 400 square pixels.",
        ),
        (
            "margin_of_error_tolerance",
            {"_type": "MarginOfErrorTolerance", "max_pixel": 5},
            "point",
            "誤差許容範囲は5ピクセルです。",
            "The error tolerance is 5 pixels.",
        ),
        (
            "display_line_direction",
            {"_type": "DisplayLineDirection", "has_direction": True},
            "polyline",
            "ポリラインの向きの表示は有効です。",
            "Polyline direction display is enabled.",
        ),
        (
            "display_line_direction",
            {"_type": "DisplayLineDirection", "has_direction": False},
            "polyline",
            "ポリラインの向きの表示は無効です。",
            "Polyline direction display is disabled.",
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
    expected = ja if lang == "ja" else en
    assert result.text == expected


@pytest.mark.parametrize("lang", ["ja", "en"])
@pytest.mark.parametrize("position", ["omitted", None, [0, 30]])
def test_矩形挿入はサイズと位置を説明する(position, lang):
    value = {"_type": "MinimumSize2dWithDefaultInsertPosition", "min_warn_rule": {"_type": "Or"}, "min_width": 20, "min_height": 40}
    if position != "omitted":
        value["position_for_minimum_bounding_box_insertion"] = position
    result = describe("minimum_size_2d_with_default_insert_position", value, annotation_type="bounding_box", lang=lang)
    assert result.is_supported
    if lang == "ja":
        base = "最小サイズ制約は、幅20ピクセル以上、かつ高さ40ピクセル以上です。"
        if isinstance(position, list):
            expected = base + "最小矩形の挿入位置は(x=0, y=30)です。"
        elif position is None:
            expected = base + "最小矩形の挿入位置は未指定（null）です。"
        else:
            expected = base + "最小矩形の挿入位置は省略されています。"
    else:
        base = "Minimum size: width of at least 20 pixels and height of at least 40 pixels."
        if isinstance(position, list):
            expected = base + " The minimum-box insertion position is (x=0, y=30)."
        elif position is None:
            expected = base + " The minimum-box insertion position is unspecified (null)."
        else:
            expected = base + " The minimum-box insertion position is omitted."
    assert result.text == expected


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
        expected = (
            "作図モード「追記」の選択は有効です。作図モード「消しゴム」の選択は無効です。"
            "作図ツール「フリーハンド」は有効です。作図ツール「矩形」は無効です。"
            "作図ツール「自由形状」は有効です。作図ツール「近似色塗りつぶし」は無効です。"
        )
    else:
        expected = (
            "Selection of the append drawing mode is enabled. Selection of the eraser drawing mode is disabled. "
            "The freehand drawing tool is enabled. The rectangle fill drawing tool is disabled. "
            "The polygon fill drawing tool is enabled. The similar-color fill drawing tool is disabled."
        )
    assert result.text == expected
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
        ("vertex_count_min_max", {"_type": "VertexCountMinMax", "min": 2, "max": {}}, "polyline"),
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
    assert "Minimum size:" not in result.text


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


@pytest.mark.parametrize("lang", ["ja", "en"])
@pytest.mark.parametrize("bounds", [{}, {"min": None}, {"max": None}, {"min": None, "max": None}])
def test_頂点数の省略とnullはJSONの指定状態だけを説明する(bounds, lang):
    result = describe("vertex_count_min_max", {"_type": "VertexCountMinMax"} | bounds, lang=lang)
    assert result.is_supported
    lower = ("省略" if lang == "ja" else "omitted") if "min" not in bounds else "null"
    upper = ("省略" if lang == "ja" else "omitted") if "max" not in bounds else "null"
    expected = (
        f"頂点数の下限設定は{lower}（追加の下限制約なし）です。頂点数の上限設定は{upper}（追加の上限制約なし）です。"
        if lang == "ja"
        else f"The vertex-count lower bound is {lower} (no additional lower bound). The vertex-count upper bound is {upper} (no additional upper bound)."
    )
    assert result.text == expected


@pytest.mark.parametrize("lang", ["ja", "en"])
def test_許容誤差0は設定値をそのまま説明する(lang):
    result = describe("margin_of_error_tolerance", {"_type": "MarginOfErrorTolerance", "max_pixel": 0}, lang=lang)
    assert result.is_supported
    assert result.text == ("誤差許容範囲は0ピクセルです。" if lang == "ja" else "The error tolerance is 0 pixels.")


@pytest.mark.parametrize("lang", ["ja", "en"])
def test_矩形の最小サイズ0は補正せず設定値を説明する(lang):
    result = describe(
        "minimum_size_2d_with_default_insert_position",
        {
            "_type": "MinimumSize2dWithDefaultInsertPosition",
            "min_warn_rule": {"_type": "Or"},
            "min_width": 0,
            "min_height": 0,
            "position_for_minimum_bounding_box_insertion": [0, 0],
        },
        annotation_type="bounding_box",
        lang=lang,
    )
    assert result.is_supported
    expected = (
        "最小サイズ制約は、幅0ピクセル以上、かつ高さ0ピクセル以上です。最小矩形の挿入位置は(x=0, y=0)です。"
        if lang == "ja"
        else "Minimum size: width of at least 0 pixels and height of at least 0 pixels. The minimum-box insertion position is (x=0, y=0)."
    )
    assert result.text == expected
