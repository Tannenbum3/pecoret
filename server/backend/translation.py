from modeltranslation.translator import TranslationOptions, register
from backend.models import (
    VulnerabilityTemplate,
    VulnerabilityCategory,
    ProjectVulnerability,
)


@register(VulnerabilityTemplate)
class VulnerabilityTemplateTranslation(TranslationOptions):
    fields = ["name", "description", "recommendation"]


@register(VulnerabilityCategory)
class VulnerabilityCategoryTranslation(TranslationOptions):
    fields = ["name"]


@register(ProjectVulnerability)
class ProjectVulnerabilityTranslation(TranslationOptions):
    fields = ["name", "description", "recommendation"]
