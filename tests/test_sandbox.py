"""
Annofabプロジェクトやタスクに大きく依存したテストコードです。
"""

import configparser

import annofabapi

inifile = configparser.ConfigParser()
inifile.read("./pytest.ini", "UTF-8")

project_id = inifile["annofab"]["project_id"]
task_id = inifile["annofab"]["task_id"]


test_dir = "./tests/data"
out_dir = "./tests/out"

endpoint_url = inifile["annofab"].get("endpoint_url", None)
if endpoint_url is not None:
    service = annofabapi.build(endpoint_url=endpoint_url)
else:
    service = annofabapi.build()


class TestAnnotation:
    def test_wrapper_put_annotation_for_simple_annotation_json_v1(self):
        """2021/07以降に廃止する予定"""
        project_id = "bf530c4e-1185-4a0c-994f-502fb01ea37e"
        annotation_specs_v1, _ = service.api.get_annotation_specs(project_id, query_params={"v": "1"})
        service.wrapper.put_annotation_for_simple_annotation_json(
            project_id=project_id,
            task_id="sample_0",
            input_data_id="0733d1e1-ef85-455e-aec0-ff05c499b711",
            simple_annotation_json=str(test_dir + "/simple-annotation/sample_1/c6e1c2ec-6c7c-41c6-9639-4244c2ed2839.json"),
            annotation_specs_labels=annotation_specs_v1["labels"],
        )

    def test_wrapper_put_annotation_for_simple_annotation_json_v2(self):
        project_id = "bf530c4e-1185-4a0c-994f-502fb01ea37e"
        annotation_specs_v2, _ = service.api.get_annotation_specs(project_id, query_params={"v": "2"})
        service.wrapper.put_annotation_for_simple_annotation_json(
            project_id=project_id,
            task_id="sample_0",
            input_data_id="0733d1e1-ef85-455e-aec0-ff05c499b711",
            simple_annotation_json=str(test_dir + "/simple-annotation/sample_1/c6e1c2ec-6c7c-41c6-9639-4244c2ed2839.json"),
            annotation_specs_labels=annotation_specs_v2["labels"],
            annotation_specs_additionals=annotation_specs_v2["additionals"],
        )
