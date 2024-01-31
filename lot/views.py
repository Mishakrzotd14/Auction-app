from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from lot.models import Lot
from lot.serializers import LotSerializer


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['auction__auction_status', ]
