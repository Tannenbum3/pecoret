from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django_q.tasks import async_task
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from backend.models import User
from backend import permissions
from backend.serializers import user as serializers
from backend.throttle import AuthFlowThrottle
from backend.tasks import mail
from pecoret.core.viewsets import PeCoReTModelViewSet, PeCoReTReadOnlyModelViewSet


class UserViewSet(PeCoReTModelViewSet):
    queryset = User.objects.all()
    filterset_class = None
    search_fields = ["username", "first_name", "last_name"]
    api_scope = None
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[], read_only_groups=[permissions.Groups.GROUP_MANAGEMENT]
        )
    ]

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserCreateSerializer
        if self.action in ["update", "partial_update"]:
            return serializers.UserAdminUpdateSerializer
        return serializers.BaseUserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        context = {"user": instance}
        async_task(mail.send_activation_mail, context, instance.email)

    @action(
        detail=False,
        methods=["patch"],
        serializer_class=serializers.UpdateProfileSerializer,
        permission_classes=[IsAuthenticated],
    )
    def update_profile(self, request, *args, **kwargs):
        obj = request.user
        serializer = serializers.UpdateProfileSerializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=serializers.PasswordResetSerializer,
        permission_classes=[AllowAny],
        throttle_classes=[AuthFlowThrottle],
    )
    def reset_password(self, request, *args, **kwargs):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()
        if user:
            context = {"user": user}
            async_task(mail.send_password_reset_mail, context, user.email)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=serializers.PasswordResetConfirmSerializer,
        permission_classes=[AllowAny],
    )
    def reset_password_confirm(self, request, *args, **kwargs):
        serializer = serializers.PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.user.set_password(serializer.data["new_password"])
        serializer.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=serializers.ActivationSerializer,
        permission_classes=[AllowAny],
    )
    @method_decorator(csrf_protect)
    def activation(self, request, *args, **kwargs):
        serializer = serializers.ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        serializer.user.set_password(serializer.data["new_password"])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(PeCoReTReadOnlyModelViewSet):
    queryset = Group.objects.all()
    filterset_class = None
    search_fields = ["name"]
    permission_classes = [
        permissions.GroupPermission(read_write_groups=[], read_only_groups=[])
    ]
    serializer_class = serializers.GroupSerializer
