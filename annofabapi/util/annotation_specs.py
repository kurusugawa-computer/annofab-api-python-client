from typing import Any, Literal, TypedDict, cast

import more_itertools

from annofabapi.models import Lang
from annofabapi.pydantic_models.additional_data_definition_type import AdditionalDataDefinitionType


class InternationalizationMessageItem(TypedDict):
    """多言語メッセージの1要素です。"""

    lang: str
    message: str


class InternationalizationMessage(TypedDict):
    """多言語メッセージです。"""

    messages: list[InternationalizationMessageItem]


class AttributeChoice(TypedDict):
    """属性の選択肢です。"""

    choice_id: str
    name: InternationalizationMessage


class AttributeDefinition(TypedDict):
    """アノテーション仕様上の属性定義です。"""

    additional_data_definition_id: str
    name: InternationalizationMessage
    type: AdditionalDataDefinitionType
    choices: list[AttributeChoice] | None


class LabelDefinition(TypedDict):
    """アノテーション仕様上のラベル定義です。"""

    label_id: str
    label_name: InternationalizationMessage
    additional_data_definitions: list[str]


def get_english_message(internationalization_message: InternationalizationMessage | dict[str, Any]) -> str:
    """
    `InternationalizationMessage`クラスの値から、英語メッセージを取得します。
    英語メッセージが見つからない場合は ``ValueError`` をスローします。

    Notes:
        英語メッセージは必ず存在するはずなので、英語メッセージが見つからない場合は ``ValueError`` をスローするようにしました。

    Args:
        internationalization_message: 多言語化されたメッセージ。キー ``messages`` が存在している必要があります。

    Returns:
        指定した言語に対応するメッセージ。

    Raises:
        ValueError: 英語メッセージが見つからない場合
    """
    messages = cast(list[InternationalizationMessageItem], internationalization_message["messages"])
    result = more_itertools.first_true(messages, pred=lambda e: e["lang"] == Lang.EN_US.value)
    if result is not None:
        return result["message"]
    else:
        raise ValueError(f"'{internationalization_message}'に英語のメッセージは存在しません。")


STR_LANG = Literal["en-US", "ja-JP", "vi-VN"]
"""
対応している ``lang`` の文字列
"""


def get_message_with_lang(internationalization_message: InternationalizationMessage | dict[str, Any], lang: Lang | STR_LANG) -> str | None:
    """
    `InternationalizationMessage`クラスの値から、指定した ``lang`` に対応するメッセージを取得します。

    Args:
        internationalization_message: 多言語化されたメッセージ。キー ``messages`` が存在している必要があります。
        lang: 取得したいメッセージに対応する言語コード。

    Returns:
        指定した言語に対応するメッセージ。見つからない場合はNoneを返します。

    """
    messages = cast(list[InternationalizationMessageItem], internationalization_message["messages"])
    if isinstance(lang, Lang):
        str_lang = lang.value
    else:
        str_lang = str(lang)

    result = more_itertools.first_true(messages, pred=lambda e: e["lang"] == str_lang)
    if result is not None:
        return result["message"]
    return None


def get_choice(choices: list[AttributeChoice], *, choice_id: str | None = None, choice_name: str | None = None) -> AttributeChoice:
    """
    選択肢情報を取得します。

    Args:
        choice_id: 選択肢ID
        choice_name: 選択肢名(英語)

    Raises:
        ValueError: 'choice_id'か'choice_name'の指定方法が間違っている。または引数に合致する選択肢情報が見つからない。または複数見つかった。

    """
    if choice_id is not None and choice_name is not None:
        raise ValueError("'choice_id'か'choice_name'のどちらかはNoneにしてください。")

    if choice_id is not None:
        result = [e for e in choices if e["choice_id"] == choice_id]
    elif choice_name is not None:
        result = [e for e in choices if get_english_message(e["name"]) == choice_name]
    else:
        raise ValueError("'choice_id'か'choice_name'のどちらかはNone以外にしてください。")

    if len(result) == 0:
        raise ValueError(f"選択肢情報が見つかりませんでした。 :: choice_id='{choice_id}', choice_name='{choice_name}'")
    if len(result) > 1:
        raise ValueError(f"選択肢情報が複数（{len(result)}件）見つかりました。 :: choice_id='{choice_id}', choice_name='{choice_name}'")
    return result[0]


