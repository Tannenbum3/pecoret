from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters


class PeCoReTFilterBackendMixin:
    """Mixin that adds basic filtering backends"""

    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]


class PeCoReTModelViewSet(PeCoReTFilterBackendMixin, viewsets.ModelViewSet):
    pass


class PeCoReTNoDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    PeCoReTFilterBackendMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class PeCoReTNoUpdateViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]


class PeCoReTReadOnlyModelViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]


class PeCoReTCreateUpdateDestroyModelViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class PeCoReTListUpdateRetrieveModelViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class PeCoReTUpdateRetrieveModelViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class GenericViewSet(viewsets.GenericViewSet):
    pass
