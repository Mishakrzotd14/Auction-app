from rest_framework import serializers

from auction.serializers import EnglishAuctionSerializer, DutchAuctionSerializer
from item.serializers import ItemSerializer
from lot.models import Lot


class LotSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    english_auction = EnglishAuctionSerializer()
    dutch_auction = DutchAuctionSerializer()

    class Meta:
        model = Lot
        fields = ('id', 'item', 'english_auction', 'dutch_auction')
