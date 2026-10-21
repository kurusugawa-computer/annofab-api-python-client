"""
Annofabの画面に関するユーティリティ関数を定義します。
"""

from dataclasses import dataclass
from math import isfinite
from urllib.parse import SplitResult, parse_qs, unquote, urlsplit


def create_project_url(project_id: str) -> str:
    """プロジェクトトップ画面のURLを生成します。

    Args:
        project_id: プロジェクトID

    Returns:
        プロジェクトトップ画面のURL
        （例： ``https://annofab.com/projects/p1`` ）
    """
    return f"https://annofab.com/projects/{project_id}"


def create_video_editor_url(project_id: str, task_id: str, *, annotation_id: str | None = None, seek_seconds: float | None = None) -> str:
    """
    動画エディタ画面のURLを生成します。

    Args:
        project_id: プロジェクトID
        task_id: タスクID
        annotation_id: アノテーションID
        seek_seconds: 動画の再生位置（単位は秒）

    Returns:
        動画エディタ画面のURL
        （例： ``https://annofab.com/projects/p1/tasks/t1/timeline?#a1/3.3`` ）

    """
    url = f"https://annofab.com/projects/{project_id}/tasks/{task_id}/timeline"

    if annotation_id is not None or seek_seconds is not None:
        url += "?#"
        if annotation_id is not None:
            url += annotation_id
        if seek_seconds is not None:
            url += f"/{round(seek_seconds, 3)}"

    return url


def create_image_editor_url(project_id: str, task_id: str, *, input_data_id: str | None = None, annotation_id: str | None = None) -> str:
    """
    画像エディタ画面のURLを生成します。

    Args:
        project_id: プロジェクトID
        task_id: タスクID
        input_data_id: 入力データID
        annotation_id: アノテーションID。指定した場合は、input_data_idも指定する必要があります。

    Returns:
        画像エディタ画面のURL
        （例： ``https://annofab.com/projects/p1/tasks/t1/editor?#i1/a1`` ）

    """
    url = f"https://annofab.com/projects/{project_id}/tasks/{task_id}/editor"

    if input_data_id is not None:
        url += f"?#{input_data_id}"

    if annotation_id is not None:
        if input_data_id is None:
            raise ValueError("'input_data_id' must be specified if 'annotation_id' is specified")
        url += f"/{annotation_id}"

    return url


def create_3dpc_editor_url(
    project_id: str,
    task_id: str,
    *,
    input_data_id: str | None = None,
    annotation_id: str | None = None,
    base_url: str = "https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html",
) -> str:
    """
    3次元エディタ画面のURLを生成します。

    Args:
        project_id: プロジェクトID
        task_id: タスクID
        input_data_id: 入力データID
        annotation_id: アノテーションID。指定した場合は、input_data_idも指定する必要があります。
        base_url: 3次元エディタ画面のベースとなるURL。この部分はプラグインにより変更可能なので、引数として受け取るようにしました。

    Returns:
        3次元エディタ画面のURL
        （例： ``https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html?p=p1&t=t1#/i1/a1`` ）

    """
    url = f"{base_url}?p={project_id}&t={task_id}"

    if input_data_id is not None:
        url += f"#/{input_data_id}"

    if annotation_id is not None:
        if input_data_id is None:
            raise ValueError("'input_data_id' must be specified if 'annotation_id' is specified")
        url += f"/{annotation_id}"

    return url


@dataclass(frozen=True)
class ParsedProjectUrl:
    """プロジェクトに属する画面のURLから抽出した情報。"""

    project_id: str
    """プロジェクトID。"""


@dataclass(frozen=True)
class ParsedTaskUrl(ParsedProjectUrl):
    """タスクに属する画面のURLから抽出した情報。"""

    task_id: str
    """タスクID。"""


@dataclass(frozen=True)
class ParsedImageEditorUrl(ParsedTaskUrl):
    """画像エディタのURLから抽出した情報。"""

    input_data_id: str | None = None
    """入力データID。URLで省略されている場合はNone。"""
    annotation_id: str | None = None
    """アノテーションID。URLで省略されている場合はNone。"""


