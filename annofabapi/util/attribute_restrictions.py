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
from typing import Any, Literal, NoReturn

from pydantic import BaseModel, ConfigDict, Field, model_validator

from annofabapi.pydantic_models.additional_data_definition_type import AdditionalDataDefinitionType
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


class RestrictionAst(BaseModel):
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

    model_config = ConfigDict(extra="forbid", frozen=True)

    type: RestrictionAstType = Field(description="ASTノードの種類です。")
    attribute_name: str | None = Field(default=None, description="対象属性の名前です。")
    value: str | int | None = Field(default=None, description="文字列や整数の比較値です。")
    choice_name: str | None = Field(default=None, description="選択系属性で利用する選択肢名です。")
    enable: bool | None = Field(default=None, description="`can_input` ノードで使う真偽値です。")
    label_names: list[str] | None = Field(default=None, description="`has_label` ノードで使うラベル名の一覧です。")
    premise: "RestrictionAst | None" = Field(default=None, description="`imply` ノードの前提です。")
    conclusion: "RestrictionAst | None" = Field(default=None, description="`imply` ノードの結論です。")

    @model_validator(mode="after")
    def validate_restriction_ast(self) -> "RestrictionAst":
        _validate_restriction_ast(self)
        return self

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


RestrictionAst.model_rebuild()


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

    attribute_name: str = Field(description="アノテーション仕様に定義された属性名です。LLMはこの名前を使って属性を参照します。")
    attribute_type: AdditionalDataDefinitionType = Field(
        description="アノテーション仕様上の属性種類です。例えば flag、text、integer、tracking、link、choice、select などです。"
    )
    allowed_ast_types: list[RestrictionAstType] = Field(
        description="この属性で利用できる意味ベースAST種別の一覧です。LLMはこの一覧に含まれないAST種別を使ってはいけません。"
    )
    choice_names: list[str] | None = Field(
        default=None,
        description="choice/select 属性で利用できる選択肢名の一覧です。それ以外の属性では null です。",
    )
    label_names: list[str] | None = Field(
        default=None,
        description="link 属性で利用できるラベル名の一覧です。それ以外の属性では null です。",
    )


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
        choice_names = None
        label_names = None
        match attribute_type:
            case "choice" | "select":
                choice_names = [get_english_message(choice["name"]) for choice in attribute["choices"]]
            case "link":
                label_names = [get_english_message(label["label_name"]) for label in accessor.labels]
        item = AttributeRestrictionCatalogItem(
            attribute_name=get_english_message(attribute["name"]),
            attribute_type=attribute_type,
            allowed_ast_types=_get_allowed_ast_types(attribute_type),
            choice_names=choice_names,
            label_names=label_names,
        )
        catalog.append(item)
    return catalog


def _from_restriction_dict(obj: dict[str, Any], *, fac: AttributeFactory | None) -> Restriction:
    """
    API向けの制約辞書から `Restriction` を復元します。

    Args:
        obj: APIの `restrictions` 要素を表す辞書です。
        fac: Noneでなければ、属性型に応じた妥当性検証に使う `AttributeFactory` です。

    Returns:
        復元した `Restriction` オブジェクトです。
    """
    attribute_id = obj["additional_data_definition_id"]
    condition = obj["condition"]
    return _from_condition_dict(attribute_id=attribute_id, condition=condition, fac=fac)


def _get_required_ast_fields(ast_type: RestrictionAstType) -> set[str]:
    """
    AST種別ごとに必須なフィールド名を返します。

    Args:
        ast_type: ASTノードの種類です。

    Returns:
        AST種別に対応する必須フィールド名です。

    Raises:
        ValueError: 未知のAST種別が指定された場合
    """
    match ast_type:
        case "checked" | "unchecked" | "is_empty" | "is_not_empty":
            return {"attribute_name"}
        case "equals_string" | "not_equals_string" | "matches_string" | "not_matches_string" | "equals_integer" | "not_equals_integer":
            return {"attribute_name", "value"}
        case "has_choice" | "not_has_choice":
            return {"attribute_name", "choice_name"}
        case "has_label":
            return {"attribute_name", "label_names"}
        case "can_input":
            return {"attribute_name", "enable"}
        case "imply":
            return {"premise", "conclusion"}
        case _:
            raise ValueError(f"未知のAST種別です。 :: type='{ast_type}'")


