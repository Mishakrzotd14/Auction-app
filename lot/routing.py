from django.urls import path

from lot import consumers

websocket_urlpatterns = [
    path('ws/price_change', consumers.LotConsumer.as_asgi()),
    path('ws/<int:lot_id>/recent_offer', consumers.OfferConsumer.as_asgi()),
]
