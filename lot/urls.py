from django.urls import path, include
from rest_framework import routers

from lot.views import LotListView

router = routers.SimpleRouter()
router.register('lot', LotListView, basename='lot')


urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/make_offer', LotListView.as_view({'post': 'make_offer'}), name='make-offer'),
    path('<int:pk>/buy_it_now', LotListView.as_view({'post': 'make_offer_buy_it_now'}), name='make_offer_buy_it_now'),
]