@dataclass(frozen=True)
class ParsedVideoEditorUrl(ParsedTaskUrl):
    """動画エディタのURLから抽出した情報。"""

    annotation_id: str | None = None
    """アノテーションID。URLで省略されている場合はNone。"""
    seek_seconds: float | None = None
    """動画の再生位置（秒）。URLで省略されている場合はNone。"""


@dataclass(frozen=True)
class Parsed3dpcEditorUrl(ParsedTaskUrl):
    """3次元エディタのURLから抽出した情報。"""

    input_data_id: str | None = None
    """入力データID。URLで省略されている場合はNone。"""
    annotation_id: str | None = None
    """アノテーションID。URLで省略されている場合はNone。"""


def _split_annofab_url(url: str) -> tuple[SplitResult, list[str]]:
    parsed = urlsplit(url)
    parts = parsed.path.split("/")
    if parsed.scheme != "https" or parsed.netloc.lower() != "annofab.com" or len(parts) < 3 or parts[1] != "projects" or not parts[2]:
        raise ValueError("Annofabのプロジェクトに属する画面のURLを指定してください。")
    return parsed, parts


def _task_ids(parts: list[str]) -> ParsedTaskUrl:
    if len(parts) < 5 or parts[3] != "tasks" or not parts[4]:
        raise ValueError("Annofabのタスクに属する画面のURLを指定してください。")
    return ParsedTaskUrl(project_id=unquote(parts[2]), task_id=unquote(parts[4]))


def _split_editor_url(url: str, screen: str) -> tuple[SplitResult, ParsedTaskUrl]:
    parsed, parts = _split_annofab_url(url)
    ids = _task_ids(parts)
    if parts[5:] not in ([screen], [screen, ""]):
        raise ValueError(f"Annofabの{screen}画面のURLを指定してください。")
    return parsed, ids


def _input_and_annotation_ids(fragment: str) -> tuple[str | None, str | None]:
    if not fragment:
        return None, None
    parts = fragment.split("/")
    if len(parts) > 2 or not parts[0] or (len(parts) == 2 and not parts[1]):
        raise ValueError("入力データIDまたはアノテーションIDの形式が不正です。")
    return unquote(parts[0]), unquote(parts[1]) if len(parts) == 2 else None


def parse_project_url(url: str) -> ParsedProjectUrl:
    """プロジェクトに属する画面のURLからプロジェクトIDを抽出します。

    ``https://annofab.com/projects/{project_id}[/...]`` に対応します。
    後続のパス、クエリ、フラグメントは無視し、画面の存在やアクセス権は検証しません。
    IDはパーセントデコードして返します。

    Args:
        url: Annofabの画面のURL。

    Returns:
        抽出したプロジェクトIDを持つ解析結果。

    Raises:
        ValueError: URLが対応する形式ではない場合。
    """
    _, parts = _split_annofab_url(url)
    return ParsedProjectUrl(project_id=unquote(parts[2]))


def parse_task_url(url: str) -> ParsedTaskUrl:
    """タスクに属する画面のURLからプロジェクトIDとタスクIDを抽出します。

    ``https://annofab.com/projects/{project_id}/tasks/{task_id}[/...]`` に対応します。
    履歴・画像エディタ・動画エディタなど、画面名に依存せず抽出します。
    後続のパス、クエリ、フラグメントは無視し、画面の存在やアクセス権は検証しません。
    IDはパーセントデコードして返します。

    Args:
        url: Annofabのタスクに属する画面のURL。

    Returns:
        抽出したプロジェクトIDとタスクIDを持つ解析結果。

    Raises:
        ValueError: URLが対応する形式ではない場合。
    """
    _, parts = _split_annofab_url(url)
    return _task_ids(parts)


