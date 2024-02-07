from config.celery import app
from datetime import datetime

from auction.models import Auction, Status


@app.task
def open_auction_task(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    auction.auction_status = Status.IN_PROGRESS
    auction.save()


@app.task
def close_auction_task(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    auction.auction_status = Status.COMPLETED
    auction.save()