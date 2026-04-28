---
name: python-coding-style
description: Pythonコードを作成・修正するときに使用。
---

# 全般
* できるだけ型ヒントを付ける。
    * できるだけ汎用的な型ヒントをつける。たとえばlistでもsetでも良いならば、`Collection`や`Iterable`を使う。
    * 特に理由がない限り、`object`や`Any`は避ける。
* docstring は Google スタイルで記述する。
* ログメッセージやコメントは日本語で記述する
* 戻り値をtupleで返そうとする場合は、`NamedTuple`, `dataclass`, pydantic modelの使用を検討して、本当にtupleが適切かどうかを判断する。
* モジュールレベルの定数、クラス属性、インスタンス属性などには直後に docstring として記述する。VSCodeのtooltipに表示させるため。

