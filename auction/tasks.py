from config.celery import app

from auction.models import Auction, Status, DutchAuction


@app.task
def open_auction_task(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    if hasattr(auction, 'englishauction'):
        auction.current_price = auction.englishauction.opening_price
    elif hasattr(auction, 'dutchauction'):
        auction.current_price = auction.dutchauction.start_price

    auction.auction_status = Status.IN_PROGRESS
    auction.save(update_fields=['auction_status', 'current_price'])


@app.task
def close_auction_task(auction_id):
    Auction.objects.filter(pk=auction_id).update(auction_status=Status.CLOSED)


@app.task
def update_dutch_auction_price_task(auction_id, delta_price):
    auction = DutchAuction.objects.get(pk=auction_id)
    auction.current_price -= delta_price
    auction.save(update_fields=['current_price'])
