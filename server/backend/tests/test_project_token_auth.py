from django.utils import timezone
from rest_framework.test import APITestCase
from backend.models import ProjectToken
from pecoret.core.test import PeCoReTTestCaseMixin


class ProjectTokenAuth(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        valid_date = timezone.now() + timezone.timedelta(days=3)
        self.token1 = self.create_instance(
            ProjectToken,
            project=self.project1,
            user=self.pentester1,
            date_expire=valid_date,
        )
        self.token2 = self.create_instance(
            ProjectToken, project=self.project1, user=self.pentester1
        )
        self.client.defaults["HTTP_AUTHORIZATION"] = "ProjectToken " + str(
            self.token1.key
        )
        self.url = self.get_url("backend:host-list", project=self.project1.pk)

    def test_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_foreign_project_asset_denied(self):
        self.url = self.get_url("backend:host-list", project=self.project2.pk)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_token_expired(self):
        self.token1.date_expire = self.token1.date_expire - timezone.timedelta(days=5)
        self.token1.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class ProjectTokenCreate(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url("backend:api-token-list", project=self.project1.pk)
        valid_date = timezone.now() + timezone.timedelta(days=3)
        self.data = {"name": "test", "date_expire": valid_date}

    def test_allowed(self):
        users = [
            self.pentester1, self.management1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden(self):
        users = [
            self.pentester2, self.management2, self.read_only1, self.advisory_manager1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)
