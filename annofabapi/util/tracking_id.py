"""Annofabのtracking_idを生成する機能を提供します。"""

import secrets
import string
from collections.abc import Iterable

_LETTERS_PER_GROUP = 3
"""tracking_idのハイフン前後に配置する英字の文字数。"""

_MAX_GENERATION_ATTEMPTS = 100
"""重複しないtracking_idを生成する最大試行回数。"""


class TrackingIdGenerator:
    """タスク内で重複しないtracking_idを生成します。

    このクラスのインスタンスはタスクごとに作成してください。生成したIDは
    インスタンス内に記録され、以降の生成では使用されません。

    Args:
        existing_tracking_ids: タスク内ですでに使用されているtracking_id。
    """

    def __init__(self, existing_tracking_ids: Iterable[str] = ()) -> None:
        self._used_tracking_ids = set(existing_tracking_ids)
        """タスク内で使用済みのtracking_id。"""

    def generate(self) -> str:
        """新しいtracking_idを生成します。

        Returns:
            ``XXX-YYY9`` 形式のtracking_id。

        Raises:
            RuntimeError: 規定回数試行しても未使用のtracking_idを生成できなかった場合。
        """
        for _ in range(_MAX_GENERATION_ATTEMPTS):
            tracking_id = self._generate_candidate()
            if tracking_id in self._used_tracking_ids:
                continue

            self._used_tracking_ids.add(tracking_id)
            return tracking_id

        raise RuntimeError("重複しないtracking_idを生成できませんでした。")

    @staticmethod
    def _generate_candidate() -> str:
        first_letters = "".join(secrets.choice(string.ascii_uppercase) for _ in range(_LETTERS_PER_GROUP))
        last_letters = "".join(secrets.choice(string.ascii_uppercase) for _ in range(_LETTERS_PER_GROUP))
        digit = secrets.choice(string.digits)
        return f"{first_letters}-{last_letters}{digit}"
