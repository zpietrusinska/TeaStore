from django.contrib import admin

from .models import TeaCategory, Origin, Tea, Order, OrderItem


@admin.register(TeaCategory)
class TeaCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ["country_code", "region", "farm_name", "is_organic"]
    list_filter = ["country_code", "is_organic"]
    search_fields = ["region", "farm_name"]


@admin.register(Tea)
class TeaAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "tea_type", "caffeine_level", "price", "stock_qty", "is_active"]
    list_filter = ["category", "tea_type", "caffeine_level", "is_active"]
    search_fields = ["name"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "created_at", "delivery_date"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "tea", "quantity", "unit_price"]
    list_filter = ["tea"]
