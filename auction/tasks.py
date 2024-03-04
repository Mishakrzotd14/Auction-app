from django.core.mail import send_mail

from config import settings
from config.celery import app

from auction.models import Auction, Status, DutchAuction
from lot.models import Lot


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


@app.task
def send_price_change_email_task(lot, email, new_price):
    subject = 'Price change notification'
    message = f'The price of the lot "{lot.item.title}" has changed.\n\nOld Price: ${lot.auction.current_price}\nNew ' \
              f'Price: ${new_price}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
