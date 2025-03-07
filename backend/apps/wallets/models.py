import uuid
from decimal import Decimal

from django.db import models


class Wallet(models.Model):
    """
    Wallet model to store information about user wallets.

    Can't be deleted if it has transactions.
    """

    # uuid as id, in order to hide wallets number in the system.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=28, decimal_places=18, default=Decimal("0"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Protect balance on the DB level from being negative.
        constraints = [
            models.CheckConstraint(
                name="balance_non_negative", condition=models.Q(balance__gte=Decimal("0"))
            )
        ]

    def __str__(self):
        return f"{self.label} ({self.balance:.3f})"
