import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Auction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("opening_date", models.DateTimeField()),
                ("closing_date", models.DateTimeField()),
                (
                    "auction_status",
                    models.IntegerField(
                        choices=[(0, "Pending"), (1, "In Progress"), (2, "Closed")],
                        default=0,
                    ),
                ),
                ("current_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="DutchAuction",
            fields=[
                (
                    "auction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="auction.auction",
                    ),
                ),
                ("start_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("end_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("frequency", models.IntegerField()),
            ],
            bases=("auction.auction",),
        ),
        migrations.CreateModel(
            name="EnglishAuction",
            fields=[
                (
                    "auction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="auction.auction",
                    ),
                ),
                ("opening_price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "buy_it_now_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("reserve_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            bases=("auction.auction",),
        ),
    ]
