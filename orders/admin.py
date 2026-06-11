from django.contrib import admin
from .models import Cart, Order, OrderItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'variant', 'quantity', 'added_at']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'shop', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['customer__username', 'shop__name']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'variant', 'quantity', 'price_at_order', 'is_confirmed']