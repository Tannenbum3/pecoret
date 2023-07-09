from rest_framework.test import APITestCase
from backend.models import Finding, Proof
from pecoret.core.test import PeCoReTTestCaseMixin


class ProofListViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            project=self.project1,
            component=self.asset1,
            user=self.pentester1,
            vulnerability__project=self.project1,
        )
        self.finding2 = self.create_finding(
            project=self.project2,
            component=self.asset2,
            user=self.pentester2,
            vulnerability__project=self.project2,
        )
        self.proof1 = self.create_instance(Proof, finding=self.finding1, title="proof1")
        self.proof2 = self.create_instance(Proof, finding=self.finding2, title="proof2")
        self.url = self.get_url(
            "backend:findings:proof-list",
            project=self.project1.pk,
            finding=self.finding1.pk,
        )

    def test_allowed_status(self):
        for user in [self.pentester1, self.management1, self.read_only1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden_status(self):
        for user in [self.pentester2, self.user1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)

    def test_idor(self):
        self.client.force_login(self.pentester1)
        url = self.get_url(
            "backend:findings:proof-list",
            project=self.project2.pk,
            finding=self.finding1.pk,
        )
        self.basic_status_code_check(url, self.client.get, 403)
        url = self.get_url(
            "backend:findings:proof-list",
            project=self.project1.pk,
            finding=self.finding2.pk,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class ProofCreateViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            project=self.project1,
            component=self.asset1,
            user=self.pentester1,
            vulnerability__project=self.project1,
        )
        self.finding2 = self.create_finding(
            project=self.project2,
            component=self.asset2,
            user=self.pentester2,
            vulnerability__project=self.project2,
        )
        self.url = self.get_url(
            "backend:findings:proof-list",
            project=self.project1.pk,
            finding=self.finding1.pk,
        )
        self.data = {
            "text": "proof1",
            "order": 1,
            "title": "proof1",
        }

    def test_allowed_stats_code(self):
        for user in [self.pentester1, self.management1]:
            data = self.data
            data["title"] = "proof-%s" % user.username
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=data)

    def test_forbidden_status_code(self):
        for user in [self.pentester2, self.read_only1, self.user1]:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )


class ProofDestroyViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.finding1 = self.create_finding(
            project=self.project1,
            component=self.asset1,
            user=self.pentester1,
            vulnerability__project=self.project1,
        )
        self.finding2 = self.create_finding(
            project=self.project2,
            component=self.asset2,
            user=self.pentester2,
            vulnerability__project=self.project2,
        )
        self.proof1 = self.create_instance(Proof, finding=self.finding1, title="proof1")
        self.proof2 = self.create_instance(Proof, finding=self.finding2, title="proof2")
        self.url = self.get_url(
            "backend:findings:proof-detail",
            project=self.project1.pk,
            pk=self.proof1.pk,
            finding=self.finding1.pk,
        )

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204, data={})

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204, data={})

    def test_forbidden(self):
        users = [self.management2, self.read_only1, self.user1, self.pentester2]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403, data={})
