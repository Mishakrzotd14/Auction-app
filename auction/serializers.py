from rest_framework import serializers

from auction.models import EnglishAuction, DutchAuction


class EnglishAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnglishAuction
        fields = ('opening_price', 'opening_date', 'closing_date',
                  'auction_status', 'buy_it_now_price', 'reserve_price')


class DutchAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DutchAuction
        fields = ('start_price', 'end_price', 'opening_date', 'closing_date',
                  'auction_status', 'frequency')