def _validate_restriction_ast(ast: RestrictionAst) -> None:
    """
    `RestrictionAst` の構造がAST種別に整合しているか検証します。

    Args:
        ast: 検証対象のASTです。

    Raises:
        ValueError: AST種別に対して必須フィールドが不足している場合、または型が不正な場合
    """
    required_fields = _get_required_ast_fields(ast.type)
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
        raise ValueError(f"AST種別'{ast.type}'のフィールドが不正です。 :: required={sorted(required_fields)}, actual={sorted(actual_fields)}")

    match ast.type:
        case "equals_string" | "not_equals_string" | "matches_string" | "not_matches_string":
            if not isinstance(ast.value, str):
                raise ValueError(f"AST種別'{ast.type}'の'value'は文字列である必要があります。")
        case "equals_integer" | "not_equals_integer":
            if not isinstance(ast.value, int):
                raise ValueError(f"AST種別'{ast.type}'の'value'は整数である必要があります。")
        case "has_choice" | "not_has_choice":
            if not isinstance(ast.choice_name, str):
                raise ValueError(f"AST種別'{ast.type}'の'choice_name'は文字列である必要があります。")
        case "has_label":
            if not isinstance(ast.label_names, list) or any(not isinstance(label_name, str) for label_name in ast.label_names):
                raise ValueError("AST種別'has_label'の'label_names'は文字列のリストである必要があります。")
        case "can_input":
            if not isinstance(ast.enable, bool):
                raise ValueError("AST種別'can_input'の'enable'は真偽値である必要があります。")
        case _:
            pass


def _get_allowed_ast_types(attribute_type: str) -> list[RestrictionAstType]:
    """
    属性種類ごとに利用可能なAST種別を返します。

    Args:
        attribute_type: アノテーション仕様上の属性種類です。

    Returns:
        指定した属性種類で利用可能なAST種別の一覧です。

    Raises:
        ValueError: 未対応の属性種類が指定された場合
    """
    match attribute_type:
        case "flag":
            return ["can_input", "checked", "unchecked"]
        case "text" | "comment":
            return ["can_input", "is_empty", "is_not_empty", "equals_string", "not_equals_string", "matches_string", "not_matches_string"]
        case "integer":
            return ["can_input", "is_empty", "is_not_empty", "equals_integer", "not_equals_integer"]
        case "link":
            return ["can_input", "is_empty", "is_not_empty", "has_label"]
        case "tracking":
            return ["can_input", "is_empty", "is_not_empty", "equals_string", "not_equals_string"]
        case "choice" | "select":
            return ["can_input", "is_empty", "is_not_empty", "has_choice", "not_has_choice"]
        case _:
            raise ValueError(f"未対応の属性種類です。 :: attribute_type='{attribute_type}'")


def _from_condition_dict(*, attribute_id: str, condition: dict[str, Any], fac: AttributeFactory | None) -> Restriction:
    """
    条件部分の辞書から `Restriction` を復元します。

    Args:
        attribute_id: 対象属性のIDです。
        condition: 条件部分のみを表す辞書です。
        fac: Noneでなければ、属性型に応じた妥当性検証に使う `AttributeFactory` です。

    Returns:
        復元した `Restriction` オブジェクトです。
    """
    condition_type = condition["_type"]
    match condition_type:
        case "Imply":
            premise_restriction = _from_restriction_dict(condition["premise"], fac=fac)
            conclusion_restriction = _from_condition_dict(attribute_id=attribute_id, condition=condition["condition"], fac=fac)
            return Imply(premise_restriction=premise_restriction, conclusion_restriction=conclusion_restriction)
        case _ if fac is None:
            return _from_condition_dict_without_validation(attribute_id=attribute_id, condition=condition)
        case _:
            return _from_condition_dict_with_validation(attribute_id=attribute_id, condition=condition, fac=fac)


def _from_condition_dict_without_validation(*, attribute_id: str, condition: dict[str, Any]) -> Restriction:
    """
    妥当性検証を行わずに条件辞書から `Restriction` を復元します。

    Args:
        attribute_id: 対象属性のIDです。
        condition: 条件部分のみを表す辞書です。

    Returns:
        復元した `Restriction` オブジェクトです。

    Raises:
        ValueError: 未知の制約種別が指定された場合
    """
    condition_type = condition["_type"]
    match condition_type:
        case "CanInput":
            return CanInput(attribute_id, enable=condition["enable"])
        case "Equals":
            return Equals(attribute_id, value=condition["value"])
        case "NotEquals":
            return NotEquals(attribute_id, value=condition["value"])
        case "Matches":
            return Matches(attribute_id, value=condition["value"])
        case "NotMatches":
            return NotMatches(attribute_id, value=condition["value"])
        case "HasLabel":
            return HasLabel(attribute_id, label_ids=condition["labels"])
        case _:
            raise ValueError(f"未知の制約種別です。 :: _type='{condition_type}'")


