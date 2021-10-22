"""
AnnofabApi, Wrapperのテストコード

### テストの観点
【注意】
* 基本的にHTTP GETのテストのみ行うこと。PUT/POST/DELETEのテストがあると、間違えて修正してまうおそれあり。

"""
import configparser
import datetime
import os
import uuid

import pytest
import requests
from more_itertools import first_true

import annofabapi
import annofabapi.utils
from annofabapi.models import GraphType, ProjectJobType
from annofabapi.wrapper import TaskFrameKey
from tests.utils_for_test import WrapperForTest, create_csv_for_task

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")
inifile = configparser.ConfigParser()
inifile.read("./pytest.ini", "UTF-8")

project_id = inifile["annofab"]["project_id"]
task_id = inifile["annofab"]["task_id"]
changed_task_id = inifile["annofab"]["changed_task_id"]

test_dir = "./tests/data"
out_dir = "./tests/out"

endpoint_url = inifile["annofab"].get("endpoint_url", None)
if endpoint_url is not None:
    service = annofabapi.build(endpoint_url=endpoint_url)
else:
    service = annofabapi.build()
api = service.api
wrapper = service.wrapper
test_wrapper = WrapperForTest(api)


class TestAccount:
    pass


class TestAnnotation:
    @classmethod
    def setup_class(cls):
        cls.input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)

    def test_wrapper_get_all_annotation_list(self):
        assert len(wrapper.get_all_annotation_list(project_id, {"query": {"task_id": task_id}})) >= 0

    def test_get_annotation(self):
        assert type(api.get_annotation(project_id, task_id, self.input_data_id)[0]) == dict

    def test_get_editor_annotation(self):
        assert type(api.get_editor_annotation(project_id, task_id, self.input_data_id)[0]) == dict

    def test_get_annotation_archive(self):
        content, response = api.get_annotation_archive(project_id)
        assert response.headers["Location"].startswith("https://")

    def test_get_archive_full_with_pro_id(self):
        content, response = api.get_archive_full_with_pro_id(project_id)
        assert response.headers["Location"].startswith("https://")

    def test_wrapper_download_annotation_archive(self):
        wrapper.download_annotation_archive(project_id, f"{out_dir}/simple-annotation.zip")

    @pytest.mark.submitting_job
    def test_post_annotation_archive_update(self):
        content = api.post_annotation_archive_update(project_id, query_params={"v": "2"})[0]
        job = content["job"]
        assert job["job_type"] == ProjectJobType.GEN_ANNOTATION.value

    def test_wrapper_copy_annotation(self):
        src = TaskFrameKey(project_id, task_id, self.input_data_id)
        dest = TaskFrameKey(project_id, task_id, self.input_data_id)
        result = wrapper.copy_annotation(src, dest)
        assert result == True

    def test_wrapper_put_annotation_for_simple_annotation_json(self):
        input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)
        annotation_specs_v2, _ = service.api.get_annotation_specs(project_id, query_params={"v": "2"})
        wrapper.put_annotation_for_simple_annotation_json(
            project_id,
            changed_task_id,
            input_data_id,
            simple_annotation_json="tests/data/simple-annotation/sample_1/c6e1c2ec-6c7c-41c6-9639-4244c2ed2839.json",
            annotation_specs_labels=annotation_specs_v2["labels"],
            annotation_specs_additionals=annotation_specs_v2["additionals"],
        )


class TestAnnotationSpecs:
    def test_get_annotation_specs(self):
        annotation_spec, _ = api.get_annotation_specs(project_id)
        assert type(annotation_spec) == dict

    def test_put_annotation_specs(self):
        annotation_spec, _ = api.get_annotation_specs(project_id)
        last_updated_datetime = annotation_spec["updated_datetime"] if annotation_spec is not None else None
        request_body = {
            "labels": annotation_spec["labels"],
            "inspection_phrases": annotation_spec["inspection_phrases"],
            "comment": f"{annofabapi.utils.str_now()} に更新しました。",
            "last_updated_datetime": last_updated_datetime,
        }
        puted_annotation_spec, _ = api.put_annotation_specs(project_id, request_body=request_body)
        assert type(puted_annotation_spec) == dict

    def test_get_annotation_specs_histories(self):
        annotation_specs_histories = api.get_annotation_specs_histories(project_id)[0]
        assert type(annotation_specs_histories) == list

    def test_get_annotation_specs_relation(self):
        result = wrapper.get_annotation_specs_relation(project_id, project_id)
        assert type(result) == annofabapi.wrapper.AnnotationSpecsRelation


