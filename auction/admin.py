from datetime import timedelta

from django.contrib import admin
from auction.tasks import open_auction_task, close_auction_task, update_dutch_auction_price_task
from auction.models import EnglishAuction, DutchAuction, TASK_NAME_UPDATE_PRICE, TASK_NAME_CLOSE_AUCTION

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
    pass


@admin.register(DutchAuction)
class DutchAuctionAdmin(BaseAuctionAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        total_tasks = int((obj.closing_date - obj.opening_date).total_seconds() / (obj.frequency * 60))
        delta = (obj.start_price - obj.end_price) / total_tasks

        for i in range(1, total_tasks + 1):
            task_eta = obj.opening_date + timedelta(minutes=obj.frequency * i)
            update_dutch_auction_price_task.apply_async(args=(obj.id, delta), eta=task_eta,
                                                        task_id=f"{TASK_NAME_UPDATE_PRICE}_{obj.id}")