def _from_condition_dict_with_validation(*, attribute_id: str, condition: dict[str, Any], fac: AttributeFactory) -> Restriction:
    """
    属性型の妥当性を検証しながら条件辞書から `Restriction` を復元します。

    Args:
        attribute_id: 対象属性のIDです。
        condition: 条件部分のみを表す辞書です。
        fac: 属性生成と妥当性検証に使う `AttributeFactory` です。

    Returns:
        復元した `Restriction` オブジェクトです。

    Raises:
        ValueError: 属性型に対して許可されていない制約が指定された場合
    """
    attribute = fac.accessor.get_attribute(attribute_id=attribute_id)
    attribute_obj = _create_attribute_object(fac, attribute)
    attribute_type = attribute["type"]
    condition_type = condition["_type"]

    match condition_type:
        case "CanInput":
            return attribute_obj.enabled() if condition["enable"] else attribute_obj.disabled()
        case _:
            return _from_condition_dict_for_attribute_type(
                attribute=attribute,
                attribute_obj=attribute_obj,
                condition=condition,
                attribute_type=attribute_type,
            )


def _from_condition_dict_for_attribute_type(
    *,
    attribute: dict[str, Any],
    attribute_obj: Attribute,
    condition: dict[str, Any],
    attribute_type: str,
) -> Restriction:
    match attribute_type:
        case "flag":
            assert isinstance(attribute_obj, Checkbox)
            return _from_flag_condition(attribute=attribute, attribute_obj=attribute_obj, condition=condition)
        case "text" | "comment":
            assert isinstance(attribute_obj, StringTextbox)
            return _from_string_condition(attribute=attribute, attribute_obj=attribute_obj, condition=condition)
        case "integer":
            assert isinstance(attribute_obj, IntegerTextbox)
            return _from_integer_condition(attribute=attribute, attribute_obj=attribute_obj, condition=condition)
        case "link":
            assert isinstance(attribute_obj, AnnotationLink)
            return _from_link_condition(attribute=attribute, attribute_obj=attribute_obj, condition=condition)
        case "tracking":
            assert isinstance(attribute_obj, TrackingId)
            return _from_tracking_condition(attribute=attribute, attribute_obj=attribute_obj, condition=condition)
        case "choice" | "select":
            assert isinstance(attribute_obj, Selection)
            return _from_selection_condition(attribute=attribute, attribute_obj=attribute_obj, condition=condition)
        case _:
            raise ValueError(f"未対応の属性種類です。 :: attribute_type='{attribute_type}'")


def _from_flag_condition(*, attribute: dict[str, Any], attribute_obj: Checkbox, condition: dict[str, Any]) -> Restriction:
    match condition["_type"]:
        case "Equals" if condition["value"] == "true":
            return attribute_obj.checked()
        case "NotEquals" if condition["value"] == "true":
            return attribute_obj.unchecked()
        case _:
            _raise_invalid_restriction(attribute=attribute, condition=condition)


def _from_string_condition(*, attribute: dict[str, Any], attribute_obj: StringTextbox, condition: dict[str, Any]) -> Restriction:
    match condition["_type"]:
        case "Equals":
            return attribute_obj.equals(condition["value"])
        case "NotEquals":
            return attribute_obj.not_equals(condition["value"])
        case "Matches":
            return attribute_obj.matches(condition["value"])
        case "NotMatches":
            return attribute_obj.not_matches(condition["value"])
        case _:
            _raise_invalid_restriction(attribute=attribute, condition=condition)


def _from_integer_condition(*, attribute: dict[str, Any], attribute_obj: IntegerTextbox, condition: dict[str, Any]) -> Restriction:
    match condition["_type"]:
        case "Equals":
            if condition["value"] == "":
                return attribute_obj.is_empty()
            return attribute_obj.equals(_parse_integer_value(condition["value"], attribute=attribute, condition=condition))
        case "NotEquals":
            if condition["value"] == "":
                return attribute_obj.is_not_empty()
            return attribute_obj.not_equals(_parse_integer_value(condition["value"], attribute=attribute, condition=condition))
        case _:
            _raise_invalid_restriction(attribute=attribute, condition=condition)


def _from_link_condition(*, attribute: dict[str, Any], attribute_obj: AnnotationLink, condition: dict[str, Any]) -> Restriction:
    match condition["_type"]:
        case "HasLabel":
            return attribute_obj.has_label(label_ids=condition["labels"])
        case "Equals" if condition["value"] == "":
            return attribute_obj.is_empty()
        case "NotEquals" if condition["value"] == "":
            return attribute_obj.is_not_empty()
        case _:
            _raise_invalid_restriction(attribute=attribute, condition=condition)


def _from_tracking_condition(*, attribute: dict[str, Any], attribute_obj: TrackingId, condition: dict[str, Any]) -> Restriction:
    match condition["_type"]:
        case "Equals":
            if condition["value"] == "":
                return attribute_obj.is_empty()
            return attribute_obj.equals(condition["value"])
        case "NotEquals":
            if condition["value"] == "":
                return attribute_obj.is_not_empty()
            return attribute_obj.not_equals(condition["value"])
        case _:
            _raise_invalid_restriction(attribute=attribute, condition=condition)


