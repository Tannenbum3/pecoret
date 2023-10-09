from rest_framework.test import APITestCase
from django_q.tasks import async_task, result
from backend import models
from backend.tasks.finding_export import export_advisory, export_advisory_markdown
from pecoret.core.test import PeCoReTTestCaseMixin


class ExportAdvisoryTask(APITestCase, PeCoReTTestCaseMixin):
    """test if advisory export is successful"""

    def setUp(self) -> None:
        self.init_mixin()
        self.report_template = models.ReportTemplate.objects.get(
            name="default_template"
        )
        self.advisory = self.create_instance(models.Advisory, is_draft=False, user=self.pentester1)

    def test_export_advisory(self):
        """test pdf export of advisory
        """
        task_id = async_task(
            export_advisory, self.advisory, self.report_template, sync=True
        )
        task_result = result(task_id, 200)
        self.assertIsNotNone(task_result)

    def test_markdown_export(self):
        """test if markdown export of advisory works
        """
        task_id = async_task(
            export_advisory_markdown, self.advisory, self.report_template, sync=True
        )
        task_result = result(task_id, 200)
        self.assertIsNotNone(task_result)
