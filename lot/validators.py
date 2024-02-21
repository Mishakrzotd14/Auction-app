from rest_framework.serializers import ValidationError

from auction.models import Status


def validate_status(lot):
    auction_status = lot.auction.status
    if auction_status != Status.IN_PROGRESS:
        raise ValidationError(f"The status is incorrect, current status is {auction_status}")


def validate_offer_price(lot, offer_price):
    if lot.auction.current_price >= offer_price:
        raise ValidationError("Offer price must be more than current price")


def validate_type_auction_english(lot):
    if not hasattr(lot.auction, 'englishauction'):
        raise ValidationError('Inсorrect type of auction')


def validate_offer_price_buy_it_now(lot):
    if lot.auction.current_price >= lot.auction.englishauction.buy_it_now_price:
        raise ValidationError('Buy it now price less than current price')
