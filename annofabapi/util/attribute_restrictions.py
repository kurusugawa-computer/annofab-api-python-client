"""
属性の制約に関するモジュール。

以下のサンプルコードのように属性名で制約情報を出力できます。

Example:
    >>> import annofabapi
    >>> from annofabapi.util.attribute_restrictions import AttributeFactory
    >>> service = annofabapi.build()
    >>> annotation_specs, _ = service.api.get_annotation_specs("prj1", query_params={"v": "3"})
    >>> fac = AttributeFactory(annotation_specs)

    >>> premise_restriction = fac.checkbox(attribute_name="occluded").checked()
    >>> conclusion_restriction = fac.string_textbox(attribute_name="note").is_not_empty()
    >>> restriction = premise_restriction.imply(conclusion_restriction)
    >>> restriction.to_dict()
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
"""

from abc import ABC, abstractmethod
from collections.abc import Collection
from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict
from annofabapi.util.annotation_specs import AnnotationSpecsAccessor, get_choice, get_english_message

RestrictionAstType = Literal[
    "checked",
    "unchecked",
    "is_empty",
    "is_not_empty",
    "equals_string",
    "not_equals_string",
    "matches_string",
    "not_matches_string",
    "equals_integer",
    "not_equals_integer",
    "has_choice",
    "not_has_choice",
    "has_label",
    "can_input",
    "imply",
]


class Restriction(ABC):
    """属性の制約を表すクラス。"""

    def __init__(self, attribute_id: str) -> None:
        self.attribute_id = attribute_id

    def to_dict(self) -> dict[str, Any]:
        """
        アノテーション仕様の`restrictions`に格納できるdictを出力します。

        Returns:
            `restrictions` に格納できる辞書形式の制約情報です。
        """
        return {"additional_data_definition_id": self.attribute_id, "condition": self._to_dict_only_condition()}

    @classmethod
    def from_dict(cls, obj: dict[str, Any], annotation_specs: dict[str, Any] | None = None) -> "Restriction":
        """
        dictからRestrictionオブジェクトを復元します。

        Args:
            obj: `restrictions` の1要素を表す辞書です。
            annotation_specs: Noneでなければ、アノテーション仕様を用いて属性型ごとの妥当性を検証します。

        Returns:
            復元した `Restriction` オブジェクトです。

        Raises:
            ValueError: 制約の形式が不正な場合、または `annotation_specs` を使った妥当性検証に失敗した場合
        """
        fac = AttributeFactory(annotation_specs) if annotation_specs is not None else None
        return _from_restriction_dict(obj, fac=fac)

    def to_python_expr(self, annotation_specs: dict[str, Any], *, factory_name: str = "fac") -> str:
        """
        Restrictionオブジェクトを、高水準APIに近いPython式へ変換します。

        Args:
            annotation_specs: アノテーション仕様(v3)の情報です。
            factory_name: `AttributeFactory` の変数名です。

        Returns:
            高水準APIに近い Python 式です。

        Raises:
            ValueError: 高水準APIの式へ変換できない制約が含まれている場合
        """
        accessor = AnnotationSpecsAccessor(annotation_specs)
        return _restriction_to_python_expr(self, accessor=accessor, factory_name=factory_name)

    def to_ast(self, annotation_specs: dict[str, Any]) -> "RestrictionAst":
        """
        Restrictionオブジェクトを、LLMやCLIで扱いやすい意味ベースのASTへ変換します。

        Args:
            annotation_specs: アノテーション仕様(v3)の情報です。

        Returns:
            名前ベースで表現された `RestrictionAst` です。
        """
        accessor = AnnotationSpecsAccessor(annotation_specs)
        return _restriction_to_ast(self, accessor=accessor)

    def to_human_readable(self, annotation_specs: dict[str, Any]) -> str:
        """
        Restrictionオブジェクトを、人にとって読みやすい文字列表現へ変換します。

        Args:
            annotation_specs: アノテーション仕様(v3)の情報です。

        Returns:
            CLIなどで表示しやすい文字列表現です。
        """
        return self.to_ast(annotation_specs).to_human_readable()

    @classmethod
    def from_ast(cls, ast: "RestrictionAst", annotation_specs: dict[str, Any]) -> "Restriction":
        """
        意味ベースのASTからRestrictionオブジェクトを復元します。

        Args:
            ast: 復元元の `RestrictionAst` です。
            annotation_specs: アノテーション仕様(v3)の情報です。

        Returns:
            復元した `Restriction` オブジェクトです。
        """
        return ast.to_restriction(annotation_specs)

    @abstractmethod
    def _to_dict_only_condition(self) -> dict[str, Any]:
        """
        制約の条件部分のみdictで出力します。

        Returns:
            制約の条件部分のみを表す辞書です。
        """

    def imply(self, conclusion_restriction: "Restriction") -> "Restriction":
        return Imply(premise_restriction=self, conclusion_restriction=conclusion_restriction)


class Imply(Restriction):
    """
    「AならB」という制約を表すクラス。

    Args:
        premise_restriction: 前提となる制約です。
        conclusion_restriction: 最終的に満たしたい制約です。
    """

    def __init__(self, premise_restriction: Restriction, conclusion_restriction: Restriction) -> None:
        super().__init__(conclusion_restriction.attribute_id)
        self.premise_restriction = premise_restriction
        self.conclusion_restriction = conclusion_restriction

    def imply(self, conclusion_restriction: "Restriction") -> "Restriction":
        raise NotImplementedError("`imply`メソッドの戻り値に対して`imply`メソッドを実行できません。")

    def _to_dict_only_condition(self) -> dict[str, Any]:
        return {"_type": "Imply", "premise": self.premise_restriction.to_dict(), "condition": self.conclusion_restriction._to_dict_only_condition()}


