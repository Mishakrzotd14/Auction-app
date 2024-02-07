from django.contrib import admin
from auction.tasks import open_auction_task, close_auction_task
from auction.models import EnglishAuction, DutchAuction
from django.db import transaction

from lot.admin import LotInline


@admin.register(EnglishAuction)
class EnglishAuctionAdmin(admin.ModelAdmin):
    inlines = [LotInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        open_auction_task.apply_async(args=(obj.id,), eta=obj.opening_date)
        close_auction_task.apply_async(args=(obj.id,), eta=obj.closing_date)


@admin.register(DutchAuction)
class DutchAuctionAdmin(admin.ModelAdmin):
    inlines = [LotInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        open_auction_task.apply_async(args=(obj.id,), eta=obj.opening_date)
        close_auction_task.apply_async(args=(obj.id,), eta=obj.closing_date)
