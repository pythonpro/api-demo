from django_filters import rest_framework as filters

from .models import Transaction


class TransactionFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr="lte")
    start_date = filters.DateTimeFilter(field_name="created_at__date", lookup_expr="gte")
    end_date = filters.DateTimeFilter(field_name="created_at__date", lookup_expr="lte")

    class Meta:
        model = Transaction
        fields = {
            "txid": ["exact", "contains", "icontains"],
            "wallet": ["exact"],
        }