class CanInput(Restriction):
    def __init__(self, attribute_id: str, enable: bool) -> None:
        super().__init__(attribute_id)
        self.enable = enable

    def _to_dict_only_condition(self) -> dict[str, Any]:
        return {"_type": "CanInput", "enable": self.enable}


class Equals(Restriction):
    def __init__(self, attribute_id: str, value: str) -> None:
        super().__init__(attribute_id)
        self.value = value

    def _to_dict_only_condition(self) -> dict[str, Any]:
        return {"_type": "Equals", "value": self.value}


class NotEquals(Restriction):
    def __init__(self, attribute_id: str, value: str) -> None:
        super().__init__(attribute_id)
        self.value = value

    def _to_dict_only_condition(self) -> dict[str, Any]:
        return {"_type": "NotEquals", "value": self.value}


class Matches(Restriction):
    def __init__(self, attribute_id: str, value: str) -> None:
        super().__init__(attribute_id)
        self.value = value

    def _to_dict_only_condition(self) -> dict[str, Any]:
        return {"_type": "Matches", "value": self.value}


class NotMatches(Restriction):
    def __init__(self, attribute_id: str, value: str) -> None:
        super().__init__(attribute_id)
        self.value = value

    def _to_dict_only_condition(self) -> dict[str, Any]:
        return {"_type": "NotMatches", "value": self.value}


class HasLabel(Restriction):
    def __init__(self, attribute_id: str, label_ids: Collection[str]) -> None:
        super().__init__(attribute_id)
        self.label_ids = label_ids

    def _to_dict_only_condition(self) -> dict[str, Any]:
        return {"_type": "HasLabel", "labels": list(self.label_ids)}


class EmptyCheckMixin:
    """属性が空かどうかを判定するメソッドを提供するMix-inクラス"""

    attribute_id: str

    def is_empty(self) -> Restriction:
        """属性値が空であるという制約"""
        return Equals(self.attribute_id, value="")

    def is_not_empty(self) -> Restriction:
        """属性値が空でないという制約"""
        return NotEquals(self.attribute_id, value="")


class Attribute(ABC):
    def __init__(self, accessor: AnnotationSpecsAccessor, *, attribute_id: str | None = None, attribute_name: str | None = None) -> None:
        self.accessor = accessor
        self.attribute = self.accessor.get_attribute(attribute_id=attribute_id, attribute_name=attribute_name)
        self.attribute_id = self.attribute["additional_data_definition_id"]
        if self._is_valid_attribute_type() is False:
            raise ValueError(f"属性の種類が'{self.attribute['type']}'である属性は、クラス'{self.__class__.__name__}'では扱えません。")

    def enabled(self) -> Restriction:
        """属性値を入力できるという制約"""
        return CanInput(self.attribute_id, enable=True)

    def disabled(self) -> Restriction:
        """属性値を入力できないという制約"""
        return CanInput(self.attribute_id, enable=False)

    @abstractmethod
    def _is_valid_attribute_type(self) -> bool:
        pass


class Checkbox(Attribute):
    """チェックボックスの属性"""

    def checked(self) -> Restriction:
        """チェックされているという制約"""
        return Equals(self.attribute_id, "true")

    def unchecked(self) -> Restriction:
        """チェックされていないという制約"""
        return NotEquals(self.attribute_id, "true")

    def _is_valid_attribute_type(self) -> bool:
        return self.attribute["type"] == "flag"


class StringTextbox(Attribute, EmptyCheckMixin):
    """文字列用のテキストボックス（自由記述）の属性"""

    def _is_valid_attribute_type(self) -> bool:
        return self.attribute["type"] in {"text", "comment"}

    def equals(self, value: str) -> Restriction:
        """引数`value`に渡された文字列に一致するという制約"""
        return Equals(self.attribute_id, value)

    def not_equals(self, value: str) -> Restriction:
        """引数`value`に渡された文字列に一致しないという制約"""
        return NotEquals(self.attribute_id, value)

    def matches(self, value: str) -> Restriction:
        """引数`value`に渡された正規表現に一致するという制約"""
        return Matches(self.attribute_id, value)

    def not_matches(self, value: str) -> Restriction:
        """引数`value`に渡された正規表現に一致しないという制約"""
        return NotMatches(self.attribute_id, value)


class IntegerTextbox(Attribute, EmptyCheckMixin):
    """整数用のテキストボックスの属性"""

    def _is_valid_attribute_type(self) -> bool:
        return self.attribute["type"] == "integer"

    def equals(self, value: int) -> Restriction:
        """引数`value`に渡された整数に一致するという制約"""
        return Equals(self.attribute_id, str(value))

    def not_equals(self, value: int) -> Restriction:
        """引数`value`に渡された整数に一致しないという制約"""
        return NotEquals(self.attribute_id, str(value))


class AnnotationLink(Attribute, EmptyCheckMixin):
    """アノテーションリンク属性"""

    def _is_valid_attribute_type(self) -> bool:
        return self.attribute["type"] == "link"

    def has_label(self, label_ids: Collection[str] | None = None, label_names: Collection[str] | None = None) -> Restriction:
        """リンク先のアノテーションが、引数`label_ids`または`label_names`に一致するラベルであるという制約"""
        if label_ids is not None:
            labels = [self.accessor.get_label(label_id=label_id) for label_id in label_ids]
        elif label_names is not None:
            labels = [self.accessor.get_label(label_name=label_name) for label_name in label_names]
        else:
            raise ValueError("label_idsまたはlabel_namesのいずれかを指定してください。")

        return HasLabel(self.attribute_id, label_ids=[label["label_id"] for label in labels])


