import abc
import json
import os
import zipfile
from pathlib import Path
from typing import Any, Iterator, List, Optional

from annofabapi.dataclass.annotation import FullAnnotation, SimpleAnnotation


def _trim_extension(file_path: str) -> str:
    """ファイルパスから拡張子を除去した文字列を返す"""
    return os.path.splitext(file_path)[0]


class SimpleAnnotationParser(abc.ABC):
    """
    Simple Annotationのparser

    以下のフォルダ構成であることを期待します。

    ```
    ├── {task_id}/
    │   ├── {input_data_name}.json
    │   ├── {input_data_name}/
    │   │   ├── {annotation_id}
    ```

    Args:
        json_file_path: パースするJSONファイルのパス。

    """
    def __init__(self, json_file_path: str):
        p = Path(json_file_path)
        self.__json_file_path = json_file_path
        self.__task_id = p.parent.name
        self.__expected_input_data_name = _trim_extension(p.name).replace("__", "/")

    @property
    def task_id(self) -> str:
        """JSONファイルの親ディレクトリ名から決まる task_id """
        return self.__task_id

    @property
    def json_file_path(self) -> str:
        """
        パースするJSONファイルのパス。
        """
        return self.__json_file_path

    @property
    def expected_input_data_name(self) -> str:
        """
        JSONファイル名から決まる、おそらく正しい input_data_nameです。

         zipファイル内のファイル名は、input_data_nameになっています。
         しかし、'/'がinput_data_nameに含まれる場合'__'に変換されて格納されています。
         そのため、真に正しいinput_data_nameはファイルの中身をparseしないと見つかりません。
         """
        return self.__expected_input_data_name

    @abc.abstractmethod
    def open_outer_file(self, data_uri: str):
        """
        外部ファイル（塗りつぶし画像など）を開き、対応するファイルオブジェクトを返す。
        JSONファイルと同階層にある、"JSONファイルの拡張子を除いた名前"のディレクトリ配下を探します。

        Args:
            data_uri: 外部ファイルのパス

        Returns:
            外部ファイルのファイルオブジェクト

        """
    @abc.abstractmethod
    def parse(self) -> SimpleAnnotation:
        """
        JSONファイルをパースする。
        """


class FullAnnotationParser(abc.ABC):
    """
    Full Annotationのparser

    以下のフォルダ構成であることを期待します。

    ```
    ├── {task_id}/
    │   ├── {input_data_id}.json
    │   ├── {input_data_id}/
    │   │   ├── {annotation_id}
    ```

    Args:
        json_file_path: パースするJSONファイルのパス。


    """
    def __init__(self, json_file_path: str):
        p = Path(json_file_path)
        self.__json_file_path = json_file_path
        self.__task_id = p.parent.name
        self.__input_data_id = _trim_extension(p.name)

    @property
    def task_id(self) -> str:
        """JSONファイルの親ディレクトリ名から決まる task_id """
        return self.__task_id

    @property
    def json_file_path(self) -> str:
        """
        パースするJSONファイルのパス。
        """
        return self.__json_file_path

    @property
    def input_data_id(self) -> str:
        """
        JSONファイルから決まる、input_data_id
         """
        return self.__input_data_id

    @abc.abstractmethod
    def open_outer_file(self, data_uri: str):
        """
        外部ファイル（塗りつぶし画像など）を開き、対応するファイルオブジェクトを返す。
        JSONファイルと同階層にある、"JSONファイルの拡張子を除いた名前"のディレクトリ配下を探します。

        Args:
            data_uri: 外部ファイルのパス

        Returns:
            外部ファイルのファイルオブジェクト

        """
    @abc.abstractmethod
    def parse(self) -> FullAnnotation:
        """
        JSONファイルをパースする。
        """


class SimpleAnnotationZipParser(SimpleAnnotationParser):
    """
    Simple AnnotationのzipファイルのParser
    """
    def __init__(self, zip_file: zipfile.ZipFile, json_file_path: str):
        self.__zip_file = zip_file
        super().__init__(json_file_path)

    def parse(self) -> SimpleAnnotation:
        with self.__zip_file.open(self.json_file_path) as entry:
            anno_dict: dict = json.load(entry)
            # mypyの "has no attribute "from_dict" " をignore
            return SimpleAnnotation.from_dict(anno_dict)  # type: ignore

    def open_outer_file(self, data_uri: str):
        outer_file_path = _trim_extension(self.json_file_path) + "/" + data_uri
        return self.__zip_file.open(outer_file_path)


class SimpleAnnotationDirParser(SimpleAnnotationParser):
    """
    Simpleアノテーションzipを展開した、ティレクトリのParser

    Args:
        json_file_path: パースするJSONファイルのパス

    """
    def __init__(self, json_file_path: Path):
        super().__init__(str(json_file_path))

    def parse(self) -> SimpleAnnotation:
        with open(self.json_file_path, encoding="utf-8") as f:
            anno_dict: dict = json.load(f)
            return SimpleAnnotation.from_dict(anno_dict)  # type: ignore

    def open_outer_file(self, data_uri: str):
        outer_file_path = _trim_extension(self.json_file_path) + "/" + data_uri
        return open(outer_file_path, mode='rb')


