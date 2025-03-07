from django_filters import rest_framework as filters

from .models import Wallet


class WalletFilter(filters.FilterSet):
    min_balance = filters.NumberFilter(field_name="balance", lookup_expr="gte")
    max_balance = filters.NumberFilter(field_name="balance", lookup_expr="lte")
    start_date = filters.DateTimeFilter(field_name="created_at__date", lookup_expr="gte")
    end_date = filters.DateTimeFilter(field_name="created_at__date", lookup_expr="lte")

    class Meta:
        model = Wallet
        fields = {
            "label": ["exact", "contains", "icontains"],
        }
