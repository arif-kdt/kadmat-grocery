from django.contrib import admin
from .models import Category, BaseProduct

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','created_at']
    search_fields = ['name']

@admin.register(BaseProduct)
class BaseProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['name']