import json
import zipfile
from pathlib import Path
from typing import Iterator, List, Optional

from annofabapi.dataclass import afanno


class LazyAnnotationParser:
    __file: zipfile.ZipFile
    __info: zipfile.ZipInfo
    __task_id: str
    __input_data_name: str
    __expected_data_name: str

    def __init__(self, file: zipfile.ZipFile, info: zipfile.ZipInfo, task_id: str, data_name_base: str):
        self.__file = file
        self.__info = info
        self.__task_id = task_id
        self.__data_name_base = data_name_base
        self.__expected_data_name = data_name_base.replace("__", "/")

    @property
    def task_id(self) -> str:
        return self.__task_id

    @property
    def expected_input_data_name(self) -> str:
        """ おそらく正しい、input_data_nameです。

         zipファイル内のファイル名は、input_data_nameになっています。
         しかし、'/'がinput_data_nameに含まれる場合'__'に変換されて格納されています。
         そのため、真に正しいinput_data_nameはファイルの中身をparseしないと見つかりません。
         """
        return self.__expected_data_name

    def can_match_input_data_name(self, input_data_name: str) -> bool:
        """ 引数に与えたinput_data_nameが、parse結果のinput_data_nameと一致し得るかどうかを判定します。

        Args:
            input_data_name: テストしたい input_at_name

        Returns: Trueの場合、input_data_nameが真に一致する可能性がある。 Falseの場合、一致しない

        """
        return input_data_name.replace("/", "__") == self.__data_name_base

    def parse(self) -> afanno.SimpleAnnotation:
        def parse_detail(d: dict) -> afanno.SimpleAnnotationDetail:
            return afanno.SimpleAnnotationDetail(annotation_id=["annotation_id"], label=d["label"],
                                                 attributes=d["attributes"], data=d["data"])

        with self.__file.open(self.__info) as entry:
            anno_dict: dict = json.load(entry)
            detail_arr: List[dict] = anno_dict["details"]

            return afanno.SimpleAnnotation(project_id=anno_dict["project_id"], task_id=anno_dict["task_id"],
                                           input_data_id=anno_dict["input_data_id"],
                                           input_data_name=anno_dict["input_data_name"],
                                           comment=anno_dict.get("comment",
                                                                 ""), details=[parse_detail(d) for d in detail_arr])


def parse_simple_zip(zip_file_path: Path) -> Iterator[LazyAnnotationParser]:
    """ 引数のzipファイル内を探索し、各annotationをparse可能なオブジェクトの列を返します。

    大量のファイルを含むzipファイルを展開せず、task_idなどを確認して最小限のデータのみをparseすることを目的としたユーティリティです。

    Args:
        zip_file_path: annofabからダウンロードしたsimple annotationのzipファイルへのパス

    Yields:
        annotationの遅延Parseが可能なインスタンス列。 順番は（多分）zipファイル内のエントリー順です
    """
    def lazy_parser(zip_file: zipfile.ZipFile, info: zipfile.ZipInfo) -> Optional[LazyAnnotationParser]:
        paths = [p for p in info.filename.split("/") if len(p) != 0]
        if len(paths) != 2:
            return None
        if not paths[1].endswith(".json"):
            return None

        task_id = paths[0]
        input_data_name = paths[1][0:-5]  # .jsonを取り除いたものがdata_name
        return LazyAnnotationParser(zip_file, info, task_id, input_data_name)

    with zipfile.ZipFile(zip_file_path, mode="r") as file:
        info_list: List[zipfile.ZipInfo] = file.infolist()

        # 内包表記でiterator作りたいところだけど、withを抜けちゃうので yieldで
        for info in info_list:
            if info.is_dir():
                continue

            parser = lazy_parser(file, info)
            if parser is not None:
                yield parser
