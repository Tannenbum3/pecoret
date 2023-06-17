from rest_framework import serializers
from backend.serializers.user import MinimalUserSerializer
from backend.models.reports.report import Report, ReportVariant
from backend.models import User, ReportTemplate
from pecoret.core.serializers import (
    ValuedChoiceField,
    ReportAuthorRelatedField,
)


class ReportSerializer(serializers.ModelSerializer):
    variant = ValuedChoiceField(choices=ReportVariant.choices)
    author = ReportAuthorRelatedField(
        serializer=MinimalUserSerializer, queryset=User.objects.all()
    )
    template = serializers.PrimaryKeyRelatedField(
        queryset=ReportTemplate.objects.active()
    )

    class Meta:
        fields = [
            "pk",
            "date_created",
            "date_updated",
            "name",
            "title",
            "template",
            "author",
            "variant",
            "recommendation",
            "evaluation",
        ]
        model = Report
