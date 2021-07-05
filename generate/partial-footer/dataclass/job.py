# 2021-09-01以降に削除する予定
@deprecated_class(deprecated_date="2021-09-01", new_class_name=f"{ProjectJobInfo.__module__}.{ProjectJobInfo.__name__}")
@dataclass
class JobInfo(DataClassJsonMixin):
    """プロジェクトのジョブ情報

    .. deprecated:: 2021-09-01
    """

    project_id: Optional[str]
    """プロジェクトID。[値の制約についてはこちら。](#section/API-Convention/APIID) """

    job_type: Optional[ProjectJobType]
    """"""

    job_id: Optional[str]
    """"""

    job_status: Optional[JobStatus]
    """"""

    job_execution: Optional[Dict[str, Any]]
    """ジョブの内部情報"""

    job_detail: Optional[Dict[str, Any]]
    """ジョブ結果の内部情報"""

    created_datetime: Optional[str]
    """"""

    updated_datetime: Optional[str]
    """"""
