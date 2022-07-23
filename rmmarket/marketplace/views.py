from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from django.shortcuts import render
from rest_framework import authentication, status
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from .models import BuyOrRentDeal, MarketplaceService
from .serializers import BuyOrRentDealSerializer, MarketplaceServiceSerializer


# Create your views here.


class UserBuyOrRentDealListAPIView(ListAPIView):
    serializer_class = BuyOrRentDealSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return BuyOrRentDeal.objects.filter(user_id=user_id).order_by('date')


class CreateDealAPIView(APIView):
    serializer_class = BuyOrRentDealSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=BuyOrRentDealSerializer, responses={status.HTTP_201_CREATED: ''})
    def post(self, request):
        user_data = check_auth(request)
        if user_data.get('pk'):
            deal, _ = BuyOrRentDeal.objects.get_or_create(
                user_id=user_data['pk'],
                commercial_id=request.data['commercial_id'],
                price=request.data['price'],
                deal_type=request.data['deal_type'],
                expires=request.data['expires']
            )
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


def check_auth(request):
    auth_header = authentication.get_authorization_header(request).split()
    auth_header_prefix = settings.AUTHENTICATION_HEADER_PREFIX.lower()

    if not auth_header:
        return

    if len(auth_header) == 1:
        return

    elif len(auth_header) > 2:
        return

    prefix = auth_header[0].decode('utf-8')
    token = auth_header[1].decode('utf-8')

    if prefix.lower() != auth_header_prefix:
        return

    res = requests.get(headers={'Authorization': f'{prefix} {token}'}, url=settings.AUTH_SERVICE_URL + 'user/')
    return res.json()


class UpdateDealStatusAPIView(APIView):
    serializer_class = BuyOrRentDealSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'commercial_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='commercial apart id'),
            'owner_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='owner id'),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='status'),
        },
    ),
        responses={
            status.HTTP_200_OK: ''
        }
    )
    def post(self, request, deal_id):
        user_data = check_auth(request)
        if user_data.get('pk'):
            if user_data['is_staff']:
                deal = BuyOrRentDeal.objects.get(pk=deal_id)
                deal.status = request.data['status']
                if request.data['status'] == '3':
                    if deal.deal_type == '1':
                        requests.post(settings.AUTH_SERVICE_URL + 'updaterole/', data={
                            'role': 'Renter',
                        })
                        requests.put(settings.COMMERCIAL_URL + '/', data={
                            'id': request.data['commercial_id'],
                            'owner_id': request.data['owner_id'],
                            'status': 'Rented'
                        })
                    else:
                        requests.post(settings.AUTH_SERVICE_URL + 'updaterole/', data={
                            'role': 'Owner',
                        })
                        requests.put(settings.COMMERCIAL_URL + '/', data={
                            'id': request.data['commercial_id'],
                            'owner_id': request.data['owner_id'],
                            'status': 'Owned'
                        })
                deal.save(updated_fields=('status',))
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)


class DealListAPIView(ListAPIView):
    serializer_class = BuyOrRentDealSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return BuyOrRentDeal.objects.filter(status='1').order_by('-date')


class MarketplaceServiceListAPIView(ListCreateAPIView):
    serializer_class = MarketplaceServiceSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        user_data = check_auth(request)
        if user_data.get('pk'):
            if user_data['is_staff']:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
