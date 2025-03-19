"""属性の制約を定義するモジュール。"""

from typing import Any
from abc import ABC, abstractmethod


class Condition(ABC):
    def __init__(self, attribute_id):
        self._attr_id = attribute_id

    @property
    def attr_id(self) -> str:
        return self._attr_id

    def generate(self) -> dict[str, Any]:
        return {"additional_data_definition_id": self.attr_id, "condition": self.generate_condition()}

    @abstractmethod
    def generate_condition(self) -> dict[str, Any]:
        pass

    # def imply(self, condition: Condition) -> Condition2:
    #     # implyを連続で使えない
    #     return Imply(self, condition)


class CanInput(Condition):
    def __init__(self, attribute_id: str, enable: bool):
        super().__init__(attribute_id)
        self.enable = enable

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "CanInput", "enable": self.enable}


class Equals(Condition):
    def __init__(self, attribute_id: str, value: str):
        super().__init__(attribute_id)
        self.value = value

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "Equals", "value": self.value}


class NotEquals(Condition):
    def __init__(self, attribute_id: str, value: str):
        super().__init__(attribute_id)
        self.value = value

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "NotEquals", "value": self.value}


class Matches(Condition):
    def __init__(self, attribute_id: str, value: str):
        super().__init__(attribute_id)
        self.value = value

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "Matches", "value": self.value}


class NotMatches(Condition):
    def __init__(self, attribute_id: str, value: str):
        super().__init__(attribute_id)
        self.value = value

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "NotMatches", "value": self.value}


class HasLabel(Condition):
    def __init__(self, attr_id: str, label_ids: list[str]):
        super().__init__(attr_id)
        self.label_ids = label_ids

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "HasLabel", "value": self.label_ids}


class Imply(Condition):
    def __init__(self, pre_condition: Condition, post_condition: Condition):
        super().__init__(post_condition.attr_id)
        self.pre_condition = pre_condition
        self.post_condition = post_condition

    def generate(self) -> dict[str, Any]:
        return {"additional_data_definition_id": self.attr_id, "condition": self.generate_condition()}

    def generate_condition(self) -> dict[str, Any]:
        return {"_type": "Imply", "premise": self.pre_condition.generate(), "condition": self.post_condition.generate_condition()}


class Attribute(ABC):
    def __init__(self, attribute_id: str) -> None:
        self.attribute_id = attribute_id

    def disabled(self) -> Condition:
        """属性値を入力できないようにします。"""
        return CanInput(self.attribute_id, enable=False)


class Checkbox(Attribute):
    """チェックボックスの属性"""

    def checked(self) -> Condition:
        """チェックされているという条件"""
        return Equals(self.attribute_id, "true")

    def unchecked(self) -> Condition:
        """チェックされていないという条件"""
        return NotEquals(self.attribute_id, "true")


class StringTextBox(Attribute):
    """文字列用のテキストボックス（自由記述）の属性"""

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


class LinkAttribute:
    """アノテーションリンク属性"""

    pass


class IntegerTextBoxAttribute:
    """整数用のテキストボックスの属性"""

    pass


class SelectionAttribute:
    """排他選択の属性（ドロップダウンまたラジオボタン）"""

    pass


class TrackingIdAttribute:
    """トラッキングID属性"""

    pass
