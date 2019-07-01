"""
AnnofabApi, Wrapperのテストコード

### テストの観点
【注意】
* 基本的にHTTP GETのテストのみ行うこと。PUT/POST/DELETEのテストがあると、間違えて修正してまうおそれあり。

"""
import configparser
import datetime
import logging
import os
import time
import uuid
from distutils.util import strtobool

import annofabapi
import annofabapi.utils
from tests.utils_for_test import WrapperForTest, create_csv_for_task

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")
inifile = configparser.ConfigParser()
inifile.read('./pytest.ini', 'UTF-8')
project_id = inifile.get('annofab', 'project_id')
should_execute_job_api: bool = strtobool(inifile.get('annofab', 'should_execute_job_api'))
should_print_log_message: bool = strtobool(inifile.get('annofab', 'should_print_log_message'))

test_dir = './tests/data'
out_dir = './tests/out'

if should_print_log_message:
    logging_formatter = '%(levelname)s : %(asctime)s : %(name)s : %(funcName)s : %(message)s'
    logging.basicConfig(format=logging_formatter)
    logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)

service = annofabapi.build_from_netrc()
api = service.api
wrapper = service.wrapper
test_wrapper = WrapperForTest(api)

my_account_id = api.get_my_account()[0]['account_id']
organization_name = api.get_organization_of_project(project_id)[0]['organization_name']

annofab_user_id = service.api.login_user_id


def test_account():
    pass


def test_my():
    print(f"get_my_account")
    my_account, _ = api.get_my_account()
    assert type(my_account) == dict

    # print(f"put_my_account")
    # my_account_request_body = {
    #     'user_id': my_account['user_id'],
    #     'username': my_account['username'],
    #     'lang': my_account['lang'],
    #     'keylayout': my_account['keylayout'],
    #     'last_updated_datetime': my_account['updated_datetime']
    # }
    # puted_my_account, _ = api.put_my_account(request_body=my_account_request_body)
    # assert type(puted_my_account) == dict

    print(f"get_my_project_members")
    my_project_members, _ = api.get_my_project_members()
    assert len(my_project_members) > 0

    print(f"get_my_organizations")
    my_organizations, _ = api.get_my_organizations()
    assert len(my_organizations['list']) > 0

    print(f"get_my_projects")
    my_projects, _ = api.get_my_projects()
    assert len(my_projects['list']) > 0

    print(f"get_my_member_by_project_id")
    my_member_in_project, _ = api.get_my_member_in_project(project_id)
    assert type(my_member_in_project) == dict


def test_annotation():
    """
    batchUpdateAnnotations, putAnnotationはテストしない.
    """

    task_id = test_wrapper.get_first_task_id(project_id)
    input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)

    print("get_annotation_list in wrapper.get_all_annotation_list")
    assert len(wrapper.get_all_annotation_list(project_id, {"query": {"task_id": task_id}})) >= 0

    print("get_annotation")
    assert type(api.get_annotation(project_id, task_id, input_data_id)[0]) == dict

    print("get_annotation_archive")
    content, response = api.get_annotation_archive(project_id)
    assert response.headers["Location"].startswith("https://")

    print("wrapper.download_annotation_archive")
    wrapper.download_annotation_archive(project_id, f'{out_dir}/simple-annotation.zip')

    if should_execute_job_api:
        print("post_annotation_archive_update")
        assert type(api.post_annotation_archive_update(project_id)[0]) == dict


def test_annotation_specs():
    print(f"get_annotation_specs")
    annotation_spec, _ = api.get_annotation_specs(project_id)
    assert type(annotation_spec) == dict

    print(f"put_annotation_specs")
    request_body = {
        "labels": annotation_spec["labels"],
        "inspection_phrases": annotation_spec["inspection_phrases"],
        "updated_datetime": annotation_spec["updated_datetime"],
    }
    puted_annotation_spec, _ = api.put_annotation_specs(project_id, request_body=request_body)
    assert type(puted_annotation_spec) == dict

    print("wrapper.copy_annotation_specs")
    content = wrapper.copy_annotation_specs(src_project_id=project_id, dest_project_id=project_id)
    assert type(content) == dict


