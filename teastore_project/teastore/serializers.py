from django.contrib.auth.models import User
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

    def validate_country_code(self, value):
        if len(value) != 2 or not value.isalpha() or not value.isupper():
            raise serializers.ValidationError(
                "Kod kraju musi skladac sie z 2 wielkich liter, np. PL."
            )
        return value


class TeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tea
        fields = "__all__"
        read_only_fields = ["added_at"]

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Nazwa herbaty jest wymagana.")
        first_char = value[0]
        if not first_char.isupper():
            raise serializers.ValidationError(
                "Nazwa herbaty powinna zaczynac sie wielka litera."
            )
        return value

    def validate(self, data):
        price = data.get("price")
        stock_qty = data.get("stock_qty")

        if price is not None and price <= 0:
            raise serializers.ValidationError({"price": "Cena musi byc wieksza od 0."})
        if stock_qty is not None and stock_qty < 0:
            raise serializers.ValidationError(
                {"stock_qty": "Stan magazynowy nie moze byc ujemny."}
            )
        return data


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

    def validate(self, data):
        quantity = data.get("quantity")
        unit_price = data.get("unit_price")

        if quantity is not None and quantity <= 0:
            raise serializers.ValidationError(
                {"quantity": "Ilosc musi byc wieksza od 0."}
            )
        if unit_price is not None and unit_price <= 0:
            raise serializers.ValidationError(
                {"unit_price": "Cena jednostkowa musi byc wieksza od 0."}
            )
        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["created_at", "user"]

    def validate_delivery_date(self, value):
        from django.utils import timezone

        if value and value < timezone.localdate():
            raise serializers.ValidationError("Data dostawy nie moze byc z przeszlosci.")
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
