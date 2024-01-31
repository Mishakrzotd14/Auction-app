from django.contrib import admin

from auction.models import EnglishAuction, DutchAuction
from lot.models import Lot


class LotInline(admin.TabularInline):
    model = Lot


@admin.register(EnglishAuction)
class EnglishAuctionAdmin(admin.ModelAdmin):
    inlines = [LotInline]


@admin.register(DutchAuction)
class DutchAuctionAdmin(admin.ModelAdmin):
    inlines = [LotInline]