class TestComment:
    @classmethod
    def setup_class(cls):
        task, _ = api.get_task(project_id, task_id)
        if task["account_id"] != api.account_id:
            task = wrapper.change_task_operator(project_id, task_id, operator_account_id=api.account_id)
        if task["status"] != "working":
            task = wrapper.change_task_status_to_working(project_id, task_id)
        cls.task = task

    def test_put_get_delete_comment(self):
        task = self.task
        comment_id = str(uuid.uuid4())
        put_request_body = [
            {
                "comment_id": comment_id,
                "phase": task["phase"],
                "phase_stage": task["phase_stage"],
                "account_id": api.account_id,
                "comment_type": "onhold",
                "phrases": [],
                "comment": "foo-bar",
                "comment_node": {
                    "data": None,
                    "annotation_id": None,
                    "label_id": None,
                    "status": "open",
                    "_type": "Root",
                },
                "datetime_for_sorting": annofabapi.utils.str_now(),
                "_type": "Put",
            }
        ]
        input_data_id = task["input_data_id_list"][0]
        result, _ = api.batch_update_comments(project_id, task_id, input_data_id, request_body=put_request_body)

        comments, _ = api.get_comments(project_id, task_id, input_data_id)
        assert first_true(comments, pred=lambda e: e["comment_id"] == comment_id) is not None

        # コメントの削除
        delete_request_body = [
            {
                "comment_id": comment_id,
                "_type": "Delete",
            }
        ]
        api.batch_update_comments(project_id, task_id, input_data_id, request_body=delete_request_body)

        # コメントの削除確認
        comments, _ = api.get_comments(project_id, task_id, input_data_id)
        assert first_true(comments, pred=lambda e: e["comment_id"] == comment_id) is None

    @classmethod
    def teardown_class(cls):
        wrapper.change_task_status_to_break(project_id, task_id)


class TestInputData:
    @classmethod
    def setup_class(cls):
        cls.input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)

    def test_wrapper_get_input_data_list(self):
        assert type(wrapper.get_all_input_data_list(project_id, {"input_data_name": "foo"})) == list

    def test_get_input_data(self):
        test_input_data = api.get_input_data(project_id, self.input_data_id)[0]
        assert type(test_input_data) == dict

    def test_wrapper_put_input_data_from_file_and_delete_input_data(self):
        test_input_data_id = str(uuid.uuid4())
        print("")
        print(f"put_input_data: input_data_id={test_input_data_id}")
        assert type(wrapper.put_input_data_from_file(project_id, test_input_data_id, f"{test_dir}/lenna.png")) == dict
        assert type(api.delete_input_data(project_id, test_input_data_id)[0]) == dict

    def test_put_input_data_from_file_and_batch_update_inputs(self):
        test_input_data_id = str(uuid.uuid4())
        print("")
        print(f"put_input_data: input_data_id={test_input_data_id}")
        wrapper.put_input_data_from_file(project_id, test_input_data_id, f"{test_dir}/lenna.png")

        request_body = [{"project_id": project_id, "input_data_id": test_input_data_id, "_type": "Delete"}]
        assert type(api.batch_update_inputs(project_id, request_body=request_body)[0]) == list


class TestInspection:
    @classmethod
    def setup_class(cls):
        cls.input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)

    def test_get_inspections(self):
        assert len(api.get_inspections(project_id, task_id, self.input_data_id)[0]) >= 0


