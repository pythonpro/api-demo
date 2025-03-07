from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    """

    class Meta:
        model = Transaction
        fields = ["txid", "wallet", "amount", "created_at"]

    def create(self, validated_data):
        """
        Catch transaction amount check errors raised by model and DB.
        """
        try:
            return super().create(validated_data)
        except DjangoValidationError as err:
            # Convert Django ValidationError to DRF's ValidationError for API response.
            raise ValidationError(err.messages[0])
        # Should never happen unless somebody removes atomic amount validation in the model.
        except IntegrityError:
            raise ValidationError("Transaction would result in negative wallet balance")
