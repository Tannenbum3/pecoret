from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from ddf import G
from backend.models import User, Project, Membership, ReportTemplate
from backend.models import WebApplication
from backend.models.membership import Roles


class PeCoReTTestCaseMixin(object):
    def init_mixin(self):
        self.pentester1 = self.create_user("pentester1", "changeme", group="Pentester")
        self.project1 = self.create_project()
        self.assign_project_role(self.pentester1, Roles.CONTRIBUTOR, self.project1)
        # create second project
        self.pentester2 = self.create_user("pentester2", "changeme", group="Pentester")
        self.project2 = self.create_project()
        self.assign_project_role(self.pentester2, Roles.CONTRIBUTOR, self.project2)
        # read only
        self.read_only1 = self.create_user("readonly1", "changeme", group="Pentester")
        self.assign_project_role(self.read_only1, Roles.READ_ONLY, self.project1)
        #management
        self.management1 = self.create_user("management1", "changeme", group="Management")
        self.assign_project_role(self.management1, Roles.OWNER, self.project1)
        self.management2 = self.create_user("management2", "changeme", group="Management")
        self.assign_project_role(self.management2, Roles.OWNER, self.project2)
        # non-grouped user
        self.user1 = self.create_user("user1", "changeme")

        # superuser
        self.superuser = self.create_user("superuser", "changeme", is_superuser=True, is_staff=True)

        self.advisory_manager1 = self.create_user("advisory1", "changeme", group="Advisory Management")

        # assets
        self.asset1 = self.create_instance(WebApplication, project=self.project1)
        self.asset2 = self.create_instance(WebApplication, project=self.project2)

    def create_user(self, username, password, is_staff=False, group=None, **kwargs):
        email = "%s@example.com" % username
        user = User.objects.create_user(username, password=password, is_staff=is_staff, email=email, **kwargs)
        if group:
            user.groups.add(Group.objects.get(name=group))
            user.save()
        return user

    def add_user_to_group(self, user, group_name):
        user.groups.add(Group.objects.get(name=group_name))
        user.save()

    def create_project(self):
        return G(Project, company__report_template=ReportTemplate.objects.get(name="default_template"))

    def assign_project_role(self, user, role, project):
        return G(Membership, user=user, role=role, project=project)

    def get_url(self, endpoint, **kwargs):
        return reverse_lazy(endpoint, kwargs=kwargs)

    def create_instance(self, obj_class, **kwargs):
        return G(obj_class, **kwargs)

    def basic_permission_checks(self, url, user_status_map, req_func, data=None, debug=False):
        for u in user_status_map:
            user = u[0]
            status_code = u[1]
            self.client.force_login(user)
            if data is None:
                response = req_func(url)
            else:
                response = req_func(url, data)
            if debug:
                print(response.json())
            self.assertEqual(response.status_code, status_code, msg="Usermap: %s" % str(u))

    def basic_status_code_check(self, url, req_func, status_code, data=None, debug=False):
        if data is None:
            response = req_func(url)
        else:
            response = req_func(url, data, format="json")
        if debug:
            print(response.json())
        self.assertEqual(response.status_code, status_code)
        return response
