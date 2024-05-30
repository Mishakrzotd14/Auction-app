import json

import channels.layers as channels_layers
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from auction.tasks import send_price_change_email_task
from lot.models import Offer


def get_last_offer(lot):
    offer = Offer.objects.filter(lot=lot.pk)
    if offer.exists():
        return offer.latest('date_creation')
    return None


def send_email_about_change_price(lot, current_user, current_price):
    last_offer = get_last_offer(lot)
    if last_offer:
        user_of_offer = last_offer.user
        user_email = user_of_offer.email
        if user_email:
            if user_of_offer != current_user:
                send_price_change_email_task(lot, user_email, current_price)


def send_event_about_price_change(lot_id, offered_price):
    channel_layer = channels_layers.get_channel_layer()
    data = json.dumps({'lot_id': lot_id, 'price': offered_price},  default=float)
    async_to_sync(channel_layer.group_send)('price_changes', {'type': 'send_price_change', 'text_data': data})


def send_event_about_recent_offer(lot):
    user_offers = get_recent_offers(lot)
    if user_offers:
        channel_layer = channels_layers.get_channel_layer()
        data = json.dumps(user_offers, default=float)
        async_to_sync(channel_layer.group_send)(f'lot_{lot.id}_offers', {'type': 'send_recent_offer', 'text_data': data})


@database_sync_to_async
def get_recent_offers(lot):
    return list(Offer.objects.filter(lot=lot)
                .order_by('-date_creation')
                .values_list('user__username', 'price')[:5])