def _from_selection_condition(*, attribute: dict[str, Any], attribute_obj: Selection, condition: dict[str, Any]) -> Restriction:
    match condition["_type"]:
        case "Equals":
            if condition["value"] == "":
                return attribute_obj.is_empty()
            return attribute_obj.has_choice(choice_id=condition["value"])
        case "NotEquals":
            if condition["value"] == "":
                return attribute_obj.is_not_empty()
            return attribute_obj.not_has_choice(choice_id=condition["value"])
        case _:
            _raise_invalid_restriction(attribute=attribute, condition=condition)


def _ast_to_atomic_restriction(ast: RestrictionAst, *, fac: AttributeFactory, attribute: dict[str, Any]) -> Restriction:
    assert ast.attribute_name is not None
    attribute_type = attribute["type"]

    match ast.type:
        case "checked":
            restriction = fac.checkbox(attribute_name=ast.attribute_name).checked()
        case "unchecked":
            restriction = fac.checkbox(attribute_name=ast.attribute_name).unchecked()
        case "is_empty":
            restriction = _attribute_with_empty_check(fac, ast.attribute_name).is_empty()
        case "is_not_empty":
            restriction = _attribute_with_empty_check(fac, ast.attribute_name).is_not_empty()
        case "can_input":
            assert ast.enable is not None
            attribute_obj = _create_attribute_object_with_name(fac, ast.attribute_name)
            restriction = attribute_obj.enabled() if ast.enable else attribute_obj.disabled()
        case "equals_string" | "not_equals_string":
            restriction = _ast_string_equality_to_restriction(ast=ast, fac=fac, attribute=attribute, attribute_type=attribute_type)
        case "matches_string" | "not_matches_string":
            restriction = _ast_string_match_to_restriction(ast=ast, fac=fac, attribute=attribute, attribute_type=attribute_type)
        case "equals_integer" | "not_equals_integer":
            restriction = _ast_integer_to_restriction(ast=ast, fac=fac)
        case "has_choice" | "not_has_choice":
            restriction = _ast_selection_to_restriction(ast=ast, fac=fac)
        case "has_label":
            restriction = _ast_label_to_restriction(ast=ast, fac=fac)
        case _:
            raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")
    return restriction


def _ast_string_equality_to_restriction(
    *,
    ast: RestrictionAst,
    fac: AttributeFactory,
    attribute: dict[str, Any],
    attribute_type: str,
) -> Restriction:
    assert isinstance(ast.value, str)
    attribute_obj: StringTextbox | TrackingId
    match attribute_type:
        case "text" | "comment":
            attribute_obj = fac.string_textbox(attribute_name=ast.attribute_name)
        case "tracking":
            attribute_obj = fac.tracking_id(attribute_name=ast.attribute_name)
        case _:
            _raise_invalid_ast(attribute=attribute, ast=ast)

    match ast.type:
        case "equals_string":
            return attribute_obj.equals(ast.value)
        case "not_equals_string":
            return attribute_obj.not_equals(ast.value)
        case _:
            raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")


def _ast_string_match_to_restriction(
    *,
    ast: RestrictionAst,
    fac: AttributeFactory,
    attribute: dict[str, Any],
    attribute_type: str,
) -> Restriction:
    assert isinstance(ast.value, str)
    if attribute_type not in {"text", "comment"}:
        _raise_invalid_ast(attribute=attribute, ast=ast)

    attribute_obj = fac.string_textbox(attribute_name=ast.attribute_name)
    match ast.type:
        case "matches_string":
            return attribute_obj.matches(ast.value)
        case "not_matches_string":
            return attribute_obj.not_matches(ast.value)
        case _:
            raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")


def _ast_integer_to_restriction(*, ast: RestrictionAst, fac: AttributeFactory) -> Restriction:
    assert isinstance(ast.value, int)
    attribute_obj = fac.integer_textbox(attribute_name=ast.attribute_name)
    match ast.type:
        case "equals_integer":
            return attribute_obj.equals(ast.value)
        case "not_equals_integer":
            return attribute_obj.not_equals(ast.value)
        case _:
            raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")


def _ast_selection_to_restriction(*, ast: RestrictionAst, fac: AttributeFactory) -> Restriction:
    assert ast.choice_name is not None
    attribute_obj = fac.selection(attribute_name=ast.attribute_name)
    match ast.type:
        case "has_choice":
            return attribute_obj.has_choice(choice_name=ast.choice_name)
        case "not_has_choice":
            return attribute_obj.not_has_choice(choice_name=ast.choice_name)
        case _:
            raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")


def _ast_label_to_restriction(*, ast: RestrictionAst, fac: AttributeFactory) -> Restriction:
    assert ast.label_names is not None
    return fac.annotation_link(attribute_name=ast.attribute_name).has_label(label_names=ast.label_names)


