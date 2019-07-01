import csv
import os

from annofabapi import AnnofabApi


def create_csv_for_task(file_path, first_input_data):
    """
    タスク生成用のCSVを作成する
    """
    first_line = ["1", first_input_data['input_data_name'], first_input_data['input_data_id']]
    lines = [first_line]

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerows(lines)


class WrapperForTest:
    """
    テスト用のUtils
    """

    def __init__(self, api: AnnofabApi):
        self.api = api

    def get_first_task_id(self, project_id):
        r1 = self.api.get_tasks(project_id)[0]
        task_list = r1["list"]
        task_id = task_list[0]["task_id"]
        return task_id

    def get_first_input_data_id_in_task(self, project_id, task_id):
        r = self.api.get_task(project_id, task_id)[0]
        input_data_id = r["input_data_id_list"][0]
        return input_data_id

    def get_first_input_data(self, project_id):
        r = self.api.get_input_data_list(project_id)[0]
        input_data_list = r['list']
        return input_data_list[0]

    def get_first_annotation(self, project_id):
        first_input_data = self.api.get_annotation_list(project_id)[0]['list'][0]
        first_annotation = first_input_data['detail']
        return {
            'task_id': first_input_data['task_id'],
            'input_data_id': first_input_data['input_data_id'],
            'annotation_id': first_annotation['annotation_id']
        }
