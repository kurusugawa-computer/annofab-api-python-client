"""
属性の制約に関するモジュール。

以下のサンプルコードのように属性名で制約情報を出力できます。

Examples:
    # 「'occluded'チェックボックスがONならば、'note'テキストボックスは空ではない」という制約
    >>> premise_restriction = Checkbox(accessor, attribute_name="occluded").checked()
    >>> conclusion_restriction = StringTextBox(accessor, attribute_name="note").is_not_empty()
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

    # 「'occluded'チェックボックスがONならば、'car_kind'セレクトボックス(ラジオボタン)は選択肢'general_car'を選択しない」という制約
    >>> premise_restriction = Checkbox(accessor, attribute_name="occluded").checked()
    >>> conclusion_restriction = Selection(accessor, attribute_name="car_kind").not_has_choice(choice_name="general_car")
    >>> restriction = premise_restriction.imply(conclusion_restriction)
    >>> restriction.to_dict()
    {
        "additional_data_definition_id": "cbb0155f-1631-48e1-8fc3-43c5f254b6f2",
        "condition": {
            "_type": "Imply",
            "premise": {
                "additional_data_definition_id": "2517f635-2269-4142-8ef4-16312b4cc9f7",
                "condition": {"_type": "Equals", "value": "true"},
            },
            "condition": {"_type": "Equals", "value": "7512ee39-8073-4e24-9b8c-93d99b76b7d2"},
        },
    }
"""

from abc import ABC, abstractmethod
from collections.abc import Collection
from typing import Any, Optional

from annofabapi.util.annotation_specs import AnnotationSpecsAccessor, get_choice


class Restriction(ABC):
    """
    属性の制約を表すクラス。
    """

    def __init__(self, attribute_id: str) -> None:
        self.attribute_id = attribute_id

    def to_dict(self) -> dict[str, Any]:
        """
        アノテーション仕様の`restrictions`に格納できるdictを出力します。
        """
        return {"additional_data_definition_id": self.attribute_id, "condition": self._to_dict_only_condition()}

    @abstractmethod
    def _to_dict_only_condition(self) -> dict[str, Any]:
        """
        制約の条件部分のみdictで出力します。
        """

    def imply(self, conclusion_restriction: "Restriction") -> "Restriction":
        return Imply(premise_restriction=self, conclusion_restriction=conclusion_restriction)


class Imply(Restriction):
    """
    「AならB」という制約を表すクラス

    Args:
        premise_restriction: 前提となる制約
        conclusion_restriction: 最終的に満たしたい制約
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
    def __init__(self, accessor: AnnotationSpecsAccessor, *, attribute_id: Optional[str] = None, attribute_name: Optional[str] = None) -> None:
        self.accessor = accessor
        self.attribute = self.accessor.get_attribute(attribute_id=attribute_id, attribute_name=attribute_name)
        self.attribute_id = self.attribute["additional_data_definition_id"]
        if self._is_valid_attribute_type() is False:
            raise ValueError(f"属性の種類が'{self.attribute['type']}'である属性は、クラス'{self.__class__.__name__}'では扱えません。")

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


class StringTextBox(Attribute, EmptyCheckMixin):
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


class IntegerTextBox(Attribute, EmptyCheckMixin):
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

    def has_label(self, label_ids: Optional[Collection[str]] = None, label_names: Optional[Collection[str]] = None) -> Restriction:
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

    def has_choice(self, *, choice_id: Optional[str] = None, choice_name: Optional[str] = None) -> Restriction:
        """引数`choice_id`または`choice_name`に一致する選択肢が選択されているという制約"""
        choices = self.attribute["choices"]
        choice = get_choice(choices, choice_id=choice_id, choice_name=choice_name)
        return Equals(self.attribute_id, choice["choice_id"])

    def not_has_choice(self, *, choice_id: Optional[str] = None, choice_name: Optional[str] = None) -> Restriction:
        """引数`choice_id`または`choice_name`に一致する選択肢が選択されていないという制約"""
        choices = self.attribute["choices"]
        choice = get_choice(choices, choice_id=choice_id, choice_name=choice_name)
        return NotEquals(self.attribute_id, choice["choice_id"])


######

# accessor = AnnotationSpecsAccessor()
# s.get_attribute(name=)
# Selection("id1", choices=[]).is_selected("choice1").imply()

# Selection(accessor, attribute_name="id1").is_selected("choice1").imply()


# TrackingId(s.get_attribute_id(name="foo"))
