from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Shop, SellerProduct, ProductVariant
from products.models import BaseProduct

@login_required
def customer_home(request):
    query = request.GET.get('q', '')
    shops = Shop.objects.filter(is_active=True)
    if query:
        shops = shops.filter(name__icontains=query)
    shops_with_count = []
    for shop in shops:
        count = shop.products.filter(is_available=True).count()
        shops_with_count.append({'shop': shop, 'product_count': count})
    return render(request, 'customer/home.html', {'shops': shops_with_count, 'query': query})

@login_required
def shop_detail(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, is_active=True)
    seller_products = SellerProduct.objects.filter(shop=shop, is_available=True)
    
    categories = {}
    for sp in seller_products:
        variants = sp.variants.filter(stock__gt=0)
        if variants.exists():
            cat_name = sp.base_product.category.name if sp.base_product.category else 'Other'
            if cat_name not in categories:
                categories[cat_name] = []
            for variant in variants:
                variant.seller_product = sp
                categories[cat_name].append(variant)
    
    return render(request, 'customer/shop_detail.html', {
        'shop': shop,
        'categories': categories,
    })