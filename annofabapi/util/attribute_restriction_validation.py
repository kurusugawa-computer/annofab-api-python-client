"""Simple Annotationの属性制約を、API通信せずに検証します。

Annofabの提出時検証の完全な再現ではありません。欠落・nullは空値として扱い、
デフォルト値は補完しません。正規表現にはPythonの ``re.fullmatch`` を使用します。
"""

import copy
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from annofabapi.util.annotation_specs import get_attribute_name_en, get_choice_name_en, get_label_name_en


@dataclass(frozen=True)
class AttributeRestrictionViolation:
    """違反したアノテーション・属性・トップレベル制約の組。"""

    annotation_id: str
    """評価対象のアノテーションID。"""
    attribute_id: str
    """制約対象の属性ID。"""
    attribute_name: str
    """制約対象の属性の英語名。Simple Annotationのattributesのキーに対応します。"""
    restriction_index: int
    """仕様の ``restrictions`` 内の0始まりの位置。"""


class AttributeRestrictionValidator:
    """v3の仕様に含まれる属性制約でSimple Annotationを検証します。

    同じインスタンスを複数の入力データに使えます。仕様は初期化時にコピーします。
    制約の適用先はラベルの属性定義で決定します。読取専用属性の制約と、
    結論がCanInputである制約は評価対象から除外します。

    Args:
        annotation_specs: APIのv3形式のアノテーション仕様の辞書。
    """

    def __init__(self, annotation_specs: Mapping[str, Any]) -> None:
        specs = copy.deepcopy(annotation_specs)
        self._labels = specs["labels"]
        self._attributes = {attribute["additional_data_definition_id"]: attribute for attribute in specs["additionals"]}
        self._restrictions = specs["restrictions"]

    def validate_simple_annotation_details(self, details: Iterable[Mapping[str, Any]]) -> list[AttributeRestrictionViolation]:
        """同一入力データに属するSimple Annotationのdetails全件を検証します。

        Args:
            details: 同一タスク・同一入力データの ``annotation["details"]`` 全件。
                リンク先の解決に使うため、ラベル等による絞り込み前の全件を渡してください。
                各要素にはannotation_id、label、attributesが必要です。

        Returns:
            アノテーション順・制約順の違反一覧。成立・適用対象外の制約は含めません。
            違反がない場合は空リストを返します。Implyでは後続条件の属性ID・英語名を返します。

        Raises:
            ValueError: 名前を一意に解決できない、条件を評価できない、
                または同一入力データ内でアノテーションIDが重複している場合。
            KeyError: 必須の入力フィールドがない場合。
        """
        annotations = list(details)
        by_id = {annotation["annotation_id"]: annotation for annotation in annotations}
        if len(by_id) != len(annotations):
            raise ValueError("アノテーションIDが重複しています。")
        results = []
        for annotation in annotations:
            # 必須フィールドの欠落は、制約違反とは区別して呼び出し側に通知します。
            annotation["label"]
            annotation["attributes"]
            for index, restriction in enumerate(self._restrictions):
                attribute_id = restriction["additional_data_definition_id"]
                attribute = self._attributes.get(attribute_id)
                if self._is_editability(restriction["condition"]) or (attribute is not None and attribute.get("read_only", False)):
                    continue
                label = self._find_label(annotation["label"])
                if attribute is None:
                    raise ValueError(f"属性IDが仕様にありません: {attribute_id}")
                if attribute_id not in label["additional_data_definitions"]:
                    continue
                if not self._evaluate(restriction, annotation, by_id):
                    results.append(AttributeRestrictionViolation(annotation["annotation_id"], attribute_id, get_attribute_name_en(attribute), index))
        return results

    def _find_label(self, name: str) -> Mapping[str, Any]:
        labels = [label for label in self._labels if get_label_name_en(label) == name]
        if len(labels) != 1:
            raise ValueError(f"ラベル名を一意に解決できません: {name!r}")
        return labels[0]

    @staticmethod
    def _is_editability(condition: Mapping[str, Any]) -> bool:
        while isinstance(condition, Mapping) and condition.get("_type") == "Imply":
            condition = condition.get("condition", {})
        return isinstance(condition, Mapping) and condition.get("_type") == "CanInput"

    def _evaluate(self, restriction: Mapping[str, Any], annotation: Mapping[str, Any], by_id: Mapping[str, Mapping[str, Any]]) -> bool:
        try:
            attribute_id = restriction["additional_data_definition_id"]
            condition = restriction["condition"]
            if condition["_type"] == "Imply":
                if not self._evaluate(condition["premise"], annotation, by_id):
                    return True
                return self._evaluate({"additional_data_definition_id": attribute_id, "condition": condition["condition"]}, annotation, by_id)
            return self._evaluate_atomic(attribute_id, condition, annotation, by_id)
        except (KeyError, TypeError, OverflowError, RecursionError, re.error) as exc:
            raise ValueError(f"条件を評価できません: {exc}") from exc

    def _attribute_value(self, attribute_id: str, annotation: Mapping[str, Any]) -> str | int | bool:
        attribute = self._attributes[attribute_id]
        label = self._find_label(annotation["label"])
        if attribute_id not in label["additional_data_definitions"]:
            raise ValueError(f"ラベルに属性がありません: {attribute_id}")
        name = get_attribute_name_en(attribute)
        same_name = [
            item
            for item_id, item in self._attributes.items()
            if item_id in label["additional_data_definitions"] and get_attribute_name_en(item) == name
        ]
        if len(same_name) != 1:
            raise ValueError(f"属性名を一意に解決できません: {name!r}")
        value = annotation["attributes"].get(name)
        attribute_type = attribute["type"]
        if attribute_type not in {"flag", "integer", "text", "comment", "tracking", "choice", "select", "link"}:
            raise ValueError(f"未対応の属性型です: {attribute_type!r}")
        if value is None or value == "":
            return False if attribute_type == "flag" else ""
        match attribute_type:
            case "flag" if type(value) is bool:
                return value
            case "integer" if type(value) is int or isinstance(value, str):
                return int(value)
            case "text" | "comment" | "tracking" | "link" if isinstance(value, str):
                return value
            case "choice" | "select" if isinstance(value, str):
                choices = [choice for choice in attribute["choices"] if get_choice_name_en(choice) == value]
                if len(choices) != 1:
                    raise ValueError(f"選択肢名を一意に解決できません: {value!r}")
                return str(choices[0]["choice_id"])
            case _:
                raise ValueError(f"属性型に適合しない値です: {name!r}={value!r}")

    def _evaluate_atomic(
        self, attribute_id: str, condition: Mapping[str, Any], annotation: Mapping[str, Any], by_id: Mapping[str, Mapping[str, Any]]
    ) -> bool:
        value = self._attribute_value(attribute_id, annotation)
        attribute_type = self._attributes[attribute_id]["type"]
        match condition["_type"]:
            case "Equals" | "NotEquals":
                expected = condition["value"]
                if not isinstance(expected, str):
                    raise TypeError("比較条件の値は文字列で指定してください。")
                match attribute_type:
                    case "flag":
                        if expected not in {"true", "false"}:
                            raise ValueError("チェックボックスの比較値はtrueまたはfalseで指定してください。")
                        equal = value == (expected == "true")
                    case "integer" if expected != "":
                        equal = value == int(expected)
                    case _:
                        equal = value == expected
                return equal if condition["_type"] == "Equals" else not equal
            case "Matches" | "NotMatches" if attribute_type in {"text", "comment"}:
                matches = re.fullmatch(condition["value"], str(value)) is not None
                return matches if condition["_type"] == "Matches" else not matches
            case "HasLabel" if attribute_type == "link":
                labels = condition["labels"]
                if not isinstance(labels, list) or any(not isinstance(label_id, str) for label_id in labels):
                    raise ValueError("HasLabelのlabelsにはラベルIDの配列を指定してください。")
                # 空リンクにラベル制約は適用しません。必須条件はNotEqualsで別途評価します。
                if value == "":
                    return True
                target = by_id.get(str(value))
                if target is None:
                    raise ValueError(f"リンク先が見つかりません: {value!r}")
                target_label = self._find_label(target["label"])
                return not labels or target_label["label_id"] in labels
            case _:
                raise ValueError(f"未対応の条件または属性型との組み合わせです: {condition['_type']!r}, {attribute_type!r}")
