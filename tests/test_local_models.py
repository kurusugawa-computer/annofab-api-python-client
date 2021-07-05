import warnings

from annofabapi.models import JobType


class TestDeprecation:
    def test_job_deprecated(self):
        with warnings.catch_warnings(record=True) as found_warnings:
            print(JobType.GEN_ANNOTATION)
            assert len(found_warnings) == 1
            single_warning = found_warnings[0]
            assert str(single_warning.message) == (
                "deprecated: 'annofabapi.models.JobType'は2021-09-01以降に廃止します。"
                "替わりに'annofabapi.models.ProjectJobType'を使用してください。"
            )
