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
from enum import Enum
from typing import Any, NoReturn

from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator

from annofabapi.pydantic_models.additional_data_definition_type import AdditionalDataDefinitionType
from annofabapi.util.annotation_specs import AnnotationSpecsAccessor, AttributeChoice, AttributeDefinition, get_choice, get_english_message
from annofabapi.util.type_util import assert_noreturn


class RestrictionAstType(str, Enum):
    """属性制約ASTの種別です。"""

    CHECKED = "checked"
    """チェックボックス属性がチェックされていることを表すAST種別です。"""
    UNCHECKED = "unchecked"
    """チェックボックス属性がチェックされていないことを表すAST種別です。"""
    IS_EMPTY = "is_empty"
    """属性値が空であることを表すAST種別です。"""
    IS_NOT_EMPTY = "is_not_empty"
    """属性値が空でないことを表すAST種別です。"""
    EQUALS_STRING = "equals_string"
    """文字列属性またはtracking属性が指定文字列と一致することを表すAST種別です。"""
    NOT_EQUALS_STRING = "not_equals_string"
    """文字列属性またはtracking属性が指定文字列と一致しないことを表すAST種別です。"""
    MATCHES_STRING = "matches_string"
    """文字列属性が指定した正規表現に一致することを表すAST種別です。"""
    NOT_MATCHES_STRING = "not_matches_string"
    """文字列属性が指定した正規表現に一致しないことを表すAST種別です。"""
    EQUALS_INTEGER = "equals_integer"
    """整数属性が指定した整数値と一致することを表すAST種別です。"""
    NOT_EQUALS_INTEGER = "not_equals_integer"
    """整数属性が指定した整数値と一致しないことを表すAST種別です。"""
    HAS_CHOICE = "has_choice"
    """選択属性で指定した選択肢が選ばれていることを表すAST種別です。"""
    NOT_HAS_CHOICE = "not_has_choice"
    """選択属性で指定した選択肢が選ばれていないことを表すAST種別です。"""
    HAS_LABEL = "has_label"
    """リンク属性が指定したラベル群のいずれかを指すことを表すAST種別です。"""
    CAN_INPUT = "can_input"
    """属性が編集可能かどうかを表すAST種別です。"""
    IMPLY = "imply"
    """前提を満たす場合に結論を要求する含意制約を表すAST種別です。"""

    def __str__(self) -> str:
        return self.value


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
    def from_dict(cls, obj: dict[str, Any]) -> "Restriction":
        """
        dictからRestrictionオブジェクトを復元します。

        Args:
            obj: `restrictions` の1要素を表す辞書です。

        Returns:
            復元した `Restriction` オブジェクトです。

        Raises:
            ValueError: 制約の形式が不正な場合
        """
        return _from_restriction_dict(obj)

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
        choices = _get_attribute_choices(self.attribute)
        choice = get_choice(choices, choice_id=choice_id, choice_name=choice_name)
        return Equals(self.attribute_id, choice["choice_id"])

    def not_has_choice(self, *, choice_id: str | None = None, choice_name: str | None = None) -> Restriction:
        """引数`choice_id`または`choice_name`に一致する選択肢が選択されていないという制約"""
        choices = _get_attribute_choices(self.attribute)
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

    @classmethod
    def _get_required_fields(cls, ast_type: RestrictionAstType) -> set[str]:
        """
        AST種別ごとに必須なフィールド名を返します。

        Args:
            ast_type: ASTノードの種類です。

        Returns:
            AST種別に対応する必須フィールド名です。
        """
        match ast_type:
            case RestrictionAstType.CHECKED | RestrictionAstType.UNCHECKED | RestrictionAstType.IS_EMPTY | RestrictionAstType.IS_NOT_EMPTY:
                return {"attribute_name"}
            case (
                RestrictionAstType.EQUALS_STRING
                | RestrictionAstType.NOT_EQUALS_STRING
                | RestrictionAstType.MATCHES_STRING
                | RestrictionAstType.NOT_MATCHES_STRING
                | RestrictionAstType.EQUALS_INTEGER
                | RestrictionAstType.NOT_EQUALS_INTEGER
            ):
                return {"attribute_name", "value"}
            case RestrictionAstType.HAS_CHOICE | RestrictionAstType.NOT_HAS_CHOICE:
                return {"attribute_name", "choice_name"}
            case RestrictionAstType.HAS_LABEL:
                return {"attribute_name", "label_names"}
            case RestrictionAstType.CAN_INPUT:
                return {"attribute_name", "enable"}
            case RestrictionAstType.IMPLY:
                return {"premise", "conclusion"}
            case _ as never:
                assert_noreturn(never)

    @model_validator(mode="after")
    def validate_restriction_ast(self) -> "RestrictionAst":  # noqa: PLR0912
        """
        `RestrictionAst` の構造がAST種別に整合しているか検証します。

        Raises:
            ValueError: AST種別に対して必須フィールドが不足している場合、または型が不正な場合
        """
        required_fields = self._get_required_fields(self.type)
        actual_fields = {
            field_name
            for field_name, value in (
                ("attribute_name", self.attribute_name),
                ("value", self.value),
                ("choice_name", self.choice_name),
                ("enable", self.enable),
                ("label_names", self.label_names),
                ("premise", self.premise),
                ("conclusion", self.conclusion),
            )
            if value is not None
        }
        if actual_fields != required_fields:
            raise ValueError(f"AST種別'{self.type}'のフィールドが不正です。 :: required={sorted(required_fields)}, actual={sorted(actual_fields)}")

        match self.type:
            case (
                RestrictionAstType.EQUALS_STRING
                | RestrictionAstType.NOT_EQUALS_STRING
                | RestrictionAstType.MATCHES_STRING
                | RestrictionAstType.NOT_MATCHES_STRING
            ):
                if not isinstance(self.value, str):
                    raise ValueError(f"AST種別'{self.type}'の'value'は文字列である必要があります。")
            case RestrictionAstType.EQUALS_INTEGER | RestrictionAstType.NOT_EQUALS_INTEGER:
                if not isinstance(self.value, int):
                    raise ValueError(f"AST種別'{self.type}'の'value'は整数である必要があります。")
            case RestrictionAstType.HAS_CHOICE | RestrictionAstType.NOT_HAS_CHOICE:
                if not isinstance(self.choice_name, str):
                    raise ValueError(f"AST種別'{self.type}'の'choice_name'は文字列である必要があります。")
            case RestrictionAstType.HAS_LABEL:
                if not isinstance(self.label_names, list) or any(not isinstance(label_name, str) for label_name in self.label_names):
                    raise ValueError("AST種別'has_label'の'label_names'は文字列のリストである必要があります。")
            case RestrictionAstType.CAN_INPUT:
                if not isinstance(self.enable, bool):
                    raise ValueError("AST種別'can_input'の'enable'は真偽値である必要があります。")
            case (
                RestrictionAstType.CHECKED
                | RestrictionAstType.UNCHECKED
                | RestrictionAstType.IS_EMPTY
                | RestrictionAstType.IS_NOT_EMPTY
                | RestrictionAstType.IMPLY
            ):
                pass
            case _ as never:
                assert_noreturn(never)

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

        Raises:
            ValueError: 未知のAST種別が指定された場合
        """

        def flatten_imply_conditions(ast: RestrictionAst) -> tuple[list[RestrictionAst], RestrictionAst]:
            """
            右側にネストした `imply` を条件列と結論へ分解します。

            Args:
                ast: `imply` 種別のASTです。

            Returns:
                条件ASTの一覧と最終的な結論ASTです。
            """
            assert ast.premise is not None
            assert ast.conclusion is not None

            conditions = [ast.premise]
            conclusion = ast.conclusion
            while conclusion.type == RestrictionAstType.IMPLY:
                assert conclusion.premise is not None
                assert conclusion.conclusion is not None
                conditions.append(conclusion.premise)
                conclusion = conclusion.conclusion
            return conditions, conclusion

        def to_human_condition_text(ast: RestrictionAst) -> str:
            """
            条件節で使う人間向け文字列表現へ変換します。

            Args:
                ast: 変換対象のASTです。

            Returns:
                条件節で使いやすい文字列表現です。
            """
            if ast.type == RestrictionAstType.IMPLY:
                return f"({ast.to_human_readable()})"
            return ast.to_human_readable()

        def imply_to_human_readable(ast: RestrictionAst) -> str:
            """
            `imply` AST を自然文スタイルの文字列へ変換します。

            右側にネストした `imply` は条件を畳み込んで、
            `If A and B, C.` のような形へ変換します。

            Args:
                ast: `imply` 種別のASTです。

            Returns:
                自然文スタイルの文字列表現です。
            """
            conditions, conclusion = flatten_imply_conditions(ast)
            conditions_text = " and ".join(to_human_condition_text(condition) for condition in conditions)
            return f"If {conditions_text}, {conclusion.to_human_readable()}."

        if self.type == RestrictionAstType.IMPLY:
            return imply_to_human_readable(self)

        assert self.attribute_name is not None
        attribute_name = repr(self.attribute_name)
        return _restriction_ast_to_human_readable_text(self, attribute_name=attribute_name)


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

    @field_serializer("attribute_type")
    def serialize_attribute_type(self, attribute_type: AdditionalDataDefinitionType) -> str:
        return attribute_type.value

    @field_serializer("allowed_ast_types")
    def serialize_allowed_ast_types(self, allowed_ast_types: list[RestrictionAstType]) -> list[str]:
        return [ast_type.value for ast_type in allowed_ast_types]


def get_attribute_restriction_catalog(annotation_specs: dict[str, Any]) -> list[AttributeRestrictionCatalogItem]:
    """
    属性制約ASTを組み立てるための属性カタログを返します。

    Args:
        annotation_specs: アノテーション仕様(v3)の情報です。

    Returns:
        LLMへのプロンプトや入力候補生成に使いやすい属性カタログです。
    """

    def get_allowed_ast_types(attribute_type: AdditionalDataDefinitionType) -> list[RestrictionAstType]:
        """
        属性種類ごとに利用可能なAST種別を返します。

        Args:
            attribute_type: アノテーション仕様上の属性種類です。

        Returns:
            指定した属性種類で利用可能なAST種別の一覧です。
        """
        match attribute_type:
            case "flag":
                return [RestrictionAstType.CAN_INPUT, RestrictionAstType.CHECKED, RestrictionAstType.UNCHECKED]
            case "text" | "comment":
                return [
                    RestrictionAstType.CAN_INPUT,
                    RestrictionAstType.IS_EMPTY,
                    RestrictionAstType.IS_NOT_EMPTY,
                    RestrictionAstType.EQUALS_STRING,
                    RestrictionAstType.NOT_EQUALS_STRING,
                    RestrictionAstType.MATCHES_STRING,
                    RestrictionAstType.NOT_MATCHES_STRING,
                ]
            case "integer":
                return [
                    RestrictionAstType.CAN_INPUT,
                    RestrictionAstType.IS_EMPTY,
                    RestrictionAstType.IS_NOT_EMPTY,
                    RestrictionAstType.EQUALS_INTEGER,
                    RestrictionAstType.NOT_EQUALS_INTEGER,
                ]
            case "link":
                return [
                    RestrictionAstType.CAN_INPUT,
                    RestrictionAstType.IS_EMPTY,
                    RestrictionAstType.IS_NOT_EMPTY,
                    RestrictionAstType.HAS_LABEL,
                ]
            case "tracking":
                return [
                    RestrictionAstType.CAN_INPUT,
                    RestrictionAstType.IS_EMPTY,
                    RestrictionAstType.IS_NOT_EMPTY,
                    RestrictionAstType.EQUALS_STRING,
                    RestrictionAstType.NOT_EQUALS_STRING,
                ]
            case "choice" | "select":
                return [
                    RestrictionAstType.CAN_INPUT,
                    RestrictionAstType.IS_EMPTY,
                    RestrictionAstType.IS_NOT_EMPTY,
                    RestrictionAstType.HAS_CHOICE,
                    RestrictionAstType.NOT_HAS_CHOICE,
                ]
            case _:
                raise ValueError(f"未対応の属性種類です。 :: attribute_type='{attribute_type}'")

    accessor = AnnotationSpecsAccessor(annotation_specs)
    catalog: list[AttributeRestrictionCatalogItem] = []
    for attribute in accessor.additionals:
        attribute_type = attribute["type"]
        choice_names = None
        label_names = None
        match attribute_type:
            case "choice" | "select":
                choice_names = [get_english_message(choice["name"]) for choice in _get_attribute_choices(attribute)]
            case "link":
                label_names = [get_english_message(label["label_name"]) for label in accessor.labels]
        item = AttributeRestrictionCatalogItem(
            attribute_name=get_english_message(attribute["name"]),
            attribute_type=attribute_type,
            allowed_ast_types=get_allowed_ast_types(attribute_type),
            choice_names=choice_names,
            label_names=label_names,
        )
        catalog.append(item)
    return catalog


def _get_attribute_choices(attribute: AttributeDefinition) -> list[AttributeChoice]:
    """
    属性定義から選択肢一覧を取得します。

    Args:
        attribute: アノテーション仕様上の属性定義です。

    Returns:
        属性に紐づく選択肢一覧です。

    Raises:
        ValueError: 選択肢を持たない属性に対して呼び出された場合
    """
    choices = attribute["choices"]
    if choices is None:
        raise ValueError(f"属性(type='{attribute['type']}')には選択肢がありません。")
    return choices


def _from_restriction_dict(obj: dict[str, Any]) -> Restriction:
    """
    API向けの制約辞書から `Restriction` を復元します。

    Args:
        obj: APIの `restrictions` 要素を表す辞書です。
    Returns:
        復元した `Restriction` オブジェクトです。
    """
    attribute_id = obj["additional_data_definition_id"]
    condition = obj["condition"]
    return _from_condition_dict(attribute_id=attribute_id, condition=condition)


def _restriction_ast_to_human_readable_text(ast: RestrictionAst, *, attribute_name: str) -> str:  # noqa: PLR0912
    """
    `imply` 以外のASTを人間向けの読みやすい文字列へ変換します。

    Args:
        ast: 変換対象のASTです。
        attribute_name: `repr()` 済みの属性名です。

    Returns:
        人間向けの読みやすい文字列です。
    """
    match ast.type:
        case RestrictionAstType.CHECKED:
            text = f"{attribute_name} is checked"
        case RestrictionAstType.UNCHECKED:
            text = f"{attribute_name} is unchecked"
        case RestrictionAstType.IS_EMPTY:
            text = f"{attribute_name} is empty"
        case RestrictionAstType.IS_NOT_EMPTY:
            text = f"{attribute_name} is not empty"
        case RestrictionAstType.EQUALS_STRING | RestrictionAstType.EQUALS_INTEGER:
            text = f"{attribute_name} is " + repr(ast.value)
        case RestrictionAstType.NOT_EQUALS_STRING | RestrictionAstType.NOT_EQUALS_INTEGER:
            text = f"{attribute_name} is not " + repr(ast.value)
        case RestrictionAstType.MATCHES_STRING:
            text = f"{attribute_name} matches " + repr(ast.value)
        case RestrictionAstType.NOT_MATCHES_STRING:
            text = f"{attribute_name} does not match " + repr(ast.value)
        case RestrictionAstType.HAS_CHOICE:
            text = f"{attribute_name} is " + repr(ast.choice_name)
        case RestrictionAstType.NOT_HAS_CHOICE:
            text = f"{attribute_name} is not " + repr(ast.choice_name)
        case RestrictionAstType.HAS_LABEL:
            assert ast.label_names is not None
            text = f"{attribute_name} has labels {', '.join(repr(label_name) for label_name in ast.label_names)}"
        case RestrictionAstType.CAN_INPUT:
            assert ast.enable is not None
            text = f"{attribute_name} can be edited" if ast.enable else f"{attribute_name} is read-only"
        case RestrictionAstType.IMPLY:
            raise AssertionError("`imply`は事前に処理されるため、ここには到達しません。")
        case _ as never:
            assert_noreturn(never)
    return text


def _from_condition_dict(*, attribute_id: str, condition: dict[str, Any]) -> Restriction:
    """
    条件部分の辞書から `Restriction` を復元します。

    Args:
        attribute_id: 対象属性のIDです。
        condition: 条件部分のみを表す辞書です。
    Returns:
        復元した `Restriction` オブジェクトです。
    """
    condition_type = condition["_type"]
    restriction: Restriction
    match condition_type:
        case "Imply":
            premise_restriction = _from_restriction_dict(condition["premise"])
            conclusion_restriction = _from_condition_dict(attribute_id=attribute_id, condition=condition["condition"])
            restriction = Imply(premise_restriction=premise_restriction, conclusion_restriction=conclusion_restriction)
        case "CanInput":
            restriction = CanInput(attribute_id, enable=condition["enable"])
        case "Equals":
            restriction = Equals(attribute_id, value=condition["value"])
        case "NotEquals":
            restriction = NotEquals(attribute_id, value=condition["value"])
        case "Matches":
            restriction = Matches(attribute_id, value=condition["value"])
        case "NotMatches":
            restriction = NotMatches(attribute_id, value=condition["value"])
        case "HasLabel":
            restriction = HasLabel(attribute_id, label_ids=condition["labels"])
        case _:
            raise ValueError(f"未知の制約種別です。 :: _type='{condition_type}'")
    return restriction


def _ast_to_atomic_restriction(ast: RestrictionAst, *, fac: AttributeFactory, attribute: AttributeDefinition) -> Restriction:  # noqa: PLR0912
    assert ast.attribute_name is not None
    attribute_type = attribute["type"]
    restriction: Restriction

    match ast.type:
        case RestrictionAstType.CHECKED:
            restriction = fac.checkbox(attribute_name=ast.attribute_name).checked()
        case RestrictionAstType.UNCHECKED:
            restriction = fac.checkbox(attribute_name=ast.attribute_name).unchecked()
        case RestrictionAstType.IS_EMPTY:
            restriction = _attribute_with_empty_check(fac, ast.attribute_name).is_empty()
        case RestrictionAstType.IS_NOT_EMPTY:
            restriction = _attribute_with_empty_check(fac, ast.attribute_name).is_not_empty()
        case RestrictionAstType.CAN_INPUT:
            assert ast.enable is not None
            attribute_obj = _create_attribute_object_with_name(fac, ast.attribute_name)
            restriction = attribute_obj.enabled() if ast.enable else attribute_obj.disabled()
        case RestrictionAstType.EQUALS_STRING | RestrictionAstType.NOT_EQUALS_STRING:
            restriction = _ast_string_equality_to_restriction(ast=ast, fac=fac, attribute=attribute, attribute_type=attribute_type)
        case RestrictionAstType.MATCHES_STRING | RestrictionAstType.NOT_MATCHES_STRING:
            restriction = _ast_string_match_to_restriction(ast=ast, fac=fac, attribute=attribute, attribute_type=attribute_type)
        case RestrictionAstType.EQUALS_INTEGER | RestrictionAstType.NOT_EQUALS_INTEGER:
            assert isinstance(ast.value, int)
            attribute_obj = fac.integer_textbox(attribute_name=ast.attribute_name)
            match ast.type:
                case RestrictionAstType.EQUALS_INTEGER:
                    restriction = attribute_obj.equals(ast.value)
                case RestrictionAstType.NOT_EQUALS_INTEGER:
                    restriction = attribute_obj.not_equals(ast.value)
                case _:
                    raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")
        case RestrictionAstType.HAS_CHOICE | RestrictionAstType.NOT_HAS_CHOICE:
            assert ast.choice_name is not None
            attribute_obj = fac.selection(attribute_name=ast.attribute_name)
            match ast.type:
                case RestrictionAstType.HAS_CHOICE:
                    restriction = attribute_obj.has_choice(choice_name=ast.choice_name)
                case RestrictionAstType.NOT_HAS_CHOICE:
                    restriction = attribute_obj.not_has_choice(choice_name=ast.choice_name)
                case _:
                    raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")
        case RestrictionAstType.HAS_LABEL:
            assert ast.label_names is not None
            restriction = fac.annotation_link(attribute_name=ast.attribute_name).has_label(label_names=ast.label_names)
        case RestrictionAstType.IMPLY:
            raise AssertionError("`imply`は `_ast_to_restriction` で処理されるため、ここには到達しません。")
        case _ as never:
            assert_noreturn(never)
    return restriction


def _ast_string_equality_to_restriction(
    *,
    ast: RestrictionAst,
    fac: AttributeFactory,
    attribute: AttributeDefinition,
    attribute_type: AdditionalDataDefinitionType,
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
        case RestrictionAstType.EQUALS_STRING:
            return attribute_obj.equals(ast.value)
        case RestrictionAstType.NOT_EQUALS_STRING:
            return attribute_obj.not_equals(ast.value)
        case _:
            raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")


def _ast_string_match_to_restriction(
    *,
    ast: RestrictionAst,
    fac: AttributeFactory,
    attribute: AttributeDefinition,
    attribute_type: AdditionalDataDefinitionType,
) -> Restriction:
    assert isinstance(ast.value, str)
    if attribute_type not in {"text", "comment"}:
        _raise_invalid_ast(attribute=attribute, ast=ast)

    attribute_obj = fac.string_textbox(attribute_name=ast.attribute_name)
    match ast.type:
        case RestrictionAstType.MATCHES_STRING:
            return attribute_obj.matches(ast.value)
        case RestrictionAstType.NOT_MATCHES_STRING:
            return attribute_obj.not_matches(ast.value)
        case _:
            raise ValueError(f"未知のAST種別です。 :: type='{ast.type}'")


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
    attribute_id = attribute["additional_data_definition_id"]
    attribute_type: AdditionalDataDefinitionType = attribute["type"]
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
        case RestrictionAstType.IMPLY:
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
    attribute: AttributeDefinition,
    attribute_name: str,
) -> RestrictionAst:
    attribute_type = attribute["type"]
    match restriction:
        case CanInput(enable=enable):
            return RestrictionAst(type=RestrictionAstType.CAN_INPUT, attribute_name=attribute_name, enable=enable)
        case Equals(value=value):
            return _equals_restriction_to_ast(attribute=attribute, attribute_name=attribute_name, attribute_type=attribute_type, value=value)
        case NotEquals(value=value):
            return _not_equals_restriction_to_ast(attribute=attribute, attribute_name=attribute_name, attribute_type=attribute_type, value=value)
        case Matches(value=value) if attribute_type in {"text", "comment"}:
            return RestrictionAst(type=RestrictionAstType.MATCHES_STRING, attribute_name=attribute_name, value=value)
        case NotMatches(value=value) if attribute_type in {"text", "comment"}:
            return RestrictionAst(type=RestrictionAstType.NOT_MATCHES_STRING, attribute_name=attribute_name, value=value)
        case HasLabel(label_ids=label_ids) if attribute_type == "link":
            label_names = [get_english_message(accessor.get_label(label_id=label_id)["label_name"]) for label_id in label_ids]
            return RestrictionAst(type=RestrictionAstType.HAS_LABEL, attribute_name=attribute_name, label_names=label_names)
        case _:
            _raise_invalid_restriction(attribute=attribute, condition=restriction.to_dict()["condition"])


def _equals_restriction_to_ast(
    *,
    attribute: AttributeDefinition,
    attribute_name: str,
    attribute_type: AdditionalDataDefinitionType,
    value: str,
) -> RestrictionAst:
    match attribute_type:
        case "flag" if value == "true":
            return RestrictionAst(type=RestrictionAstType.CHECKED, attribute_name=attribute_name)
        case "text" | "comment" | "integer" | "link" | "tracking" | "choice" | "select" if value == "":
            return RestrictionAst(type=RestrictionAstType.IS_EMPTY, attribute_name=attribute_name)
        case "text" | "comment" | "tracking":
            return RestrictionAst(type=RestrictionAstType.EQUALS_STRING, attribute_name=attribute_name, value=value)
        case "integer":
            return RestrictionAst(
                type=RestrictionAstType.EQUALS_INTEGER,
                attribute_name=attribute_name,
                value=_parse_integer_value(value, attribute=attribute, condition={"_type": "Equals", "value": value}),
            )
        case "choice" | "select":
            choice = get_choice(_get_attribute_choices(attribute), choice_id=value)
            return RestrictionAst(type=RestrictionAstType.HAS_CHOICE, attribute_name=attribute_name, choice_name=get_english_message(choice["name"]))
        case _:
            raise ValueError(f"RestrictionをASTへ変換できません。 :: restriction_type='Equals', attribute_type='{attribute_type}', value={value!r}")


def _not_equals_restriction_to_ast(
    *,
    attribute: AttributeDefinition,
    attribute_name: str,
    attribute_type: AdditionalDataDefinitionType,
    value: str,
) -> RestrictionAst:
    match attribute_type:
        case "flag" if value == "true":
            return RestrictionAst(type=RestrictionAstType.UNCHECKED, attribute_name=attribute_name)
        case "text" | "comment" | "integer" | "link" | "tracking" | "choice" | "select" if value == "":
            return RestrictionAst(type=RestrictionAstType.IS_NOT_EMPTY, attribute_name=attribute_name)
        case "text" | "comment" | "tracking":
            return RestrictionAst(type=RestrictionAstType.NOT_EQUALS_STRING, attribute_name=attribute_name, value=value)
        case "integer":
            return RestrictionAst(
                type=RestrictionAstType.NOT_EQUALS_INTEGER,
                attribute_name=attribute_name,
                value=_parse_integer_value(value, attribute=attribute, condition={"_type": "NotEquals", "value": value}),
            )
        case "choice" | "select":
            choice = get_choice(_get_attribute_choices(attribute), choice_id=value)
            return RestrictionAst(
                type=RestrictionAstType.NOT_HAS_CHOICE,
                attribute_name=attribute_name,
                choice_name=get_english_message(choice["name"]),
            )
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


def _raise_invalid_ast(*, attribute: AttributeDefinition, ast: RestrictionAst) -> NoReturn:
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


def _parse_integer_value(value: str, *, attribute: AttributeDefinition, condition: dict[str, Any]) -> int:
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


def _raise_invalid_restriction(*, attribute: AttributeDefinition, condition: dict[str, Any], detail: str | None = None) -> NoReturn:
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
                type=RestrictionAstType.IMPLY,
                premise=_restriction_to_ast(premise_restriction, accessor=accessor),
                conclusion=_restriction_to_ast(conclusion_restriction, accessor=accessor),
            )

    attribute = accessor.get_attribute(attribute_id=restriction.attribute_id)
    attribute_name = get_english_message(attribute["name"])
    return _restriction_to_atomic_ast(restriction, accessor=accessor, attribute=attribute, attribute_name=attribute_name)
