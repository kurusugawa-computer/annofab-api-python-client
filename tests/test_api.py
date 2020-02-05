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
from distutils.util import strtobool

import pytest

import annofabapi
import annofabapi.utils
from annofabapi.models import GraphType, JobType
from tests.utils_for_test import WrapperForTest, create_csv_for_task, set_logging_from_inifile

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")
inifile = configparser.ConfigParser()
inifile.read('./pytest.ini', 'UTF-8')
project_id = inifile.get('annofab', 'project_id')
should_execute_job_api: bool = strtobool(inifile.get('annofab', 'should_execute_job_api'))
should_print_log_message: bool = strtobool(inifile.get('annofab', 'should_print_log_message'))

test_dir = './tests/data'
out_dir = './tests/out'

set_logging_from_inifile(inifile)

service = annofabapi.build_from_netrc()
api = service.api
wrapper = service.wrapper
test_wrapper = WrapperForTest(api)

my_account_id = api.get_my_account()[0]['account_id']
organization_name = api.get_organization_of_project(project_id)[0]['organization_name']

annofab_user_id = service.api.login_user_id

task_id = test_wrapper.get_first_task_id(project_id)
input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)


class TestAccount:
    pass


class TestAnnotation:
    def test_wrapper_get_all_annotation_list(self):
        assert len(wrapper.get_all_annotation_list(project_id, {"query": {"task_id": task_id}})) >= 0

    def test_get_annotation(self):
        assert type(api.get_annotation(project_id, task_id, input_data_id)[0]) == dict

    def test_get_editor_annotation(self):
        assert type(api.get_editor_annotation(project_id, task_id, input_data_id)[0]) == dict

    def test_get_annotation_archive(self):
        content, response = api.get_annotation_archive(project_id)
        assert response.headers["Location"].startswith("https://")

        # v2版の確認
        content, response = api.get_annotation_archive(project_id, query_params={"v2": True})
        assert response.headers["Location"].startswith("https://")

    def test_get_archive_full_with_pro_id(self):
        content, response = api.get_archive_full_with_pro_id(project_id)
        assert response.headers["Location"].startswith("https://")

    def test_wrapper_download_annotation_archive(self):
        wrapper.download_annotation_archive(project_id, f'{out_dir}/simple-annotation.zip')

    @pytest.mark.submitting_job
    def test_post_annotation_archive_update(self):
        content = api.post_annotation_archive_update(project_id, query_params={"v": "2"})[0]
        job = content["job"]
        assert job["job_type"] == JobType.GEN_ANNOTATION.value


class TestAnnotationSpecs:
    def test_get_annotation_specs(self):
        annotation_spec, _ = api.get_annotation_specs(project_id)
        assert type(annotation_spec) == dict

    def test_put_annotation_specs(self):
        annotation_spec, _ = api.get_annotation_specs(project_id)

        request_body = {
            "labels": annotation_spec["labels"],
            "inspection_phrases": annotation_spec["inspection_phrases"],
            "comment": f"{annofabapi.utils.str_now()} に更新しました。",
        }
        puted_annotation_spec, _ = api.put_annotation_specs(project_id, request_body=request_body)
        assert type(puted_annotation_spec) == dict

    def test_get_annotation_specs_histories(self):
        annotation_specs_histories = api.get_annotation_specs_histories(project_id)[0]
        assert type(annotation_specs_histories) == list


class TestInput:
    def test_wrapper_get_input_data_list(self):
        assert type(wrapper.get_all_input_data_list(project_id, {"input_data_name": "foo"})) == list

    def test_get_input_data(self):
        test_input_data = api.get_input_data(project_id, input_data_id)[0]
        assert type(test_input_data) == dict

    def test_wrapper_put_input_data_from_file_and_delete_input_data(self):
        test_input_data_id = str(uuid.uuid4())
        print("")
        print(f"put_input_data: input_data_id={test_input_data_id}")
        assert type(wrapper.put_input_data_from_file(project_id, test_input_data_id, f'{test_dir}/lenna.png')) == dict
        assert type(api.delete_input_data(project_id, test_input_data_id)[0]) == dict

    def test_batch_update_inputs(self):
        test_input_data_id = str(uuid.uuid4())
        print("")
        print(f"put_input_data: input_data_id={test_input_data_id}")
        wrapper.put_input_data_from_file(project_id, test_input_data_id, f'{test_dir}/lenna.png')

        request_body = [{'project_id': project_id, 'input_data_id': test_input_data_id, '_type': 'Delete'}]
        assert type(api.batch_update_inputs(project_id, request_body=request_body)[0]) == list


