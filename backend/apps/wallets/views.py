from rest_framework.exceptions import ValidationError
from rest_framework_json_api.django_filters import DjangoFilterBackend
from rest_framework_json_api.filters import OrderingFilter, QueryParameterValidationFilter
from rest_framework_json_api.views import ModelViewSet

from .filters import WalletFilter
from .models import Wallet
from .serializers import WalletSerializer


class WalletViewSet(ModelViewSet):
    """
    ViewSet for viewing and editing Wallet instances.
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend, QueryParameterValidationFilter]
    filterset_class = WalletFilter
    ordering = ["-updated_at"]
    ordering_fields = ["updated_at", "balance", "created_at"]

    def perform_destroy(self, instance):
        """
        Raises a ValidationError if the instance has any associated transactions.
        Deletes the specified instance if no transactions are associated.
        """
        if instance.transactions.exists():
            raise ValidationError("Wallet with transactions cannot be deleted")
        instance.delete()
