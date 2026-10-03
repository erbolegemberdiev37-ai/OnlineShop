from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent", "image", "is_active")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "is_main")


class ProductListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка товаров."""
    category = CategorySerializer(read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "sku",
            "price",
            "old_price",
            "stock",
            "category",
            "main_image",
            "is_active",
            "created_at",
        )

    def get_main_image(self, obj):
        main = obj.images.filter(is_main=True).first()
        if main:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(main.image.url)
            return main.image.url
        # fallback — первое изображение
        first = obj.images.first()
        if first:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(first.image.url)
            return first.image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Полный сериализатор для карточки товара."""
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "sku",
            "description",
            "price",
            "old_price",
            "stock",
            "category",
            "images",
            "is_active",
            "created_at",
            "updated_at",
        )
