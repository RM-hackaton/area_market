from rest_framework import serializers

from .models import BuyOrRentDeal, MarketplaceService


class BuyOrRentDealSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuyOrRentDeal
        fields = ('pk', 'user_id', 'commercial_id', 'price', 'deal_type', 'status', 'expires')


class MarketplaceServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketplaceService
        fields = ('name', 'image', 'url', 'descr')