class TrackingId(Attribute, EmptyCheckMixin):
    """トラッキングID属性"""

    def _is_valid_attribute_type(self) -> bool:
        return self.attribute["type"] == "tracking"

    def equals(self, value: str) -> Restriction:
        """引数`value`に渡された文字列に一致するという制約"""
        return Equals(self.attribute_id, value)

    def not_equals(self, value: str) -> Restriction:
        """引数`value`に渡された文字列に一致しないという制約"""
        return NotEquals(self.attribute_id, value)


class Selection(Attribute, EmptyCheckMixin):
    """排他選択の属性（ドロップダウンまたラジオボタン）"""

    def _is_valid_attribute_type(self) -> bool:
        return self.attribute["type"] in {"choice", "select"}

    def has_choice(self, *, choice_id: str | None = None, choice_name: str | None = None) -> Restriction:
        """引数`choice_id`または`choice_name`に一致する選択肢が選択されているという制約"""
        choices = self.attribute["choices"]
        choice = get_choice(choices, choice_id=choice_id, choice_name=choice_name)
        return Equals(self.attribute_id, choice["choice_id"])

    def not_has_choice(self, *, choice_id: str | None = None, choice_name: str | None = None) -> Restriction:
        """引数`choice_id`または`choice_name`に一致する選択肢が選択されていないという制約"""
        choices = self.attribute["choices"]
        choice = get_choice(choices, choice_id=choice_id, choice_name=choice_name)
        return NotEquals(self.attribute_id, choice["choice_id"])


class AttributeFactory:
    """
    属性を生成するためのFactoryクラス。

    Args:
        annotation_specs: アノテーション仕様(v3)の情報です。
    """

    def __init__(self, annotation_specs: dict[str, Any]) -> None:
        self.accessor = AnnotationSpecsAccessor(annotation_specs)

    def checkbox(self, *, attribute_id: str | None = None, attribute_name: str | None = None) -> Checkbox:
        return Checkbox(self.accessor, attribute_id=attribute_id, attribute_name=attribute_name)

    def string_textbox(self, *, attribute_id: str | None = None, attribute_name: str | None = None) -> StringTextbox:
        return StringTextbox(self.accessor, attribute_id=attribute_id, attribute_name=attribute_name)

    def integer_textbox(self, *, attribute_id: str | None = None, attribute_name: str | None = None) -> IntegerTextbox:
        return IntegerTextbox(self.accessor, attribute_id=attribute_id, attribute_name=attribute_name)

    def annotation_link(self, *, attribute_id: str | None = None, attribute_name: str | None = None) -> AnnotationLink:
        return AnnotationLink(self.accessor, attribute_id=attribute_id, attribute_name=attribute_name)

    def tracking_id(self, *, attribute_id: str | None = None, attribute_name: str | None = None) -> TrackingId:
        return TrackingId(self.accessor, attribute_id=attribute_id, attribute_name=attribute_name)

    def selection(self, *, attribute_id: str | None = None, attribute_name: str | None = None) -> Selection:
        return Selection(self.accessor, attribute_id=attribute_id, attribute_name=attribute_name)


@dataclass(frozen=True)
class RestrictionAst:
    """
    LLMやCLI向けの意味ベースな属性制約ASTを表すクラス。

    `type` に応じて必要なフィールドが変わります。例えば `checked` では
    `attribute_name` を使い、`imply` では `premise` と `conclusion` を使います。

    Args:
        type: ASTノードの種類です。
        attribute_name: 対象属性の名前です。
        value: 文字列や整数の比較値です。
        choice_name: 選択肢名です。
        enable: `can_input` ノードで使う真偽値です。
        label_names: `has_label` ノードで使うラベル名の一覧です。
        premise: `imply` ノードの前提です。
        conclusion: `imply` ノードの結論です。
    """

    type: str
    attribute_name: str | None = None
    value: str | int | None = None
    choice_name: str | None = None
    enable: bool | None = None
    label_names: list[str] | None = None
    premise: "RestrictionAst | None" = None
    conclusion: "RestrictionAst | None" = None

    def __post_init__(self) -> None:
        _validate_restriction_ast(self)

    def to_dict(self) -> dict[str, Any]:
        """
        ASTをJSONシリアライズしやすい辞書へ変換します。

        Returns:
            辞書形式のASTです。
        """
        result: dict[str, Any] = {"type": self.type}
        if self.attribute_name is not None:
            result["attribute_name"] = self.attribute_name
        if self.value is not None:
            result["value"] = self.value
        if self.choice_name is not None:
            result["choice_name"] = self.choice_name
        if self.enable is not None:
            result["enable"] = self.enable
        if self.label_names is not None:
            result["label_names"] = self.label_names
        if self.premise is not None:
            result["premise"] = self.premise.to_dict()
        if self.conclusion is not None:
            result["conclusion"] = self.conclusion.to_dict()
        return result

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> "RestrictionAst":
        """
        辞書からASTを復元します。

        Args:
            obj: ASTを表す辞書です。

        Returns:
            復元した `RestrictionAst` です。
        """
        premise = cls.from_dict(obj["premise"]) if obj.get("premise") is not None else None
        conclusion = cls.from_dict(obj["conclusion"]) if obj.get("conclusion") is not None else None
        return cls(
            type=obj["type"],
            attribute_name=obj.get("attribute_name"),
            value=obj.get("value"),
            choice_name=obj.get("choice_name"),
            enable=obj.get("enable"),
            label_names=obj.get("label_names"),
            premise=premise,
            conclusion=conclusion,
        )

    def to_restriction(self, annotation_specs: dict[str, Any]) -> Restriction:
        """
        ASTをRestrictionオブジェクトへコンパイルします。

        Args:
            annotation_specs: アノテーション仕様(v3)の情報です。

        Returns:
            コンパイル後の `Restriction` オブジェクトです。
        """
        fac = AttributeFactory(annotation_specs)
        return _ast_to_restriction(self, fac=fac)

    def to_human_readable(self) -> str:
        """
        ASTを人間向けの読みやすい文字列へ変換します。

        Returns:
            CLIなどで表示しやすい文字列表現です。
        """
        return _ast_to_human_readable(self)


