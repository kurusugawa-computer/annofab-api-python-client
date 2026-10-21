"""ラベルの明示的な ``field_values`` を、仕様に基づく定型文で説明します。"""

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, TypeGuard


@dataclass(frozen=True)
class FieldValueDescription:
    """フィールドIDと、その設定全体の説明です。"""

    field_id: str
    """元の ``field_values`` のキー。コンテナ自体が不正な場合は ``field_values``。"""

    text: str
    """指定した言語の説明。未対応の場合は元のキー・値も含みます。"""

    is_supported: bool
    """設定全体を解釈できたかどうか。"""


_FIELD_TYPES = {
    "minimum_size_2d": ("MinimumSize2d", {"polygon", "polyline", "segmentation", "segmentation_v2"}),
    "minimum_size_2d_with_default_insert_position": ("MinimumSize2dWithDefaultInsertPosition", {"bounding_box"}),
    "minimum_area_2d": ("MinimumArea2d", {"polygon"}),
    "vertex_count_min_max": ("VertexCountMinMax", {"polygon", "polyline"}),
    "margin_of_error_tolerance": (
        "MarginOfErrorTolerance",
        {"bounding_box", "polygon", "polyline", "point", "segmentation", "segmentation_v2"},
    ),
    "display_line_direction": ("DisplayLineDirection", {"polyline"}),
    "annotation_editor_feature": ("AnnotationEditorFeature", {"segmentation", "segmentation_v2"}),
}
"""標準ラベルのフィールドID、値の型、適用可能なアノテーション種類です。"""

_EDITOR_FEATURES = {
    "append": ("追記", "append"),
    "erase": ("消しゴム", "eraser"),
    "freehand": ("フリーハンド", "freehand"),
    "rectangle_fill": ("矩形", "rectangle fill"),
    "polygon_fill": ("自由形状", "polygon fill"),
    "fill_near": ("近似色塗りつぶし", "similar-color fill"),
}
"""塗りつぶしの作図機能の表示名です。"""


def _text(ja: str, en: str, lang: Literal["ja", "en"]) -> str:
    return ja if lang == "ja" else en


def _integer(value: object, *, minimum: int = 0) -> TypeGuard[int]:
    return type(value) is int and value >= minimum


def _keys_match(value: Mapping[str, object], required: set[str], optional: set[str] | None = None) -> bool:
    keys = set(value) - {"_type"}
    return required <= keys <= required | (optional or set())