def _create_attribute_object(fac: AttributeFactory, attribute: dict[str, Any]) -> Attribute:
    """
    属性定義から対応する高水準属性オブジェクトを生成します。

    Args:
        fac: 属性生成に使う `AttributeFactory` です。
        attribute: アノテーション仕様上の属性定義です。

    Returns:
        対応する高水準属性オブジェクトです。

    Raises:
        ValueError: 未対応の属性種類が指定された場合
    """
    attribute_id = attribute["additional_data_definition_id"]
    attribute_type = attribute["type"]
    match attribute_type:
        case "flag":
            return fac.checkbox(attribute_id=attribute_id)
        case "text" | "comment":
            return fac.string_textbox(attribute_id=attribute_id)
        case "integer":
            return fac.integer_textbox(attribute_id=attribute_id)
        case "link":
            return fac.annotation_link(attribute_id=attribute_id)
        case "tracking":
            return fac.tracking_id(attribute_id=attribute_id)
        case "choice" | "select":
            return fac.selection(attribute_id=attribute_id)
        case _:
            raise ValueError(f"未対応の属性種類です。 :: attribute_type='{attribute_type}'")


def _create_attribute_object_with_name(fac: AttributeFactory, attribute_name: str) -> Attribute:
    """
    属性名から対応する高水準属性オブジェクトを生成します。

    Args:
        fac: 属性生成に使う `AttributeFactory` です。
        attribute_name: 属性名です。

    Returns:
        対応する高水準属性オブジェクトです。
    """
    attribute = fac.accessor.get_attribute(attribute_name=attribute_name)
    return _create_attribute_object(fac, attribute)


def _ast_to_restriction(ast: RestrictionAst, *, fac: AttributeFactory) -> Restriction:
    """
    意味ベースのASTを `Restriction` オブジェクトへコンパイルします。

    Args:
        ast: 変換元のASTです。
        fac: 属性生成と妥当性検証に使う `AttributeFactory` です。

    Returns:
        変換後の `Restriction` オブジェクトです。

    Raises:
        ValueError: AST種別が未知の場合、または属性型に対して利用できないASTが指定された場合
    """
    match ast.type:
        case "imply":
            assert ast.premise is not None
            assert ast.conclusion is not None
            premise_restriction = _ast_to_restriction(ast.premise, fac=fac)
            conclusion_restriction = _ast_to_restriction(ast.conclusion, fac=fac)
            return premise_restriction.imply(conclusion_restriction)

    assert ast.attribute_name is not None
    attribute = fac.accessor.get_attribute(attribute_name=ast.attribute_name)
    return _ast_to_atomic_restriction(ast, fac=fac, attribute=attribute)


def _restriction_to_atomic_ast(
    restriction: Restriction,
    *,
    accessor: AnnotationSpecsAccessor,
    attribute: dict[str, Any],
    attribute_name: str,
) -> RestrictionAst:
    attribute_type = attribute["type"]
    match restriction:
        case CanInput(enable=enable):
            return RestrictionAst(type="can_input", attribute_name=attribute_name, enable=enable)
        case Equals(value=value):
            return _equals_restriction_to_ast(attribute=attribute, attribute_name=attribute_name, attribute_type=attribute_type, value=value)
        case NotEquals(value=value):
            return _not_equals_restriction_to_ast(attribute=attribute, attribute_name=attribute_name, attribute_type=attribute_type, value=value)
        case Matches(value=value) if attribute_type in {"text", "comment"}:
            return RestrictionAst(type="matches_string", attribute_name=attribute_name, value=value)
        case NotMatches(value=value) if attribute_type in {"text", "comment"}:
            return RestrictionAst(type="not_matches_string", attribute_name=attribute_name, value=value)
        case HasLabel(label_ids=label_ids) if attribute_type == "link":
            label_names = [get_english_message(accessor.get_label(label_id=label_id)["label_name"]) for label_id in label_ids]
            return RestrictionAst(type="has_label", attribute_name=attribute_name, label_names=label_names)
        case _:
            raise ValueError(f"RestrictionをASTへ変換できません。 :: restriction={restriction.to_dict()}")


def _equals_restriction_to_ast(*, attribute: dict[str, Any], attribute_name: str, attribute_type: str, value: str) -> RestrictionAst:
    match attribute_type:
        case "flag" if value == "true":
            return RestrictionAst(type="checked", attribute_name=attribute_name)
        case "text" | "comment" | "integer" | "link" | "tracking" | "choice" | "select" if value == "":
            return RestrictionAst(type="is_empty", attribute_name=attribute_name)
        case "text" | "comment" | "tracking":
            return RestrictionAst(type="equals_string", attribute_name=attribute_name, value=value)
        case "integer":
            return RestrictionAst(type="equals_integer", attribute_name=attribute_name, value=int(value))
        case "choice" | "select":
            choice = get_choice(attribute["choices"], choice_id=value)
            return RestrictionAst(type="has_choice", attribute_name=attribute_name, choice_name=get_english_message(choice["name"]))
        case _:
            raise ValueError(f"RestrictionをASTへ変換できません。 :: restriction_type='Equals', attribute_type='{attribute_type}', value={value!r}")


