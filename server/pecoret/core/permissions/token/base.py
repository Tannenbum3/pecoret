from rest_framework.permissions import SAFE_METHODS
from backend.models.api_token import APIToken, AccessChoices
from pecoret.core.permissions.base import BasePermission


class BaseAPITokenPermission(BasePermission):
    def __init__(self, scope):
        super().__init__()
        self.scope = scope

    def __call__(self):
        # required because `permission_class` requires a class and not an instance
        return self

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)

    def has_object_permission(self, request, view, obj):
        if isinstance(request.auth, APIToken):
            if not self.scope:
                return False
            scope_attr = getattr(request.auth, self.scope)
            if not scope_attr:
                return False
            if scope_attr is AccessChoices.NO_ACCESS:
                return False
            if request.method in SAFE_METHODS:
                # in safe methods, we usually accept all access choices
                if scope_attr == AccessChoices.READ:
                    return True
                if scope_attr == AccessChoices.READ_WRITE:
                    return True
            if scope_attr == AccessChoices.READ_WRITE:
                return True
        return False


class TokenPermissionMixin:

    def has_token_permission(self, request, view, obj):
        scope = getattr(view, "api_scope")
        if not scope:
            return False
        if isinstance(request.auth, APIToken):
            if not scope:
                return False
            scope_attr = getattr(request.auth, scope)
            if not scope_attr:
                return False
            if scope_attr is AccessChoices.NO_ACCESS:
                return False
            if request.method in SAFE_METHODS:
                # in safe methods, we usually accept all access choices
                if scope_attr == AccessChoices.READ:
                    return True
                if scope_attr == AccessChoices.READ_WRITE:
                    return True
            if scope_attr == AccessChoices.READ_WRITE:
                return True
        return False
