from django.contrib import admin
from auction.tasks import open_auction_task, close_auction_task
from auction.models import EnglishAuction, DutchAuction

from lot.admin import LotInline


class BaseAuctionAdmin(admin.ModelAdmin):
    inlines = [LotInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        open_auction_task.apply_async(args=(obj.id,), eta=obj.opening_date)
        close_auction_task.apply_async(args=(obj.id,), eta=obj.closing_date)


@admin.register(EnglishAuction)
class EnglishAuctionAdmin(BaseAuctionAdmin):
    pass


@admin.register(DutchAuction)
class DutchAuctionAdmin(BaseAuctionAdmin):
    pass
