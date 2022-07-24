from django.contrib import admin

from .models import MarketplaceService, BuyOrRentDeal

# Register your models here.

admin.site.register(MarketplaceService)
admin.site.register(BuyOrRentDeal)