def test_login():
    print(f"login")
    assert api.login()[0]['token'].keys() >= {'id_token', 'access_token', 'refresh_token'}
    print(f"refresh_token with logging in")
    assert api.refresh_token()[0].keys() >= {'id_token', 'access_token', 'refresh_token'}
    print(f"logout with logging in")
    assert type(api.logout()[0]) == dict

    print(f"refresh_token with logging out")
    assert api.refresh_token() is None

    print(f"logout with logging out")
    assert api.logout() is None


def test_input():
    test_input_data_id = str(uuid.uuid4())
    print(f"wrapper.put_input_data_from_file (内部でput_input_dataとcreate_temp_pathが実行される）. test_id={test_input_data_id}")
    assert type(wrapper.put_input_data_from_file(project_id, test_input_data_id, f'{test_dir}/lenna.png')) == dict

    print(f"get_input_data")
    test_input_data = api.get_input_data(project_id, test_input_data_id)[0]
    assert type(test_input_data) == dict

    print(f"get_input_data_list in wrapper.get_all_input_data_list")
    # すぐには反映されないので、少し待つ
    time.sleep(5)
    assert len(wrapper.get_all_input_data_list(project_id, {"input_data_id": test_input_data_id})) == 1

    print(f"delete_input_data")
    assert type(api.delete_input_data(project_id, test_input_data_id)[0]) == dict
    time.sleep(3)
    content, _ = api.get_input_data_list(project_id, query_params={'input_data_id': test_input_data_id})
    assert len(content['list']) == 0

    test2_input_data_id = str(uuid.uuid4())
    print(f"入力データの一括更新（削除）(batch_update_inputs). test_id2={test2_input_data_id}")
    wrapper.put_input_data_from_file(project_id, test2_input_data_id, f'{test_dir}/lenna.png')
    request_body1 = [{'project_id': project_id, 'input_data_id': test2_input_data_id, '_type': 'Delete'}]
    assert type(api.batch_update_inputs(project_id, request_body=request_body1)[0]) == list


def test_supplementary():
    input_data_id = test_wrapper.get_first_input_data(project_id)['input_data_id']

    print("wrapper.put_supplementary_data_from_file（内部でput_supplementary_dataが実行される）")
    supplementary_data_id = str(uuid.uuid4())
    request_body = {'supplementary_data_number': 1}
    content = wrapper.put_supplementary_data_from_file(project_id, input_data_id, supplementary_data_id,
                                                       f'{test_dir}/sample.txt', request_body=request_body)
    assert type(content) == dict

    print("get_supplementary_data_list")
    supplementary_data_list = api.get_supplementary_data_list(project_id, input_data_id)[0]
    assert len([e for e in supplementary_data_list if e['supplementary_data_id'] == supplementary_data_id]) == 1

    print("delete_supplementary_data")
    api.delete_supplementary_data(project_id, input_data_id, supplementary_data_id)
    supplementary_data_list = api.get_supplementary_data_list(project_id, input_data_id)[0]
    assert len([e for e in supplementary_data_list if e['supplementary_data_id'] == supplementary_data_id]) == 0


def test_inspection():
    """
    batchUpdateInspectionsはテストしない.
    """

    task_id = test_wrapper.get_first_task_id(project_id)
    input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)

    # # 作業中のタスクでなくても、検査コメントは付与できる
    # req_inspection = [{
    #     "data": {
    #         "project_id": project_id,
    #         "comment": f"test comment by test code {annofabapi.utils.str_now()}",
    #         "task_id": task_id,
    #         "input_data_id": input_data_id,
    #         "inspection_id": str(uuid.uuid4()),
    #         "phase": "acceptance",
    #         "commenter_account_id": my_account_id,
    #         "data": {
    #             "x": 0,
    #             "y": 0,
    #             "_type": "Point"
    #         },
    #         "status": "annotator_action_required",
    #         "created_datetime": annofabapi.utils.str_now()
    #     },
    #     "_type": "Put",
    # }]
    #
    # api.batch_update_inspections(project_id, task_id, input_data_id,
    #                                             request_body=req_inspection)
    print("get_inspections")
    assert len(api.get_inspections(project_id, task_id, input_data_id)[0]) >= 0


