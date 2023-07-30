from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core import mail
from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin
from backend.models import User


class UserListViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:user-list")

    def test_allowed_status(self):
        for user in [self.management1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden_status(self):
        for user in [self.user1, self.pentester1, self.pentester2, self.read_only1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class UserDeleteViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.test_user = self.create_user("test_user123", "changeme1234")
        self.url = self.get_url("backend:user-detail", pk=self.test_user.pk)

    def test_delete_not_allowed(self):
        self.client.force_login(self.management1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)


class UserUpdateViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.test_user = self.create_user("test_user123", "changeme1234")
        self.url = self.get_url("backend:user-detail", pk=self.test_user.pk)

    def test_update_not_allowed(self):
        self.client.force_login(self.management1)
        data = {"username": "admin"}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 403)

    def test_group_changed(self):
        self.client.force_login(self.superuser)
        data = {"groups": [Group.objects.get(name="Advisory Management").pk]}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(User.objects.get(username="test_user123").groups.values_list("pk", flat=True)),
                         data["groups"])


class UserCreateViewSetTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:user-list")
        self.data = {"first_name": "Test", "last_name": "Last", "username": "tlast", "email": "test@eexample.ccom",
                     "groups": [Group.objects.get(name="Pentester").pk]}

    def test_create_forbidden(self):
        self.client.force_login(self.management1)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(username="tlast").count(), 1)
        user = User.objects.get(username="tlast")
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.has_usable_password(), False)
        self.assertEqual(len(mail.outbox), 1)


class AccountActivationView(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.activation_user = self.create_user("testactivation", None, is_active=False)
        self.uid = force_str(urlsafe_base64_encode(force_bytes(self.activation_user.pk)))
        self.token = default_token_generator.make_token(self.activation_user)
        self.url = self.get_url("backend:user-activation")
        self.data = {"uid": self.uid, "token": self.token, "new_password": "mysupersecurepassword1234!"}

    def test_activation(self):
        self.assertEqual(self.activation_user.has_usable_password(), False)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 204)
        user = User.objects.get(username="testactivation")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.has_usable_password(), True)

        # test login
        login_url = self.get_url("backend:login")
        data = {"username": "testactivation", "password": "mysupersecurepassword1234!"}
        response = self.client.post(login_url, data)
        self.assertIn("csrf_token", response.json())
        self.assertEqual(response.json().get("user", {}).get("username"), "testactivation")

    def test_invalid_token(self):
        # TODO: fixme
        headers = {"X-CSRFToken": "random"}
        response = self.client.post(self.url, self.data, headers=headers)
        # self.assertEqual(response.status_code, 400)
