from django.core.mail import send_mail

from config import settings
from config.celery import app

from auction.models import Auction, Status, DutchAuction, EnglishAuction
from lot.models import Offer


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


@app.task
def send_lot_sold_email_task(lot, email):
    subject = 'Lot sold notification'
    message = f'Congratulations! You bought a lot "{lot.item.title}" for ${lot.auction.current_price}.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


@app.task
def send_english_auction_lot_sold_email_task(auction_id):
    auction = EnglishAuction.objects.get(pk=auction_id)
    offer = Offer.objects.filter(lot=auction.lot)
    if offer.exists():
        last_offer = offer.latest('date_creation')
        user_email = last_offer.user.email
        if user_email != '':
            if offer.price >= auction.reserve_price:
                send_lot_sold_email_task(offer.lot.pk, user_email)
