import configparser
import json
import os
from pathlib import Path

from annofabapi.dataclass.annotation import FullAnnotation, SimpleAnnotation
from annofabapi.dataclass.annotation_specs import AnnotationSpecs
from annofabapi.dataclass.input import InputData
from annofabapi.dataclass.inspection import Inspection
from annofabapi.dataclass.job import JobInfo
from annofabapi.dataclass.my import MyAccount, MyOrganization
from annofabapi.dataclass.organization import Organization, OrganizationActivity
from annofabapi.dataclass.organization_member import OrganizationMember
from annofabapi.dataclass.project import Project
from annofabapi.dataclass.project_member import ProjectMember
from annofabapi.dataclass.statistics import (InspectionStatistics, LabelStatistics, ProjectAccountStatistics,
                                             ProjectTaskStatisticsHistory, TaskPhaseStatistics, WorktimeStatistics)
from annofabapi.dataclass.supplementary import SupplementaryData
from annofabapi.dataclass.task import Task, TaskHistory
from annofabapi.dataclass.webhook import Webhook
from annofabapi.dataclass.instruction import Instruction, InstructionHistory, InstructionImage


# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")
inifile = configparser.ConfigParser()
inifile.read('./pytest.ini', 'UTF-8')

test_dir = Path('./tests/data/dataclass')


class TestAnnotation:
    def test_simple_annotation(self):
        simple_annotaion_json = test_dir / "simple-annotation.json"
        with simple_annotaion_json.open(encoding="utf-8") as f:
            dict_full_annotation = json.load(f)
        simple_annotion = SimpleAnnotation.from_dict(dict_full_annotation)
        assert type(simple_annotion) == SimpleAnnotation

    def test_full_annotation(self):
        full_annotaion_json = test_dir / "full-annotation.json"
        with full_annotaion_json.open(encoding="utf-8") as f:
            dict_full_annotation = json.load(f)
        full_annotion = FullAnnotation.from_dict(dict_full_annotation)
        assert type(full_annotion) == FullAnnotation


class TestAnnotationSpecs:
    def test_annotation_specs(self):
        annotaion_specs_json = test_dir / "annotation-specs.json"
        with annotaion_specs_json.open(encoding="utf-8") as f:
            dict_annotation_specs = json.load(f)
        annotation_specs = AnnotationSpecs.from_dict(dict_annotation_specs)
        assert type(annotation_specs) == AnnotationSpecs


class TestInput:
    def test_input_data(self):
        input_data_json = test_dir / "input-data.json"
        with input_data_json.open(encoding="utf-8") as f:
            dict_input_data = json.load(f)
        input_data = InputData.from_dict(dict_input_data)
        assert type(input_data) == InputData


class TestInspection:
    def test_inspection(self):
        inspection_json = test_dir / "inspection.json"
        with inspection_json.open(encoding="utf-8") as f:
            dict_inspection = json.load(f)
        inspection = Inspection.from_dict(dict_inspection)
        assert type(inspection) == Inspection

class TestInstruction:
    def test_instruction(self):
        json_path = test_dir / "instruction.json"
        with json_path.open(encoding="utf-8") as f:
            dict_data = json.load(f)
        data = Instruction.from_dict(dict_data)
        assert type(data) == Instruction

    def test_instruction_history(self):
        json_path = test_dir / "instruction-history.json"
        with json_path.open(encoding="utf-8") as f:
            dict_data = json.load(f)
        data = InstructionHistory.from_dict(dict_data)
        assert type(data) == InstructionHistory

    def test_instruction_image(self):
        json_path = test_dir / "instruction-image.json"
        with json_path.open(encoding="utf-8") as f:
            dict_data = json.load(f)
        data = InstructionImage.from_dict(dict_data)
        assert type(data) == InstructionImage

class TestJob:
    def test_job(self):
        job_json = test_dir / "job.json"
        with job_json.open(encoding="utf-8") as f:
            dict_job = json.load(f)
        job = JobInfo.from_dict(dict_job)
        assert type(job) == JobInfo


class TestMy:
    def test_my_organization(self):
        json_path = test_dir / "my-organization.json"
        with json_path.open(encoding="utf-8") as f:
            dict_data = json.load(f)
        data = MyOrganization.from_dict(dict_data)
        assert type(data) == MyOrganization

    def test_my_account(self):
        json_path = test_dir / "my-account.json"
        with json_path.open(encoding="utf-8") as f:
            dict_data = json.load(f)
        data = MyAccount.from_dict(dict_data)
        assert type(data) == MyAccount


