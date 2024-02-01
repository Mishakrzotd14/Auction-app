from django.contrib import admin

from auction.models import EnglishAuction, DutchAuction
from lot.admin import LotInline


@admin.register(EnglishAuction)
class EnglishAuctionAdmin(admin.ModelAdmin):
    inlines = [LotInline]


@admin.register(DutchAuction)
class DutchAuctionAdmin(admin.ModelAdmin):
    inlines = [LotInline]
