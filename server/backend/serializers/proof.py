from rest_framework import serializers
from backend.models.proof import Proof


class ProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proof
        fields = [
            "pk", "date_created", "date_updated", "title", "order", "text",
            "image_caption", "image"
        ]
