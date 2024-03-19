from datetime import timedelta

from django.contrib import admin
from auction.tasks import (
    open_auction_task,
    close_auction_task,
    update_dutch_auction_price_task,
    send_english_auction_lot_sold_email_task
)
from auction.models import (
    EnglishAuction,
    DutchAuction,
    TASK_NAME_UPDATE_PRICE,
    TASK_NAME_CLOSE_AUCTION,
    TASK_NAME_ENG_AUC_LOT_SOLD_EMAIL
)
from lot.admin import LotInline


class BaseAuctionAdmin(admin.ModelAdmin):
    inlines = [LotInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        open_auction_task.apply_async(args=(obj.id,), eta=obj.opening_date)
        close_auction_task.apply_async(args=(obj.id,), eta=obj.closing_date,
                                       task_id=f"{TASK_NAME_CLOSE_AUCTION}_{obj.id}")


@admin.register(EnglishAuction)
class EnglishAuctionAdmin(BaseAuctionAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        send_english_auction_lot_sold_email_task.apply_async(args=(obj.id,), eta=obj.closing_date,
                                                             task_id=f"{TASK_NAME_ENG_AUC_LOT_SOLD_EMAIL}_{obj.id}")


@admin.register(DutchAuction)
class DutchAuctionAdmin(BaseAuctionAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        total_tasks = obj.total_tasks
        delta = (obj.start_price - obj.end_price) / total_tasks
        for idx in range(1, total_tasks + 1):
            task_eta = obj.opening_date + timedelta(minutes=obj.frequency * idx)
            task_id = f"{TASK_NAME_UPDATE_PRICE}_{obj.id}_{idx}"
            update_dutch_auction_price_task.apply_async(args=(obj.id, delta), eta=task_eta,
                                                        task_id=task_id)
