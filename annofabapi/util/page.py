"""
Annofabの画面に関するユーティリティ関数を定義します。   
"""


def create_video_editor_url(project_id: str, task_id: str, *, annotation_id: str | None = None, seconds: float | None = None) -> str:
    """
    動画エディタ画面のURLを生成します。
    
    Args:
        project_id: プロジェクトID
        task_id: タスクID
        annotation_id: アノテーションID
        seconds: 動画の再生位置（単位は秒）

    Returns:
        動画エディタ画面のURL（例：https://annofab.com/projects/p1/tasks/t1/timeline?#a1/3.3）

    """
    url = f"https://annofab.com/projects/{project_id}/tasks/{task_id}/timeline"

    if annotation_id is not None or seconds is not None:
        url += "?#"
        if annotation_id is not None:
            url += annotation_id
        if seconds is not None:
            url += f"/{round(seconds,3)}"

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
        画像エディタ画面のURL（例：https://annofab.com/projects/p1/tasks/t1/editor?#i1/a1）

    """
    url = f"https://annofab.com/projects/{project_id}/tasks/{task_id}/editor"

    if input_data_id is not None:
        url += f"?#{input_data_id}"

    if annotation_id is not None:
        assert input_data_id is not None
        url += f"/{annotation_id}"

    return url



https://d2rljy8mjgrfyd.cloudfront.net/3d-editor-latest/index.html?p=ad05bf60-01d4-4f66-aa82-0e95e6f4c95b&t=002#/002-0