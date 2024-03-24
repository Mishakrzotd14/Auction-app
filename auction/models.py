from django.db import models

TASK_NAME_CLOSE_AUCTION = 'close_auction'
TASK_NAME_UPDATE_PRICE = 'update_dutch_auction_price'
TASK_NAME_ENG_AUC_LOT_SOLD_EMAIL = 'send_english_auction_lot_sold_email'


class Status(models.IntegerChoices):
    PENDING = 0
    IN_PROGRESS = 1
    CLOSED = 2


class Auction(models.Model):
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    auction_status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)


class EnglishAuction(Auction):
    opening_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_it_now_price = models.DecimalField(max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2)


class DutchAuction(Auction):
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    end_price = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.IntegerField()

    @property
    def total_tasks(self):
        return int((self.closing_date - self.opening_date).total_seconds() / (self.frequency * 60))
