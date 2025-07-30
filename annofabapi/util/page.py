"""
Annofabの画面に関するユーティリティ関数を定義します。
"""

from typing import Optional


def create_video_editor_url(project_id: str, task_id: str, *, annotation_id: Optional[str] = None, seek_seconds: Optional[float] = None) -> str:
    """
    動画エディタ画面のURLを生成します。

    Args:
        project_id: プロジェクトID
        task_id: タスクID
        annotation_id: アノテーションID
        seek_seconds: 動画の再生位置（単位は秒）

    Returns:
        動画エディタ画面のURL（例：https://annofab.com/projects/p1/tasks/t1/timeline?#a1/3.3）

    """
    url = f"https://annofab.com/projects/{project_id}/tasks/{task_id}/timeline"

    if annotation_id is not None or seek_seconds is not None:
        url += "?#"
        if annotation_id is not None:
            url += annotation_id
        if seek_seconds is not None:
            url += f"/{round(seek_seconds, 3)}"

    return url


def create_image_editor_url(project_id: str, task_id: str, *, input_data_id: Optional[str] = None, annotation_id: Optional[str] = None) -> str:
    """
    画像エディタ画面のURLを生成します。

    Args:
        project_id: プロジェクトID
        task_id: タスクID
        input_data_id: 入力データID
        annotation_id: アノテーションID。指定した場合は、input_data_idも指定する必要があります。

    Returns:
        画像エディタ画面のURL（例：https://annofab.com/projects/p1/tasks/t1/editor?#i1/a1）

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
    input_data_id: Optional[str] = None,
    annotation_id: Optional[str] = None,
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
        3次元エディタ画面のURL（例：https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html?p=p1&t=t1#/i1/a1）

    """
    url = f"{base_url}?p={project_id}&t={task_id}"

    if input_data_id is not None:
        url += f"/#{input_data_id}"

    if annotation_id is not None:
        if input_data_id is None:
            raise ValueError("'input_data_id' must be specified if 'annotation_id' is specified")
        url += f"/{annotation_id}"

    return url
