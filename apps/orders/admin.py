from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "price", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "total", "status", "created_at", "user")
    list_filter = ("status", "created_at", "delivery_method", "payment_method")
    search_fields = ("full_name", "email", "phone")
    inlines = [OrderItemInline]
    readonly_fields = ("total", "created_at")
    list_editable = ("status",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_name", "price", "quantity")
    list_filter = ("order__status",)
