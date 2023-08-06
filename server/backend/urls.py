from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend import views
from backend.viewsets import assets as asset_viewsets
from . import viewsets


app_name = "backend"


router = DefaultRouter()
router.register("projects", viewsets.ProjectViewSet, "project")
router.register(
    "vulnerability-templates",
    viewsets.VulnerabilityTemplateViewSet,
    "vulnerability-template",
)
router.register("companies", viewsets.CompanyViewSet, "company")
router.register("cwes", viewsets.CWEViewSet, "cwe")
router.register("report-templates", viewsets.ReportTemplateViewSet, "report-template")
router.register(
    "vulnerability-categories",
    viewsets.VulnerabilityCategoryViewSet,
    "vulnerability-category",
)
router.register("users", viewsets.UserViewSet, "user")
router.register("groups", viewsets.GroupViewSet, "group")
router.register("advisories", viewsets.AdvisoryViewSet, "advisory")

router.register("pentest-types", viewsets.PentestTypeViewSet, "pentest-type")


# company routes
company_router = DefaultRouter()
company_router.register("contacts", viewsets.CompanyContactViewSet, "contact")
company_router.register("information", viewsets.CompanyInformationViewSet, "information")

# project routes
project_router = DefaultRouter()
project_router.register(
    "vulnerabilities", viewsets.ProjectVulnerabilityViewSet, "vulnerability"
)
project_router.register(
    "web-applications", asset_viewsets.WebApplicationViewSet, "web-application"
)
project_router.register("hosts", asset_viewsets.HostViewSet, "host")
project_router.register("services", asset_viewsets.ServiceViewSet, "service")
project_router.register(
    "mobile-applications", asset_viewsets.MobileApplicationViewSet, "mobile-application"
)
project_router.register("findings", viewsets.FindingViewSet, "finding")
project_router.register("accounts", viewsets.AccountViewSet, "account")
project_router.register("api-tokens", viewsets.ProjectTokenViewSet, "api-token")
project_router.register("reports", viewsets.ProjectReportViewSet, "report")
project_router.register("memberships", viewsets.MembershipViewSet, "membership")
project_router.register(
    "contacts", viewsets.ProjectContactViewSet, "contact"
)
project_router.register("files", viewsets.ProjectFileViewSet, "file")
#project_router.register("tasks", viewsets.AssetTaskViewSet, "task")
#project_router.register("checklists", viewsets.ProjectChecklistViewSet, "checklist")


# finding routes
finding_router = DefaultRouter()
finding_router.register("cvss-scores", viewsets.CVSSBaseScoreViewSet, "cvss-score")
finding_router.register("owasp-risk-ratings", viewsets.OWASPRiskRatingViewSet, "owasp-risk-rating")
finding_router.register("timelines", viewsets.FindingTimelineViewSet, "timeline")
finding_router.register("comments", viewsets.FindingCommentViewSet, "comment")
finding_router.register("proofs", viewsets.ProofViewSet, "proof")


# reports routes
report_router = DefaultRouter()
report_router.register(
    "report-releases", viewsets.ReportReleaseViewSet, "report-release"
)
report_router.register(
    "change-histories", viewsets.ChangeHistoryViewSet, "change-history"
)

# advisory routes
advisory_router = DefaultRouter()
advisory_router.register("timelines", viewsets.AdvisoryTimelineViewSet, "timeline")
advisory_router.register(
    "memberships", viewsets.AdvisoryMembershipViewSet, "membership"
)
advisory_router.register("proofs", viewsets.AdvisoryProofViewSet, "proof")
advisory_router.register("comments", viewsets.AdvisoryCommentViewSet, "comment")


urlpatterns = [
    path(
        "users/user-settings/",
        viewsets.UserSettingsViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update"}
        ), name="user-settings-detail"
    ),
    path("", include(router.urls)),
    path("auth/login/", views.LoginView.as_view(), name="login"),
    path("auth/logout/", views.LogoutView.as_view(), name="logout"),
    path("auth/check/", views.AuthCheckView.as_view(), name="auth-check"),
    path("projects/<int:project>/", include(project_router.urls)),
    path(
        "projects/<int:project>/findings/<int:finding>/",
        include((finding_router.urls, "backend"), namespace="findings"),
    ),
    path("projects/<int:project>/reports/<int:report>/", include(report_router.urls)),
    path(
        "advisories/<str:advisory>/",
        include((advisory_router.urls, "backend"), namespace="advisories"),
    ),
    path(
        "companies/<int:company>/",
        include((company_router.urls, "backend"), namespace="companies"),
    ),
]
