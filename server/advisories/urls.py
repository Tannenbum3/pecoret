from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets

app_name = "advisories"

management_router = DefaultRouter()
router = DefaultRouter()

# advisory core routes
router.register("advisories", viewsets.AdvisoryViewSet, "advisory")

# advisory routes
advisory_router = DefaultRouter()
advisory_router.register("timelines", viewsets.AdvisoryTimelineViewSet, "timeline")
advisory_router.register(
    "memberships", viewsets.AdvisoryMembershipViewSet, "membership"
)
advisory_router.register("comments", viewsets.AdvisoryCommentViewSet, "comment")
advisory_router.register("attachments", viewsets.ImageAttachmentViewSet, "attachment")


# management routes
management_router.register("inbox", viewsets.AdvisoryManagementInboxViewSet, "inbox")
management_router.register("labels", viewsets.LabelViewSet, "label")

urlpatterns = [
    path('advisory-management/', include(management_router.urls)),
    path('', include(router.urls)),
    path('advisories/<str:advisory>/', include(advisory_router.urls))
]
