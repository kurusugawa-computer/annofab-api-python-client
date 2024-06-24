from __future__ import annotations

from typing import Any, Literal, Optional, Union

import more_itertools

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
