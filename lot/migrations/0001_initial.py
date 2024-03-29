# Generated by Django 5.0.1 on 2024-02-06 08:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auction", "0001_initial"),
        ("item", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lot",
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
                (
                    "auction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auction.auction",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="item.item"
                    ),
                ),
            ],
        ),
    ]
