from django.utils import timezone
from rest_framework.test import APITestCase
from backend.models import ProjectToken
from pecoret.core.test import PeCoReTTestCaseMixin


class TokenAuthCheckView(APITestCase, PeCoReTTestCaseMixin):
    """check validity and project details for ProjectToken Auth
    """

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

    def test_check_view(self):
        """check if valid token returns current project details
        """
        url = self.get_url("backend:project-token-check")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.project1.pk)

    def test_check_expiry(self):
        """test if expired token results in 403 Forbidden
        """
        self.client.defaults["HTTP_AUTHORIZATION"] = "ProjectToken " + str(
            self.token2.key
        )
        url = self.get_url("backend:project-token-check")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