class TestInspection:
    def test_get_inspections(self):
        assert len(api.get_inspections(project_id, task_id, input_data_id)[0]) >= 0


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
        wrapper.upload_instruction_image(project_id, test_image_id, f'{test_dir}/lenna.png')

        api.delete_instruction_image(project_id, test_image_id)

    def test_get_instruction_images(self):
        image_list = api.get_instruction_images(project_id)[0]
        assert type(image_list) == list

    def test_put_instruction(self):
        str_now = datetime.datetime.now().isoformat()
        html_data = f"<h1>時間 {str_now}</h1>"

        histories = api.get_instruction_history(project_id)[0]
        put_request_body = {'html': html_data, 'last_updated_datetime': histories[0]['updated_datetime']}
        assert type(api.put_instruction(project_id, request_body=put_request_body)[0]) == dict


class TestJob:
    def test_wait_for_completion(self):
        # 実行中のジョブはないので、必ずTrue
        result = wrapper.wait_for_completion(project_id, JobType.GEN_TASKS, job_access_interval=1, max_job_access=1)
        assert result == True

    def test_get_all_project_job(self):
        assert len(wrapper.get_all_project_job(project_id, {"type": JobType.GEN_INPUTS.value})) >= 0

    def test_delete_all_succeeded_job(self):
        assert len(wrapper.delete_all_succeeded_job(project_id, JobType.GEN_TASKS)) >= 0

    def test_job_in_progress(self):
        assert type(wrapper.job_in_progress(project_id, JobType.GEN_TASKS)) == bool


class TestLogin:
    def test_login(self):
        assert api.login()[0]['token'].keys() >= {'id_token', 'access_token', 'refresh_token'}

        assert api.refresh_token()[0].keys() >= {'id_token', 'access_token', 'refresh_token'}

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
        assert len(my_projects['list']) > 0

    def test_get_my_member_in_project(self):
        my_member_in_project, _ = api.get_my_member_in_project(project_id)
        assert type(my_member_in_project) == dict


class TestOrganization:
    def test_get_organization(self):
        assert type(api.get_organization(organization_name)[0]) == dict

    def test_get_organization_activity(self):
        assert type(api.get_organization_activity(organization_name)[0]) == dict

    def test_wrapper_get_all_projects_of_organization(self):
        assert len(wrapper.get_all_projects_of_organization(organization_name)) > 0


class TestOrganizationMember:
    def test_wrapper_get_all_organization_members(self):
        assert len(wrapper.get_all_organization_members(organization_name)) > 0

    def test_get_organization_member(self):
        organization_member = api.get_organization_member(organization_name, annofab_user_id)[0]
        assert type(organization_member) == dict

    def test_update_organization_member_role(self):
        organization_member = api.get_organization_member(organization_name, annofab_user_id)[0]
        request_body = {'role': 'owner', 'last_updated_datetime': organization_member['updated_datetime']}
        api.update_organization_member_role(organization_name, annofab_user_id, request_body=request_body)