def _minimum_size(value: Mapping[str, object], *, annotation_type: str, lang: Literal["ja", "en"]) -> str | None:  # noqa: PLR0912
    with_position = annotation_type == "bounding_box"
    position_key = "position_for_minimum_bounding_box_insertion"
    if not _keys_match(value, {"min_warn_rule", "min_width", "min_height"}, {position_key} if with_position else set()):
        return None
    width, height = value["min_width"], value["min_height"]
    if not _integer(width) or not _integer(height):
        return None
    # 実際のレスポンスの判別子付きオブジェクトと、OpenAPIの文字列形式に対応します。
    rule = value["min_warn_rule"]
    match rule:
        case {"_type": "And", **rest} if not rest:
            rule = "and"
        case {"_type": "Or", **rest} if not rest:
            rule = "or"
    match rule:
        case "and":
            text = _text(
                f"幅が{width}ピクセル未満、かつ高さが{height}ピクセル未満の場合にサイズ制約の警告を表示します。",
                f"A size warning is shown when both width is less than {width} pixels and height is less than {height} pixels.",
                lang,
            )
        case "or":
            text = _text(
                f"幅が{width}ピクセル未満、または高さが{height}ピクセル未満の場合にサイズ制約の警告を表示します。",
                f"A size warning is shown when width is less than {width} pixels or height is less than {height} pixels.",
                lang,
            )
        case _:
            return None
    if annotation_type in {"segmentation", "segmentation_v2"}:
        measurement = _text(
            "幅・高さは塗りつぶし領域の外接矩形の大きさです。",
            "Width and height are measured using the filled region's axis-aligned bounding box. ",
            lang,
        )
    else:
        measurement = _text(
            "幅・高さは、頂点座標を整数に丸めて求める外接矩形の大きさです。",
            "Width and height are measured using the axis-aligned bounding box after rounding vertex coordinates to integers. ",
            lang,
        )
    text = measurement + text
    if annotation_type in {"polygon", "polyline"}:
        text += _text(
            "この最小サイズ制約は提出時にも検証され、違反すると提出できません。",
            " This minimum-size constraint is also checked on submission; a violation prevents submission.",
            lang,
        )
    else:
        text += _text(
            "このサイズ警告自体はタスクの提出・合格を妨げません。",
            " This size warning itself does not prevent task submission or acceptance.",
            lang,
        )
    if not with_position:
        return text
    insert_width, insert_height = max(width, 1), max(height, 1)
    if width == 0 or height == 0:
        text += _text(
            "矩形の挿入時は、0の幅・高さを1ピクセルに補正します。",
            " When inserting a box, a zero width or height is replaced with 1 pixel.",
            lang,
        )
    position = value.get(position_key)
    match position:
        case None:
            state = _text("省略", "omitted", lang) if position_key not in value else "null"
            text += _text(
                f"挿入位置は{state}です。作図モードで作図ボタンを押すと、幅{insert_width}・高さ{insert_height}ピクセルの矩形を、"
                "表示範囲の中央を基準に配置します。左上座標が0未満になる場合は、その座標を0に補正します。",
                f" The insertion position is {state}. In drawing mode, the drawing button creates a {insert_width} by {insert_height} pixel box"
                " positioned relative to the center of the visible canvas. Each negative top-left coordinate is clamped to 0.",
                lang,
            )
        case [x, y] if type(x) is int and type(y) is int:
            text += _text(
                f"作図モードで作図ボタンを押すと、画像左上を原点とする左上座標(x={x}, y={y})に"
                f"幅{insert_width}・高さ{insert_height}ピクセルの矩形を作成します。",
                f" In drawing mode, the drawing button creates a {insert_width} by {insert_height} pixel box"
                f" with top-left coordinates (x={x}, y={y}), relative to the top-left of the image.",
                lang,
            )
        case _:
            return None
    return text


def _vertex_count(value: Mapping[str, object], *, annotation_type: str, lang: Literal["ja", "en"]) -> str | None:
    if not _keys_match(value, set(), {"min", "max"}):
        return None
    minimum, maximum = value.get("min"), value.get("max")
    geometric_minimum = 3 if annotation_type == "polygon" else 2
    if minimum is not None and not _integer(minimum, minimum=geometric_minimum):
        return None
    if maximum is not None and not _integer(maximum, minimum=geometric_minimum):
        return None
    if isinstance(minimum, int) and isinstance(maximum, int) and minimum > maximum:
        return None
    lower_state = _text("省略", "omitted", lang) if "min" not in value else "null"
    upper_state = _text("省略", "omitted", lang) if "max" not in value else "null"
    lower = _text(
        f"頂点数の下限設定は{lower_state}（追加の下限制約なし）です。" if minimum is None else f"頂点数の下限は{minimum}個です。",
        f"The vertex-count lower bound is {lower_state} (no additional lower bound)."
        if minimum is None
        else f"The minimum vertex count is {minimum}.",
        lang,
    )
    upper = _text(
        f"頂点数の上限設定は{upper_state}（追加の上限制約なし）です。" if maximum is None else f"頂点数の上限は{maximum}個です。",
        f"The vertex-count upper bound is {upper_state} (no additional upper bound)."
        if maximum is None
        else f"The maximum vertex count is {maximum}.",
        lang,
    )
    text = lower + ("" if lang == "ja" else " ") + upper
    if minimum is not None or maximum is not None:
        text += _text(
            "この追加の頂点数制約に違反すると警告を表示します。この警告自体はタスクの提出・合格を妨げません。",
            " Violating these additional vertex-count bounds shows a warning. This warning itself does not prevent task submission or acceptance.",
            lang,
        )
    text += _text(
        f"図形自体に必要な{geometric_minimum}頂点未満の場合は、提出時にエラーになります。",
        f" Fewer than the {geometric_minimum} vertices required by the shape itself causes a submission error.",
        lang,
    )
    if annotation_type == "polygon":
        initial_vertices = maximum if isinstance(maximum, int) else max(minimum or 0, 16)
        text += _text(
            f"多角形作図ツールの頂点数の初期値は{initial_vertices}個です。",
            f" The initial vertex count for the polygon-by-rectangle drawing tool is {initial_vertices}.",
            lang,
        )
    return text


