from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin


class AdvisoryInboxListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("advisories:inbox-list")

    def test_allowed(self):
        self.client.force_login(self.advisory_manager1)
        response = self.basic_status_code_check(self.url, self.client.get, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["pk"], self.advisory1.pk)

    def test_forbidden(self):
        users = [
            self.pentester1,
            self.pentester2,
            self.user1,
            self.read_only1,
            self.management1,
            self.management2,
            self.vendor1,
            self.vendor2,
            self.read_only_vendor,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)
