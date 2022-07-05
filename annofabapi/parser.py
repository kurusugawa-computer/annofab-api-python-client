import abc
import json
import os
import zipfile
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional

from annofabapi.dataclass.annotation import FullAnnotation, SimpleAnnotation
from annofabapi.exceptions import AnnotationOuterFileNotFoundError

CONVERT_ANNOTATION_DETAIL_DATA_FUNC = Callable[[Dict[str, Any]], Any]


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
        """JSONファイルの親ディレクトリ名から決まる task_id"""
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
        JSONファイルから決まるinput_data_id.
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

    def parse(self, convert_detail_data_func: Optional[CONVERT_ANNOTATION_DETAIL_DATA_FUNC] = None) -> SimpleAnnotation:
        """JSONファイルをパースする

        Args:
            convert_detail_data_func: SimpleAnnotationDetailクラスのdataプロパティを変換する関数を指定します。
                dictからdataclassに変換する際に使います。

        Returns:
            SimpleAnnotationインスタンス
        """

        simple_annotation = SimpleAnnotation.from_dict(self.load_json())  # type: ignore
        if convert_detail_data_func is not None:
            for detail in simple_annotation.details:
                detail.data = convert_detail_data_func(detail.data)
        return simple_annotation

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
        """JSONファイルの親ディレクトリ名から決まる task_id"""
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
    def load_json(self) -> Any:
        """
        JSONファイルをloadします。
        """

    def parse(self, convert_detail_data_func: Optional[CONVERT_ANNOTATION_DETAIL_DATA_FUNC] = None) -> FullAnnotation:
        """JSONファイルをパースする

        Args:
            convert_detail_data_func: FullAnnotationDetailクラスのdataプロパティを変換する関数を指定します。
                dictからdataclassに変換する際に使います。

        Returns:
            FullAnnotationインスタンス
        """

        full_annotation = FullAnnotation.from_dict(self.load_json())  # type: ignore
        if convert_detail_data_func is not None:
            for detail in full_annotation.details:
                detail.data = convert_detail_data_func(detail.data)
        return full_annotation


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

    def load_json(self) -> Any:
        with self.__zip_file.open(self.json_file_path) as entry:
            return json.load(entry)

    def open_outer_file(self, data_uri: str):
        outer_file_path = _trim_extension(self.json_file_path) + "/" + data_uri
        try:
            return self.__zip_file.open(outer_file_path, mode="r")
        except KeyError as e:
            # mypyの `error: "ZipFile" has no attribute "filename"` という警告を無視する
            raise AnnotationOuterFileNotFoundError(
                str(outer_file_path), self.__zip_file.filename
            ) from e  # type: ignore


class SimpleAnnotationDirParser(SimpleAnnotationParser):
    """
    Simpleアノテーションzipを展開した、ティレクトリのParser

    Args:
        json_file_path: パースするJSONファイルのパス

    Examples:
        JSONファイルをパースする::

            p = SimpleAnnotationDirParser(Path("annotation/task_id/input_data_id.json"))
            annotation = p.parse()

    """

    def __init__(self, json_file_path: Path):
        super().__init__(str(json_file_path))

    def load_json(self) -> Any:
        with open(self.json_file_path, encoding="utf-8") as f:
            return json.load(f)

    def open_outer_file(self, data_uri: str):
        outer_file_path = _trim_extension(self.json_file_path) + "/" + data_uri
        try:
            return open(outer_file_path, mode="rb")  # pylint: disable=consider-using-with
        except FileNotFoundError as e:
            raise AnnotationOuterFileNotFoundError(str(outer_file_path)) from e


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

    def load_json(self) -> Any:
        with self.__zip_file.open(self.json_file_path) as entry:
            return json.load(entry)

    def open_outer_file(self, data_uri: str):
        outer_file_path = _trim_extension(self.json_file_path) + "/" + data_uri
        try:
            return self.__zip_file.open(outer_file_path, mode="r")
        except KeyError as e:
            # mypyの `error: "ZipFile" has no attribute "filename"` という警告を無視する
            raise AnnotationOuterFileNotFoundError(
                str(outer_file_path), self.__zip_file.filename
            ) from e  # type: ignore


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

    def load_json(self) -> Any:
        with open(self.json_file_path, encoding="utf-8") as f:
            return json.load(f)

    def open_outer_file(self, data_uri: str):
        outer_file_path = _trim_extension(self.json_file_path) + "/" + data_uri
        try:
            return open(outer_file_path, mode="rb")  # pylint: disable=consider-using-with
        except FileNotFoundError as e:
            raise AnnotationOuterFileNotFoundError(str(outer_file_path)) from e


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

    @property
    @abc.abstractmethod
    def json_file_path_list(self) -> List[str]:
        """
        パースするJSONファイルパスのリスト
        """

    @abc.abstractmethod
    def get_parser(self, json_file_path: str) -> SimpleAnnotationParser:
        """
        JSONファイルパスから、Simple Annotation parserを取得する。

        Args:
            json_file_path: パースするJSONファイルのパス。``json_file_path_list`` に含まれる値を指定すること。

        Returns:
            Simple Annotation parser

        Raises:
            ValueError: ``json_file_path`` の値が ``json_file_path_list`` に含まれていないとき

        """

    @abc.abstractmethod
    def lazy_parse(self) -> Iterator[SimpleAnnotationParser]:
        pass


