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
    input_data_id: str

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







