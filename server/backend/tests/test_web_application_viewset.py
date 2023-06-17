from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models.assets.web_application import WebApplication
from backend.models.assets.base import Environment, AssetAccessibility


class WebApplicationListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.web_application1 = self.create_instance(WebApplication, project=self.project1)
        self.web_application2 = self.create_instance(WebApplication, project=self.project2)
        self.url = self.get_url("backend:web-application-list", project=self.project1.pk)

    def test_status_allowed(self):
        users = [
            self.pentester1, self.management1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        users = [
            self.pentester2, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class WebApplicationCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:web-application-list", project=self.project1.pk)
        self.data = {"name": "testcreateview", "base_url": "http://webappcreate.com", "version": "1.0",
                     "environment": Environment.UNKNOWN.label, "accessible": AssetAccessibility.UNKNOWN.label}

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_status_forbidden(self):
        users = [
            self.pentester2, self.management2, self.user1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)


class WebApplicationUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.web_application1 = self.create_instance(WebApplication, project=self.project1)
        self.web_application2 = self.create_instance(WebApplication, project=self.project2)
        self.url = self.get_url("backend:web-application-detail", project=self.project1.pk, pk=self.web_application1.pk)
        self.data = {"version": "2.0"}

    def test_allowed(self):
        users = [
            self.management1, self.pentester1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_forbidden(self):
        users = [
            self.management2, self.pentester2, self.read_only1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_broken_access(self):
        url = self.get_url("backend:web-application-detail", project=self.project2.pk, pk=self.web_application1.pk)
        self.client.force_login(self.pentester2)
        response = self.client.patch(url, self.data, format="json")
        self.assertEqual(response.status_code, 404)

        url = self.get_url("backend:web-application-detail", project=self.project1.pk, pk=self.web_application2.pk)
        self.client.force_login(self.pentester2)
        response = self.client.patch(url, self.data, format="json")
        self.assertEqual(response.status_code, 403)


class WebApplicationDeleteViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.web_application1 = self.create_instance(WebApplication, project=self.project1)
        self.url = self.get_url("backend:web-application-detail", project=self.project1.pk, pk=self.web_application1.pk)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [
            self.read_only1, self.management2, self.user1, self.pentester2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)