class SimpleAnnotationZipParserByTask(SimpleAnnotationParserByTask):
    """
    Simple Annotation zipのparserをタスクごとにまとめたもの。

    Args:
        zip_file: Simple Annotation zipのzipfileオブジェクト
        task_id: タスクID
        json_path_list: パースするJSONパスのリスト。
            Noneの場合は、``zipfile.ZipFile.infolist()`` 関数を呼び出して、JSONパスのリストを生成します。

    Examples:
        JSONファイルをパースする::

            with zipfile.ZipFile("simple-annotation.zip", "r") as zip_file:
                p = SimpleAnnotationZipParserByTask(zip_file, "task1")

    """

    def __get_json_file_path_list(self, task_id: str) -> List[str]:
        """
        task_idとJSONパスリストの辞書を取得する。
        """

        def _match_task_id_and_contain_input_data_json(zip_info: zipfile.ZipInfo) -> bool:
            """
            task_idディレクトリ配下の入力データJSONかどうか
            """
            paths = [p for p in zip_info.filename.split("/") if len(p) != 0]
            if len(paths) != 2:
                return False
            if paths[0] != task_id:
                return False
            if not paths[1].endswith(".json"):
                return False
            return True

        return [
            zip_info.filename
            for zip_info in self.__zip_file.infolist()
            if _match_task_id_and_contain_input_data_json(zip_info)
        ]

    def __init__(self, zip_file: zipfile.ZipFile, task_id: str, json_path_list: Optional[List[str]] = None):
        self.__zip_file = zip_file
        if json_path_list is not None:
            self.__json_path_list = json_path_list
        else:
            self.__json_path_list = self.__get_json_file_path_list(task_id)
        super().__init__(task_id)

    def lazy_parse(self) -> Iterator[SimpleAnnotationZipParser]:
        return (SimpleAnnotationZipParser(self.__zip_file, e) for e in self.__json_path_list)

    @property
    def json_file_path_list(self) -> List[str]:
        return self.__json_path_list

    def get_parser(self, json_file_path: str) -> SimpleAnnotationParser:
        if json_file_path in self.__json_path_list:
            return SimpleAnnotationZipParser(self.__zip_file, json_file_path)
        else:
            raise ValueError(f"json_file_path '{json_file_path}' は `json_file_path_list` に含まれていません。")


