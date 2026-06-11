from django.urls import path
from . import views, seller_views

urlpatterns = [
    path('', views.customer_home, name='home'),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('seller/', seller_views.seller_dashboard, name='seller_dashboard'),
    path('seller/orders/confirm/', seller_views.confirm_order, name='confirm_order'),
    path('seller/orders/cancel/<int:order_id>/', seller_views.cancel_order, name='cancel_order'),
    path('seller/orders/ready/<int:order_id>/', seller_views.mark_ready, name='mark_ready'),
    path('seller/orders/collected/<int:order_id>/', seller_views.mark_collected, name='mark_collected'),
    path('seller/inventory/', seller_views.inventory, name='inventory'),
    path('seller/inventory/add/', seller_views.add_product, name='add_product'),
    path('seller/inventory/toggle/<int:sp_id>/', seller_views.toggle_product, name='toggle_product'),
    path('seller/inventory/edit/<int:sp_id>/', seller_views.edit_product, name='edit_product'),
    path('seller/inventory/variant/add/<int:sp_id>/', seller_views.add_variant, name='add_variant'),
    path('seller/inventory/variant/update/<int:variant_id>/', seller_views.update_variant, name='update_variant'),
]