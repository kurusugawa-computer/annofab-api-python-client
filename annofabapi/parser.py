import abc
import json
import os
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

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
        JSONファイルから決まる、input_data_id.
        Simple(v2)版用です。
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
    def parse(self) -> SimpleAnnotation:
        """
        JSONファイルをパースする。
        """

    @abc.abstractmethod
    def load_json(self) -> Any:
        """
        JSONファイルをloadします。
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
                p = SimpleAnnotationZipParser(zip_file, "task_id/input_data_id.json")
                annotation = p.parse()


    """

    def __init__(self, zip_file: zipfile.ZipFile, json_file_path: str):
        self.__zip_file = zip_file
        super().__init__(json_file_path)

    def parse(self) -> SimpleAnnotation:
        return SimpleAnnotation.from_dict(self.load_json())  # type: ignore

    def load_json(self) -> Any:
        with self.__zip_file.open(self.json_file_path) as entry:
            return json.load(entry)

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

            p = SimpleAnnotationDirParser(Path("task_id/input_data_id.json"))
            annotation = p.parse()

    """

    def __init__(self, json_file_path: Path):
        super().__init__(str(json_file_path))

    def parse(self) -> SimpleAnnotation:
        return SimpleAnnotation.from_dict(self.load_json())  # type: ignore

    def load_json(self) -> Any:
        with open(self.json_file_path, encoding="utf-8") as f:
            return json.load(f)

    def open_outer_file(self, data_uri: str):
        outer_file_path = _trim_extension(self.json_file_path) + "/" + data_uri
        try:
            return open(outer_file_path, mode="rb")
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
                p = FullAnnotationZipParser(zip_file, "task_id/input_data_id.json")
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

            p = FullAnnotationDirParser(Path("task_id/input_data_id.json"))
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
            return open(outer_file_path, mode="rb")
        except FileNotFoundError:
            raise AnnotationOuterFileNotFoundError(str(outer_file_path))


class SimpleAnnotationParserByTask(abc.ABC):
    """
    Simple Annotationのparserをタスクごとにまとめたもの。


    Args:
        task_id: タスクID
    """

    def __init__(self, task_id: str):
        self.__task_id = task_id

    @property
    def task_id(self) -> str:
        return self.__task_id

    @abc.abstractmethod
    def lazy_parse(self) -> Iterator[SimpleAnnotationParser]:
        pass


class SimpleAnnotationZipParserByTask(SimpleAnnotationParserByTask):
    def __init__(self, zip_file: zipfile.ZipFile, task_id: str, json_path_list: List[str]):
        self.__zip_file = zip_file
        self.__json_path_list = json_path_list
        super().__init__(task_id)

    def lazy_parse(self) -> Iterator[SimpleAnnotationZipParser]:
        return (SimpleAnnotationZipParser(self.__zip_file, e) for e in self.__json_path_list)


class SimpleAnnotationDirParserByTask(SimpleAnnotationParserByTask):
    def __init__(self, task_id: str, json_path_list: List[Path]):
        self.__json_path_list = json_path_list
        super().__init__(task_id)

    def lazy_parse(self) -> Iterator[SimpleAnnotationDirParser]:
        return (SimpleAnnotationDirParser(e) for e in self.__json_path_list)


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


def lazy_parse_simple_annotation_zip_by_task(zip_file_path: Path) -> Iterator[SimpleAnnotationParserByTask]:
    """
    Simpleアノテーションzipファイル内を探索し、タスクごとに各annotationをparse可能なオブジェクトの列を返します。

    Args:
        zip_file_path: annofabからダウンロードしたsimple annotationのzipファイルへのパス

    Yields:
        対象タスク内の、annotationの遅延Parseが可能なインスタンス列
    """

    def get_task_id_from_path(path: str) -> str:
        """
        1階層目のディレクトリをtask_idとみなして、task_idを取得する。
        """
        return path.split("/")[0]

    def is_input_data_json(zip_info: zipfile.ZipInfo) -> bool:
        """
        task_idディレクトリ配下の入力データJSONかどうか
        """
        paths = [p for p in zip_info.filename.split("/") if len(p) != 0]
        if len(paths) != 2:
            return False
        if not paths[1].endswith(".json"):
            return False
        return True

    def create_task_dict(arg_info_list: List[zipfile.ZipInfo]) -> Dict[str, List[str]]:
        task_dict: Dict[str, List[str]] = {}
        sorted_path_list = sorted([e.filename for e in arg_info_list if is_input_data_json(e)])

        before_task_id = None
        start_index = len(sorted_path_list)  # 初期値として無効な値を設定する
        for index, path in enumerate(sorted_path_list):
            task_id = get_task_id_from_path(path)
            if before_task_id != task_id:
                if before_task_id is not None:
                    task_dict[before_task_id] = sorted_path_list[start_index:index]

                start_index = index
                before_task_id = task_id

        if before_task_id is not None:
            task_dict[before_task_id] = sorted_path_list[start_index:]

        return task_dict

    with zipfile.ZipFile(zip_file_path, mode="r") as file:
        info_list: List[zipfile.ZipInfo] = file.infolist()

        task_dict: Dict[str, List[str]] = create_task_dict(info_list)
        for task_id, json_path_list in task_dict.items():
            yield SimpleAnnotationZipParserByTask(zip_file=file, task_id=task_id, json_path_list=json_path_list)


def lazy_parse_simple_annotation_dir_by_task(annotaion_dir_path: Path) -> Iterator[SimpleAnnotationParserByTask]:
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
        json_path_list = [e for e in task_dir.iterdir() if e.is_file() and e.suffix == ".json"]
        yield SimpleAnnotationDirParserByTask(task_id=task_id, json_path_list=json_path_list)


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
