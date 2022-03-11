import configparser
import os
from pathlib import Path

import annofabapi
import annofabapi.utils
from annofabapi.dataclass.annotation import Annotation, SimpleAnnotation, SingleAnnotation
from annofabapi.dataclass.annotation_specs import AnnotationSpecsV1
from annofabapi.dataclass.input import InputData
from annofabapi.dataclass.inspection import Inspection
from annofabapi.dataclass.instruction import Instruction, InstructionHistory, InstructionImage
from annofabapi.dataclass.job import ProjectJobInfo
from annofabapi.dataclass.my import MyAccount, MyOrganization
from annofabapi.dataclass.organization import Organization, OrganizationActivity
from annofabapi.dataclass.organization_member import OrganizationMember
from annofabapi.dataclass.project import Project
from annofabapi.dataclass.project_member import ProjectMember
from annofabapi.dataclass.statistics import LabelStatistics, Markers
from annofabapi.dataclass.supplementary import SupplementaryData
from annofabapi.dataclass.task import Task, TaskHistory
from annofabapi.dataclass.webhook import Webhook
from tests.utils_for_test import WrapperForTest

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")
inifile = configparser.ConfigParser()
inifile.read("./pytest.ini", "UTF-8")
project_id = inifile["annofab"]["project_id"]
task_id = inifile["annofab"]["task_id"]

test_dir = Path("./tests/data")

endpoint_url = inifile["annofab"].get("endpoint_url", None)
if endpoint_url is not None:
    service = annofabapi.build(endpoint_url=endpoint_url)
else:
    service = annofabapi.build()
test_wrapper = WrapperForTest(service.api)


class TestAnnotation:
    @classmethod
    def setup_class(cls):
        cls.input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)

    def test_get_editor_annotation(self):
        dict_obj, _ = service.api.get_editor_annotation(project_id, task_id, self.input_data_id)
        dataclass_obj = Annotation.from_dict(dict_obj)
        assert type(dataclass_obj) == Annotation

    def test_simple_annotation(self):
        annotation_list = service.wrapper.get_all_annotation_list(
            project_id, query_params={"query": {"task_id": task_id}}
        )
        single_annotation = SingleAnnotation.from_dict(annotation_list[0])
        assert type(single_annotation) == SingleAnnotation

    def test_full_annotation(self):
        dict_simple_annotation, _ = service.api.get_annotation(project_id, task_id, self.input_data_id)
        simple_annotation = SimpleAnnotation.from_dict(dict_simple_annotation)
        assert type(simple_annotation) == SimpleAnnotation


class TestAnnotationSpecsV1:
    def test_annotation_specs(self):
        dict_annotation_specs, _ = service.api.get_annotation_specs(project_id)
        annotation_specs = AnnotationSpecsV1.from_dict(dict_annotation_specs)
        assert type(annotation_specs) == AnnotationSpecsV1


class TestInput:
    def test_input_data(self):
        input_data_list = service.wrapper.get_all_input_data_list(project_id, query_params={"task_id": task_id})
        input_data = InputData.from_dict(input_data_list[0])
        assert type(input_data) == InputData


class TestInspection:
    @classmethod
    def setup_class(cls):
        cls.input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)

    def test_inspection(self):
        inspection_list, _ = service.api.get_inspections(project_id, task_id, self.input_data_id)
        inspection = Inspection.from_dict(inspection_list[0])
        assert type(inspection) == Inspection


class TestInstruction:
    def test_instruction(self):
        dict_instruction = service.wrapper.get_latest_instruction(project_id)
        instruction = Instruction.from_dict(dict_instruction)
        assert type(instruction) == Instruction

    def test_instruction_history(self):
        instruction_history_list, _ = service.api.get_instruction_history(project_id)
        instruction_history = InstructionHistory.from_dict(instruction_history_list[0])
        assert type(instruction_history) == InstructionHistory

    def test_instruction_image(self):
        instruction_image_list, _ = service.api.get_instruction_images(project_id)
        instruction_image = InstructionImage.from_dict(instruction_image_list[0])
        assert type(instruction_image) == InstructionImage


class TestJob:
    def test_job(self):
        job_list = service.wrapper.get_all_project_job(project_id)
        if len(job_list) > 0:
            job = ProjectJobInfo.from_dict(job_list[0])
            assert type(job) == ProjectJobInfo
        else:
            print(f"ジョブが存在しませんでした。")


class TestMy:
    def test_my_organization(self):
        my_organizations = service.wrapper.get_all_my_organizations()
        my_organization = MyOrganization.from_dict(my_organizations[0])
        assert type(my_organization) == MyOrganization

    def test_my_account(self):
        dict_my_account, _ = service.api.get_my_account()
        my_account = MyAccount.from_dict(dict_my_account)
        assert type(my_account) == MyAccount


class TestOrganization:
    @classmethod
    def setup_class(cls):
        cls.organization_name = service.api.get_organization_of_project(project_id)[0]["organization_name"]

    def test_organization(self):
        dict_organization, _ = service.api.get_organization(self.organization_name)
        organization = Organization.from_dict(dict_organization)
        assert type(organization) == Organization

    def test_organization_activity(self):
        dict_organization_activity, _ = service.api.get_organization_activity(self.organization_name)
        organization_activity = OrganizationActivity.from_dict(dict_organization_activity)
        assert type(organization_activity) == OrganizationActivity


class TestOrganizationMember:
    @classmethod
    def setup_class(cls):
        cls.organization_name = service.api.get_organization_of_project(project_id)[0]["organization_name"]

    def test_organization_member(self):
        dict_organization_member, _ = service.api.get_organization_member(
            self.organization_name, service.api.login_user_id
        )
        organization_member = OrganizationMember.from_dict(dict_organization_member)
        assert type(organization_member) == OrganizationMember


class TestProject:
    def test_project(self):
        dict_project, _ = service.api.get_project(project_id)
        project = Project.from_dict(dict_project)
        assert type(project) == Project


class TestProjectMember:
    def test_project_member(self):
        dict_project_member, _ = service.api.get_project_member(project_id, service.api.login_user_id)
        project_member = ProjectMember.from_dict(dict_project_member)
        assert type(project_member) == ProjectMember


class TestStatistics:
    def test_statistics_get_label_statistics(self):
        stat_list = service.wrapper.get_label_statistics(project_id)
        stat = LabelStatistics.from_dict(stat_list[0])
        assert type(stat) == LabelStatistics

    def test_markers(self):
        content, _ = service.api.get_markers(project_id)
        markers = Markers.from_dict(content)
        assert type(markers) == Markers


class TestSupplementary:
    @classmethod
    def setup_class(cls):
        cls.input_data_id = test_wrapper.get_first_input_data_id_in_task(project_id, task_id)

    def test_supplementary(self):
        supplementary_data_list, _ = service.api.get_supplementary_data_list(project_id, self.input_data_id)
        supplementary_data = SupplementaryData.from_dict(supplementary_data_list[0])
        assert type(supplementary_data) == SupplementaryData


class TestTask:
    def test_task(self):
        dict_task, _ = service.api.get_task(project_id, task_id)
        task = Task.from_dict(dict_task)
        assert type(task) == Task

    def test_task_history(self):
        task_histories, _ = service.api.get_task_histories(project_id, task_id)
        task_history = TaskHistory.from_dict(task_histories[0])
        assert type(task_history) == TaskHistory


class TestWebhook:
    def test_webhook(self):
        webhook_list = service.api.get_webhooks(project_id)[0]
        webhook = Webhook.from_dict(webhook_list[0])
        assert type(webhook) == Webhook
