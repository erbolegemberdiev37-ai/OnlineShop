from rest_framework import serializers
from django.db import transaction
from apps.catalog.models import Product
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "product", "product_name", "price", "quantity")


class OrderItemCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True))
    quantity = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "full_name",
            "phone",
            "email",
            "address",
            "comment",
            "delivery_method",
            "payment_method",
            "status",
            "total",
            "created_at",
            "items",
        )
        read_only_fields = ("status", "total", "created_at")


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "full_name",
            "phone",
            "email",
            "address",
            "comment",
            "delivery_method",
            "payment_method",
            "items",
        )

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Заказ должен содержать хотя бы один товар.")
        return value

    def validate(self, attrs):
        items_data = attrs["items"]
        for item in items_data:
            product = item["product"]
            qty = item["quantity"]
            if product.stock < qty:
                raise serializers.ValidationError(
                    f"Недостаточно товара «{product.name}» на складе (доступно: {product.stock})."
                )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user
        if user.is_authenticated:
            validated_data["user"] = user

        total = 0
        order_items = []
        for item_data in items_data:
            product = item_data["product"]
            qty = item_data["quantity"]
            price = product.price
            total += price * qty
            order_items.append(
                {
                    "product": product,
                    "product_name": product.name,
                    "price": price,
                    "quantity": qty,
                }
            )

        order = Order.objects.create(total=total, **validated_data)

        for item in order_items:
            OrderItem.objects.create(order=order, **item)
            # уменьшаем остаток
            product = item["product"]
            product.stock -= item["quantity"]
            product.save(update_fields=["stock"])

        return order