class TestInstruction:
    def test_wrapper_get_latest_instruction(self):
        assert type(wrapper.get_latest_instruction(project_id)) == dict

    def test_get_instruction_history(self):
        histories = api.get_instruction_history(project_id)[0]
        assert len(histories) > 0

    def test_wrapper_upload_instruction_image_and_delete_instruction_image(self):
        test_image_id = str(uuid.uuid4())
        print("")
        print(f"wrapper.upload_instruction_image: image_id={test_image_id}")
        wrapper.upload_instruction_image(project_id, test_image_id, f"{test_dir}/lenna.png")

        api.delete_instruction_image(project_id, test_image_id)

    def test_get_instruction_images(self):
        image_list = api.get_instruction_images(project_id)[0]
        assert type(image_list) == list

    def test_put_instruction(self):
        str_now = datetime.datetime.now().isoformat()
        html_data = f"<h1>時間 {str_now}</h1>"

        histories = api.get_instruction_history(project_id)[0]
        put_request_body = {"html": html_data, "last_updated_datetime": histories[0]["updated_datetime"]}
        assert type(api.put_instruction(project_id, request_body=put_request_body)[0]) == dict


class TestJob:
    def test_wait_for_completion(self):
        # 実行中のジョブはないので、必ずTrue
        result = wrapper.wait_for_completion(
            project_id, ProjectJobType.GEN_TASKS, job_access_interval=1, max_job_access=1
        )
        assert result == True

    def test_wait_until_job_finished(self):
        # 実行中のジョブはないはずので、必ずTrue
        result = wrapper.wait_until_job_finished(
            project_id, ProjectJobType.GEN_TASKS, job_access_interval=1, max_job_access=1
        )
        assert result is None

    def test_get_all_project_job(self):
        assert len(wrapper.get_all_project_job(project_id, {"type": ProjectJobType.GEN_INPUTS.value})) >= 0

    def test_delete_all_succeeded_job(self):
        assert len(wrapper.delete_all_succeeded_job(project_id, ProjectJobType.GEN_TASKS)) >= 0

    def test_job_in_progress(self):
        assert type(wrapper.job_in_progress(project_id, ProjectJobType.GEN_TASKS)) == bool

    def test_can_execute_job(self):
        assert type(wrapper.can_execute_job(project_id, ProjectJobType.GEN_TASKS)) == bool

    def test_wait_until_job_is_executable(self):
        # ただ実行するだけ
        result = wrapper.wait_until_job_is_executable(project_id, ProjectJobType.GEN_TASKS)
        type(result) == bool

    @pytest.mark.submitting_job
    def test_delete_project_job(self):
        content, _ = api.post_project_tasks_update(project_id)
        job = content["job"]
        job_type = job["job_type"]
        job_id = job["job_id"]
        job_list = wrapper.get_all_project_job(project_id, {"type": job_type})
        assert first_true(job_list, pred=lambda e: e["job_id"] == job_id) is not None
        api.delete_project_job(project_id, job_type=job["job_type"], job_id=job["job_id"])
        job_list = wrapper.get_all_project_job(project_id, {"type": job_type})
        assert first_true(job_list, pred=lambda e: e["job_id"] == job_id) is None


class TestLogin:
    def test_login(self):
        assert api.login()[0]["token"].keys() >= {"id_token", "access_token", "refresh_token"}

        assert api.refresh_token()[0].keys() >= {"id_token", "access_token", "refresh_token"}

        assert type(api.logout()[0]) == dict

        assert api.refresh_token() is None, "ログアウト状態では、refresh_tokenメソッドはNoneを返す"

        assert api.logout() is None, "ログアウト状態では、logoutメソッドはNoneを返す"


class TestMy:
    def test_get_my_account(self):
        my_account, _ = api.get_my_account()
        assert type(my_account) == dict

    def test_get_my_project_members(self):
        my_project_members, _ = api.get_my_project_members()
        assert len(my_project_members) > 0

    def test_wrapper_get_all_my_organizations(self):
        my_organizations = wrapper.get_all_my_organizations()
        assert len(my_organizations) > 0

    def test_get_my_projects(self):
        my_projects, _ = api.get_my_projects()
        assert len(my_projects["list"]) > 0

    def test_get_my_member_in_project(self):
        my_member_in_project, _ = api.get_my_member_in_project(project_id)
        assert type(my_member_in_project) == dict


