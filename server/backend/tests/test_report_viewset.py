from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.reports.report import ReportVariant, Report
from backend.models import ReportTemplate
from backend.models.report_templates import ReportTemplateStatus


class ReportListViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:report-list", project=self.project1.pk)

    def test_permissions(self):
        user_status_map = [
            (self.pentester1, 200),
            (self.management1, 200),
            (self.pentester2, 403),
            (self.read_only1, 200),
            (self.user1, 403),
        ]
        self.basic_permission_checks(self.url, user_status_map, self.client.get)


class ReportCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:report-list", project=self.project1.pk)
        self.report_template = self.create_instance(
            ReportTemplate, status=ReportTemplateStatus.ACTIVE
        )
        self.data = {
            "name": "Test",
            "title": "Test Report",
            "project": self.project1.pk,
            "author": self.pentester1.pk,
            "variant": ReportVariant.VULNERABILITY_CSV_REPORT.label,
            "language": "English",
            "recommendation": "",
            "evaluation": "",
            "template": self.report_template.pk,
        }

    def test_inactive_report_template(self):
        new_template = self.create_instance(
            ReportTemplate, status=ReportTemplateStatus.DRAFT
        )
        self.data["template"] = new_template.pk
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)

    def test_permissions(self):
        user_status_map = [
            (self.pentester1, 201),
            (self.management1, 201),
            (self.pentester2, 403),
            (self.read_only1, 403),
            (self.user1, 403),
        ]
        self.basic_permission_checks(
            self.url, user_status_map, self.client.post, data=self.data
        )

    def test_foreign_author(self):
        data = self.data
        data["author"] = self.pentester2.pk
        self.client.force_login(self.pentester1)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)


class ReportUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(
            Report,
            project=self.project1,
            variant=ReportVariant.PENTEST_PDF_REPORT.value,
        )
        self.url = self.get_url(
            "backend:report-detail", project=self.project1.pk, pk=self.report1.pk
        )
        self.data = {"name": "test2"}

    def test_basic_permissions(self):
        user_status_map = [
            (self.pentester1, 200),
            (self.management1, 200),
            (self.pentester2, 403),
            (self.read_only1, 403),
            (self.user1, 403),
        ]
        self.basic_permission_checks(
            self.url, user_status_map, self.client.patch, data=self.data
        )

    def test_change_report_variant(self):
        """ensure that report variant cannot be changed after report was created"""
        variant = ReportVariant.VULNERABILITY_CSV_REPORT.label
        self.data["variant"] = variant
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.patch, 400, data=self.data)


class ReportDeleteViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(Report, project=self.project1)
        self.url = self.get_url(
            "backend:report-detail", project=self.project1.pk, pk=self.report1.pk
        )

    def test_permissions(self):
        user_status_map = [
            (self.pentester1, 204),
            (self.pentester2, 403),
            (self.read_only1, 403),
            (self.read_only1, 403),
        ]
        self.basic_permission_checks(self.url, user_status_map, self.client.delete)

    def test_management(self):
        # would fail if instance is already deleted by pentester1
        user_status_map = [(self.management1, 204)]
        self.basic_permission_checks(self.url, user_status_map, self.client.delete)


class ReportDetailViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    # TODO: implement
    pass