def test_organization():
    """
    createNewOrganization はテストしない
    """

    print("get_organization")
    assert type(api.get_organization(organization_name)[0]) == dict

    print("get_projects_of_organization in wrapper.get_all_projects_of_organization")
    assert len(wrapper.get_all_projects_of_organization(organization_name)) > 0

    print("get_organization_activity")
    assert type(api.get_organization_activity(organization_name)[0]) == dict


def test_organization_member():
    """
    招待関係のAPI、削除関係のAPIはテストしない
    """

    print("api.get_organization_members in wrapper.get_all_organization_members")
    assert len(wrapper.get_all_organization_members(organization_name)) > 0

    print("api.get_organization_member")
    organization_member = api.get_organization_member(organization_name, annofab_user_id)[0]
    assert type(organization_member) == dict

    print("api.put_role_of_organization_member")
    request_body = {'role': 'owner', 'last_updated_datetime': organization_member['updated_datetime']}
    api.update_organization_member_role(organization_name, annofab_user_id, request_body=request_body)


def test_project():
    """

    間違って操作してしまうと危険なので、プロジェクトの複製、作成、削除はテストしない。

    """
    print("get_project")
    assert type(api.get_project(project_id)[0]) == dict

    print("get_organization_of_project")
    assert type(api.get_organization_of_project(project_id)[0]) == dict

    print("wrapper.download_....")
    assert wrapper.download_project_tasks_url(project_id, f'{out_dir}/tasks.json').startswith("https://")

    assert wrapper.download_project_task_history_events_url(
        project_id, f'{out_dir}/task_history_events.json').startswith("https://")

    assert wrapper.download_project_inspections_url(project_id, f'{out_dir}/inspections.json').startswith("https://")


def test_project_member():
    print(f"get_project_member")
    my_member = api.get_project_member(project_id, annofab_user_id)[0]
    assert type(my_member) == dict

    print(f"get_project_members in wrapper.get_all_project_members")
    assert len(wrapper.get_all_project_members(project_id)) >= 0

    print("wrapper.copy_project_member -> wrapper.put_project_members -> put_project_member")
    content = wrapper.copy_project_members(src_project_id=project_id, dest_project_id=project_id, delete_dest=False)
    assert type(content) == list


def test_statistics():
    print("get_task_statistics")
    assert type(api.get_task_statistics(project_id)[0]) == list

    print("get_account_statistics")
    assert type(api.get_account_statistics(project_id)[0]) == list

    print("get_inspection_statistics")
    assert type(api.get_inspection_statistics(project_id)[0]) == list

    print("get_task_phase_statistics")
    assert type(api.get_task_phase_statistics(project_id)[0]) == list

    print("get_label_statistics")
    assert type(api.get_label_statistics(project_id)[0]) == list

    print("get_worktime_statistics")
    assert type(api.get_worktime_statistics(project_id)[0]) == list