class TestProject:
    def test_get_project(self):
        assert type(api.get_project(project_id)[0]) == dict

    def test_get_organization_of_project(self):
        assert type(api.get_organization_of_project(project_id)[0]) == dict

    @pytest.mark.submitting_job
    def test_post_project_tasks_update(self):
        assert type(api.post_project_tasks_update(project_id)[0]) == dict

    def test_wrapper_download_project_inputs_url(self):
        assert wrapper.download_project_inputs_url(project_id, f'{out_dir}/inputs.json').startswith("https://")

    def test_wrapper_download_project_tasks_url(self):
        assert wrapper.download_project_tasks_url(project_id, f'{out_dir}/tasks.json').startswith("https://")

    def test_wrapper_download_project_task_history_events_url(self):
        assert wrapper.download_project_task_history_events_url(
            project_id, f'{out_dir}/task_history_events.json').startswith("https://")

    def test_wrapper_download_project_inspections_url(self):
        assert wrapper.download_project_inspections_url(project_id,
                                                        f'{out_dir}/inspections.json').startswith("https://")


class TestProjectMember:
    def test_get_project_member(self):
        my_member = api.get_project_member(project_id, annofab_user_id)[0]
        assert type(my_member) == dict

    def test_wrapper_get_all_project_members(self):
        assert len(wrapper.get_all_project_members(project_id)) >= 0

    def test_wrapper_copy_project_member(self):
        content = wrapper.copy_project_members(src_project_id=project_id, dest_project_id=project_id, delete_dest=False)
        assert type(content) == list


class TestStatistics:
    def test_statistics(self):
        assert type(api.get_task_statistics(project_id)[0]) == list

    def test_get_account_statistics(self):
        assert type(api.get_account_statistics(project_id)[0]) == list

    def test_get_inspection_statistics(self):
        assert type(api.get_inspection_statistics(project_id)[0]) == list

    def test_get_task_phase_statistics(self):
        assert type(api.get_task_phase_statistics(project_id)[0]) == list

    def test_get_label_statistics(self):
        assert type(api.get_label_statistics(project_id)[0]) == list

    def test_wrapper_get_worktime_statistics(self):
        assert type(wrapper.get_worktime_statistics(project_id)) == list

    def test_graph_marker(self):
        print("get_markers")
        content, _ = api.get_markers(project_id)
        assert type(content) == dict

        markers = [{
            "marker_id": str(uuid.uuid4()),
            "title": "add in test code",
            "graph_type": GraphType.TASK_PROGRESS.value,
            "marked_at": annofabapi.utils.str_now()
        }]
        request_body = {"markers": markers, "last_updated_datetime": content["updated_datetime"]}
        print("put_markers")
        assert type(api.put_markers(project_id, request_body=request_body)[0]) == dict


class Testsupplementary:
    def test_supplementary(self):
        supplementary_data_id = str(uuid.uuid4())
        request_body = {'supplementary_data_number': 1}

        print("")
        print(f"wrapper.put_supplementary_data_from_file: supplementary_data_id={supplementary_data_id}")
        content = wrapper.put_supplementary_data_from_file(project_id, input_data_id, supplementary_data_id,
                                                           f'{test_dir}/sample.txt', request_body=request_body)
        assert type(content) == dict

        supplementary_data_list = api.get_supplementary_data_list(project_id, input_data_id)[0]
        assert len([e for e in supplementary_data_list if e['supplementary_data_id'] == supplementary_data_id]) == 1

        api.delete_supplementary_data(project_id, input_data_id, supplementary_data_id)
        supplementary_data_list = api.get_supplementary_data_list(project_id, input_data_id)[0]
        assert len([e for e in supplementary_data_list if e['supplementary_data_id'] == supplementary_data_id]) == 0


