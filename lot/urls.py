from django.urls import path, include
from rest_framework import routers

from lot.views import LotListView

router = routers.SimpleRouter()
router.register('lot', LotListView, basename='lot')


urlpatterns = [
    path('', include(router.urls)),
]
