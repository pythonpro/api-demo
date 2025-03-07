from rest_framework import mixins
from rest_framework.pagination import CursorPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api.django_filters import DjangoFilterBackend
from rest_framework_json_api.filters import OrderingFilter, QueryParameterValidationFilter
from rest_framework_json_api.views import AutoPrefetchMixin, PreloadIncludesMixin, RelatedMixin

from .filters import TransactionFilter
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionPagination(CursorPagination):
    """
    Fast pagination for supposedly large table.
    """

    ordering = "-created_at"


class TransactionViewSet(
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    ViewSet for creating and viewing Transaction instances.
    """

    queryset = Transaction.objects.all()
    pagination_class = TransactionPagination
    serializer_class = TransactionSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend, QueryParameterValidationFilter]
    filterset_class = TransactionFilter
    ordering = ["-created_at"]
    ordering_fields = [
        "created_at",
        "wallet",
        "amount",
    ]
