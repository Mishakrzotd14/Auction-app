from django.contrib import admin

from lot.models import Lot


class LotInline(admin.TabularInline):
    model = Lot
