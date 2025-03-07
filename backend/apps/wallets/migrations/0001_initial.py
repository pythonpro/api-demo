import uuid
from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Wallet",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("label", models.CharField(max_length=255)),
                (
                    "balance",
                    models.DecimalField(decimal_places=18, default=Decimal("0"), max_digits=28),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(("balance__gte", Decimal("0"))),
                        name="balance_non_negative",
                    )
                ],
            },
        ),
    ]
