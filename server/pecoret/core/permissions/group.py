from rest_framework.permissions import SAFE_METHODS
from backend.models import ProjectToken
from .base import BasePermission


class Groups(object):
    GROUP_PENTESTER = "Pentester"
    GROUP_MANAGEMENT = "Management"
    ADVISORY_MANAGEMENT = "Advisory Management"
    VENDOR = "Vendor"


class GroupPermission(BasePermission):
    def __init__(self, read_write_groups=[], read_only_groups=[]):
        super().__init__()
        self.read_write_groups = read_write_groups
        self.read_only_groups = read_only_groups

    def __call__(self):
        # required because `permission_class` requires a class and not an instance
        return self

    def _check_read_write(self, request, _view):
        if request.user.groups.filter(name__in=self.read_write_groups):
            return True
        return False

    def _check_read_only(self, request, _view):
        read_both = self.read_only_groups + self.read_write_groups
        if request.user.groups.filter(name__in=read_both):
            return True
        return False

    def has_permission(self, request, view):
        # do not allow project tokens on global endpoints that are not safe
        if isinstance(request.auth, ProjectToken) and request.method not in SAFE_METHODS:
            return False
        if request.user.is_superuser:
            return True
        if request.method not in SAFE_METHODS:
            return self._check_read_write(request, view)
        return self._check_read_only(request, view)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