def _not_equals_restriction_to_ast(*, attribute: dict[str, Any], attribute_name: str, attribute_type: str, value: str) -> RestrictionAst:
    match attribute_type:
        case "flag" if value == "true":
            return RestrictionAst(type="unchecked", attribute_name=attribute_name)
        case "text" | "comment" | "integer" | "link" | "tracking" | "choice" | "select" if value == "":
            return RestrictionAst(type="is_not_empty", attribute_name=attribute_name)
        case "text" | "comment" | "tracking":
            return RestrictionAst(type="not_equals_string", attribute_name=attribute_name, value=value)
        case "integer":
            return RestrictionAst(type="not_equals_integer", attribute_name=attribute_name, value=int(value))
        case "choice" | "select":
            choice = get_choice(attribute["choices"], choice_id=value)
            return RestrictionAst(type="not_has_choice", attribute_name=attribute_name, choice_name=get_english_message(choice["name"]))
        case _:
            raise ValueError(
                f"RestrictionをASTへ変換できません。 :: restriction_type='NotEquals', attribute_type='{attribute_type}', value={value!r}"
            )


def _attribute_with_empty_check(fac: AttributeFactory, attribute_name: str) -> EmptyCheckMixin:
    """
    空判定をサポートする属性オブジェクトを取得します。

    Args:
        fac: 属性生成に使う `AttributeFactory` です。
        attribute_name: 属性名です。

    Returns:
        `is_empty()` / `is_not_empty()` を持つ属性オブジェクトです。

    Raises:
        ValueError: 指定した属性で空判定を利用できない場合
    """
    attribute_obj = _create_attribute_object_with_name(fac, attribute_name)
    if not isinstance(attribute_obj, EmptyCheckMixin):
        attribute = fac.accessor.get_attribute(attribute_name=attribute_name)
        _raise_invalid_restriction(
            attribute=attribute,
            condition={"_type": "EmptyCheck"},
            detail="空判定はこの属性種類では利用できません。",
        )
    assert isinstance(attribute_obj, EmptyCheckMixin)
    return attribute_obj


def _raise_invalid_ast(*, attribute: dict[str, Any], ast: RestrictionAst) -> NoReturn:
    """
    属性型に対して不正なAST種別が指定されたことを表す例外を送出します。

    Args:
        attribute: アノテーション仕様上の属性定義です。
        ast: 不正だったASTです。

    Raises:
        ValueError: 常に送出されます。
    """
    attribute_name = get_english_message(attribute["name"])
    raise ValueError(f"属性'{attribute_name}'(type='{attribute['type']}')ではAST種別'{ast.type}'を利用できません。")


def _parse_integer_value(value: str, *, attribute: dict[str, Any], condition: dict[str, Any]) -> int:
    """
    整数属性向けの文字列値を整数へ変換します。

    Args:
        value: 変換対象の文字列値です。
        attribute: アノテーション仕様上の属性定義です。
        condition: 元の条件辞書です。

    Returns:
        変換後の整数値です。

    Raises:
        ValueError: 整数へ変換できない場合
    """
    try:
        return int(value)
    except ValueError as exc:
        _raise_invalid_restriction(attribute=attribute, condition=condition, detail="整数属性には整数値を指定してください。")
        raise AssertionError("unreachable") from exc


def _raise_invalid_restriction(*, attribute: dict[str, Any], condition: dict[str, Any], detail: str | None = None) -> NoReturn:
    """
    属性型に対して不正な制約が指定されたことを表す例外を送出します。

    Args:
        attribute: アノテーション仕様上の属性定義です。
        condition: 不正だった制約条件です。
        detail: 補足メッセージです。

    Raises:
        ValueError: 常に送出されます。
    """
    attribute_name = get_english_message(attribute["name"])
    message = f"属性'{attribute_name}'(type='{attribute['type']}')では制約'{condition['_type']}'を利用できません。"
    if detail is not None:
        message += f" {detail}"
    raise ValueError(message)


