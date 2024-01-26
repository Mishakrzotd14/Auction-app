from django.db import models


AUCTION_STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('IN_PROGRESS', 'In Progress'),
    ('CLOSED', 'Closed'),
]


class Auction(models.Model):
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    auction_status = models.CharField(max_length=20, choices=AUCTION_STATUS_CHOICES)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)


class EnglishAuction(Auction):
    opening_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_it_now_price = models.DecimalField(max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2)


class DutchAuction(Auction):
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    end_price = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.IntegerField()
