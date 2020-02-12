import abc
import json
import os
import re
import warnings
import zipfile
from pathlib import Path
from typing import Any, Generic, Iterator, List, Optional, TypeVar

from annofabapi.dataclass.annotation import FullAnnotation, SimpleAnnotation
from annofabapi.exceptions import AnnotationOuterFileNotFoundError


def _trim_extension(file_path: str) -> str:
    """ファイルパスから拡張子を除去した文字列を返す"""
    return os.path.splitext(file_path)[0]


class SimpleAnnotationParser(abc.ABC):
    """
    Simple Annotationのparser

    以下のフォルダ構成であることを期待します。::

        ├── {task_id}/
        │   ├── {input_data_name}.json
        │   ├── {input_data_name}/
        │   │   ├── {annotation_id}

    Args:
        json_file_path: パースするJSONファイルのパス。

    """
    def __init__(self, json_file_path: str):
        p = Path(json_file_path)
        self.__json_file_path = json_file_path
        self.__task_id = p.parent.name
        self.__expected_input_data_name = _trim_extension(p.name).replace("__", "/")
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
        JSONファイルから決まる、input_data_id.
        Simple(v2)版用です。
         """
        return self.__input_data_id

    @property
    def expected_input_data_name(self) -> str:
        """
        JSONファイル名から決まる、おそらく正しい input_data_nameです。
        Simple(v1)用です。いずれ廃止されるので、非推奨です。
        https://annofab.com/docs/releases/deprecation-announcements.html#notice12

         zipファイル内のファイル名は、input_data_nameになっています。
         しかし、'/'がinput_data_nameに含まれる場合'__'に変換されて格納されています。
         そのため、真に正しいinput_data_nameはファイルの中身をparseしないと見つかりません。
         """
        warnings.warn("deprecated", DeprecationWarning)
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

        Raises:
            AnnotationOuterFileNotFoundError: 外部ファイルが存在しないときに、例外を発生します。

        """

    @abc.abstractmethod
    def parse(self) -> SimpleAnnotation:
        """
        JSONファイルをパースする。
        """


class FullAnnotationParser(abc.ABC):
    """
    Full Annotationのparser

    以下のフォルダ構成であることを期待します。::

        ├── {task_id}/
        │   ├── {input_data_id}.json
        │   ├── {input_data_id}/
        │   │   ├── {annotation_id}

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

        Raises:
            AnnotationOuterFileNotFoundError: 外部ファイルが存在しないときに、例外を発生します。
        """

    @abc.abstractmethod
    def parse(self) -> FullAnnotation:
        """
        JSONファイルをパースする。
        """


class SimpleAnnotationZipParser(SimpleAnnotationParser):
    """
    Simple AnnotationのzipファイルのParser

    Args:
        zip_file: ZipFileオブジェクト。
        json_file_path: パースするJSONファイルのパス。

    Examples:
        JSONファイルをパースする::

            with zipfile.ZipFile('annotation.zip', 'r') as zip_file:
                p = SimpleAnnotationZipParser(zip_file, "task_id/input_data_name.json")
                annotation = p.parse()


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
        try:
            return self.__zip_file.open(outer_file_path, mode="r")
        except KeyError:
            # mypyの `error: "ZipFile" has no attribute "filename"` という警告を無視する
            raise AnnotationOuterFileNotFoundError(str(outer_file_path), self.__zip_file.filename)  # type: ignore


class SimpleAnnotationDirParser(SimpleAnnotationParser):
    """
    Simpleアノテーションzipを展開した、ティレクトリのParser

    Args:
        json_file_path: パースするJSONファイルのパス

    Examples:
        JSONファイルをパースする::

            p = SimpleAnnotationDirParser(Path("task_id/input_data_name.json"))
            annotation = p.parse()

    """
    def __init__(self, json_file_path: Path):
        super().__init__(str(json_file_path))

    def parse(self) -> SimpleAnnotation:
        with open(self.json_file_path, encoding="utf-8") as f:
            anno_dict: dict = json.load(f)
            return SimpleAnnotation.from_dict(anno_dict)  # type: ignore

    def open_outer_file(self, data_uri: str):
        outer_file_path = _trim_extension(self.json_file_path) + "/" + data_uri
        try:
            return open(outer_file_path, mode='rb')
        except FileNotFoundError:
            raise AnnotationOuterFileNotFoundError(str(outer_file_path))


class FullAnnotationZipParser(FullAnnotationParser):
    """
    AnnotationのzipファイルのParser

    Args:
        zip_file: ZipFileオブジェクト。
        json_file_path: パースするJSONファイルのパス。

    Examples:
        JSONファイルをパースする::

            with zipfile.ZipFile('annotation.zip', 'r') as zip_file:
                p = FullAnnotationZipParser(zip_file, "task_id/input_data_name.json")
                annotation = p.parse()


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
        try:
            return self.__zip_file.open(outer_file_path, mode="r")
        except KeyError:
            # mypyの `error: "ZipFile" has no attribute "filename"` という警告を無視する
            raise AnnotationOuterFileNotFoundError(str(outer_file_path), self.__zip_file.filename)  # type: ignore


