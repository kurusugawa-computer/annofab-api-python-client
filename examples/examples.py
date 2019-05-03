"""

"""

from annofabapi import AnnofabApi
from typing import Dict, List, Any, Optional, Union, Tuple


class ExampleWrapper:
    """
    サンプル用のAnnofabApiのラッパークラス。
    """

    def __init__(self, api: AnnofabApi):
        """
        Args:
            api: AnnofabApi Instance
        """
        self.api = api

    def get_tasks_by_input_data_id(self, project_id: str, input_data_id: str) -> List[Dict[str, Any]]:
        """
        指定したinput_data_idを含む複数のtaskを取得する。
        注意：`get_all_tasks`メソッドを実行するので、遅い。
        """
        tasks = self.get_all_tasks(project_id)[0]
        return [t for t in tasks if input_data_id in t["input_data_id_list"]]