def test_task():
    test_task_id = str(uuid.uuid4())

    print(f"put_task. test_task_id={test_task_id}")
    first_input_data = test_wrapper.get_first_input_data(project_id)
    input_data_id_list = [first_input_data['input_data_id']]
    request_body = {"input_data_id_list": input_data_id_list}
    test_task_data = api.put_task(project_id, test_task_id, request_body=request_body)[0]
    assert type(test_task_data) == dict

    print(f"get_task")
    assert type(api.get_task(project_id, test_task_id)[0]) == dict

    print(f"get_tasks in wrapper.get_all_tasks")
    time.sleep(3)  # sleepしないと失敗したため
    assert len(wrapper.get_all_tasks(project_id, query_params={'task_id': test_task_id})) == 1

    print(f"start_task (annotation)")
    request_body = {"phase": "annotation"}
    assert type(api.start_task(project_id, request_body=request_body)[0]) == dict

    print(f"operate_task")
    request_body1 = {
        'status': 'not_started',
        'last_updated_datetime': test_task_data['updated_datetime'],
        'account_id': my_account_id
    }
    assert type(api.operate_task(project_id, test_task_id, request_body=request_body1)[0]) == dict

    print(f"get_task_histories")
    assert len(api.get_task_histories(project_id, test_task_id)[0]) > 0

    print(f"get_task_validation")
    assert type(api.get_task_validation(project_id, test_task_id)[0]) == dict

    print(f"delete_task")
    assert type(api.delete_task(project_id, test_task_id)[0]) == dict

    test2_task_id = str(uuid.uuid4())
    print(f"batch_update_tasks. test_task_id={test2_task_id}")
    request_body = {"input_data_id_list": input_data_id_list}
    test_task_data = api.put_task(project_id, test2_task_id, request_body=request_body)[0]

    request_body = [{'project_id': project_id, 'task_id': test2_task_id, '_type': 'Delete'}]
    content = api.batch_update_tasks(project_id, request_body=request_body)[0]
    assert type(content) == list

    if should_execute_job_api:
        print(f"initiate_tasks_generation in wrapper.initiate_tasks_generation_by_csv")
        csv_file_path = f'{test_dir}/tmp/create_task.csv'
        create_csv_for_task(csv_file_path, first_input_data)
        task_id_prefix = str(uuid.uuid4())
        content = wrapper.initiate_tasks_generation_by_csv(project_id, csv_file_path, task_id_prefix)
        assert type(content) == dict


def test_instruction():
    str_now = datetime.datetime.now().isoformat()
    html_data = f"<h1>時間 {str_now}</h1>"

    print("put_instruction")
    assert type(api.put_instruction(project_id, request_body=html_data)[0]) == dict

    print("get_instruction_history")
    histories = api.get_instruction_history(project_id)[0]
    assert len(histories) > 0

    # print("get_instruction")
    # history_id = histories[0]['history_id']
    # 2019/05/02 時点ではAPIのcontent-typeがoctet-streamのため、型が異なるというエラーになる
    # assert api.get_instruction(project_id, {"history_id": history_id})[0] == html_data

    # print("wrapper.get_latest_instruction")
    # assert wrapper.get_latest_instruction(project_id) == html_data

    print("upload_instruction_image. 内部でget_instruction_image_url_for_put を実行している")
    test_image_id = str(uuid.uuid4())
    wrapper.upload_instruction_image(project_id, test_image_id, f'{test_dir}/lenna.png')

    print("get_instruction_images")
    images = api.get_instruction_images(project_id)[0]
    assert len([e for e in images if e["image_id"] == test_image_id]) == 1

    print("delete_instruction_image")
    api.delete_instruction_image(project_id, test_image_id)


def test_job():
    print("get_project_job in wrapper.get_all_project_job")
    assert len(wrapper.get_all_project_job(project_id, {"type": "gen-inputs"})) >= 0

    print("wrapper.delete_all_succeeded_job")
    assert len(wrapper.delete_all_succeeded_job(project_id, "gen-tasks")) >= 0


def test_webhook():
    print("put_webhook")
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
    assert type(api.put_webhook(project_id, test_webhook_id, request_body=request_body)[0]) == dict

    print("get_webhooks")
    webhook_list = api.get_webhooks(project_id)[0]
    assert len([e for e in webhook_list if e["webhook_id"] == test_webhook_id]) == 1

    # Errorが発生するので実行しない
    # print("test_webhook")
    # assert type(api.test_webhook(project_id, test_webhook_id)[0]) == dict

    print("delete_webhook")
    assert type(api.delete_webhook(project_id, test_webhook_id)[0]) == dict
