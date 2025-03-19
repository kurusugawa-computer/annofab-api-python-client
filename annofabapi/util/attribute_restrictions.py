"""属性の制約を定義するモジュール。"""

from typing import Any
from abc import ABC, abstractmethod


class Condition(ABC):
    def __init__(self, attr_id):
        self._attr_id = attr_id

    @property
    def attr_id(self) -> str:
        return self._attr_id

    def generate(self) -> dict[str, Any]:
        return {
            "additional_data_definition_id": self.attr_id,
            "condition": self.generate_condition()
        }

    @abstractmethod
    def generate_condition(self) -> dict[str, Any]:
        pass

    def imply(self, condition: Condition) -> Condition2:
        # implyを連続で使えない
        return Imply(self, condition)


class CanInput(Condition):
    def __init__(self, attr_id: str, enable = False):
        super().__init__(attr_id)
        self.enable = enable

    def generate_condition(self) -> dict[str, Any]:
        return {
            "_type": "CanInput",
            "enable": self.enable
        }

class Equals(Condition):
    def __init__(self, attr_id: str, value: str):
        super().__init__(attr_id)
        self.value = value

    def generate_condition(self) -> dict[str, Any]:
        return {
            "_type": "Equals",
            "value": self.value
        }

class NotEquals(Condition):
    def __init__(self, attr_id: str, value: str):
        super().__init__(attr_id)
        self.value = value

    def generate_condition(self) -> dict[str, Any]:
        return {
            "_type": "NotEquals",
            "value": self.value
        }

class Matches(Condition):
    def __init__(self, attr_id: str, re: str):
        super().__init__(attr_id)
        self.re = re

    def generate_condition(self) -> dict[str, Any]:
        return {
            "_type": "Matches",
            "value": self.re
        }

class NotMatches(Condition):
    def __init__(self, attr_id: str, re: str):
        super().__init__(attr_id)
        self.re = re

    def generate_condition(self) -> dict[str, Any]:
        return {
            "_type": "NotMatches",
            "value": self.re
        }

class HasLabel(Condition):
    def __init__(self, attr_id: str, label_ids: list[str]):
        super().__init__(attr_id)
        self.label_ids = label_ids

    def generate_condition(self) -> dict[str, Any]:
        return {
            "_type": "HasLabel",
            "value": self.label_ids
        }

class Imply(Condition):
    def __init__(self, pre_condition: Condition, post_condition: Condition):
        super().__init__(post_condition.attr_id)
        self.pre_condition = pre_condition
        self.post_condition = post_condition

    def generate(self) -> dict[str, Any]:
        return {
            "additional_data_definition_id": self.attr_id,
            "condition": self.generate_condition()
        }

    def generate_condition(self) -> dict[str, Any]:
        return {
            "_type": "Imply",
            "premise": self.pre_condition.generate(),
            "condition": self.post_condition.generate_condition()
        }





class Attribute(ABC):
    def __init__(self, attribute_id: str):
        self.attr_id = attribute_id
        
        
class LinkAttribute:
    """アノテーションリンク属性"""
    pass


class Checkbox(Attribute):
    """チェックボックスの属性"""
    def checked(self) -> Condition:
        return Equals(self.attr_id, value)

    def unchecked(self) -> Condition:
        return Equals(self.attr_id, value)


class StringTextBoxAttribute:
    """文字列用のテキストボックス（自由記述）の属性"""
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

