from rest_framework_json_api import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for the Wallet model
    """

    class Meta:
        model = Wallet
        fields = ["id", "label", "balance", "created_at", "updated_at"]
        read_only_fields = ["balance"]