class TestOrganization:
    @classmethod
    def setup_class(cls):
        cls.organization_name = api.get_organization_of_project(project_id)[0]["organization_name"]

    def test_get_organization(self):
        assert type(api.get_organization(self.organization_name)[0]) == dict

    def test_get_organization_activity(self):
        assert type(api.get_organization_activity(self.organization_name)[0]) == dict

    def test_wrapper_get_all_projects_of_organization(self):
        assert len(wrapper.get_all_projects_of_organization(self.organization_name)) > 0


class TestOrganizationMember:
    @classmethod
    def setup_class(cls):
        cls.organization_name = api.get_organization_of_project(project_id)[0]["organization_name"]

    def test_wrapper_get_all_organization_members(self):
        assert len(wrapper.get_all_organization_members(self.organization_name)) > 0

    def test_get_organization_member(self):
        organization_member = api.get_organization_member(self.organization_name, api.login_user_id)[0]
        assert type(organization_member) == dict

    def test_update_organization_member_role(self):
        organization_member = api.get_organization_member(self.organization_name, api.login_user_id)[0]
        request_body = {"role": "owner", "last_updated_datetime": organization_member["updated_datetime"]}
        api.update_organization_member_role(self.organization_name, api.login_user_id, request_body=request_body)


class TestProject:
    def test_get_project(self):
        assert type(api.get_project(project_id)[0]) == dict

    def test_get_organization_of_project(self):
        assert type(api.get_organization_of_project(project_id)[0]) == dict

    @pytest.mark.submitting_job
    def test_post_project_tasks_update(self):
        assert type(api.post_project_tasks_update(project_id)[0]) == dict

    def test_wrapper_download_project_inputs_url(self):
        assert wrapper.download_project_inputs_url(project_id, f"{out_dir}/inputs.json").startswith("https://")

    def test_wrapper_download_project_tasks_url(self):
        assert wrapper.download_project_tasks_url(project_id, f"{out_dir}/tasks.json").startswith("https://")

    def test_wrapper_download_project_task_history_events_url(self):
        assert wrapper.download_project_task_history_events_url(
            project_id, f"{out_dir}/task_history_events.json"
        ).startswith("https://")

    def test_wrapper_download_project_task_histories_url(self):
        assert wrapper.download_project_task_histories_url(project_id, f"{out_dir}/task_histories.json").startswith(
            "https://"
        )

    def test_wrapper_download_project_inspections_url(self):
        assert wrapper.download_project_inspections_url(project_id, f"{out_dir}/inspections.json").startswith(
            "https://"
        )


class TestProjectMember:
    def test_get_project_member(self):
        my_member = api.get_project_member(project_id, api.login_user_id)[0]
        assert type(my_member) == dict

    def test_wrapper_get_all_project_members(self):
        assert len(wrapper.get_all_project_members(project_id)) >= 0


