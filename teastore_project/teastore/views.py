from rest_framework import viewsets

from .models import TeaCategory, Origin, Tea, Order, OrderItem
from .serializers import (
    TeaCategorySerializer,
    OriginSerializer,
    TeaSerializer,
    OrderSerializer,
    OrderItemSerializer,
)


class TeaCategoryViewSet(viewsets.ModelViewSet):
    queryset = TeaCategory.objects.all()
    serializer_class = TeaCategorySerializer


class OriginViewSet(viewsets.ModelViewSet):
    queryset = Origin.objects.all()
    serializer_class = OriginSerializer


class TeaViewSet(viewsets.ModelViewSet):
    queryset = Tea.objects.all()
    serializer_class = TeaSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
