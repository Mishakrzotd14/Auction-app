from celery import shared_task
from datetime import datetime

from auction.models import Auction


@shared_task
def change_auction_status(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    now = datetime.now()
    if now < auction.opening_date:
        auction.auction_status = 'PENDING'
    elif auction.opening_date >= now < auction.closing_date:
        auction.auction_status = 'IN_PROGRESS'
    elif auction.opening_date >= now < auction.closing_date:
        auction.auction_status = 'CLOSED'
    auction.save()