class TestTask:
    def test_wraper_get_all_tasks(self):
        assert type(wrapper.get_all_tasks(project_id, query_params={'task_id': "foo"})) == list

    @pytest.mark.submitting_job
    def test_initiate_tasks_generation_by_csv(self):
        csv_file_path = f'{test_dir}/tmp/create_task.csv'
        test_task_id = str(uuid.uuid4())
        create_csv_for_task(csv_file_path, test_task_id, input_data_id)
        content = wrapper.initiate_tasks_generation_by_csv(project_id, csv_file_path)
        assert type(content) == dict

    def test_get_task(self):
        assert type(api.get_task(project_id, task_id)[0]) == dict

    def test_put_task_and_delete_task(self):
        test_task_id = str(uuid.uuid4())
        request_body = {"input_data_id_list": [input_data_id]}
        print("")
        print(f"put_task: task_id={task_id}")
        test_task_data = api.put_task(project_id, test_task_id, request_body=request_body)[0]
        assert type(test_task_data) == dict

        assert type(api.delete_task(project_id, test_task_id)[0]) == dict

    def test_assign_task(self):
        request_body = {"request_type": {"phase": "annotation", "_type": "Random"}}
        assert type(api.assign_tasks(project_id, request_body=request_body)[0]) == list

    def test_operate_task(self):
        task, _ = api.get_task(project_id, task_id)
        request_body = {
            'status': 'not_started',
            'last_updated_datetime': task['updated_datetime'],
            'account_id': my_account_id
        }
        assert type(api.operate_task(project_id, task_id, request_body=request_body)[0]) == dict

    def test_get_task_histories(self):
        assert len(api.get_task_histories(project_id, task_id)[0]) > 0

    def test_batch_update_tasks(self):
        test_task_id = str(uuid.uuid4())
        request_body = {"input_data_id_list": [input_data_id]}
        print("")
        print(f"put_task: task_id={task_id}")
        test_task_data = api.put_task(project_id, test_task_id, request_body=request_body)[0]

        request_body = [{'project_id': project_id, 'task_id': test_task_id, '_type': 'Delete'}]
        content = api.batch_update_tasks(project_id, request_body=request_body)[0]
        assert type(content) == list


class TestWebhook:
    def test_get_webhooks(self):
        webhook_list = api.get_webhooks(project_id)[0]
        assert type(webhook_list) == list

    def test_put_webhook_and_delete_webhook(self):
        test_webhook_id = str(uuid.uuid4())
        request_body = {
            "project_id": project_id,
            "event_type": "task-completed",
            "webhook_id": test_webhook_id,
            "webhook_status": "active",
            "method": "POST",
            "headers": [{
                "name": "Content-Type",
                "value": "application/json"
            }],
            "body": "test",
            "url": "https://annofab.com/",
            "created_datetime": None,
            "updated_datetime": None,
        }
        print("")
        print(f"put_webhook: webhook_id={test_webhook_id}")
        assert type(api.put_webhook(project_id, test_webhook_id, request_body=request_body)[0]) == dict

        assert type(api.delete_webhook(project_id, test_webhook_id)[0]) == dict


class TestGetObjOrNone:
    """
    wrapper.get_xxx_or_none メソッドの確認
    """
    def test_get_input_data_or_none(self):
        assert type(wrapper.get_input_data_or_none(project_id, input_data_id)) == dict

        assert wrapper.get_input_data_or_none(project_id, "not-exists") is None

        assert wrapper.get_input_data_or_none("not-exists", input_data_id) is None

    def test_get_organization_or_none(self):
        assert type(wrapper.get_organization_or_none(organization_name)) == dict

        assert wrapper.get_organization_or_none("not-exists") is None

    def test_get_organization_member_or_none(self):
        assert type(wrapper.get_organization_member_or_none(organization_name, annofab_user_id)) == dict

        assert wrapper.get_organization_member_or_none("not-exists", annofab_user_id) is None

        assert wrapper.get_organization_member_or_none(organization_name, "not-exists") is None

    def test_get_project_or_none(self):
        assert type(wrapper.get_project_or_none(project_id)) == dict

        assert wrapper.get_project_or_none("not-exists") is None

    def test_get_project_member_or_none(self):
        assert type(wrapper.get_project_member_or_none(project_id, annofab_user_id)) == dict

        assert wrapper.get_project_member_or_none(project_id, "not-exists") is None

        assert wrapper.get_project_member_or_none("not-exists", annofab_user_id) is None

    def test_get_task_or_none(self):
        assert type(wrapper.get_task_or_none(project_id, task_id)) == dict

        assert wrapper.get_task_or_none(project_id, "not-exists") is None

        assert wrapper.get_task_or_none("not-exists", task_id) is None
