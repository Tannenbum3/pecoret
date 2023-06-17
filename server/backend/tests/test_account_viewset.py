from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin


class AccountListViewSet(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:account-list", project=self.project1.pk)

    def test_allowed_status(self):
        for user in [self.read_only1, self.pentester1, self.management1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden_status(self):
        for user in [self.pentester2, self.user1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class AccountCreateViewSet(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("backend:account-list", project=self.project1.pk)
        self.data = {
            "role": "Admin", "username": "TestAdmin", "asset": {"pk": self.asset1.pk, "type": self.asset1.asset_type},
            "accessible": False, "compromised": False, "password": ""
        }

    def test_allowed_status(self):
        for user in [self.pentester1, self.management1]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_forbidden_status(self):
        for user in [self.read_only1, self.user1, self.pentester2]:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_foreign_asset(self):
        data = self.data
        data["asset"]["pk"] = self.asset2.pk
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)


class AccountUpdateViewSet(APITestCase, PeCoReTTestCaseMixin):
    # TODO: implement
    pass


class AccountDeleteViewSet(APITestCase, PeCoReTTestCaseMixin):
    # TODO: implement
    pass
