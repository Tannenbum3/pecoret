from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters


class PeCoReTFilterBackendMixin:
    """Mixin that adds basic filtering backends"""

    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
