from rest_framework.test import APITestCase
from pecoret.core.test import AdvisoryTestCaseMixin
from backend.models.report_templates import ReportTemplate


class AdvisoryExportViewTestCase(APITestCase, AdvisoryTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report_template = ReportTemplate.objects.get(name="default_template")
        self.url = self.get_url("backend:advisory-export-pdf", pk=self.advisory1.pk)

    def test_allowed(self):
        users = [
            self.pentester1,
            self.vendor1,
            self.advisory_manager1,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.management1,
            self.management2,
            self.user1,
            self.vendor2,
            self.read_only1,
            self.pentester2,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_management_draft(self):
        self.advisory1.is_draft = True
        self.advisory1.save()
        self.client.force_login(self.advisory_manager1)
        self.basic_status_code_check(self.url, self.client.get, 403)


class AdvisoryMarkdownExportView(APITestCase, AdvisoryTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url(
            "backend:advisory-export-markdown", pk=self.advisory1.pk
        )

    def test_allowed(self):
        users = [
            self.vendor1,
            self.pentester1,
            self.advisory_manager1,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.management2,
            self.management1,
            self.user1,
            self.vendor2,
            self.read_only1,
            self.pentester2,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertNotEqual(response.headers.get("Content-Disposition"), None)
        self.assertIn(self.advisory1.pk, response.headers["Content-Disposition"])

    def test_advisory_management1_draft(self):
        # test draft is not downloadable
        self.advisory1.is_draft = True
        self.advisory1.save()
        self.client.force_login(self.advisory_manager1)
        self.basic_status_code_check(self.url, self.client.get, 403)
