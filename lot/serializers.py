from rest_framework.serializers import ModelSerializer

from .models import Lot


class LotSerializer(ModelSerializer):
    class Meta:
        model = Lot
        fields = '__all__'
