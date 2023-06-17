from rest_framework import serializers
from backend.models import Company


class CompanySerializer(serializers.ModelSerializer):
    self = serializers.HyperlinkedIdentityField(view_name="backend:company-detail")

    class Meta:
        model = Company
        fields = [
            "pk",
            "date_created",
            "date_updated",
            "name",
            "street",
            "self",
            "zipcode",
            "city",
            "country",
            "report_template",
        ]
