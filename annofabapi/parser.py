import abc
import json
import os
import zipfile
from pathlib import Path
from typing import Iterator, List, Optional

from annofabapi.dataclass.annotation import SimpleAnnotation


def _trim_extension(file_path: str) -> str:
    """ファイルパスから拡張子を除去した文字列を返す"""
    return os.path.splitext(file_path)[0]


class LazySimpleAnnotationParser(abc.ABC):
    """
    Simple Annotationの遅延Parser

    Args:
        task_id:
        data_name_base: json_fileの拡張子を取り除いた部分

    """

    __task_id: str
    __data_name_base: str
    __expected_data_name: str

    def __init__(self, task_id: str, data_name_base: str):
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

    @abc.abstractmethod
    def parse(self) -> SimpleAnnotation:
        pass

    @abc.abstractmethod
    def open_outer_file(self, data_uri: str, **kwargs):
        """
        外部ファイル（塗りつぶし画像など）を開き、対応する ファイルオブジェクトを返す。
        Args:
            data_uri: 外部ファイルのパス(input_data_name ディレクトリからのパス）

        Returns:
            外部ファイルのファイルオブジェクト

        """


class LazySimpleAnnotationZipParser(LazySimpleAnnotationParser):
    """
    Simple Annotationのzipファイルの遅延Parser
    """

    __file: zipfile.ZipFile
    __info: zipfile.ZipInfo

    def __init__(self, file: zipfile.ZipFile, info: zipfile.ZipInfo, task_id: str, data_name_base: str):
        self.__file = file
        self.__info = info
        super().__init__(task_id, data_name_base)

    def parse(self) -> SimpleAnnotation:
        with self.__file.open(self.__info) as entry:
            anno_dict: dict = json.load(entry)
            # mypyの "has no attribute "from_dict" " をignore
            return SimpleAnnotation.from_dict(anno_dict)  # type: ignore

    def open_outer_file(self, data_uri: str, **kwargs):
        outer_file_path = _trim_extension(self.__info.filename) + "/" + data_uri
        return self.__file.open(outer_file_path, **kwargs)


class LazySimpleAnnotationDirParser(LazySimpleAnnotationParser):
    """
    Simple Annotationのディレクトリの遅延Parser
    """
    __json_file: Path

    def __init__(self, json_file: Path, task_id: str):
        self.json_file = json_file
        super().__init__(task_id, json_file.stem)

    def parse(self) -> SimpleAnnotation:
        with self.__json_file.open() as f:
            anno_dict: dict = json.load(f)
            return SimpleAnnotation.from_dict(anno_dict)  # type: ignore

    def open_outer_file(self, data_uri: str, **kwargs):
        outer_file_path = _trim_extension(str(self.__json_file)) + "/" + data_uri
        return open(outer_file_path, **kwargs)


def parse_simple_annotation_dir(annotaion_dir_path: Path) -> Iterator[LazySimpleAnnotationParser]:
    """ アノテーションzipを展開したディレクトリ内を探索し、各annotationをparse可能なオブジェクトの列を返します。

    task_idなどを確認して最小限のデータのみをparseすることを目的としたユーティリティです。

    Args:
        annotaion_dir_path: annofabからダウンロードしたsimple annotationのzipファイルを展開したディレクトリ

    Yields:
        annotationの遅延Parseが可能なインスタンス列。 順番は（多分）zipファイル内のエントリー順です
    """

    for task_dir in annotaion_dir_path.iterdir():
        if not task_dir.is_dir():
            continue

        task_id = task_dir.name
        for input_data_file in task_dir.iterdir():
            if not input_data_file.is_file():
                continue

            if not input_data_file.suffix == ".json":
                continue

            parser = LazySimpleAnnotationDirParser(input_data_file, task_id)
            yield parser


def parse_simple_annotation_zip(zip_file_path: Path) -> Iterator[LazySimpleAnnotationParser]:
    """ 引数のzipファイル内を探索し、各annotationをparse可能なオブジェクトの列を返します。

    大量のファイルを含むzipファイルを展開せず、task_idなどを確認して最小限のデータのみをparseすることを目的としたユーティリティです。

    Args:
        zip_file_path: annofabからダウンロードしたsimple annotationのzipファイルへのパス

    Yields:
        annotationの遅延Parseが可能なインスタンス列。 順番は（多分）zipファイル内のエントリー順です
    """
    def lazy_parser(zip_file: zipfile.ZipFile, info: zipfile.ZipInfo) -> Optional[LazySimpleAnnotationParser]:
        paths = [p for p in info.filename.split("/") if len(p) != 0]
        if len(paths) != 2:
            return None
        if not paths[1].endswith(".json"):
            return None

        task_id = paths[0]
        input_data_name = _trim_extension(paths[1])  # .jsonを取り除いたものがdata_name
        return LazySimpleAnnotationZipParser(zip_file, info, task_id, input_data_name)

    with zipfile.ZipFile(zip_file_path, mode="r") as file:
        info_list: List[zipfile.ZipInfo] = file.infolist()

        # 内包表記でiterator作りたいところだけど、withを抜けちゃうので yieldで
        for info in info_list:
            if info.is_dir():
                continue

            parser = lazy_parser(file, info)
            if parser is not None:
                yield parser
