from rest_framework.permissions import SAFE_METHODS
from backend.models import Project, ProjectToken
from backend.models.membership import Membership
from .base import BasePermission


class ProjectPermission(BasePermission):
    def __init__(self, read_write_roles=[], read_only_roles=[]):
        super().__init__()
        self.read_only_roles = read_only_roles
        self.read_write_roles = read_write_roles

    def __call__(self):
        # required because `permission_class` requires a class and not an instance
        return self

    def _check_project_membership(self, user, project):
        return Membership.objects.for_project(project).for_user(user)

    @staticmethod
    def project_from_request(request):
        """extract the project from the request path

        Args:
            request (_type_): _description_

        Returns:
            Project: the project that was specified in the request path
        """
        project_id = None
        try:
            if "project" in request.resolver_match.kwargs:
                project_id = int(request.resolver_match.kwargs["project"])
            if (
                    request.resolver_match.url_name.startswith("project-")
                    and "pk" in request.resolver_match.kwargs
            ):
                project_id = int(request.resolver_match.kwargs["pk"])
        except ValueError:
            return None
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return None
        return project

    def has_permission(self, request, view):
        """ensure that we always check object permissions"""
        return self.has_object_permission(request, view, None)

    def has_object_permission(self, request, view, obj):
        project = self.project_from_request(request)
        if not project:
            return False
        if isinstance(request.auth, ProjectToken):
            # if authentication was done using a project token, we want to only allow access to this
            # specific project
            token_project = request.auth.project
            if token_project.pk != project.pk:
                return False
        if not request.user.is_authenticated:
            return False
        membership = self._check_project_membership(request.user, project)
        if not membership.exists():
            return False
        if not membership.get().active:
            membership.delete()
            return False
        if request.method in SAFE_METHODS:
            # allow read_write roles to read
            both_values = self.read_write_roles + self.read_only_roles
            allowed = membership.for_roles(both_values).exists()
            if allowed:
                request.project = project
            return allowed
        # if method is not safe, than only members for specified roles are allowed to continue
        allowed = membership.for_roles(self.read_write_roles).exists()
        if allowed:
            request.project = project
        return allowed
