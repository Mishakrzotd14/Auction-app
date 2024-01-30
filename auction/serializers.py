from rest_framework import serializers
from auction.models import EnglishAuction, DutchAuction, Auction


class AuctionSerializer(serializers.ModelSerializer):
    specific_info = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ('opening_date', 'closing_date', 'auction_status', 'specific_info')

    def get_specific_info(self, obj):
        if isinstance(obj, EnglishAuction):
            return EnglishAuctionSerializer(obj).data
        elif isinstance(obj, DutchAuction):
            return DutchAuctionSerializer(obj).data
        else:
            return {}


class EnglishAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnglishAuction
        fields = ('opening_price', 'buy_it_now_price', 'reserve_price')


class DutchAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DutchAuction
        fields = ('start_price', 'end_price', 'frequency')