from rest_framework.test import APITestCase
from backend.models.finding_timeline import FindingTimeline
from pecoret.core.test import PeCoReTTestCaseMixin


class FindingTimelineListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.timeline1 = self.create_instance(
            FindingTimeline,
            finding__user=self.pentester1,
            finding__vulnerability__project=self.project1,
            finding__web_application=self.asset1,
            finding__project=self.project1,
        )
        self.timeline2 = self.create_instance(
            FindingTimeline,
            finding__user=self.pentester2,
            finding__vulnerability__project=self.project2,
            finding__web_application=self.asset2,
            finding__project=self.project2,
        )
        self.url = self.get_url(
            "backend:findings:timeline-list",
            project=self.project1.pk,
            finding=self.timeline1.finding.pk,
        )

    def test_allowed(self):
        users = [self.read_only1, self.pentester1, self.management1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [self.management2, self.advisory_manager1, self.pentester2, self.user1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_broken_access(self):
        self.url = self.get_url(
            "backend:findings:timeline-list",
            project=self.project1.pk,
            finding=self.timeline2.finding.pk,
        )
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.get, 403)
