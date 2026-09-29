import re
import secrets

import pytest

from annofabapi.util.tracking_id import TrackingIdGenerator


class TestTrackingIdGenerator:
    def test_generate__形式(self, monkeypatch: pytest.MonkeyPatch):
        random_values = iter("ABCDEF7")
        monkeypatch.setattr(secrets, "choice", lambda _: next(random_values))
        generator = TrackingIdGenerator()

        actual = generator.generate()

        assert actual == "ABC-DEF7"
        assert re.fullmatch(r"[A-Z]{3}-[A-Z]{3}[0-9]", actual) is not None

    def test_generate__生成済みのtracking_idと重複したら再生成する(self, monkeypatch: pytest.MonkeyPatch):
        random_values = iter("AAAAAA0AAAAAA0BBBBBB1")
        monkeypatch.setattr(secrets, "choice", lambda _: next(random_values))
        generator = TrackingIdGenerator()

        actual = [generator.generate(), generator.generate()]

        assert actual == ["AAA-AAA0", "BBB-BBB1"]

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
