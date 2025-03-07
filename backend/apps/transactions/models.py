from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction

from apps.wallets.models import Wallet


class Transaction(models.Model):
    """
    Transaction model to store information about wallet transactions.

    Can't be updated or deleted.
    """

    txid = models.CharField(max_length=128, primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="transactions")
    amount = models.DecimalField(max_digits=28, decimal_places=18)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.txid} ({self.amount:.3f})"

    def save(self, *args, **kwargs):
        """
        Override save method to validate wallet balance won't be negative after this transaction
        """
        if self.pk and self._meta.model.objects.filter(pk=self.pk).exists():
            # TODO: protect transactions data on the DB level too since this
            #  approach is not too reliable.
            raise ValidationError("Updating this instance is not allowed.")

        with transaction.atomic():
            # Lock the wallet row for update, so no other transaction can
            # modify it during this process.
            wallet = Wallet.objects.select_for_update().get(pk=self.wallet_id)
            # Calculate the potential new balance.
            potential_balance = wallet.balance + self.amount
            # Validate that the new balance won't be negative.
            if potential_balance < Decimal("0"):
                raise ValidationError("Transaction would result in a negative wallet balance")
            # At this point, the wallet is locked, and we're sure the balance
            # won't get updated by others.
            super().save(*args, **kwargs)
            # Update the wallet balance in the database.
            wallet.balance = potential_balance
            wallet.save(update_fields=["balance", "updated_at"])

    def delete(self, *args, **kwargs):
        # TODO: protect transactions data on the DB level too since this
        #  approach is not too reliable.
        raise ValidationError("Deleting this instance is not allowed.")
