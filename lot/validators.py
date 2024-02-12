from rest_framework import serializers

from auction.models import Status


def validate_status(lot):
    if lot.auction.status != Status.IN_PROGRESS:
        raise serializers.ValidationError("The status is incorrect, status not in progress")


def validate_offer_price(lot, offer_price):
    if lot.auction.current_price >= offer_price:
        raise serializers.ValidationError("Offer_price must be more than current_price")