from rest_framework import serializers

from auction.serializers import AuctionSerializer
from item.serializers import ItemSerializer
from lot.models import Lot


class LotSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    auction = AuctionSerializer()

    class Meta:
        model = Lot
        fields = ('id', 'item', 'auction')
