from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.advisory_proof import AdvisoryProof


class AdvisoryProofCreateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.data = {"title": "first_proof", "text": "lorem ipsum"}
        self.url = self.get_url("backend:advisories:proof-list", advisory=self.advisory1.pk)

    def test_allowed(self):
        users = [
            self.advisory_manager1, self.pentester1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.pentester2, self.management2, self.management1, self.vendor2, self.vendor1,
            self.user1, self.read_only1, self.read_only_vendor
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_draft_forbidden(self):
        self.url = self.get_url("backend:advisories:proof-list", advisory=self.advisory2.pk)
        users = [
            self.pentester1, self.management1, self.management2,
            self.advisory_manager1, self.vendor1, self.vendor2, self.read_only1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)


class AdvisoryProofListView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.proof1 = self.create_instance(AdvisoryProof, advisory=self.advisory1)
        self.proof2 = self.create_instance(AdvisoryProof, advisory=self.advisory2)
        self.url = self.get_url("backend:advisories:proof-list", advisory=self.advisory1.pk)

    def test_allowed(self):
        users = [
            self.pentester1, self.vendor1, self.advisory_manager1, self.read_only_vendor
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.pentester2, self.vendor2, self.read_only1, self.user1, self.management2,
            self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_draft_forbidden(self):
        self.url = self.get_url("backend:advisories:proof-list", advisory=self.advisory2.pk)
        users = [
            self.advisory_manager1, self.user1, self.management1, self.management2,
            self.read_only1, self.pentester1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class AdvisoryProofUpdateView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        pass


class AdvisoryProofDeleteView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        pass
