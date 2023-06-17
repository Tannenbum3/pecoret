from rest_framework.test import APITestCase
from backend.models import AdvisoryComment
from pecoret.core.test import AdvisoryTestCaseMixin


class AdvisoryCommentCreateView(APITestCase, AdvisoryTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.data = {"comment": "test"}
        self.url = self.get_url(
            "backend:advisories:comment-list", advisory=self.advisory1.pk
        )

    def test_allowed(self):
        users = [self.advisory_manager1, self.pentester1, self.vendor1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 201, data=self.data
            )

    def test_forbidden(self):
        users = [
            self.pentester2,
            self.management1,
            self.management2,
            self.vendor2,
            self.read_only_vendor,
            self.read_only1,
            self.user1,
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(
                self.url, self.client.post, 403, data=self.data
            )


class AdvisoryCommentDeleteView(APITestCase, AdvisoryTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.comment1 = self.create_instance(
            AdvisoryComment, advisory=self.advisory1, user=self.pentester1
        )
        self.url = self.get_url(
            "backend:advisories:comment-detail",
            advisory=self.advisory1.pk,
            pk=self.comment1.pk,
        )

    def test_allowed(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [
            self.pentester2,
            self.vendor2,
            self.management1,
            self.management2,
            self.user1,
            self.read_only1,
            self.read_only_vendor
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)

    def test_not_found(self):
        users = [self.advisory_manager1, self.vendor1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 404)


class AdvisoryCommentUpdateView(APITestCase, AdvisoryTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.comment1 = self.create_instance(
            AdvisoryComment, advisory=self.advisory1, user=self.pentester1
        )
        self.url = self.get_url(
            "backend:advisories:comment-detail",
            advisory=self.advisory1.pk,
            pk=self.comment1.pk,
        )
        self.data = {"comment": "new123"}

    def test_allowed(self):
        self.client.force_login(self.pentester1)
        response = self.basic_status_code_check(
            self.url, self.client.patch, 200, data=self.data
        )
        self.assertEqual(response.json()["comment"], self.data["comment"])

    def test_forbidden(self):
        users = [
            self.pentester2,
            self.vendor2,
            self.management1,
            self.management2,
            self.user1,
            self.read_only1,
            self.read_only_vendor
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403)

    def test_not_found(self):
        users = [self.advisory_manager1, self.vendor1]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 404)
