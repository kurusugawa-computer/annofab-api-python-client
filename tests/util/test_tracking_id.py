import re
import secrets

import pytest

from annofabapi.util.tracking_id import TrackingIdGenerator


class TestTrackingIdGenerator:
    def test_generate__形式と一意性(self):
        generator = TrackingIdGenerator()

        actual = [generator.generate() for _ in range(100)]

        assert len(set(actual)) == len(actual)
        assert all(re.fullmatch(r"[A-Z]{3}-[A-Z]{3}[0-9]", tracking_id) is not None for tracking_id in actual)

    def test_generate__既存のtracking_idと重複したら再生成する(self, monkeypatch: pytest.MonkeyPatch):
        random_values = iter("AAAAAA0BBBBBB1")
        monkeypatch.setattr(secrets, "choice", lambda _: next(random_values))
        generator = TrackingIdGenerator(["AAA-AAA0"])

        actual = generator.generate()

        assert actual == "BBB-BBB1"

    def test_generate__規定回数重複したら例外を送出する(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(secrets, "choice", lambda candidates: candidates[0])
        generator = TrackingIdGenerator(["AAA-AAA0"])

        with pytest.raises(RuntimeError):
            generator.generate()