def _editor_features(value: Mapping[str, object], *, annotation_type: str, lang: Literal["ja", "en"]) -> str | None:
    if not _keys_match(value, set(_EDITOR_FEATURES)) or any(type(value[key]) is not bool for key in _EDITOR_FEATURES):
        return None
    texts = []
    for key, (ja, en) in _EDITOR_FEATURES.items():
        state_ja, state_en = ("有効", "enabled") if value[key] else ("無効", "disabled")
        if key in {"append", "erase"}:
            texts.append(_text(f"作図モード「{ja}」の選択は{state_ja}です。", f"Selection of the {en} drawing mode is {state_en}.", lang))
        else:
            texts.append(_text(f"作図ツール「{ja}」は{state_ja}です。", f"The {en} drawing tool is {state_en}.", lang))
    if value["append"] or value["erase"]:
        texts.append(
            _text(
                "追記・消しゴムモードを利用するには、編集可能な状態で対象アノテーションを選択する必要があります。",
                "Using append or eraser mode also requires editing permission and a selected target annotation.",
                lang,
            )
        )
    if annotation_type == "segmentation_v2":
        texts.append(
            _text(
                "塗りつぶしv2は追記モードの設定にかかわらず、通常の作図でも同じラベルの既存アノテーションへ追記します。",
                "For segmentation_v2, ordinary drawing also appends to an existing annotation of the same label,"
                " regardless of the append-mode setting.",
                lang,
            )
        )
    return ("" if lang == "ja" else " ").join(texts)


def _describe(  # noqa: PLR0911
    field_id: str, value: Mapping[str, object], *, annotation_type: str, lang: Literal["ja", "en"]
) -> str | None:
    match field_id:
        case "minimum_size_2d" | "minimum_size_2d_with_default_insert_position":
            return _minimum_size(value, annotation_type=annotation_type, lang=lang)
        case "vertex_count_min_max":
            return _vertex_count(value, annotation_type=annotation_type, lang=lang)
        case "annotation_editor_feature":
            return _editor_features(value, annotation_type=annotation_type, lang=lang)
        case "minimum_area_2d" if _keys_match(value, {"min_area"}) and _integer(value["min_area"], minimum=1):
            area = value["min_area"]
            return _text(
                f"ポリゴンの面積が{area}平方ピクセル未満の場合に警告を表示します。この面積警告自体はタスクの提出・合格を妨げません。",
                f"A warning is shown when the polygon area is less than {area} square pixels."
                " This area warning itself does not prevent task submission or acceptance.",
                lang,
            )
        case "margin_of_error_tolerance" if _keys_match(value, {"max_pixel"}) and _integer(value["max_pixel"]):
            pixels = value["max_pixel"]
            return _text(
                f"誤差許容範囲は{pixels}ピクセルです。この値による誤差の自動検証は行いません。"
                + (
                    "0の場合、許容範囲の円は描画しません。"
                    if pixels == 0
                    else "画像エディタの許容範囲表示を有効にすると、カーソル付近に許容範囲を表す円を表示します。"
                ),
                f"The error tolerance is {pixels} pixels. This value is not used to automatically validate annotation errors. "
                + (
                    "No tolerance circle is drawn when the value is 0."
                    if pixels == 0
                    else "Enabling tolerance display in the image editor shows a tolerance circle near the cursor."
                ),
                lang,
            )
        case "display_line_direction" if _keys_match(value, {"has_direction"}) and type(value["has_direction"]) is bool:
            if value["has_direction"]:
                return _text(
                    "ポリラインの向きの表示を有効にします。ただし、エディタ側で線の向きを非表示にしている場合は表示されません。",
                    "Polyline direction display is enabled, but the editor's hide-line-direction setting can hide it.",
                    lang,
                )
            return _text("ポリラインの向きを表示しません。", "The polyline direction is not displayed.", lang)
        case _:
            return None


