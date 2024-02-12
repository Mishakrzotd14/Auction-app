from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from lot.filters import AuctionTypeFilter
from lot.models import Lot, Offer
from lot.serializers import LotSerializer, OfferSerializer
from lot.validators import validate_status, validate_offer_price


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

    @action(detail=True)
    def make_offer(self, request, pk=None):
        lot = self.get_object()
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            validate_status(lot)
            offer_price = serializer.validated_data['offer_price']
            validate_offer_price(lot, offer_price)

            lot.current_price = offer_price
            lot.save()

            Offer.objects.create(user=request.user, lot=lot, offer_price=offer_price)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
