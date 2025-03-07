from decimal import Decimal
from uuid import UUID

import pytest
from django.db import IntegrityError

from apps.wallets.models import Wallet

pytestmark = pytest.mark.django_db


def test_wallet_creation():
    """Test that a Wallet instance is created successfully with default values."""
    wallet = Wallet.objects.create(label="Test Wallet")
    assert wallet.id is not None  # UUID is automatically generated
    assert isinstance(wallet.id, UUID)  # Check if id is a valid UUID
    assert wallet.label == "Test Wallet"
    assert wallet.balance == Decimal("0")  # Default balance
    assert wallet.created_at is not None
    assert wallet.updated_at is not None


def test_str_representation():
    """Test the string representation of the Wallet."""
    wallet = Wallet.objects.create(label="My Wallet", balance=Decimal("123.456"))
    expected_str = "My Wallet (123.456)"
    assert str(wallet) == expected_str


def test_balance_non_negative_constraint():
    """Test the custom constraint that prevents negative wallet balance."""
    with pytest.raises(IntegrityError):
        Wallet.objects.create(label="Invalid Wallet", balance=Decimal("-10.00"))


def test_updating_balance():
    """Test that the balance can be updated to a valid non-negative value."""
    wallet = Wallet.objects.create(label="Savings Wallet", balance=Decimal("50.00"))
    wallet.balance = Decimal("30.50")
    wallet.save()
    wallet.refresh_from_db()
    assert wallet.balance == Decimal("30.50")


def test_negative_balance_update():
    """Test that updating the balance to a negative value raises an IntegrityError."""
    wallet = Wallet.objects.create(label="Spending Wallet", balance=Decimal("20.00"))
    wallet.balance = Decimal("-5.00")

    with pytest.raises(IntegrityError):
        wallet.save()
