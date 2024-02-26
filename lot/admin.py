from django.contrib import admin

from lot.models import Lot, Offer


class LotInline(admin.TabularInline):
    model = Lot


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("user", "lot", "price", "date_creation",)