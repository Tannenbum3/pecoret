from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from backend.models.user import User
from pecoret.core.utils import decode_uid

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name", "pk"]
        read_only = ["name"]


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username", "first_name", "last_name", "is_active", "email", "groups"]
        read_only_fields = ["pk", "username", "is_active", "groups"]


class UpdateProfileSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ["pk", "first_name", "last_name"]
        read_only_fields = ["pk"]


class MinimalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "pk"]
        read_only_fields = ["username", "pk"]


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["pk", "username", "first_name", "last_name", "email", "groups"]
        read_only_Fields = ["pk", "username", "is_active"]

    def create(self, validated_data):
        groups = validated_data.pop('groups')
        user = User.objects.create_user(**validated_data, is_active=False)
        user.save()
        for group in groups:
            user.groups.add(group)
        return user


class UserAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username", "first_name", "last_name", "email", "groups", "is_active"]
        read_only_fields = ["username"]


class UserMeSerializer(serializers.ModelSerializer):
    # output all details of the logged in user
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["pk", "username", "first_name", "last_name", "is_active", "email", "groups", "is_superuser"]
        read_only_Fields = ["pk", "username", "is_active", "groups", "is_superuser"]


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def get_user(self):
        try:
            user = User.objects.get(is_active=True, email=self.data.get("email"))
            if user.has_usable_password():
                return user
        except User.DoesNotExist:
            pass


class PasswordResetConfirmSerializer(serializers.Serializer):
    default_error_messages = {
        "invalid_password": "Invalid password! {msg}",
        "invalid_token": "Token is not valid",
        "invalid_uid": "Invalid user!"
    }
    new_password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        try:
            uid = decode_uid(self.initial_data.get("uid", ""))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            self.fail("invalid_uid")
        is_token_valid = default_token_generator.check_token(user, self.initial_data.get("token", ""))
        if not is_token_valid:
            self.fail("invalid_token")
        try:
            validate_password(attrs["new_password"], user)
        except ValidationError as e:
            self.fail("invalid_password", msg=str(';'.join(list(e.messages))))
        self.user = user
        return validated_data


class ActivationSerializer(PasswordResetConfirmSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.user.is_active:
            return attrs
        raise PermissionDenied()
