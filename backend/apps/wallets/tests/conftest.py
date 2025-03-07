import pytest
from rest_framework.test import APIClient

from apps.wallets.models import Wallet


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_wallets(db):
    """
    Fixture to create test Wallet objects in the database
    """
    return (
        Wallet.objects.create(balance=100, label="Wallet 1"),
        Wallet.objects.create(balance=200, label="Wallet 2"),
        Wallet.objects.create(balance=50, label="Wallet 3"),
    )