class TestStatistics:
    def test_wrapper_get_account_daily_statistics(self):
        actual = wrapper.get_account_daily_statistics(project_id, from_date="2021-04-01", to_date="2021-06-30")
        assert type(actual) == list

        # 最大取得期間の3ヶ月を超えている場合
        actual = wrapper.get_account_daily_statistics(project_id, from_date="2021-04-01", to_date="2021-07-01")
        assert type(actual) == list

        # 開始日と終了日を指定しない場合
        actual = wrapper.get_account_daily_statistics(project_id)
        assert type(actual) == list

    def test_wrapper_get_inspection_daily_statistics(self):
        actual = wrapper.get_inspection_daily_statistics(project_id, from_date="2021-04-01", to_date="2021-06-30")
        assert type(actual) == list

        # 最大取得期間の3ヶ月を超えている場合
        actual = wrapper.get_inspection_daily_statistics(project_id, from_date="2021-04-01", to_date="2021-07-01")
        assert type(actual) == list

        # 開始日と終了日を指定しない場合
        actual = wrapper.get_inspection_daily_statistics(project_id)
        assert type(actual) == list

    def test_wrapper_get_phase_daily_statistics(self):
        actual = wrapper.get_phase_daily_statistics(project_id, from_date="2021-04-01", to_date="2021-06-30")
        assert type(actual) == list

        # 最大取得期間の3ヶ月を超えている場合
        actual = wrapper.get_phase_daily_statistics(project_id, from_date="2021-04-01", to_date="2021-07-01")
        assert type(actual) == list

        # 開始日と終了日を指定しない場合
        actual = wrapper.get_phase_daily_statistics(project_id)
        assert type(actual) == list

    def test_wrapper_get_task_daily_statistics(self):
        actual = wrapper.get_task_daily_statistics(project_id, from_date="2021-04-01", to_date="2021-06-30")
        assert type(actual) == list

        # 最大取得期間の3ヶ月を超えている場合
        actual = wrapper.get_task_daily_statistics(project_id, from_date="2021-04-01", to_date="2021-07-01")
        assert type(actual) == list

        # 開始日と終了日を指定しない場合
        actual = wrapper.get_task_daily_statistics(project_id)
        assert type(actual) == list

    def test_wrapper_get_worktime_daily_statistics(self):
        actual = wrapper.get_worktime_daily_statistics(project_id, from_date="2021-04-01", to_date="2021-06-30")
        assert type(actual) == dict

        # 最大取得期間の3ヶ月を超えている場合
        actual = wrapper.get_worktime_daily_statistics(project_id, from_date="2021-04-01", to_date="2021-07-01")
        assert type(actual) == dict

        # 開始日と終了日を指定しない場合
        actual = wrapper.get_worktime_daily_statistics(project_id)
        assert type(actual) == dict

    def test_wrapper_get_worktime_daily_statistics_by_account(self):
        actual = wrapper.get_worktime_daily_statistics_by_account(project_id, from_date="2021-04-01", to_date="2021-06-30")
        assert type(actual) == dict

        # 最大取得期間の3ヶ月を超えている場合
        actual = wrapper.get_worktime_daily_statistics_by_account(project_id, from_date="2021-04-01", to_date="2021-07-01")
        assert type(actual) == dict

        # 開始日と終了日を指定しない場合
        actual = wrapper.get_worktime_daily_statistics_by_account(project_id)
        assert type(actual) == dict

    def test_wrapper_get_label_statistics(self):
        actual = wrapper.get_label_statistics(project_id)
        assert type(actual) == list

    def test_graph_marker(self):
        print("get_markers")
        content, _ = api.get_markers(project_id)
        assert type(content) == dict

        markers = [
            {
                "marker_id": str(uuid.uuid4()),
                "title": "add in test code",
                "graph_type": GraphType.TASK_PROGRESS.value,
                "marked_at": annofabapi.utils.str_now(),
            }
        ]
        request_body = {"markers": markers, "last_updated_datetime": content["updated_datetime"]}
        print("put_markers")
        assert type(api.put_markers(project_id, request_body=request_body)[0]) == dict


class Testsupplementary:
    @classmethod
    def setup_class(cls):
        cls.input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)

    def test_supplementary(self):
        supplementary_data_id = str(uuid.uuid4())
        request_body = {"supplementary_data_number": 1}

        print("")
        print(f"wrapper.put_supplementary_data_from_file: supplementary_data_id={supplementary_data_id}")
        content = wrapper.put_supplementary_data_from_file(
            project_id, self.input_data_id, supplementary_data_id, f"{test_dir}/sample.txt", request_body=request_body
        )
        assert type(content) == dict

        supplementary_data_list = api.get_supplementary_data_list(project_id, self.input_data_id)[0]
        assert len([e for e in supplementary_data_list if e["supplementary_data_id"] == supplementary_data_id]) == 1

        api.delete_supplementary_data(project_id, self.input_data_id, supplementary_data_id)
        supplementary_data_list = api.get_supplementary_data_list(project_id, self.input_data_id)[0]
        assert len([e for e in supplementary_data_list if e["supplementary_data_id"] == supplementary_data_id]) == 0