class AttributeRestrictionCatalogItem(BaseModel):
    """
    LLMへ渡す属性制約カタログの1要素を表すモデル。

    Args:
        attribute_name: 属性名です。
        attribute_type: 属性種類です。
        allowed_ast_types: その属性で利用できるAST種別の一覧です。
        choice_names: 選択系属性で利用できる選択肢名の一覧です。
        label_names: リンク属性で利用できるラベル名の一覧です。
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    attribute_name: str
    attribute_type: str
    allowed_ast_types: list[RestrictionAstType]
    choice_names: list[str] | None = None
    label_names: list[str] | None = None


def get_attribute_restriction_catalog(annotation_specs: dict[str, Any]) -> list[AttributeRestrictionCatalogItem]:
    """
    属性制約ASTを組み立てるための属性カタログを返します。

    Args:
        annotation_specs: アノテーション仕様(v3)の情報です。

    Returns:
        LLMへのプロンプトや入力候補生成に使いやすい属性カタログです。
    """
    accessor = AnnotationSpecsAccessor(annotation_specs)
    catalog: list[AttributeRestrictionCatalogItem] = []
    for attribute in accessor.additionals:
        attribute_type = attribute["type"]
        item = AttributeRestrictionCatalogItem(
            attribute_name=get_english_message(attribute["name"]),
            attribute_type=attribute_type,
            allowed_ast_types=_get_allowed_ast_types(attribute_type),
        )
        if attribute_type in {"choice", "select"}:
            item = item.model_copy(update={"choice_names": [get_english_message(choice["name"]) for choice in attribute["choices"]]})
        if attribute_type == "link":
            item = item.model_copy(update={"label_names": [get_english_message(label["label_name"]) for label in accessor.labels]})
        catalog.append(item)
    return catalog


def _from_restriction_dict(obj: dict[str, Any], *, fac: AttributeFactory | None) -> Restriction:
    attribute_id = obj["additional_data_definition_id"]
    condition = obj["condition"]
    return _from_condition_dict(attribute_id=attribute_id, condition=condition, fac=fac)


def _validate_restriction_ast(ast: RestrictionAst) -> None:
    type_to_fields = {
        "checked": {"attribute_name"},
        "unchecked": {"attribute_name"},
        "is_empty": {"attribute_name"},
        "is_not_empty": {"attribute_name"},
        "equals_string": {"attribute_name", "value"},
        "not_equals_string": {"attribute_name", "value"},
        "matches_string": {"attribute_name", "value"},
        "not_matches_string": {"attribute_name", "value"},
        "equals_integer": {"attribute_name", "value"},
        "not_equals_integer": {"attribute_name", "value"},
        "has_choice": {"attribute_name", "choice_name"},
        "not_has_choice": {"attribute_name", "choice_name"},
        "has_label": {"attribute_name", "label_names"},
        "can_input": {"attribute_name", "enable"},
        "imply": {"premise", "conclusion"},
    }
    required_fields = type_to_fields.get(ast.type)
    if required_fields is None:
        raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")

    actual_fields = {
        field_name
        for field_name, value in (
            ("attribute_name", ast.attribute_name),
            ("value", ast.value),
            ("choice_name", ast.choice_name),
            ("enable", ast.enable),
            ("label_names", ast.label_names),
            ("premise", ast.premise),
            ("conclusion", ast.conclusion),
        )
        if value is not None
    }
    if actual_fields != required_fields:
        raise ValueError(
            f"AST種別'{ast.type}'のフィールドが不正です。 :: required={sorted(required_fields)}, actual={sorted(actual_fields)}"
        )

    if ast.type in {"equals_string", "not_equals_string", "matches_string", "not_matches_string"} and not isinstance(ast.value, str):
        raise ValueError(f"AST種別'{ast.type}'の'value'は文字列である必要があります。")
    if ast.type in {"equals_integer", "not_equals_integer"} and not isinstance(ast.value, int):
        raise ValueError(f"AST種別'{ast.type}'の'value'は整数である必要があります。")
    if ast.type in {"has_choice", "not_has_choice"} and not isinstance(ast.choice_name, str):
        raise ValueError(f"AST種別'{ast.type}'の'choice_name'は文字列である必要があります。")
    if ast.type == "has_label":
        if not isinstance(ast.label_names, list) or any(not isinstance(label_name, str) for label_name in ast.label_names):
            raise ValueError("AST種別'has_label'の'label_names'は文字列のリストである必要があります。")
    if ast.type == "can_input" and not isinstance(ast.enable, bool):
        raise ValueError("AST種別'can_input'の'enable'は真偽値である必要があります。")


def _get_allowed_ast_types(attribute_type: str) -> list[RestrictionAstType]:
    if attribute_type == "flag":
        return ["can_input", "checked", "unchecked"]
    if attribute_type in {"text", "comment"}:
        return ["can_input", "is_empty", "is_not_empty", "equals_string", "not_equals_string", "matches_string", "not_matches_string"]
    if attribute_type == "integer":
        return ["can_input", "is_empty", "is_not_empty", "equals_integer", "not_equals_integer"]
    if attribute_type == "link":
        return ["can_input", "is_empty", "is_not_empty", "has_label"]
    if attribute_type == "tracking":
        return ["can_input", "is_empty", "is_not_empty", "equals_string", "not_equals_string"]
    if attribute_type in {"choice", "select"}:
        return ["can_input", "is_empty", "is_not_empty", "has_choice", "not_has_choice"]
    raise ValueError(f"未対応の属性種類です。 :: attribute_type='{attribute_type}'")


def _from_condition_dict(*, attribute_id: str, condition: dict[str, Any], fac: AttributeFactory | None) -> Restriction:
    condition_type = condition["_type"]
    if condition_type == "Imply":
        premise_restriction = _from_restriction_dict(condition["premise"], fac=fac)
        conclusion_restriction = _from_condition_dict(attribute_id=attribute_id, condition=condition["condition"], fac=fac)
        return Imply(premise_restriction=premise_restriction, conclusion_restriction=conclusion_restriction)

    if fac is None:
        return _from_condition_dict_without_validation(attribute_id=attribute_id, condition=condition)
    return _from_condition_dict_with_validation(attribute_id=attribute_id, condition=condition, fac=fac)


def _from_condition_dict_without_validation(*, attribute_id: str, condition: dict[str, Any]) -> Restriction:
    condition_type = condition["_type"]
    if condition_type == "CanInput":
        return CanInput(attribute_id, enable=condition["enable"])
    if condition_type == "Equals":
        return Equals(attribute_id, value=condition["value"])
    if condition_type == "NotEquals":
        return NotEquals(attribute_id, value=condition["value"])
    if condition_type == "Matches":
        return Matches(attribute_id, value=condition["value"])
    if condition_type == "NotMatches":
        return NotMatches(attribute_id, value=condition["value"])
    if condition_type == "HasLabel":
        return HasLabel(attribute_id, label_ids=condition["labels"])
    raise ValueError(f"未知の制約種別です。 :: _type='{condition_type}'")


def _from_condition_dict_with_validation(*, attribute_id: str, condition: dict[str, Any], fac: AttributeFactory) -> Restriction:
    attribute = fac.accessor.get_attribute(attribute_id=attribute_id)
    attribute_obj = _create_attribute_object(fac, attribute)
    attribute_type = attribute["type"]
    condition_type = condition["_type"]

    if condition_type == "CanInput":
        return attribute_obj.enabled() if condition["enable"] else attribute_obj.disabled()

    if attribute_type == "flag":
        if condition_type == "Equals" and condition["value"] == "true":
            return attribute_obj.checked()
        if condition_type == "NotEquals" and condition["value"] == "true":
            return attribute_obj.unchecked()
        _raise_invalid_restriction(attribute=attribute, condition=condition)

    if attribute_type in {"text", "comment"}:
        if condition_type == "Equals":
            return attribute_obj.equals(condition["value"])
        if condition_type == "NotEquals":
            return attribute_obj.not_equals(condition["value"])
        if condition_type == "Matches":
            return attribute_obj.matches(condition["value"])
        if condition_type == "NotMatches":
            return attribute_obj.not_matches(condition["value"])
        _raise_invalid_restriction(attribute=attribute, condition=condition)

    if attribute_type == "integer":
        if condition_type == "Equals":
            if condition["value"] == "":
                return attribute_obj.is_empty()
            return attribute_obj.equals(_parse_integer_value(condition["value"], attribute=attribute, condition=condition))
        if condition_type == "NotEquals":
            if condition["value"] == "":
                return attribute_obj.is_not_empty()
            return attribute_obj.not_equals(_parse_integer_value(condition["value"], attribute=attribute, condition=condition))
        _raise_invalid_restriction(attribute=attribute, condition=condition)

    if attribute_type == "link":
        if condition_type == "HasLabel":
            return attribute_obj.has_label(label_ids=condition["labels"])
        if condition_type == "Equals" and condition["value"] == "":
            return attribute_obj.is_empty()
        if condition_type == "NotEquals" and condition["value"] == "":
            return attribute_obj.is_not_empty()
        _raise_invalid_restriction(attribute=attribute, condition=condition)

    if attribute_type == "tracking":
        if condition_type == "Equals":
            if condition["value"] == "":
                return attribute_obj.is_empty()
            return attribute_obj.equals(condition["value"])
        if condition_type == "NotEquals":
            if condition["value"] == "":
                return attribute_obj.is_not_empty()
            return attribute_obj.not_equals(condition["value"])
        _raise_invalid_restriction(attribute=attribute, condition=condition)

    if attribute_type in {"choice", "select"}:
        if condition_type == "Equals":
            if condition["value"] == "":
                return attribute_obj.is_empty()
            return attribute_obj.has_choice(choice_id=condition["value"])
        if condition_type == "NotEquals":
            if condition["value"] == "":
                return attribute_obj.is_not_empty()
            return attribute_obj.not_has_choice(choice_id=condition["value"])
        _raise_invalid_restriction(attribute=attribute, condition=condition)

    raise ValueError(f"未対応の属性種類です。 :: attribute_type='{attribute_type}'")


def _create_attribute_object(fac: AttributeFactory, attribute: dict[str, Any]) -> Attribute:
    attribute_id = attribute["additional_data_definition_id"]
    attribute_type = attribute["type"]
    if attribute_type == "flag":
        return fac.checkbox(attribute_id=attribute_id)
    if attribute_type in {"text", "comment"}:
        return fac.string_textbox(attribute_id=attribute_id)
    if attribute_type == "integer":
        return fac.integer_textbox(attribute_id=attribute_id)
    if attribute_type == "link":
        return fac.annotation_link(attribute_id=attribute_id)
    if attribute_type == "tracking":
        return fac.tracking_id(attribute_id=attribute_id)
    if attribute_type in {"choice", "select"}:
        return fac.selection(attribute_id=attribute_id)
    raise ValueError(f"未対応の属性種類です。 :: attribute_type='{attribute_type}'")


def _create_attribute_object_with_name(fac: AttributeFactory, attribute_name: str) -> Attribute:
    attribute = fac.accessor.get_attribute(attribute_name=attribute_name)
    return _create_attribute_object(fac, attribute)


def _ast_to_restriction(ast: RestrictionAst, *, fac: AttributeFactory) -> Restriction:
    if ast.type == "imply":
        assert ast.premise is not None
        assert ast.conclusion is not None
        premise_restriction = _ast_to_restriction(ast.premise, fac=fac)
        conclusion_restriction = _ast_to_restriction(ast.conclusion, fac=fac)
        return premise_restriction.imply(conclusion_restriction)

    assert ast.attribute_name is not None
    attribute = fac.accessor.get_attribute(attribute_name=ast.attribute_name)
    attribute_type = attribute["type"]

    if ast.type == "checked":
        return fac.checkbox(attribute_name=ast.attribute_name).checked()
    if ast.type == "unchecked":
        return fac.checkbox(attribute_name=ast.attribute_name).unchecked()
    if ast.type == "is_empty":
        return _attribute_with_empty_check(fac, ast.attribute_name).is_empty()
    if ast.type == "is_not_empty":
        return _attribute_with_empty_check(fac, ast.attribute_name).is_not_empty()
    if ast.type == "can_input":
        assert ast.enable is not None
        attribute_obj = _create_attribute_object_with_name(fac, ast.attribute_name)
        return attribute_obj.enabled() if ast.enable else attribute_obj.disabled()
    if ast.type == "equals_string":
        assert isinstance(ast.value, str)
        if attribute_type in {"text", "comment"}:
            return fac.string_textbox(attribute_name=ast.attribute_name).equals(ast.value)
        if attribute_type == "tracking":
            return fac.tracking_id(attribute_name=ast.attribute_name).equals(ast.value)
        _raise_invalid_ast(attribute=attribute, ast=ast)
    if ast.type == "not_equals_string":
        assert isinstance(ast.value, str)
        if attribute_type in {"text", "comment"}:
            return fac.string_textbox(attribute_name=ast.attribute_name).not_equals(ast.value)
        if attribute_type == "tracking":
            return fac.tracking_id(attribute_name=ast.attribute_name).not_equals(ast.value)
        _raise_invalid_ast(attribute=attribute, ast=ast)
    if ast.type == "matches_string":
        assert isinstance(ast.value, str)
        if attribute_type in {"text", "comment"}:
            return fac.string_textbox(attribute_name=ast.attribute_name).matches(ast.value)
        _raise_invalid_ast(attribute=attribute, ast=ast)
    if ast.type == "not_matches_string":
        assert isinstance(ast.value, str)
        if attribute_type in {"text", "comment"}:
            return fac.string_textbox(attribute_name=ast.attribute_name).not_matches(ast.value)
        _raise_invalid_ast(attribute=attribute, ast=ast)
    if ast.type == "equals_integer":
        assert isinstance(ast.value, int)
        return fac.integer_textbox(attribute_name=ast.attribute_name).equals(ast.value)
    if ast.type == "not_equals_integer":
        assert isinstance(ast.value, int)
        return fac.integer_textbox(attribute_name=ast.attribute_name).not_equals(ast.value)
    if ast.type == "has_choice":
        assert ast.choice_name is not None
        return fac.selection(attribute_name=ast.attribute_name).has_choice(choice_name=ast.choice_name)
    if ast.type == "not_has_choice":
        assert ast.choice_name is not None
        return fac.selection(attribute_name=ast.attribute_name).not_has_choice(choice_name=ast.choice_name)
    if ast.type == "has_label":
        assert ast.label_names is not None
        return fac.annotation_link(attribute_name=ast.attribute_name).has_label(label_names=ast.label_names)

    raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")


def _attribute_with_empty_check(fac: AttributeFactory, attribute_name: str) -> EmptyCheckMixin:
    attribute_obj = _create_attribute_object_with_name(fac, attribute_name)
    if not isinstance(attribute_obj, EmptyCheckMixin):
        attribute = fac.accessor.get_attribute(attribute_name=attribute_name)
        _raise_invalid_restriction(
            attribute=attribute,
            condition={"_type": "EmptyCheck"},
            detail="空判定はこの属性種類では利用できません。",
        )
    return attribute_obj


def _raise_invalid_ast(*, attribute: dict[str, Any], ast: RestrictionAst) -> None:
    attribute_name = get_english_message(attribute["name"])
    raise ValueError(f"属性'{attribute_name}'(type='{attribute['type']}')ではAST種別'{ast.type}'を利用できません。")


def _parse_integer_value(value: str, *, attribute: dict[str, Any], condition: dict[str, Any]) -> int:
    try:
        return int(value)
    except ValueError as exc:
        _raise_invalid_restriction(attribute=attribute, condition=condition, detail="整数属性には整数値を指定してください。")
        raise AssertionError("unreachable") from exc


def _raise_invalid_restriction(*, attribute: dict[str, Any], condition: dict[str, Any], detail: str | None = None) -> None:
    attribute_name = get_english_message(attribute["name"])
    message = f"属性'{attribute_name}'(type='{attribute['type']}')では制約'{condition['_type']}'を利用できません。"
    if detail is not None:
        message += f" {detail}"
    raise ValueError(message)


def _restriction_to_ast(restriction: Restriction, *, accessor: AnnotationSpecsAccessor) -> RestrictionAst:
    if isinstance(restriction, Imply):
        return RestrictionAst(
            type="imply",
            premise=_restriction_to_ast(restriction.premise_restriction, accessor=accessor),
            conclusion=_restriction_to_ast(restriction.conclusion_restriction, accessor=accessor),
        )

    attribute = accessor.get_attribute(attribute_id=restriction.attribute_id)
    attribute_name = get_english_message(attribute["name"])
    attribute_type = attribute["type"]

    if isinstance(restriction, CanInput):
        return RestrictionAst(type="can_input", attribute_name=attribute_name, enable=restriction.enable)

    if isinstance(restriction, Equals):
        if attribute_type == "flag" and restriction.value == "true":
            return RestrictionAst(type="checked", attribute_name=attribute_name)
        if restriction.value == "" and attribute_type in {"text", "comment", "integer", "link", "tracking", "choice", "select"}:
            return RestrictionAst(type="is_empty", attribute_name=attribute_name)
        if attribute_type in {"text", "comment", "tracking"}:
            return RestrictionAst(type="equals_string", attribute_name=attribute_name, value=restriction.value)
        if attribute_type == "integer":
            return RestrictionAst(type="equals_integer", attribute_name=attribute_name, value=int(restriction.value))
        if attribute_type in {"choice", "select"}:
            choice = get_choice(attribute["choices"], choice_id=restriction.value)
            return RestrictionAst(type="has_choice", attribute_name=attribute_name, choice_name=get_english_message(choice["name"]))

    if isinstance(restriction, NotEquals):
        if attribute_type == "flag" and restriction.value == "true":
            return RestrictionAst(type="unchecked", attribute_name=attribute_name)
        if restriction.value == "" and attribute_type in {"text", "comment", "integer", "link", "tracking", "choice", "select"}:
            return RestrictionAst(type="is_not_empty", attribute_name=attribute_name)
        if attribute_type in {"text", "comment", "tracking"}:
            return RestrictionAst(type="not_equals_string", attribute_name=attribute_name, value=restriction.value)
        if attribute_type == "integer":
            return RestrictionAst(type="not_equals_integer", attribute_name=attribute_name, value=int(restriction.value))
        if attribute_type in {"choice", "select"}:
            choice = get_choice(attribute["choices"], choice_id=restriction.value)
            return RestrictionAst(type="not_has_choice", attribute_name=attribute_name, choice_name=get_english_message(choice["name"]))

    if isinstance(restriction, Matches) and attribute_type in {"text", "comment"}:
        return RestrictionAst(type="matches_string", attribute_name=attribute_name, value=restriction.value)

    if isinstance(restriction, NotMatches) and attribute_type in {"text", "comment"}:
        return RestrictionAst(type="not_matches_string", attribute_name=attribute_name, value=restriction.value)

    if isinstance(restriction, HasLabel) and attribute_type == "link":
        label_names = [get_english_message(accessor.get_label(label_id=label_id)["label_name"]) for label_id in restriction.label_ids]
        return RestrictionAst(type="has_label", attribute_name=attribute_name, label_names=label_names)

    raise ValueError(f"RestrictionをASTへ変換できません。 :: restriction={restriction.to_dict()}")


def _restriction_to_python_expr(restriction: Restriction, *, accessor: AnnotationSpecsAccessor, factory_name: str) -> str:
    if isinstance(restriction, Imply):
        premise_expr = _restriction_to_python_expr(restriction.premise_restriction, accessor=accessor, factory_name=factory_name)
        conclusion_expr = _restriction_to_python_expr(restriction.conclusion_restriction, accessor=accessor, factory_name=factory_name)
        return f"{premise_expr}.imply({conclusion_expr})"

    attribute = accessor.get_attribute(attribute_id=restriction.attribute_id)
    attribute_expr = _attribute_to_python_expr(attribute, factory_name=factory_name)
    attribute_type = attribute["type"]

    if isinstance(restriction, CanInput):
        return f"{attribute_expr}.enabled()" if restriction.enable else f"{attribute_expr}.disabled()"

    if isinstance(restriction, Equals):
        if attribute_type == "flag" and restriction.value == "true":
            return f"{attribute_expr}.checked()"
        if attribute_type in {"text", "comment"}:
            if restriction.value == "":
                return f"{attribute_expr}.is_empty()"
            return f"{attribute_expr}.equals({_repr_python_value(restriction.value)})"
        if attribute_type == "integer":
            if restriction.value == "":
                return f"{attribute_expr}.is_empty()"
            return f"{attribute_expr}.equals({int(restriction.value)})"
        if attribute_type == "link" and restriction.value == "":
            return f"{attribute_expr}.is_empty()"
        if attribute_type == "tracking":
            if restriction.value == "":
                return f"{attribute_expr}.is_empty()"
            return f"{attribute_expr}.equals({_repr_python_value(restriction.value)})"
        if attribute_type in {"choice", "select"}:
            if restriction.value == "":
                return f"{attribute_expr}.is_empty()"
            choice = get_choice(attribute["choices"], choice_id=restriction.value)
            choice_name = get_english_message(choice["name"])
            return f"{attribute_expr}.has_choice(choice_name={_repr_python_value(choice_name)})"

    if isinstance(restriction, NotEquals):
        if attribute_type == "flag" and restriction.value == "true":
            return f"{attribute_expr}.unchecked()"
        if attribute_type in {"text", "comment"}:
            if restriction.value == "":
                return f"{attribute_expr}.is_not_empty()"
            return f"{attribute_expr}.not_equals({_repr_python_value(restriction.value)})"
        if attribute_type == "integer":
            if restriction.value == "":
                return f"{attribute_expr}.is_not_empty()"
            return f"{attribute_expr}.not_equals({int(restriction.value)})"
        if attribute_type == "link" and restriction.value == "":
            return f"{attribute_expr}.is_not_empty()"
        if attribute_type == "tracking":
            if restriction.value == "":
                return f"{attribute_expr}.is_not_empty()"
            return f"{attribute_expr}.not_equals({_repr_python_value(restriction.value)})"
        if attribute_type in {"choice", "select"}:
            if restriction.value == "":
                return f"{attribute_expr}.is_not_empty()"
            choice = get_choice(attribute["choices"], choice_id=restriction.value)
            choice_name = get_english_message(choice["name"])
            return f"{attribute_expr}.not_has_choice(choice_name={_repr_python_value(choice_name)})"

    if isinstance(restriction, Matches) and attribute_type in {"text", "comment"}:
        return f"{attribute_expr}.matches({_repr_python_value(restriction.value)})"

    if isinstance(restriction, NotMatches) and attribute_type in {"text", "comment"}:
        return f"{attribute_expr}.not_matches({_repr_python_value(restriction.value)})"

    if isinstance(restriction, HasLabel) and attribute_type == "link":
        label_names = [get_english_message(accessor.get_label(label_id=label_id)["label_name"]) for label_id in restriction.label_ids]
        return f"{attribute_expr}.has_label(label_names={_repr_python_value(label_names)})"

    raise ValueError(f"Restrictionを高水準APIのPython式へ変換できません。 :: restriction={restriction.to_dict()}")


def _attribute_to_python_expr(attribute: dict[str, Any], *, factory_name: str) -> str:
    attribute_name = get_english_message(attribute["name"])
    attribute_type = attribute["type"]

    if attribute_type == "flag":
        factory_method = "checkbox"
    elif attribute_type in {"text", "comment"}:
        factory_method = "string_textbox"
    elif attribute_type == "integer":
        factory_method = "integer_textbox"
    elif attribute_type == "link":
        factory_method = "annotation_link"
    elif attribute_type == "tracking":
        factory_method = "tracking_id"
    elif attribute_type in {"choice", "select"}:
        factory_method = "selection"
    else:
        raise ValueError(f"未対応の属性種類です。 :: attribute_type='{attribute_type}'")

    return f"{factory_name}.{factory_method}(attribute_name={_repr_python_value(attribute_name)})"


def _ast_to_human_readable(ast: RestrictionAst) -> str:
    if ast.type == "imply":
        assert ast.premise is not None
        assert ast.conclusion is not None
        return f"{ast.conclusion.to_human_readable()} IF {ast.premise.to_human_readable()}"

    assert ast.attribute_name is not None
    attribute_name = _quote_human(ast.attribute_name)

    if ast.type == "checked":
        return f"{attribute_name} EQUALS 'true'"
    if ast.type == "unchecked":
        return f"{attribute_name} DOES NOT EQUAL 'true'"
    if ast.type == "is_empty":
        return f"{attribute_name} EQUALS ''"
    if ast.type == "is_not_empty":
        return f"{attribute_name} DOES NOT EQUAL ''"
    if ast.type == "equals_string":
        return f"{attribute_name} EQUALS {_quote_human(ast.value)}"
    if ast.type == "not_equals_string":
        return f"{attribute_name} DOES NOT EQUAL {_quote_human(ast.value)}"
    if ast.type == "matches_string":
        return f"{attribute_name} MATCHES {_quote_human(ast.value)}"
    if ast.type == "not_matches_string":
        return f"{attribute_name} DOES NOT MATCH {_quote_human(ast.value)}"
    if ast.type == "equals_integer":
        return f"{attribute_name} EQUALS {_quote_human(ast.value)}"
    if ast.type == "not_equals_integer":
        return f"{attribute_name} DOES NOT EQUAL {_quote_human(ast.value)}"
    if ast.type == "has_choice":
        return f"{attribute_name} EQUALS {_quote_human(ast.choice_name)}"
    if ast.type == "not_has_choice":
        return f"{attribute_name} DOES NOT EQUAL {_quote_human(ast.choice_name)}"
    if ast.type == "has_label":
        assert ast.label_names is not None
        return f"{attribute_name} HAS LABEL {', '.join(_quote_human(label_name) for label_name in ast.label_names)}"
    if ast.type == "can_input":
        assert ast.enable is not None
        return f"{attribute_name} CAN INPUT" if ast.enable else f"{attribute_name} CANNOT INPUT"

    raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")


def _repr_python_value(value: Any) -> str:
    return repr(value)


def _quote_human(value: Any) -> str:
    return f"'{value}'"