def _restriction_to_ast(restriction: Restriction, *, accessor: AnnotationSpecsAccessor) -> RestrictionAst:
    """
    `Restriction` を意味ベースの `RestrictionAst` へ変換します。

    Args:
        restriction: 変換元の `Restriction` です。
        accessor: 属性名や選択肢名の解決に使う `AnnotationSpecsAccessor` です。

    Returns:
        変換後の `RestrictionAst` です。

    Raises:
        ValueError: ASTへ変換できない制約が含まれている場合
    """
    match restriction:
        case Imply(premise_restriction=premise_restriction, conclusion_restriction=conclusion_restriction):
            return RestrictionAst(
                type="imply",
                premise=_restriction_to_ast(premise_restriction, accessor=accessor),
                conclusion=_restriction_to_ast(conclusion_restriction, accessor=accessor),
            )

    attribute = accessor.get_attribute(attribute_id=restriction.attribute_id)
    attribute_name = get_english_message(attribute["name"])
    return _restriction_to_atomic_ast(restriction, accessor=accessor, attribute=attribute, attribute_name=attribute_name)


def _restriction_to_python_expr(restriction: Restriction, *, accessor: AnnotationSpecsAccessor, factory_name: str) -> str:
    """
    `Restriction` を fluent API 形式の Python 式へ変換します。

    Args:
        restriction: 変換元の `Restriction` です。
        accessor: 属性名や選択肢名の解決に使う `AnnotationSpecsAccessor` です。
        factory_name: `AttributeFactory` の変数名です。

    Returns:
        変換後の Python 式です。

    Raises:
        ValueError: Python 式へ変換できない制約が含まれている場合
    """
    match restriction:
        case Imply(premise_restriction=premise_restriction, conclusion_restriction=conclusion_restriction):
            premise_expr = _restriction_to_python_expr(premise_restriction, accessor=accessor, factory_name=factory_name)
            conclusion_expr = _restriction_to_python_expr(conclusion_restriction, accessor=accessor, factory_name=factory_name)
            return f"{premise_expr}.imply({conclusion_expr})"

    attribute = accessor.get_attribute(attribute_id=restriction.attribute_id)
    attribute_expr = _attribute_to_python_expr(attribute, factory_name=factory_name)
    return _restriction_to_atomic_python_expr(restriction, accessor=accessor, attribute=attribute, attribute_expr=attribute_expr)


def _restriction_to_atomic_python_expr(
    restriction: Restriction,
    *,
    accessor: AnnotationSpecsAccessor,
    attribute: dict[str, Any],
    attribute_expr: str,
) -> str:
    attribute_type = attribute["type"]
    match restriction:
        case CanInput(enable=enable):
            return f"{attribute_expr}.enabled()" if enable else f"{attribute_expr}.disabled()"
        case Equals(value=value):
            return _equals_restriction_to_python_expr(attribute=attribute, attribute_expr=attribute_expr, attribute_type=attribute_type, value=value)
        case NotEquals(value=value):
            return _not_equals_restriction_to_python_expr(
                attribute=attribute,
                attribute_expr=attribute_expr,
                attribute_type=attribute_type,
                value=value,
            )
        case Matches(value=value) if attribute_type in {"text", "comment"}:
            return f"{attribute_expr}.matches({_repr_python_value(value)})"
        case NotMatches(value=value) if attribute_type in {"text", "comment"}:
            return f"{attribute_expr}.not_matches({_repr_python_value(value)})"
        case HasLabel(label_ids=label_ids) if attribute_type == "link":
            label_names = [get_english_message(accessor.get_label(label_id=label_id)["label_name"]) for label_id in label_ids]
            return f"{attribute_expr}.has_label(label_names={_repr_python_value(label_names)})"
        case _:
            raise ValueError(f"Restrictionを高水準APIのPython式へ変換できません。 :: restriction={restriction.to_dict()}")


def _equals_restriction_to_python_expr(*, attribute: dict[str, Any], attribute_expr: str, attribute_type: str, value: str) -> str:
    if value == "":
        match attribute_type:
            case "text" | "comment" | "integer" | "link" | "tracking" | "choice" | "select":
                return f"{attribute_expr}.is_empty()"

    match attribute_type:
        case "flag" if value == "true":
            expr = f"{attribute_expr}.checked()"
        case "text" | "comment":
            expr = f"{attribute_expr}.equals({_repr_python_value(value)})"
        case "integer":
            expr = f"{attribute_expr}.equals({int(value)})"
        case "tracking":
            expr = f"{attribute_expr}.equals({_repr_python_value(value)})"
        case "choice" | "select":
            choice = get_choice(attribute["choices"], choice_id=value)
            choice_name = get_english_message(choice["name"])
            expr = f"{attribute_expr}.has_choice(choice_name={_repr_python_value(choice_name)})"
        case _:
            raise ValueError(
                f"Restrictionを高水準APIのPython式へ変換できません。 :: restriction_type='Equals', attribute_type='{attribute_type}', value={value!r}"
            )
    return expr


