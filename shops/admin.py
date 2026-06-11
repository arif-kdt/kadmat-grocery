from django.contrib import admin
from .models import Shop, SellerProduct, ProductVariant

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'phone', 'location', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'seller__username']

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(SellerProduct)
class SellerProductAdmin(admin.ModelAdmin):
    list_display = ['base_product', 'shop', 'local_name', 'is_available']
    list_filter = ['is_available', 'shop']
    search_fields = ['base_product__name', 'shop__name']
    inlines = [ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['seller_product', 'unit', 'price', 'stock']
    list_filter = ['unit']