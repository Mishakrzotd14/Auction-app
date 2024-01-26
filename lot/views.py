from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Lot
from .serializers import LotSerializer


class LotListView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