class TestTask:
    @classmethod
    def setup_class(cls):
        cls.input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)

    def test_wraper_get_all_tasks(self):
        assert type(wrapper.get_all_tasks(project_id, query_params={"task_id": "foo"})) == list

    @pytest.mark.submitting_job
    def test_initiate_tasks_generation_by_csv(self):
        csv_file_path = f"{test_dir}/tmp/create_task.csv"
        test_task_id = str(uuid.uuid4())
        create_csv_for_task(csv_file_path, test_task_id, self.input_data_id)
        content = wrapper.initiate_tasks_generation_by_csv(project_id, csv_file_path)
        assert type(content) == dict

    def test_get_task(self):
        assert type(api.get_task(project_id, task_id)[0]) == dict

    def test_put_task_and_delete_task(self):
        test_task_id = str(uuid.uuid4())
        request_body = {"input_data_id_list": [self.input_data_id]}
        print("")
        print(f"put_task: task_id={task_id}")
        test_task_data = api.put_task(project_id, test_task_id, request_body=request_body)[0]
        assert type(test_task_data) == dict

        assert type(api.delete_task(project_id, test_task_id)[0]) == dict

    @pytest.mark.side_effect
    def test_assign_task(self):
        request_body = {"request_type": {"phase": "annotation", "_type": "Random"}}
        assert type(api.assign_tasks(project_id, request_body=request_body)[0]) == list

    def test_operate_task_in_change_task_status_to_break(self):
        task = wrapper.change_task_status_to_break(project_id, task_id)
        assert task["status"] == "break"

    def test_get_task_histories(self):
        assert len(api.get_task_histories(project_id, task_id)[0]) > 0

    def test_batch_update_tasks(self):
        test_task_id = str(uuid.uuid4())
        request_body = {"input_data_id_list": [self.input_data_id]}
        print("")
        print(f"put_task: task_id={task_id}")
        test_task_data = api.put_task(project_id, test_task_id, request_body=request_body)[0]

        request_body = [{"project_id": project_id, "task_id": test_task_id, "_type": "Delete"}]
        content = api.batch_update_tasks(project_id, request_body=request_body)[0]
        assert type(content) == list

    def test_patch_tasks_metadata(self):
        request_body = {task_id: {"alice": "foo", "bob": 1.23, "charlie": False}}
        content, _ = api.patch_tasks_metadata(project_id, request_body)
        assert type(content) == dict


class TestWebhook:
    def test_get_webhooks(self):
        webhook_list = api.get_webhooks(project_id)[0]
        assert type(webhook_list) == list

    def test_put_webhook_and_delete_webhook(self):
        test_webhook_id = str(uuid.uuid4())
        request_body = {
            "project_id": project_id,
            "event_type": "annotation-archive-updated",
            "webhook_id": test_webhook_id,
            "webhook_status": "active",
            "method": "POST",
            "headers": [{"name": "Content-Type", "value": "application/json"}],
            "body": "test",
            "url": "https://annofab.com/",
            "created_datetime": None,
            "updated_datetime": None,
        }
        print("")
        print(f"put_webhook: webhook_id={test_webhook_id}")
        assert type(api.put_webhook(project_id, test_webhook_id, request_body=request_body)[0]) == dict

        assert type(api.delete_webhook(project_id, test_webhook_id)[0]) == dict


