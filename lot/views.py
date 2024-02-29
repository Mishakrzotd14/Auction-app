from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db import transaction

from auction.models import Status, TASK_NAME_UPDATE_PRICE, TASK_NAME_CLOSE_AUCTION
from lot.filters import AuctionTypeFilter
from lot.models import Lot, Offer
from lot.serializers import LotSerializer, OfferSerializer
from lot.validators import validate_status, validate_offer_price, validate_type_auction_english, \
    validate_offer_price_buy_it_now
from config.celery import app


class LotsLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10


class LotListView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    pagination_class = LotsLimitOffsetPagination
    ordering_fields = ['-closing_date', 'base_price']
    ordering = ['-closing_date']
    filter_backends = [DjangoFilterBackend, AuctionTypeFilter]
    filterset_fields = ['auction__auction_status', ]

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def make_offer(self, request, pk=None):
        lot = self.get_object()
        auction = lot.auction
        serializer = OfferSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            validate_type_auction_english(lot)
            validate_status(lot)
            offer_price = serializer.validated_data['price']
            validate_offer_price(lot, offer_price)

            Offer.objects.create(user=request.user, lot=lot, price=offer_price)

            auction.current_price = offer_price
            auction.save(update_fields=['current_price'])

            return Response({"message": "Your offer has been accepted."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def buy_it_now(self, request, pk=None):
        lot = self.get_object()
        auction = lot.auction
        validate_status(lot)
        if hasattr(auction, 'englishauction'):
            validate_offer_price_buy_it_now(lot)

            buy_it_now_price = lot.auction.englishauction.buy_it_now_price
            Offer.objects.create(user=request.user, lot=lot, price=buy_it_now_price)

            auction.current_price = buy_it_now_price
            auction.auction_status = Status.CLOSED
            auction.save(update_fields=['current_price', 'auction_status'])
        elif hasattr(auction, 'dutchauction'):
            auction.auction_status = Status.CLOSED
            auction.save(update_fields=['auction_status'])
            app.control.revoke(task_id=f'{TASK_NAME_UPDATE_PRICE}_{auction.id}')
        app.control.revoke(task_id=f'{TASK_NAME_CLOSE_AUCTION}_{auction.id}')
        return Response({"message": "Buy it now offer has been accepted."}, status=status.HTTP_201_CREATED)
