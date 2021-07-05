# 以下は2021-09-01以降に廃止する予定
JobInfo = ProjectJobInfo
JobInfoContainer = ProjectJobInfoContainer


@deprecated_class(deprecated_date="2021-09-01", new_class_name=f"{ProjectJobType.__module__}.{ProjectJobType.__name__}")
class JobType(Enum):
    """
    プロジェクトのジョブ種別

    .. deprecated:: 2021-09-01
    """

    COPY_PROJECT = "copy-project"
    GEN_INPUTS = "gen-inputs"
    GEN_TASKS = "gen-tasks"
    GEN_ANNOTATION = "gen-annotation"
    GEN_TASKS_LIST = "gen-tasks-list"
    GEN_INPUTS_LIST = "gen-inputs-list"
    DELETE_PROJECT = "delete-project"
    INVOKE_HOOK = "invoke-hook"
    MOVE_PROJECT = "move-project"
