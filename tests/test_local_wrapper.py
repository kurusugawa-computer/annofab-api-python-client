from pathlib import Path

from annofabapi.wrapper import Wrapper

data_dir = Path("./tests/data")


class TestWrapperUtils:
    def test__get_mime_type(self):
        assert Wrapper._get_mime_type(str(data_dir / "lenna.png")) == "image/png"
        assert Wrapper._get_mime_type("sample.jpg") == "image/jpeg"
        assert Wrapper._get_mime_type("sample.txt") == "text/plain"
        assert Wrapper._get_mime_type("sample") == "application/octet-stream"