class FullAnnotationZipParser(FullAnnotationParser):
    """
    Lazy AnnotationのzipファイルのParser
    """
    def __init__(self, zip_file: zipfile.ZipFile, json_file_path: str):
        self.__zip_file = zip_file
        super().__init__(json_file_path)

    def parse(self) -> FullAnnotation:
        with self.__zip_file.open(self.json_file_path) as entry:
            anno_dict: dict = json.load(entry)
            # mypyの "has no attribute "from_dict" " をignore
            return FullAnnotation.from_dict(anno_dict)  # type: ignore

    def open_outer_file(self, data_uri: str):
        outer_file_path = _trim_extension(self.json_file_path) + "/" + data_uri
        return self.__zip_file.open(outer_file_path)


class FullAnnotationDirParser(FullAnnotationParser):
    """
    Full Annotationのディレクトリの遅延Parser
    """
    def __init__(self, json_file_path: Path):
        super().__init__(str(json_file_path))

    def parse(self) -> FullAnnotation:
        with open(self.json_file_path, encoding="utf-8") as f:
            anno_dict: dict = json.load(f)
            return FullAnnotation.from_dict(anno_dict)  # type: ignore

    def open_outer_file(self, data_uri: str):
        outer_file_path = _trim_extension(self.json_file_path) + "/" + data_uri
        return open(outer_file_path, mode='rb')


def __parse_annotation_dir(annotaion_dir_path: Path, clazz) -> Iterator[Any]:
    for task_dir in annotaion_dir_path.iterdir():
        if not task_dir.is_dir():
            continue

        for input_data_file in task_dir.iterdir():
            if not input_data_file.is_file():
                continue

            if not input_data_file.suffix == ".json":
                continue

            parser = clazz(input_data_file)
            yield parser


def lazy_parse_simple_annotation_dir(annotaion_dir_path: Path) -> Iterator[SimpleAnnotationParser]:
    """ Simpleアノテーションzipを展開したディレクトリ内を探索し、各annotationをparse可能なオブジェクトの列を返します。

    Args:
        annotaion_dir_path: annofabからダウンロードしたsimple annotationのzipファイルを展開したディレクトリ

    Yields:
        annotationの遅延Parseが可能なインスタンス列。
    """

    return __parse_annotation_dir(annotaion_dir_path, SimpleAnnotationDirParser)


def lazy_parse_full_annotation_dir(annotaion_dir_path: Path) -> Iterator[SimpleAnnotationParser]:
    """ Fullアノテーションzipを展開したディレクトリ内を探索し、各annotationをparse可能なオブジェクトの列を返します。

    Args:
        annotaion_dir_path: annofabからダウンロードしたsimple annotationのzipファイルを展開したディレクトリ

    Yields:
        annotationの遅延Parseが可能なインスタンス列。
    """
    return __parse_annotation_dir(annotaion_dir_path, FullAnnotationDirParser)


def __parse_annotation_zip(zip_file_path: Path, clazz) -> Iterator[Any]:
    def lazy_parser(zip_file: zipfile.ZipFile, info: zipfile.ZipInfo) -> Optional[Any]:
        paths = [p for p in info.filename.split("/") if len(p) != 0]
        if len(paths) != 2:
            return None
        if not paths[1].endswith(".json"):
            return None

        return clazz(zip_file, info.filename)

    with zipfile.ZipFile(zip_file_path, mode="r") as file:
        info_list: List[zipfile.ZipInfo] = file.infolist()

        # 内包表記でiterator作りたいところだけど、withを抜けちゃうので yieldで
        for info in info_list:
            if info.is_dir():
                continue

            parser = lazy_parser(file, info)
            if parser is not None:
                yield parser


def lazy_parse_simple_annotation_zip(zip_file_path: Path) -> Iterator[SimpleAnnotationParser]:
    """
    Simpleアノテーションzipファイル内を探索し、各annotationをparse可能なオブジェクトの列を返します。


    Args:
        zip_file_path: annofabからダウンロードしたsimple annotationのzipファイルへのパス

    Yields:
        annotationの遅延Parseが可能なインスタンス列。 順番は（多分）zipファイル内のエントリー順です
    """
    return __parse_annotation_zip(zip_file_path, SimpleAnnotationZipParser)


def lazy_parse_full_annotation_zip(zip_file_path: Path) -> Iterator[FullAnnotationParser]:
    """ 引数のFullアノテーションzipファイル内を探索し、各annotationをparse可能なオブジェクトの列を返します。

    大量のファイルを含むzipファイルを展開せず、task_idなどを確認して最小限のデータのみをparseすることを目的としたユーティリティです。

    Args:
        zip_file_path: annofabからダウンロードしたsimple annotationのzipファイルへのパス

    Yields:
        annotationの遅延Parseが可能なインスタンス列。 順番は（多分）zipファイル内のエントリー順です
    """
    return __parse_annotation_zip(zip_file_path, FullAnnotationZipParser)