class FullAnnotationDirParser(FullAnnotationParser):
    """
    Fullアノテーションzipを展開した、ティレクトリのParser


    Args:
        json_file_path: パースするJSONファイルのパス

    Examples:
        JSONファイルをパースする::

            p = FullAnnotationDirParser(Path("task_id/input_data_name.json"))
            annotation = p.parse()

    """
    def __init__(self, json_file_path: Path):
        super().__init__(str(json_file_path))

    def parse(self) -> FullAnnotation:
        with open(self.json_file_path, encoding="utf-8") as f:
            anno_dict: dict = json.load(f)
            return FullAnnotation.from_dict(anno_dict)  # type: ignore

    def open_outer_file(self, data_uri: str):
        outer_file_path = _trim_extension(self.json_file_path) + "/" + data_uri
        try:
            return open(outer_file_path, mode='rb')
        except FileNotFoundError:
            raise AnnotationOuterFileNotFoundError(str(outer_file_path))


S = TypeVar("S", bound=SimpleAnnotationParser)


class SimpleAnnotationParserGroupByTask(Generic[S]):
    """
    Simple Annotationのparserをタスクごとにまとめたもの。


    Args:
        task_id: タスクID
        parser_list: タスク配下のJSONに関するパーサのList

    """
    def __init__(self, task_id: str, parser_list: List[S]):
        self.__task_id = task_id
        self.__parser_list = parser_list

    @property
    def task_id(self) -> str:
        return self.__task_id

    @property
    def parser_list(self) -> List[S]:
        return self.__parser_list


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


def lazy_parse_simple_annotation_zip_by_task(
        zip_file_path: Path) -> Iterator[SimpleAnnotationParserGroupByTask[SimpleAnnotationZipParser]]:
    """
    Simpleアノテーションzipファイル内を探索し、タスクごとに各annotationをparse可能なオブジェクトの列を返します。

    Args:
        zip_file_path: annofabからダウンロードしたsimple annotationのzipファイルへのパス

    Yields:
        対象タスク内の、annotationの遅延Parseが可能なインスタンス列
    """
    def is_input_data_info_in_task(zip_info: zipfile.ZipInfo, task_id: str) -> bool:
        """
        指定されたtask_id配下の入力データJSONかどうか
        """
        paths = [p for p in zip_info.filename.split("/") if len(p) != 0]
        if len(paths) != 2:
            return False
        if paths[0] != task_id:
            return False
        if not paths[1].endswith(".json"):
            return False

        return True

    with zipfile.ZipFile(zip_file_path, mode="r") as file:
        info_list: List[zipfile.ZipInfo] = file.infolist()
        # 1階層目のディレクトリをtask_idとみなす
        task_info_list = [e for e in info_list if e.is_dir() and len(re.findall("/", e.filename)) == 1]

        for task_info in task_info_list:
            task_id = task_info.filename.split("/")[0]
            parser_list = [
                SimpleAnnotationZipParser(file, e.filename)
                for e in info_list
                if is_input_data_info_in_task(e, task_id)
            ]

            yield SimpleAnnotationParserGroupByTask(task_id, parser_list)


def lazy_parse_simple_annotation_dir_by_task(
        annotaion_dir_path: Path) -> Iterator[SimpleAnnotationParserGroupByTask[SimpleAnnotationDirParser]]:
    """
    Simpleアノテーションzipを展開したディレクトリ内を探索し、タスクごとに各annotationをparse可能なオブジェクトの列を返します。

    Args:
        annotaion_dir_path: annofabからダウンロードしたsimple annotationのzipファイルを展開したディレクトリ

    Yields:
        対象タスク内の、annotationの遅延Parseが可能なインスタンス列
    """

    for task_dir in annotaion_dir_path.iterdir():
        if not task_dir.is_dir():
            continue

        task_id = task_dir.name
        parser_list = [SimpleAnnotationDirParser(e) for e in task_dir.iterdir() if e.is_file() and e.suffix == ".json"]
        yield SimpleAnnotationParserGroupByTask(task_id, parser_list)


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
