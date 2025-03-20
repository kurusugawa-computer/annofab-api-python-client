from typing import Any, Literal, Optional, Union

import more_itertools
from more_itertools import first_true

from annofabapi.models import Lang


def get_english_message(internationalization_message: dict[str, Any]) -> str:
    """
    `InternalizationMessage`クラスの値から、英語メッセージを取得します。
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
    messages: list[dict[str, str]] = internationalization_message["messages"]
    result = more_itertools.first_true(messages, pred=lambda e: e["lang"] == Lang.EN_US.value)
    if result is not None:
        return result["message"]
    else:
        raise ValueError(f"'{internationalization_message}'に英語のメッセージは存在しません。")


STR_LANG = Literal["en-US", "ja-JP", "vi-VN"]
"""
対応している ``lang`` の文字列
"""


def get_message_with_lang(internationalization_message: dict[str, Any], lang: Union[Lang, STR_LANG]) -> Optional[str]:
    """
    `InternalizationMessage`クラスの値から、指定した ``lang`` に対応するメッセージを取得します。

    Args:
        internationalization_message: 多言語化されたメッセージ。キー ``messages`` が存在している必要があります。
        lang: 取得したいメッセージに対応する言語コード。

    Returns:
        指定した言語に対応するメッセージ。見つからない場合はNoneを返します。

    """
    messages: list[dict[str, str]] = internationalization_message["messages"]
    if isinstance(lang, Lang):
        str_lang = lang.value
    else:
        str_lang = str(lang)

    result = more_itertools.first_true(messages, pred=lambda e: e["lang"] == str_lang)
    if result is not None:
        return result["message"]
    return None


def get_choice(choices: list[dict[str, Any]], *, choice_id: Optional[str] = None, choice_name: Optional[str] = None) -> dict[str, Any]:
    """
    選択肢情報を取得します。

    Args:
        choice_id: 選択肢ID
        choice_name: 選択肢名(英語)
    """
    if choice_id is not None:
        result = first_true(choices, pred=lambda e: e["choice_id"] == choice_id)
    elif choice_name is not None:
        result = first_true(choices, pred=lambda e: get_english_message(e["name"]) == choice_name)
    else:
        raise ValueError("choice_idまたはchoice_nameのいずれかを指定してください。")
    if result is None:
        raise ValueError(f"選択肢情報が見つかりませんでした。 :: choice_id='{choice_id}', choice_name='{choice_name}'")
    return result


def get_attribute(additionals: list[dict[str, Any]], *, attribute_id: Optional[str] = None, attribute_name: Optional[str] = None) -> dict[str, Any]:
    """
    属性情報を取得します。

    Args:
        attribute_id: 属性ID
        attribute_name: 属性名(英語)
    """
    if attribute_id is not None:
        result = first_true(additionals, pred=lambda e: e["additional_data_definition_id"] == attribute_id)
    elif attribute_name is not None:
        result = first_true(additionals, pred=lambda e: get_english_message(e["name"]) == attribute_name)
    else:
        raise ValueError("attribute_idまたはattribute_nameのいずれかを指定してください。")
    if result is None:
        raise ValueError(f"属性情報が見つかりませんでした。 :: attribute_id='{attribute_id}', attribute_name='{attribute_name}'")
    return result


def get_label(labels: list[dict[str, Any]], *, label_id: Optional[str] = None, label_name: Optional[str] = None) -> dict[str, Any]:
    """
    ラベル情報を取得します。

    Args:
        label_id: ラベルID
        label_name: ラベル名(英語)
    """
    if label_id is not None:
        result = first_true(labels, pred=lambda e: e["label_id"] == label_id)
    elif label_name is not None:
        result = first_true(labels, pred=lambda e: get_english_message(e["label_name"]) == label_name)
    else:
        raise ValueError("label_idまたはlabel_nameのいずれかを指定してください。")
    if result is None:
        raise ValueError(f"ラベル情報が見つかりませんでした。 :: label_id='{label_id}', label_name='{label_name}'")
    return result


class AnnotationSpecsAccessor:
    """
    アノテーション仕様の情報にアクセスするためのクラス。
    
    Args:
        annotation_specs: アノテーション仕様(v3)の情報
    """
    def __init__(self, annotation_specs: dict[str, Any]) -> None:
        self.labels = annotation_specs["labels"]
        self.additionals = annotation_specs["additionals"]

    def get_attribute(self, *, attribute_id: Optional[str] = None, attribute_name: Optional[str] = None) -> dict[str, Any]:
        """
        属性情報を取得します。

        Args:
            attribute_id: 属性ID
            attribute_name: 属性名(英語)
        """
        return get_attribute(self.additionals, attribute_id=attribute_id, attribute_name=attribute_name)

    def get_label(self, *, label_id: Optional[str] = None, label_name: Optional[str] = None) -> dict[str, Any]:
        """
        ラベル情報を取得します。

        Args:
            label_id: ラベルID
            label_name: ラベル名(英語)
        """
        return get_label(self.labels, label_id=label_id, label_name=label_name)
