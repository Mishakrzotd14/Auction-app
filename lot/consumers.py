import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from lot.models import Lot
from lot.services.change_price_service import get_recent_offers


class LotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'price_changes'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_price_change(self, event):
        await self.send(text_data=json.dumps(event))


class OfferConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.lot_id = self.scope['url_route']['kwargs']['lot_id']
        self.room_group_name = f'lot_{self.lot_id}_offers'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        lot = Lot.objects.get(id=self.lot_id)
        await self.accept()
        user_offers = await get_recent_offers(lot)
        if user_offers:
            data = json.dumps(user_offers, default=float)
            await self.send(text_data=json.dumps({'data': data},
                                                 default=float))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_recent_offer(self, event):
        await self.send(text_data=json.dumps(event))