def parse_image_editor_url(url: str) -> ParsedImageEditorUrl:
    """画像エディタのURLから各IDを抽出します。

    ``https://annofab.com/projects/{project_id}/tasks/{task_id}/editor`` に対応します。
    フラグメントは ``#{input_data_id}[/{annotation_id}]`` 形式です。
    フラグメントで省略されたIDはNoneとし、IDはパーセントデコードして返します。
    クエリ（例: ``version=preview``）は無視します。

    Args:
        url: 画像エディタのURL。

    Returns:
        プロジェクト・タスク・入力データ・アノテーションのIDを持つ解析結果。

    Raises:
        ValueError: URLまたはフラグメントが対応する形式ではない場合。
    """
    parsed, ids = _split_editor_url(url, "editor")
    input_data_id, annotation_id = _input_and_annotation_ids(parsed.fragment)
    return ParsedImageEditorUrl(ids.project_id, ids.task_id, input_data_id, annotation_id)


def parse_video_editor_url(url: str) -> ParsedVideoEditorUrl:
    """動画エディタのURLから各IDと再生位置を抽出します。

    ``https://annofab.com/projects/{project_id}/tasks/{task_id}/timeline`` に対応します。
    フラグメントは ``#{annotation_id}[/{seek_seconds}]`` 形式で、
    ``#/3.3`` のように再生位置だけ指定することもできます。
    省略された値はNoneとし、IDはパーセントデコードして返します。クエリは無視します。

    Args:
        url: 動画エディタのURL。

    Returns:
        プロジェクト・タスク・アノテーションのIDと再生位置を持つ解析結果。

    Raises:
        ValueError: URLまたはフラグメントが対応する形式ではない場合。
            再生位置には有限の非負の数を指定してください。
    """
    parsed, ids = _split_editor_url(url, "timeline")
    parts = parsed.fragment.split("/")
    if len(parts) > 2:
        raise ValueError("動画エディタのフラグメントの形式が不正です。")
    annotation_id = unquote(parts[0]) if parts[0] else None
    seek_seconds = None
    if len(parts) == 2:
        seek_seconds = float(unquote(parts[1]))
        if not isfinite(seek_seconds) or seek_seconds < 0:
            raise ValueError("再生位置には有限の非負の数を指定してください。")
    return ParsedVideoEditorUrl(ids.project_id, ids.task_id, annotation_id, seek_seconds)


def parse_3dpc_editor_url(
    url: str,
    *,
    base_url: str = "https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html",
) -> Parsed3dpcEditorUrl:
    """3次元エディタのURLから各IDを抽出します。

    クエリの ``p`` からプロジェクトID、``t`` からタスクIDを抽出します。
    フラグメントは ``#/{input_data_id}[/{annotation_id}]`` 形式です。
    フラグメントで省略されたIDはNoneとし、IDはパーセントデコードして返します。
    ``p`` と ``t`` 以外のクエリは無視します。

    Args:
        url: 3次元エディタのURL。
        base_url: 対応する3次元エディタのベースURL。生成時と同じ値を指定してください。
            クエリとフラグメントを含まないHTTPまたはHTTPSのURLを指定します。

    Returns:
        プロジェクト・タスク・入力データ・アノテーションのIDを持つ解析結果。

    Raises:
        ValueError: ベースURL、URL、クエリまたはフラグメントが対応する形式ではない場合。
    """
    base = urlsplit(base_url)
    if base.scheme not in {"http", "https"} or not base.netloc or base.query or base.fragment:
        raise ValueError("クエリとフラグメントを含まないベースURLを指定してください。")
    parsed = urlsplit(url)
    if (parsed.scheme, parsed.netloc.lower(), parsed.path) != (base.scheme, base.netloc.lower(), base.path):
        raise ValueError("指定されたベースURLの3次元エディタのURLを指定してください。")
    query = parse_qs(parsed.query, keep_blank_values=True)
    for key in ("p", "t"):
        if key not in query or len(query[key]) != 1 or not query[key][0]:
            raise ValueError("プロジェクトIDとタスクIDをそれぞれ1つ指定してください。")
    fragment = parsed.fragment
    if fragment and not fragment.startswith("/"):
        raise ValueError("3次元エディタのフラグメントは'/'で始まる必要があります。")
    input_data_id, annotation_id = _input_and_annotation_ids(fragment.removeprefix("/"))
    return Parsed3dpcEditorUrl(query["p"][0], query["t"][0], input_data_id, annotation_id)
