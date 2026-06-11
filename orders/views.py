from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from shops.models import ProductVariant, Shop
from .models import Cart, Order, OrderItem

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(customer=request.user).select_related(
        'variant__seller_product__base_product',
        'variant__seller_product__shop'
    )
    cart_by_shop = {}
    total = 0
    for item in cart_items:
        shop_name = item.variant.seller_product.shop.name
        if shop_name not in cart_by_shop:
            cart_by_shop[shop_name] = []
        cart_by_shop[shop_name].append(item)
        total += item.get_total()
    return render(request, 'customer/cart.html', {
        'cart_by_shop': cart_by_shop,
        'total': total
    })

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        quantity = int(request.POST.get('quantity', 1))
        shop_id = request.POST.get('shop_id')
        variant = get_object_or_404(ProductVariant, id=variant_id)
        cart_item, created = Cart.objects.get_or_create(
            customer=request.user,
            variant=variant,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        messages.success(request, f'{variant.seller_product.base_product.name} added to cart.')
        return redirect(f'/shop/{shop_id}/')
    return redirect('/')

@login_required
def update_cart(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(Cart, id=cart_id, customer=request.user)
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('/cart/')

@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart_item = get_object_or_404(Cart, id=cart_id, customer=request.user)
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    return redirect('/cart/')

@login_required
@transaction.atomic
def checkout(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(customer=request.user).select_related(
            'variant__seller_product__shop'
        )
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('/cart/')

        # Group by shop
        orders_by_shop = {}
        for item in cart_items:
            shop = item.variant.seller_product.shop
            if shop.id not in orders_by_shop:
                orders_by_shop[shop.id] = {'shop': shop, 'items': []}
            orders_by_shop[shop.id]['items'].append(item)

        # Create one order per shop
        for shop_id, data in orders_by_shop.items():
            order = Order.objects.create(
                customer=request.user,
                shop=data['shop'],
                status='pending'
            )
            for item in data['items']:
                OrderItem.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    price_at_order=item.variant.price,
                    is_confirmed=False
                )

        # Clear cart
        cart_items.delete()
        messages.success(request, 'Orders placed successfully! Waiting for seller confirmation.')
        return redirect('/orders/')
    return redirect('/cart/')

@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'customer/orders.html', {'orders': orders})