def get_attribute(
    additionals: list[AttributeDefinition],
    *,
    attribute_id: str | None = None,
    attribute_name: str | None = None,
    label: LabelDefinition | None = None,
) -> AttributeDefinition:
    """
    属性情報を取得します。

    Args:
        attribute_id: 属性ID
        attribute_name: 属性名(英語)
        label: Noneでなければ、指定したラベルに紐づく属性情報を取得します。

    Raises:
        ValueError: 'attribute_id'か'attribute_name'の指定方法が間違っている。または引数に合致する属性情報が見つからない。または複数見つかった。
    """
    if attribute_id is not None and attribute_name is not None:
        raise ValueError("'attribute_id'か'attribute_name'のどちらかはNoneにしてください。")

    if attribute_id is not None:
        result = [e for e in additionals if e["additional_data_definition_id"] == attribute_id]
    elif attribute_name is not None:
        result = [e for e in additionals if get_english_message(e["name"]) == attribute_name]
    else:
        raise ValueError("'attribute_id'か'attribute_name'のどちらかはNone以外にしてください。")

    label_name = None
    if label is not None:
        result = [e for e in result if e["additional_data_definition_id"] in label["additional_data_definitions"]]
        label_name = get_english_message(label["label_name"])

    if len(result) == 0:
        raise ValueError(
            f"属性情報が見つかりませんでした。 :: attribute_id='{attribute_id}', attribute_name='{attribute_name}', label_name='{label_name}'"
        )
    if len(result) > 1:
        raise ValueError(
            f"属性情報が複数（{len(result)}件）見つかりました。 :: attribute_id='{attribute_id}', attribute_name='{attribute_name}', label_name='{label_name}'"  # noqa: E501
        )
    return result[0]


def get_label(labels: list[LabelDefinition], *, label_id: str | None = None, label_name: str | None = None) -> LabelDefinition:
    """
    ラベル情報を取得します。

    Args:
        label_id: ラベルID
        label_name: ラベル名(英語)

    Raises:
        ValueError: 'label_id'か'label_name'の指定方法が間違っている。または引数に合致するラベル情報が見つからない。または複数見つかった。

    """
    if label_id is not None and label_name is not None:
        raise ValueError("'label_id'か'label_name'のどちらかはNoneにしてください。")

    if label_id is not None:
        result = [e for e in labels if e["label_id"] == label_id]
    elif label_name is not None:
        result = [e for e in labels if get_english_message(e["label_name"]) == label_name]
    else:
        raise ValueError("'label_id'か'label_name'のどちらかはNone以外にしてください。")

    if len(result) == 0:
        raise ValueError(f"ラベル情報が見つかりませんでした。 :: label_id='{label_id}', label_name='{label_name}'")
    if len(result) > 1:
        raise ValueError(f"ラベル情報が複数（{len(result)}件）見つかりました。 :: label_id='{label_id}', label_name='{label_name}'")
    return result[0]


class AnnotationSpecsAccessor:
    """
    アノテーション仕様の情報にアクセスするためのクラス。

    Args:
        annotation_specs: アノテーション仕様(v3)の情報
    """

    def __init__(self, annotation_specs: dict[str, Any]) -> None:
        self.annotation_specs = annotation_specs
        self.labels: list[LabelDefinition] = annotation_specs["labels"]
        self.additionals: list[AttributeDefinition] = annotation_specs["additionals"]

    def get_attribute(
        self, *, attribute_id: str | None = None, attribute_name: str | None = None, label: LabelDefinition | None = None
    ) -> AttributeDefinition:
        """
        属性情報を取得します。

        Args:
            attribute_id: 属性ID
            attribute_name: 属性名(英語)
            label: Noneでなければ、指定したラベルに紐づく属性情報を取得します。

        Raises:
            ValueError: 'attribute_id'か'attribute_name'の指定方法が間違っている。または引数に合致する属性情報が見つからない。または複数見つかった。

        """
        return get_attribute(self.additionals, attribute_id=attribute_id, attribute_name=attribute_name, label=label)

    def get_label(self, *, label_id: str | None = None, label_name: str | None = None) -> LabelDefinition:
        """
        ラベル情報を取得します。

        Args:
            label_id: ラベルID
            label_name: ラベル名(英語)

        Raises:
            ValueError: 'label_id'か'label_name'の指定方法が間違っている。または引数に合致するラベル情報が見つからない。または複数見つかった。

        """
        return get_label(self.labels, label_id=label_id, label_name=label_name)
