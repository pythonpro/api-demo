from decimal import Decimal

import pytest

from apps.wallets.models import Wallet
from apps.wallets.serializers import WalletSerializer

pytestmark = pytest.mark.django_db


def test_wallet_serializer_valid_data():
    """
    Test that the WalletSerializer serializes valid data correctly.
    """
    valid_data = {
        "label": "Test Wallet",
    }
    serializer = WalletSerializer(data=valid_data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["label"] == "Test Wallet"


def test_wallet_serializer_read_only_balance():
    """
    Test that the `balance` field is read-only.
    """
    wallet = Wallet.objects.create(label="Test Wallet", balance=Decimal("200.00"))
    serializer = WalletSerializer(instance=wallet)
    assert Decimal(serializer.data["balance"]) == Decimal("200.00")

    update_data = {
        "label": "Updated Wallet",
        "balance": Decimal("500.00"),  # Attempt to update a read-only field
    }
    serializer = WalletSerializer(instance=wallet, data=update_data)
    assert serializer.is_valid(), serializer.errors  # Should still be valid
    updated_wallet = serializer.save()
    assert updated_wallet.label == "Updated Wallet"
    assert updated_wallet.balance == Decimal("200.00")  # Balance should remain unchanged


def test_wallet_serializer_update():
    """
    Test an update on the WalletSerializer.
    """
    wallet = Wallet.objects.create(label="Initial Wallet", balance=150.00)
    update_data = {"label": "Updated Wallet"}
    serializer = WalletSerializer(instance=wallet, data=update_data)
    assert serializer.is_valid(), serializer.errors
    updated_wallet = serializer.save()
    assert updated_wallet.label == "Updated Wallet"
    assert updated_wallet.balance == 150.00  # Ensure balance remains unchanged