def _unsupported(field_id: str, value: object, *, reason_ja: str, reason_en: str, lang: Literal["ja", "en"]) -> FieldValueDescription:
    original = json.dumps({field_id: value}, ensure_ascii=False)
    text = _text(
        f"この設定は解釈できません（{reason_ja}）。元のキーと値: {original}",
        f"Cannot interpret this setting ({reason_en}). Original key and value: {original}",
        lang,
    )
    return FieldValueDescription(field_id=field_id, text=text, is_supported=False)


def describe_label_field_values(label: Mapping[str, object], *, lang: Literal["ja", "en"] = "en") -> list[FieldValueDescription]:
    """ラベルに明示された図形設定を日本語または英語で説明します。

    ラベルのJSONを直接受け取り、設定ごとの説明を入力順に返します。
    未対応のキー・型・値、適用外の種類、未知の入れ子の項目がある設定は、
    設定全体を未対応として元のキー・値を説明に残します。
    省略された設定の既定動作は補完しません。入力は変更しません。
    対応範囲と仕様確認元はユーザーガイドの「ラベルの図形設定の説明」を参照してください。

    Args:
        label: ``annotation_type`` を含むラベルJSON。``field_values`` は省略可能です。
            値はJSONで表現可能である必要があります。
        lang: 説明の言語。``ja`` または ``en``。

    Returns:
        フィールドID・説明・対応可否の一覧。``field_values`` の省略・空オブジェクトは空リスト。
        ``field_values`` 自体がnullなどの場合は、そのコンテナを未対応として説明します。

    Raises:
        ValueError: 対応していない言語を指定した場合。
        KeyError: ``annotation_type`` がない場合。
    """
    if lang not in {"ja", "en"}:
        raise ValueError(f"対応していない言語です: {lang}")
    annotation_type = label["annotation_type"]
    if "field_values" not in label:
        return []
    fields = label["field_values"]
    if not isinstance(fields, Mapping):
        return [_unsupported("field_values", fields, reason_ja="オブジェクトではありません", reason_en="not an object", lang=lang)]
    descriptions = []
    for field_id, value in fields.items():
        if field_id not in _FIELD_TYPES:
            descriptions.append(_unsupported(field_id, value, reason_ja="未対応のフィールドIDです", reason_en="unsupported field ID", lang=lang))
            continue
        expected_type, annotation_types = _FIELD_TYPES[field_id]
        if not isinstance(annotation_type, str) or annotation_type not in annotation_types:
            descriptions.append(
                _unsupported(
                    field_id,
                    value,
                    reason_ja=f"annotation_type={annotation_type!r}への適用は未対応です",
                    reason_en=f"application to annotation_type={annotation_type!r} is unsupported",
                    lang=lang,
                )
            )
            continue
        text = None
        if isinstance(value, Mapping) and value.get("_type") == expected_type:
            text = _describe(field_id, value, annotation_type=annotation_type, lang=lang)
        if text is None:
            descriptions.append(
                _unsupported(
                    field_id,
                    value,
                    reason_ja="未対応の型・値・項目、または必須項目の欠落があります",
                    reason_en="unsupported type, value or member, or a missing required member",
                    lang=lang,
                )
            )
        else:
            descriptions.append(FieldValueDescription(field_id=field_id, text=text, is_supported=True))
    return descriptions
