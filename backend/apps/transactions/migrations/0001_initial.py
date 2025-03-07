import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wallets", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "txid",
                    models.CharField(max_length=128, primary_key=True, serialize=False),
                ),
                ("amount", models.DecimalField(decimal_places=18, max_digits=28)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "wallet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="transactions",
                        to="wallets.wallet",
                    ),
                ),
            ],
        ),
    ]
