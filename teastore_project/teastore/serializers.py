from rest_framework import serializers

from .models import TeaCategory, Origin, Tea, Order, OrderItem


class TeaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeaCategory
        fields = "__all__"


class OriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = "__all__"


class TeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tea
        fields = "__all__"
        read_only_fields = ["added_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["created_at"]
