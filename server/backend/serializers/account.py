from rest_framework import serializers
from backend.models import WebApplication, Account, Host
from backend.serializers.assets import WebApplicationSerializer
from backend.serializers.assets.host import HostSerializer
from pecoret.core.serializers import ProjectAssetField


class AccountSerializer(serializers.ModelSerializer):
    asset = ProjectAssetField(
        serializers={
            "web_application": WebApplicationSerializer(WebApplication.objects.all()),
            "host": HostSerializer(Host.objects.all()),
        },
    )

    class Meta:
        model = Account
        fields = [
            "pk",
            "date_created",
            "date_updated",
            "asset",
            "role",
            "username",
            "password",
            "accessible",
            "compromised",
        ]
