from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from .views import *


app_name = 'marketplace'
urlpatterns = [
    path('userdeals/', UserBuyOrRentDealListAPIView.as_view()),
    path('createdeal/', CreateDealAPIView.as_view()),
    path('updatestatus/', UpdateDealStatusAPIView.as_view()),
    path('deals/', DealListAPIView.as_view()),
    path('marketplace/', MarketplaceServiceListAPIView.as_view()),
    path('createservice/', MarketplaceServiceListAPIView.as_view())
]
