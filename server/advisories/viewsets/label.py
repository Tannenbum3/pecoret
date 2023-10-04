from pecoret.core.viewsets import ModelViewSet
from pecoret.core import permissions
from advisories.models.label import Label
from advisories.serializers.label import LabelSerializer


class LabelViewSet(ModelViewSet):
    permission_classes = [permissions.PRESET_GROUP_ADVISORY_MANAGEMENT]
    filterset_class = None
    search_fields = ["name", "description"]
    ordering_fields = []
    serializer_class = LabelSerializer

    def get_queryset(self):
        return Label.objects.all()
