"""属性の制約を定義するモジュール。"""

from abc import ABC, abstractmethod
from collections.abc import Collection
from typing import Any, Optional

from annofabapi.util.annotation_specs import AnnotationSpecsAccessor, get_choice


class Condition(ABC):
    def __init__(self, attribute_id: str) -> None:
        self.attribute_id = attribute_id

    # @property
    # def attribute_id(self) -> str:
    #     return self._attr_id

    def generate(self) -> dict[str, Any]:
        return {"additional_data_definition_id": self.attribute_id, "condition": self.generate_condition()}

    @abstractmethod
    def generate_condition(self) -> dict[str, Any]:
        pass

    # def imply(self, condition: Condition) -> Condition2:
    #     # implyを連続で使えない
    #     return Imply(self, condition)


class CanInput(Condition):
    def __init__(self, attribute_id: str, enable: bool) -> None:
        super().__init__(attribute_id)
        self.enable = enable

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "CanInput", "enable": self.enable}


class Equals(Condition):
    def __init__(self, attribute_id: str, value: str) -> None:
        super().__init__(attribute_id)
        self.value = value

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "Equals", "value": self.value}


class NotEquals(Condition):
    def __init__(self, attribute_id: str, value: str) -> None:
        super().__init__(attribute_id)
        self.value = value

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "NotEquals", "value": self.value}


class Matches(Condition):
    def __init__(self, attribute_id: str, value: str) -> None:
        super().__init__(attribute_id)
        self.value = value

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "Matches", "value": self.value}


class NotMatches(Condition):
    def __init__(self, attribute_id: str, value: str) -> None:
        super().__init__(attribute_id)
        self.value = value

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "NotMatches", "value": self.value}


class HasLabel(Condition):
    def __init__(self, attribute_id: str, label_ids: Collection[str]) -> None:
        super().__init__(attribute_id)
        self.label_ids = label_ids

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "HasLabel", "labels": list(self.label_ids)}


# class Imply(Condition):
#     def __init__(self, pre_condition: Condition, post_condition: Condition):
#         super().__init__(post_condition.attribute_id)
#         self.pre_condition = pre_condition
#         self.post_condition = post_condition

#     def generate(self) -> dict[str, Any]:
#         return {"additional_data_definition_id": self.attribute_id, "condition": self.generate_condition()}

#     def generate_condition(self) -> dict[str, Any]:
#         return {"_type": "Imply", "premise": self.pre_condition.generate(), "condition": self.post_condition.generate_condition()}


class EmptyCheckMixin:
    """属性が空かどうかを判定するメソッドを提供するMix-inクラス"""

    def is_empty(self) -> Condition:
        """属性が空であるという条件"""
        return Equals(self.attribute_id, "")

    def is_not_empty(self) -> Condition:
        """属性が空でないという条件"""
        return NotEquals(self.attribute_id, "")


class Attribute(ABC):
    def __init__(self, accessor: AnnotationSpecsAccessor, *, attribute_id: Optional[str] = None, attribute_name: Optional[str] = None) -> None:
        self.accessor = accessor
        self.attribute = self.accessor.get_attribute(attribute_id=attribute_id, attribute_name=attribute_name)
        self.attribute_id = self.attribute["additional_data_definition_id"]
        if self._is_valid_attribute_type() is False:
            raise ValueError(f"属性の種類が'{self.attribute['type']}'である属性は、クラス'{self.__class__.__name__}'では扱えません。")

    def disabled(self) -> Condition:
        """属性値を入力できないようにします。"""
        return CanInput(self.attribute_id, enable=False)

    @abstractmethod
    def _is_valid_attribute_type(self) -> bool:
        pass


class Checkbox(Attribute):
    """チェックボックスの属性"""

    def checked(self) -> Condition:
        """チェックされているという条件"""
        return Equals(self.attribute_id, "true")

    def unchecked(self) -> Condition:
        """チェックされていないという条件"""
        return NotEquals(self.attribute_id, "true")

    def _is_valid_attribute_type(self) -> bool:
        return self.attribute["type"] == "flag"


class StringTextBox(Attribute, EmptyCheckMixin):
    """文字列用のテキストボックス（自由記述）の属性"""

    def _is_valid_attribute_type(self) -> bool:
        return self.attribute["type"] in {"text", "comment"}

    def equals(self, value: str) -> Condition:
        return Equals(self.attribute_id, value)

    def not_equals(self, value: str) -> Condition:
        return NotEquals(self.attribute_id, value)

    def matches(self, value: str) -> Condition:
        """引数`value`に渡された正規表現に一致するという条件"""
        return Matches(self.attribute_id, value)

    def not_matches(self, value: str) -> Condition:
        """引数`value`に渡された正規表現に一致しないという条件"""
        return NotMatches(self.attribute_id, value)


class IntegerTextBox(Attribute, EmptyCheckMixin):
    """整数用のテキストボックスの属性"""

    def _is_valid_attribute_type(self) -> bool:
        return self.attribute["type"] == "integer"

    def equals(self, value: int) -> Condition:
        """引数`value`に渡された整数に一致するという条件"""
        return Equals(self.attribute_id, str(value))

    def not_equals(self, value: int) -> Condition:
        """引数`value`に渡された整数に一致しないという条件"""
        return NotEquals(self.attribute_id, str(value))


class AnnotationLink(Attribute, EmptyCheckMixin):
    """アノテーションリンク属性"""

    def _is_valid_attribute_type(self) -> bool:
        return self.attribute["type"] == "link"

    def has_label(self, label_ids: Optional[Collection[str]] = None, label_names: Optional[Collection[str]] = None) -> Condition:
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

    def equals(self, value: str) -> Condition:
        return Equals(self.attribute_id, value)

    def not_equals(self, value: str) -> Condition:
        return NotEquals(self.attribute_id, value)


class Selection(Attribute, EmptyCheckMixin):
    """排他選択の属性（ドロップダウンまたラジオボタン）"""

    def _is_valid_attribute_type(self) -> bool:
        return self.attribute["type"] in {"choice", "select"}

    def is_selected(self, choice_id: str, choice_name: str) -> Condition:
        choices = self.attribute["choices"]
        choice = get_choice(choices, choice_id=choice_id, choice_name=choice_name)
        return Equals(self.attribute_id, choice["choice_id"])

    def is_not_selected(self, choice_id: str, choice_name: str) -> Condition:
        choices = self.attribute["choices"]
        choice = get_choice(choices, choice_id=choice_id, choice_name=choice_name)
        return NotEquals(self.attribute_id, choice["choice_id"])


######

# accessor = AnnotationSpecsAccessor()
# s.get_attribute(name=)
# Selection("id1", choices=[]).is_selected("choice1").imply()

# Selection(accessor, attribute_name="id1").is_selected("choice1").imply()


# TrackingId(s.get_attribute_id(name="foo"))
