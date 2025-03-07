from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail

from apps.transactions.models import Transaction


def test_get_wallet_list(api_client, create_wallets):
    """
    Test retrieval of wallet list
    """
    url = reverse("wallet-list")  # Replace with your actual router view name if different
    response = api_client.get(url)
    assert response.status_code == 200, "Wallet list should be retrievable"
    assert len(response.data) == 3, "Should return all created wallets"


def test_ordering_wallets(api_client, create_wallets):
    """
    Test ordering on Wallet list API
    """
    url = reverse("wallet-list")
    response = api_client.get(url, {"sort": "-balance"})
    assert response.status_code == 200, "Wallet list should be retrievable"
    assert Decimal(response.data["results"][0]["balance"]) == Decimal("200"), (
        "Wallets should be ordered by balance in descending order"
    )
    assert Decimal(response.data["results"][1]["balance"]) == Decimal("100"), (
        "Wallets should be ordered by balance in descending order"
    )
    assert Decimal(response.data["results"][2]["balance"]) == Decimal("50"), (
        "Wallets should be ordered by balance in descending order"
    )


def test_filtering_wallets(api_client, create_wallets):
    """
    Test filtering functionality on Wallet list API
    """
    url = reverse("wallet-list")
    response = api_client.get(
        url, {"filter[label]": "Wallet 2"}
    )  # Adjust filter query key based on WalletFilter implementation
    assert response.status_code == 200, "Filtering should work"
    assert len(response.data["results"]) == 1, "Only one wallet should match the filter"
    assert response.data["results"][0]["label"] == "Wallet 2", (
        "The filtered wallet should have the expected label"
    )


def test_invalid_query_parameters(api_client):
    """
    Test query parameter validation
    """
    url = reverse("wallet-list")
    response = api_client.get(url, {"invalid_param": "value"})
    assert response.status_code == 400, "Invalid query parameters should return a 400 response"
    assert response.data[0]["detail"] == ErrorDetail(
        string="invalid query parameter: invalid_param", code="invalid"
    )


def test_get_single_wallet(api_client, create_wallets):
    """
    Test retrieval of a single wallet instance
    """
    wallet = create_wallets[0]
    url = reverse("wallet-detail", args=[wallet.id])  # Replace with the actual detail route
    response = api_client.get(url)
    assert response.status_code == 200, "Should retrieve the wallet successfully"
    response_data = response.data
    assert response_data["id"] == str(wallet.id), "The ID should match the requested wallet"
    assert response_data["label"] == wallet.label, "The label should match the wallet"
    assert Decimal(response_data["balance"]) == wallet.balance, (
        "The balance should match the wallet"
    )


@pytest.mark.django_db
def test_create_wallet(api_client):
    """
    Test creation of a new wallet instance
    """
    url = reverse("wallet-list")
    wallet_data = {
        "data": {
            "type": "Wallet",
            "attributes": {
                "label": "New Wallet",
            },
        }
    }
    response = api_client.post(url, wallet_data)
    assert response.status_code == 201, "Wallet should be successfully created"
    response_data = response.data
    assert response_data["label"] == wallet_data["data"]["attributes"]["label"], (
        "The label should match the input"
    )


@pytest.mark.django_db
def test_update_existing_wallet(api_client, create_wallets):
    """
    Test updating an existing wallet
    """
    wallet = create_wallets[0]
    url = reverse("wallet-detail", args=[wallet.id])  # Replace with the actual detail route
    updated_data = {
        "data": {
            "type": "Wallet",
            "id": str(wallet.id),
            "attributes": {
                "label": "Updated Wallet",
            },
        }
    }
    response = api_client.patch(url, updated_data)
    assert response.status_code == 200, "Wallet should be successfully updated"

    response_data = response.data
    assert response_data["label"] == updated_data["data"]["attributes"]["label"], (
        "The label should match the updated value"
    )


@pytest.mark.django_db
def test_delete_wallet(api_client, create_wallets):
    """
    Test deletion of an existing wallet
    """
    wallet = create_wallets[0]  # Select the first wallet from the fixture
    url = reverse("wallet-detail", args=[wallet.id])  # Replace with actual detail route

    # Send DELETE request
    response = api_client.delete(url)

    # Assert status code for successful deletion
    assert response.status_code == 204, "Wallet should be successfully deleted"

    # Verify that the wallet no longer exists
    response = api_client.get(url)
    assert response.status_code == 404, "Deleted wallet should return a 404 response"


@pytest.mark.django_db
def test_delete_wallet_with_transaction(api_client, create_wallets):
    """
    Test deletion of an existing wallet with transaction
    """
    wallet = create_wallets[0]  # Select the first wallet from the fixture
    Transaction.objects.create(txid="qwerty", wallet=wallet, amount=100)
    url = reverse("wallet-detail", args=[wallet.id])  # Replace with actual detail route

    # Send DELETE request
    response = api_client.delete(url)

    assert response.status_code == 400, "Deletion should fail if wallet has transactions"
    assert response.data[0]["detail"] == ErrorDetail(
        string="Wallet with transactions cannot be deleted", code="invalid"
    )
