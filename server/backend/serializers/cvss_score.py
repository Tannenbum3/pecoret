from rest_framework import serializers
from backend.models import cvss_score as models
from pecoret.core.serializers import ValuedChoiceField


class CVSSBaseScoreSerializer(serializers.ModelSerializer):
    """Serializer for the BaseCVSS Score model
    finding is scoped to a project to prevent BAC vulns
    """

    av = ValuedChoiceField(choices=models.AVChoices.choices)
    ac = ValuedChoiceField(choices=models.ACChoices.choices)
    i = ValuedChoiceField(choices=models.NoneLowHighChoices.choices)
    c = ValuedChoiceField(choices=models.NoneLowHighChoices.choices)
    pr = ValuedChoiceField(choices=models.NoneLowHighChoices.choices)
    a = ValuedChoiceField(choices=models.ACChoices.choices)
    s = ValuedChoiceField(choices=models.SChoices.choices)
    ui = ValuedChoiceField(choices=models.UIChoices.choices)

    class Meta:
        model = models.CVSSBaseScore
        fields = [
            "pk",
            "av",
            "s",
            "ui",
            "i",
            "a",
            "c",
            "pr",
            "ac",
            "cvss31_vector",
            "cvss31_base_score",
            "cvss31_base_severity",
        ]
