from typing import NoReturn


def assert_noreturn(x: NoReturn) -> NoReturn:
    """python 3.11 以降に追加されたassert_neverの代わり"""
    raise AssertionError(f"Invalid value: {x!r}")  # x!rは repr(x)と等価
