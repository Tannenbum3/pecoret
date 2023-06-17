from rest_framework import serializers
from backend.models.advisory_proof import AdvisoryProof


class AdvisoryProofSerializer(serializers.ModelSerializer):
    image_base64 = serializers.CharField(read_only=True)
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = AdvisoryProof
        fields = ["pk", "order", "title", "order", "text", "image", "image_caption",
                  "date_created", "date_updated", "image_base64"]