def _not_equals_restriction_to_python_expr(*, attribute: dict[str, Any], attribute_expr: str, attribute_type: str, value: str) -> str:
    if value == "":
        match attribute_type:
            case "text" | "comment" | "integer" | "link" | "tracking" | "choice" | "select":
                return f"{attribute_expr}.is_not_empty()"

    match attribute_type:
        case "flag" if value == "true":
            expr = f"{attribute_expr}.unchecked()"
        case "text" | "comment":
            expr = f"{attribute_expr}.not_equals({_repr_python_value(value)})"
        case "integer":
            expr = f"{attribute_expr}.not_equals({int(value)})"
        case "tracking":
            expr = f"{attribute_expr}.not_equals({_repr_python_value(value)})"
        case "choice" | "select":
            choice = get_choice(attribute["choices"], choice_id=value)
            choice_name = get_english_message(choice["name"])
            expr = f"{attribute_expr}.not_has_choice(choice_name={_repr_python_value(choice_name)})"
        case _:
            raise ValueError(
                "Restrictionを高水準APIのPython式へ変換できません。 "
                f":: restriction_type='NotEquals', attribute_type='{attribute_type}', value={value!r}"
            )
    return expr


def _attribute_to_python_expr(attribute: dict[str, Any], *, factory_name: str) -> str:
    """
    属性定義を `AttributeFactory` 呼び出しの Python 式へ変換します。

    Args:
        attribute: アノテーション仕様上の属性定義です。
        factory_name: `AttributeFactory` の変数名です。

    Returns:
        属性生成部分の Python 式です。

    Raises:
        ValueError: 未対応の属性種類が指定された場合
    """
    attribute_name = get_english_message(attribute["name"])
    attribute_type = attribute["type"]

    match attribute_type:
        case "flag":
            factory_method = "checkbox"
        case "text" | "comment":
            factory_method = "string_textbox"
        case "integer":
            factory_method = "integer_textbox"
        case "link":
            factory_method = "annotation_link"
        case "tracking":
            factory_method = "tracking_id"
        case "choice" | "select":
            factory_method = "selection"
        case _:
            raise ValueError(f"未対応の属性種類です。 :: attribute_type='{attribute_type}'")

    return f"{factory_name}.{factory_method}(attribute_name={_repr_python_value(attribute_name)})"


def _ast_to_human_readable(ast: RestrictionAst) -> str:
    """
    ASTを人間向けの読みやすい文字列表現へ変換します。

    Args:
        ast: 変換元のASTです。

    Returns:
        人間向けの文字列表現です。

    Raises:
        ValueError: 未知のAST種別が指定された場合
    """
    if ast.type == "imply":
        assert ast.premise is not None
        assert ast.conclusion is not None
        return f"{ast.conclusion.to_human_readable()} IF {ast.premise.to_human_readable()}"

    assert ast.attribute_name is not None
    attribute_name = _quote_human(ast.attribute_name)
    simple_text_map = {
        "checked": f"{attribute_name} EQUALS 'true'",
        "unchecked": f"{attribute_name} DOES NOT EQUAL 'true'",
        "is_empty": f"{attribute_name} EQUALS ''",
        "is_not_empty": f"{attribute_name} DOES NOT EQUAL ''",
    }
    if ast.type in simple_text_map:
        return simple_text_map[ast.type]

    match ast.type:
        case "equals_string" | "equals_integer":
            text = f"{attribute_name} EQUALS {_quote_human(ast.value)}"
        case "not_equals_string" | "not_equals_integer":
            text = f"{attribute_name} DOES NOT EQUAL {_quote_human(ast.value)}"
        case "matches_string":
            text = f"{attribute_name} MATCHES {_quote_human(ast.value)}"
        case "not_matches_string":
            text = f"{attribute_name} DOES NOT MATCH {_quote_human(ast.value)}"
        case "has_choice":
            text = f"{attribute_name} EQUALS {_quote_human(ast.choice_name)}"
        case "not_has_choice":
            text = f"{attribute_name} DOES NOT EQUAL {_quote_human(ast.choice_name)}"
        case "has_label":
            assert ast.label_names is not None
            text = f"{attribute_name} HAS LABEL {', '.join(_quote_human(label_name) for label_name in ast.label_names)}"
        case "can_input":
            assert ast.enable is not None
            text = f"{attribute_name} CAN INPUT" if ast.enable else f"{attribute_name} CANNOT INPUT"
        case _:
            raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")
    return text


def _repr_python_value(value: object) -> str:
    """
    Python 式へ埋め込む値を `repr()` で文字列化します。

    Args:
        value: 文字列化する値です。

    Returns:
        `repr()` による文字列表現です。
    """
    return repr(value)


def _quote_human(value: object) -> str:
    """
    人間向け表示用に値をシングルクォートで囲みます。

    Args:
        value: 表示対象の値です。

    Returns:
        シングルクォートで囲んだ文字列表現です。
    """
    return f"'{value}'"
