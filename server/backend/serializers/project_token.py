from rest_framework import serializers
from backend.models.project_token import ProjectToken


class ProjectTokenSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProjectToken
        fields = ["date_created", "date_updated", "user", "date_expire", "name", "pk"]
        read_only_fields = ["pk"]