class TestLabor:
    target_date = "2018-01-01"
    target_account_id = service.api.account_id

    @classmethod
    def setup_class(cls):
        cls.organization_id = api.get_organization_of_project(project_id)[0]["organization_id"]

    def test_wrapper_put_labor_control_actual_worktime_and_wrapper_get_labor_control_worktime(self):
        put_result = service.wrapper.put_labor_control_actual_worktime(
            project_id=project_id,
            organization_id=self.organization_id,
            account_id=self.target_account_id,
            date=self.target_date,
            actual_worktime=3.5,
            working_description="foo",
        )
        labor_list = wrapper.get_labor_control_worktime(
            project_id=project_id,
            account_id=self.target_account_id,
            from_date=self.target_date,
            to_date=self.target_date,
        )
        assert len(labor_list) == 1
        labor = labor_list[0]
        assert labor["actual_worktime"] == 3.5
        assert labor["working_description"] == "foo"

    def test_wrapper_put_labor_control_plan_worktime_and_wrapper_get_labor_control_worktime(self):
        put_result = service.wrapper.put_labor_control_plan_worktime(
            project_id=project_id,
            organization_id=self.organization_id,
            account_id=self.target_account_id,
            date=self.target_date,
            plan_worktime=4.5,
        )
        labor_list = wrapper.get_labor_control_worktime(
            project_id=project_id,
            account_id=self.target_account_id,
            from_date=self.target_date,
            to_date=self.target_date,
        )
        assert len(labor_list) == 1
        labor = labor_list[0]
        assert labor["plan_worktime"] == 4.5

    def test_wrapper_put_labor_control_availability_and_wrapper_get_labor_control_availability(self):
        put_result = service.wrapper.put_labor_control_availability(
            account_id=self.target_account_id, date=self.target_date, availability=6.5
        )
        labor_list = wrapper.get_labor_control_availability(
            account_id=self.target_account_id, from_date=self.target_date, to_date=self.target_date
        )
        assert len(labor_list) == 1
        labor = labor_list[0]
        assert labor["availability"] == 6.5

    def test_get_labor_control_worktime_raise(self):
        with pytest.raises(ValueError):
            wrapper.get_labor_control_worktime(account_id=api.account_id)


class TestGetObjOrNone:
    """
    wrapper.get_xxx_or_none メソッドの確認
    """

    @classmethod
    def setup_class(cls):
        cls.organization_name = api.get_organization_of_project(project_id)[0]["organization_name"]
        cls.input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)

    def test_get_input_data_or_none(self):
        assert type(wrapper.get_input_data_or_none(project_id, self.input_data_id)) == dict

        assert wrapper.get_input_data_or_none(project_id, "not-exists") is None

        assert wrapper.get_input_data_or_none("not-exists", self.input_data_id) is None

    def test_get_organization_or_none(self):
        assert type(wrapper.get_organization_or_none(self.organization_name)) == dict

        assert wrapper.get_organization_or_none("not-exists") is None

    def test_get_organization_member_or_none(self):
        assert type(wrapper.get_organization_member_or_none(self.organization_name, api.login_user_id)) == dict

        assert wrapper.get_organization_member_or_none("not-exists", api.login_user_id) is None

        assert wrapper.get_organization_member_or_none(self.organization_name, "not-exists") is None

    def test_get_project_or_none(self):
        assert type(wrapper.get_project_or_none(project_id)) == dict

        assert wrapper.get_project_or_none("not-exists") is None

    def test_get_project_member_or_none(self):
        assert type(wrapper.get_project_member_or_none(project_id, api.login_user_id)) == dict

        assert wrapper.get_project_member_or_none(project_id, "not-exists") is None

        assert wrapper.get_project_member_or_none("not-exists", api.login_user_id) is None

    def test_get_task_or_none(self):
        assert type(wrapper.get_task_or_none(project_id, task_id)) == dict

        assert wrapper.get_task_or_none(project_id, "not-exists") is None

        assert wrapper.get_task_or_none("not-exists", task_id) is None


class TestProtectedMethod:
    @classmethod
    def setup_class(cls):
        cls.input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)

    def test__request_get_with_cookie_with_project_url(self):
        images, _ = api.get_instruction_images(project_id)
        url = images[0]["url"]
        r = api._request_get_with_cookie(project_id, url)
        assert r.status_code == 200

    def test__request_get_with_cookie_with_input_data_set_url(self):
        input_data, _ = api.get_input_data(project_id, self.input_data_id)
        r = api._request_get_with_cookie(project_id, input_data["url"])
        assert r.status_code == 200

    def test_request_get_with_cookie_failed(self):
        # SignedCookieに対応するプロジェクトと、アクセス対象のプロジェクトが異なっているときの対応
        url = "https://annofab.com/projects/foo/annotation_specs_histories/foo.json"
        with pytest.raises(requests.HTTPError):
            api._request_get_with_cookie(project_id, url)


class TestProperty:
    def test_account_id(self):
        account_id = api.account_id
        assert type(account_id) == str and len(account_id) > 0