class TestOrganization:
    def test_organization(self):
        organization_activity_json = test_dir / "organization.json"
        with organization_activity_json.open(encoding="utf-8") as f:
            dict_organization = json.load(f)
        organization = Organization.from_dict(dict_organization)
        assert type(organization) == Organization

    def test_organization_activity(self):
        organization_activity_json = test_dir / "organization-activity.json"
        with organization_activity_json.open(encoding="utf-8") as f:
            dict_organization_activity = json.load(f)
        organization_activity = OrganizationActivity.from_dict(dict_organization_activity)
        assert type(organization_activity) == OrganizationActivity


class TestOrganizationMember:
    def test_organization_member(self):
        organization_member_json = test_dir / "organization-member.json"
        with organization_member_json.open(encoding="utf-8") as f:
            dict_organization_member = json.load(f)
        organization_member = OrganizationMember.from_dict(dict_organization_member)
        assert type(organization_member) == OrganizationMember


class TestProject:
    def test_project(self):
        project_json = test_dir / "project.json"
        with project_json.open(encoding="utf-8") as f:
            dict_project = json.load(f)
        project = Project.from_dict(dict_project)
        assert type(project) == Project


class TestProjectMember:
    def test_project_member(self):
        project_member_json = test_dir / "project-member.json"
        with project_member_json.open(encoding="utf-8") as f:
            dict_project_member = json.load(f)
        project_member = ProjectMember.from_dict(dict_project_member)
        assert type(project_member) == ProjectMember


class TestStatistics:
    def test_statistics_get_task_statistics(self):
        statistics_json = test_dir / "task-statistics.json"
        with statistics_json.open(encoding="utf-8") as f:
            dict_stat = json.load(f)
        stat = ProjectTaskStatisticsHistory.from_dict(dict_stat)
        assert type(stat) == ProjectTaskStatisticsHistory

    def test_statistics_get_account_statistics(self):
        statistics_json = test_dir / "account-statistics.json"
        with statistics_json.open(encoding="utf-8") as f:
            dict_stat = json.load(f)
        stat = ProjectAccountStatistics.from_dict(dict_stat)
        assert type(stat) == ProjectAccountStatistics

    def test_statistics_get_inspection_statistics(self):
        statistics_json = test_dir / "inspection-statistics.json"
        with statistics_json.open(encoding="utf-8") as f:
            dict_stat = json.load(f)
        stat = InspectionStatistics.from_dict(dict_stat)
        assert type(stat) == InspectionStatistics

    def test_statistics_get_task_phase_statistics(self):
        statistics_json = test_dir / "task-phase-statistics.json"
        with statistics_json.open(encoding="utf-8") as f:
            dict_stat = json.load(f)
        stat = TaskPhaseStatistics.from_dict(dict_stat)
        assert type(stat) == TaskPhaseStatistics

    def test_statistics_get_label_statistics(self):
        statistics_json = test_dir / "label-statistics.json"
        with statistics_json.open(encoding="utf-8") as f:
            dict_stat = json.load(f)
        stat = LabelStatistics.from_dict(dict_stat)
        assert type(stat) == LabelStatistics

    def test_statistics_get_worktime_statistics(self):
        statistics_json = test_dir / "worktime-statistics.json"
        with statistics_json.open(encoding="utf-8") as f:
            dict_stat = json.load(f)
        stat = WorktimeStatistics.from_dict(dict_stat)
        assert type(stat) == WorktimeStatistics


class TestSupplementary:
    def test_supplementary(self):
        supplementary_data_json = test_dir / "supplementary-data.json"
        with supplementary_data_json.open(encoding="utf-8") as f:
            dict_supplementary_data = json.load(f)
        supplementary_data = SupplementaryData.from_dict(dict_supplementary_data)
        assert type(supplementary_data) == SupplementaryData


class TestTask:
    def test_task(self):
        task_json = test_dir / "task.json"
        with task_json.open(encoding="utf-8") as f:
            dict_task = json.load(f)
        task = Task.from_dict(dict_task)
        assert type(task) == Task

    def test_task_history(self):
        task_history_json = test_dir / "task-history.json"
        with task_history_json.open(encoding="utf-8") as f:
            dict_task_history = json.load(f)
        task_history = TaskHistory.from_dict(dict_task_history)
        assert type(task_history) == TaskHistory


class TestWebhook:
    def test_webhook(self):
        webhook_json = test_dir / "webhook.json"
        with webhook_json.open(encoding="utf-8") as f:
            dict_webhook = json.load(f)
        webhook = Webhook.from_dict(dict_webhook)
        assert type(webhook) == Webhook