class SimpleAnnotationDirParserByTask(SimpleAnnotationParserByTask):
    """
    Simple Annotation zipを展開したディレクトリのparserをタスクごとにまとめたもの。

    Args:
        task_id: Simple Annotation zipのzipfileオブジェクト
        task_id: タスクID
        json_path_list: タスク配下のJSONパスのリスト。パスにはtask_idを含む。

    Examples:
        JSONファイルをパースする::

            with zipfile.ZipFile("simple-annotation.zip", "r") as zip_file:
                p = SimpleAnnotationZipParserByTask(zip_file, "task1", ["task1/input1.json","task1/input2.json"])

    """

    def __init__(self, task_dir_path: Path):
        self.__task_dir_path = task_dir_path
        task_id = task_dir_path.name
        super().__init__(task_id)

    def lazy_parse(self) -> Iterator[SimpleAnnotationDirParser]:
        return (
            SimpleAnnotationDirParser(e) for e in self.__task_dir_path.iterdir() if e.is_file() and e.suffix == ".json"
        )

    @property
    def json_file_path_list(self) -> List[str]:
        return [str(e) for e in self.__task_dir_path.iterdir() if e.is_file() and e.suffix == ".json"]

    def get_parser(self, json_file_path: str) -> SimpleAnnotationParser:
        if json_file_path in self.json_file_path_list:
            return SimpleAnnotationDirParser(Path(json_file_path))
        else:
            raise ValueError(f"json_file_path '{json_file_path}' は `json_file_path_list` に含まれていません。")


def __parse_annotation_dir(annotation_dir_path: Path, clazz) -> Iterator[Any]:
    for task_dir in annotation_dir_path.iterdir():
        if not task_dir.is_dir():
            continue

        for input_data_file in task_dir.iterdir():
            if not input_data_file.is_file():
                continue

            if not input_data_file.suffix == ".json":
                continue

            parser = clazz(input_data_file)
            yield parser


def lazy_parse_simple_annotation_dir(annotation_dir_path: Path) -> Iterator[SimpleAnnotationParser]:
    """Simpleアノテーションzipを展開したディレクトリ内を探索し、各annotationをparse可能なオブジェクトの列を返します。

    Args:
        annotation_dir_path: annofabからダウンロードしたsimple annotationのzipファイルを展開したディレクトリ

    Yields:
        annotationの遅延Parseが可能なインスタンス列。
    """

    return __parse_annotation_dir(annotation_dir_path, SimpleAnnotationDirParser)


def lazy_parse_full_annotation_dir(annotation_dir_path: Path) -> Iterator[SimpleAnnotationParser]:
    """Fullアノテーションzipを展開したディレクトリ内を探索し、各annotationをparse可能なオブジェクトの列を返します。

    Args:
        annotation_dir_path: annofabからダウンロードしたsimple annotationのzipファイルを展開したディレクトリ

    Yields:
        annotationの遅延Parseが可能なインスタンス列。
    """
    return __parse_annotation_dir(annotation_dir_path, FullAnnotationDirParser)


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
        """
        task_idとJSONパスリストの辞書を取得する。
        """
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


def lazy_parse_simple_annotation_dir_by_task(annotation_dir_path: Path) -> Iterator[SimpleAnnotationParserByTask]:
    """
    Simpleアノテーションzipを展開したディレクトリ内を探索し、タスクごとに各annotationをparse可能なオブジェクトの列を返します。

    Args:
        annotation_dir_path: annofabからダウンロードしたsimple annotationのzipファイルを展開したディレクトリ

    Yields:
        対象タスク内の、annotationの遅延Parseが可能なインスタンス列
    """

    for task_dir in annotation_dir_path.iterdir():
        if not task_dir.is_dir():
            continue

        task_parser = SimpleAnnotationDirParserByTask(task_dir)
        # lazy_parse_simple_annotation_zip_by_task の動きと対応させる
        if len(task_parser.json_file_path_list) == 0:
            continue
        yield task_parser


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
    """引数のFullアノテーションzipファイル内を探索し、各annotationをparse可能なオブジェクトの列を返します。

    大量のファイルを含むzipファイルを展開せず、task_idなどを確認して最小限のデータのみをparseすることを目的としたユーティリティです。

    Args:
        zip_file_path: annofabからダウンロードしたsimple annotationのzipファイルへのパス

    Yields:
        annotationの遅延Parseが可能なインスタンス列。 順番は（多分）zipファイル内のエントリー順です
    """
    return __parse_annotation_zip(zip_file_path, FullAnnotationZipParser)
