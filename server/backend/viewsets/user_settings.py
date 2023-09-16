from rest_framework.permissions import IsAuthenticated
from backend.serializers.user_settings import UserSettingsSerializer
from backend.models import UserSettings
from pecoret.core.viewsets import PeCoReTListUpdateRetrieveModelViewSet


class UserSettingsViewSet(PeCoReTListUpdateRetrieveModelViewSet):
    serializer_class = UserSettingsSerializer
    queryset = UserSettings.objects.none()
    permission_classes = [IsAuthenticated]
    api_scope = "scope_user"

    def get_object(self):
        return UserSettings.objects.for_user(self.request.user).get()
