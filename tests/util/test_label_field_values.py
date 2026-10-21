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
        expected = (
            "幅・高さは、頂点座標を整数に丸めて求める外接矩形の大きさです。"
            f"幅が100ピクセル未満、{connector}高さが200ピクセル未満の場合にサイズ制約の警告を表示します。"
            "この最小サイズ制約は提出時にも検証され、違反すると提出できません。"
        )
    else:
        condition = (
            "both width is less than 100 pixels and height is less than 200 pixels"
            if conjunction
            else "width is less than 100 pixels or height is less than 200 pixels"
        )
        expected = (
            "Width and height are measured using the axis-aligned bounding box after rounding vertex coordinates to integers. "
            f"A size warning is shown when {condition}."
            " This minimum-size constraint is also checked on submission; a violation prevents submission."
        )
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
            "ポリゴンの面積が400平方ピクセル未満の場合に警告を表示します。この面積警告自体はタスクの提出・合格を妨げません。",
            "A warning is shown when the polygon area is less than 400 square pixels. This area warning itself does not prevent task submission or acceptance.",
        ),
        (
            "margin_of_error_tolerance",
            {"_type": "MarginOfErrorTolerance", "max_pixel": 5},
            "point",
            "誤差許容範囲は5ピクセルです。この値による誤差の自動検証は行いません。画像エディタの許容範囲表示を有効にすると、カーソル付近に許容範囲を表す円を表示します。",
            "The error tolerance is 5 pixels. This value is not used to automatically validate annotation errors. Enabling tolerance display in the image editor shows a tolerance circle near the cursor.",
        ),
        (
            "display_line_direction",
            {"_type": "DisplayLineDirection", "has_direction": True},
            "polyline",
            "ポリラインの向きの表示を有効にします。ただし、エディタ側で線の向きを非表示にしている場合は表示されません。",
            "Polyline direction display is enabled, but the editor's hide-line-direction setting can hide it.",
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
    expected = ja if lang == "ja" else en
    if field_id == "vertex_count_min_max":
        assert result.text.startswith(expected)
    else:
        assert result.text == expected


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
        assert "作図モード「追記」の選択は有効です。" in result.text
        assert "作図モード「消しゴム」の選択は無効です。" in result.text
        assert "作図ツール「フリーハンド」は有効です。" in result.text
        assert "作図ツール「矩形」は無効です。" in result.text
        assert "作図ツール「自由形状」は有効です。" in result.text
        assert "作図ツール「近似色塗りつぶし」は無効です。" in result.text
        assert "編集可能な状態で対象アノテーションを選択" in result.text
    else:
        assert "Selection of the append drawing mode is enabled." in result.text
        assert "Selection of the eraser drawing mode is disabled." in result.text
        assert "The freehand drawing tool is enabled." in result.text
        assert "The rectangle fill drawing tool is disabled." in result.text
        assert "The polygon fill drawing tool is enabled." in result.text
        assert "The similar-color fill drawing tool is disabled." in result.text
        assert "editing permission and a selected target annotation" in result.text
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


# Annofab本体の確認リビジョン: 5c7c420de456b87eb29274c0b974d23045ba28da
# 以下は本体の適用処理で確認した挙動の回帰テストです。
@pytest.mark.parametrize("lang", ["ja", "en"])
@pytest.mark.parametrize("annotation_type", ["polygon", "polyline", "segmentation", "segmentation_v2", "bounding_box"])
def test_最小サイズの提出時の扱いはラベル種類によって異なる(annotation_type, lang):
    # MinimumSize2d.validateAnnotation → ValidationError.validateSingle → OperateTask.validateForSubmit
    field_id = "minimum_size_2d_with_default_insert_position" if annotation_type == "bounding_box" else "minimum_size_2d"
    value_type = "MinimumSize2dWithDefaultInsertPosition" if annotation_type == "bounding_box" else "MinimumSize2d"
    result = describe(
        field_id,
        {"_type": value_type, "min_warn_rule": {"_type": "Or"}, "min_width": 20, "min_height": 40},
        annotation_type=annotation_type,
        lang=lang,
    )
    assert result.is_supported
    if annotation_type in {"polygon", "polyline"}:
        assert ("違反すると提出できません" if lang == "ja" else "a violation prevents submission") in result.text
        assert ("妨げません" if lang == "ja" else "does not prevent") not in result.text
    else:
        assert ("このサイズ警告自体は" if lang == "ja" else "This size warning itself") in result.text
    if annotation_type.startswith("segmentation"):
        assert ("塗りつぶし領域の外接矩形" if lang == "ja" else "filled region's axis-aligned bounding box") in result.text
    else:
        assert ("頂点座標を整数に丸めて" if lang == "ja" else "rounding vertex coordinates to integers") in result.text


@pytest.mark.parametrize("lang", ["ja", "en"])
@pytest.mark.parametrize(("width", "height", "expected"), [(0, 0, (1, 1)), (0, 40, (1, 40)), (20, 0, (20, 1)), (20, 40, (20, 40))])
@pytest.mark.parametrize("position", [None, [-10, 30]])
def test_矩形挿入時だけゼロの辺を1に補正する(width, height, expected, position, lang):
    # ViewLogic.createNewMinimumDetectAnnotation
    value = {
        "_type": "MinimumSize2dWithDefaultInsertPosition",
        "min_warn_rule": {"_type": "And"},
        "min_width": width,
        "min_height": height,
        "position_for_minimum_bounding_box_insertion": position,
    }
    result = describe("minimum_size_2d_with_default_insert_position", value, annotation_type="bounding_box", lang=lang)
    assert result.is_supported
    assert (f"幅{expected[0]}・高さ{expected[1]}ピクセル" if lang == "ja" else f"{expected[0]} by {expected[1]} pixel box") in result.text
    # 警告の閾値は0のままで、挿入寸法だけが1になります。
    assert (f"幅が{width}ピクセル未満" if lang == "ja" else f"width is less than {width} pixels") in result.text
    if position is None:
        assert ("左上座標が0未満になる場合" if lang == "ja" else "negative top-left coordinate is clamped to 0") in result.text
    else:
        assert "(x=-10, y=30)" in result.text
        assert ("補正します。左上" if lang == "ja" else "clamped") not in result.text


@pytest.mark.parametrize("lang", ["ja", "en"])
@pytest.mark.parametrize(
    ("bounds", "lower_state", "upper_state"),
    [
        ({}, "omitted", "omitted"),
        ({"min": None}, "null", "omitted"),
        ({"max": None}, "omitted", "null"),
        ({"min": None, "max": None}, "null", "null"),
    ],
)
def test_頂点数の省略とnullは追加制約なしだが図形の最低頂点数は残る(bounds, lower_state, upper_state, lang):
    # AnnotationTypeFieldValue.VertexCountMinMax の Option[Int] と TaskValidation.validateSingle
    result = describe("vertex_count_min_max", {"_type": "VertexCountMinMax"} | bounds, lang=lang)
    assert result.is_supported
    if lang == "ja":
        assert f"下限設定は{'省略' if lower_state == 'omitted' else lower_state}" in result.text
        assert f"上限設定は{'省略' if upper_state == 'omitted' else upper_state}" in result.text
        assert "3頂点未満の場合は、提出時にエラー" in result.text
    else:
        assert f"lower bound is {lower_state}" in result.text
        assert f"upper bound is {upper_state}" in result.text
        assert "3 vertices required by the shape itself causes a submission error" in result.text


@pytest.mark.parametrize("lang", ["ja", "en"])
@pytest.mark.parametrize(("bounds", "initial"), [({"min": 3, "max": 10}, 10), ({"min": 20}, 20), ({"min": 3}, 16), ({"max": 3}, 3), ({}, 16)])
def test_ポリゴン頂点数は作図ツールの初期値にも使われる(bounds, initial, lang):
    # ViewLogic.calculateDefaultPolygonVerticesNumber / globalDefaultPolygonRectNum
    result = describe("vertex_count_min_max", {"_type": "VertexCountMinMax"} | bounds, lang=lang)
    assert result.is_supported
    assert (
        f"頂点数の初期値は{initial}個" if lang == "ja" else f"initial vertex count for the polygon-by-rectangle drawing tool is {initial}"
    ) in result.text


@pytest.mark.parametrize("lang", ["ja", "en"])
def test_追加の頂点数制約と図形の最低頂点数の違反を区別する(lang):
    result = describe("vertex_count_min_max", {"_type": "VertexCountMinMax", "min": 4, "max": 10}, annotation_type="polyline", lang=lang)
    assert result.is_supported
    assert (
        "この警告自体はタスクの提出・合格を妨げません" if lang == "ja" else "This warning itself does not prevent task submission or acceptance"
    ) in result.text
    assert (
        "2頂点未満の場合は、提出時にエラー" if lang == "ja" else "2 vertices required by the shape itself causes a submission error"
    ) in result.text
    assert ("作図ツールの頂点数の初期値" if lang == "ja" else "polygon-by-rectangle") not in result.text


@pytest.mark.parametrize("lang", ["ja", "en"])
def test_許容誤差0は円の表示を有効にしても円を描画しない(lang):
    # ToleranceCircleGraphics.refresh は 0 < radius の場合だけ描画します。
    result = describe("margin_of_error_tolerance", {"_type": "MarginOfErrorTolerance", "max_pixel": 0}, lang=lang)
    assert result.is_supported
    assert ("円は描画しません" if lang == "ja" else "No tolerance circle is drawn") in result.text


@pytest.mark.parametrize("lang", ["ja", "en"])
@pytest.mark.parametrize("annotation_type", ["segmentation", "segmentation_v2"])
def test_追記モード無効でも塗りつぶしv2の通常作図は既存領域へ追記する(annotation_type, lang):
    # ViewLogic.setOperation と SegmentationToolProvider.finishEdit の Add/Append 分岐
    value = {
        "_type": "AnnotationEditorFeature",
        "append": False,
        "erase": False,
        "freehand": True,
        "rectangle_fill": False,
        "polygon_fill": False,
        "fill_near": False,
    }
    result = describe("annotation_editor_feature", value, annotation_type=annotation_type, lang=lang)
    assert result.is_supported
    assert ("作図モード「追記」の選択は無効" if lang == "ja" else "Selection of the append drawing mode is disabled") in result.text
    if annotation_type == "segmentation_v2":
        assert ("追記モードの設定にかかわらず" if lang == "ja" else "regardless of the append-mode setting") in result.text
        assert ("同じラベルの既存アノテーションへ追記" if lang == "ja" else "appends to an existing annotation of the same label") in result.text
    else:
        assert "segmentation_v2" not in result.text
        assert "塗りつぶしv2" not in result.text
