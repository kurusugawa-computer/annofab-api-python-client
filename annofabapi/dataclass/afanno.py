from dataclasses import dataclass
from typing import Any, Dict, List

from dataclasses_json import DataClassJsonMixin


@dataclass(frozen=True)
class SimpleAnnotationDetail(DataClassJsonMixin):
    """ Annofabにおける個々のアノテーションの汎用構造

    """
    annotation_id: str

    #: Label Info
    label: str
    """Label Info"""
    data: Dict[str, Any]
    attributes: Dict[str, Any]


@dataclass(frozen=True)
class SimpleAnnotation(DataClassJsonMixin):
    """ Annofab におけるアノテーションの汎用構造

    一つの input_dataごとに一つのAnnofabAnnotationインスタンスが存在する

    Args:
        annotation_format_version: アノテーションフォーマットのバージョン
        project_id: アノテーションが所属しているannofab上のプロジェクトId
        task_id: str アノテーションが所属しているannofab上のタスクId
        task_phase: タスクのフェーズ
        task_phase_stage:
        task_status: タスクのステータス
        input_data_id: アノテーションが付与されているannofab上のデータId
        input_data_name: input_data_idに対応する、annofab上のデータの名前
        details:
    """
    annotation_format_version: str
    project_id: str
    task_id: str
    task_phase: str
    task_phase: str
    task_phase_stage: int
    input_data_id: str
    input_data_name: str
    details: List[SimpleAnnotationDetail]
