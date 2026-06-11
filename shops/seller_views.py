from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order, OrderItem
from .models import ProductVariant, SellerProduct, Shop

def seller_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'seller':
            return redirect('/login/')
        try:
            request.user.shop
        except Shop.DoesNotExist:
            messages.error(request, 'No shop found for your account.')
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper

@seller_required
def seller_dashboard(request):
    shop = request.user.shop
    pending_orders = Order.objects.filter(shop=shop, status='pending').order_by('-created_at')
    confirmed_orders = Order.objects.filter(shop=shop, status='confirmed').order_by('-created_at')
    ready_orders = Order.objects.filter(shop=shop, status='ready').order_by('-created_at')
    return render(request, 'seller/dashboard.html', {
        'shop': shop,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'ready_orders': ready_orders,
        'pending_count': pending_orders.count(),
        'confirmed_count': confirmed_orders.count(),
        'ready_count': ready_orders.count(),
        'collected_count': Order.objects.filter(shop=shop, status='collected').count(),
    })

@seller_required
def confirm_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        confirmed_item_ids = request.POST.getlist('confirm_items')
        order = get_object_or_404(Order, id=order_id, shop=request.user.shop)
        for item in order.items.all():
            if str(item.id) in confirmed_item_ids:
                item.is_confirmed = True
                item.save()
        order.status = 'confirmed'
        order.save()
        messages.success(request, f'Order #{order.id} confirmed.')
    return redirect('/seller/')

@seller_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, shop=request.user.shop)
    order.status = 'cancelled'
    order.save()
    messages.success(request, f'Order #{order.id} cancelled.')
    return redirect('/seller/')

@seller_required
def mark_ready(request, order_id):
    order = get_object_or_404(Order, id=order_id, shop=request.user.shop)
    order.status = 'ready'
    order.save()
    messages.success(request, f'Order #{order.id} marked as ready for pickup.')
    return redirect('/seller/')

@seller_required
def mark_collected(request, order_id):
    order = get_object_or_404(Order, id=order_id, shop=request.user.shop)
    order.status = 'collected'
    order.save()
    messages.success(request, f'Order #{order.id} marked as collected.')
    return redirect('/seller/')

@seller_required
def inventory(request):
    shop = request.user.shop
    seller_products = SellerProduct.objects.filter(shop=shop).select_related('base_product__category')
    inventory = {}
    for sp in seller_products:
        cat = sp.base_product.category.name if sp.base_product.category else 'Other'
        if cat not in inventory:
            inventory[cat] = []
        inventory[cat].append(sp)

    from products.models import BaseProduct, Category
    existing_ids = seller_products.values_list('base_product_id', flat=True)
    all_products = BaseProduct.objects.exclude(id__in=existing_ids).select_related('category')
    available_products = {}
    for p in all_products:
        cat = p.category.name if p.category else 'Other'
        if cat not in available_products:
            available_products[cat] = []
        available_products[cat].append(p)

    return render(request, 'seller/inventory.html', {
        'shop': shop,
        'seller_products': seller_products,
        'inventory': inventory,
        'available_products': available_products,
    })

@seller_required
def add_product(request):
    if request.method == 'POST':
        base_product_id = request.POST.get('base_product_id')
        local_name = request.POST.get('local_name', '')
        from products.models import BaseProduct
        base_product = get_object_or_404(BaseProduct, id=base_product_id)
        shop = request.user.shop
        sp, created = SellerProduct.objects.get_or_create(
            shop=shop,
            base_product=base_product,
            defaults={'local_name': local_name}
        )
        if created:
            messages.success(request, f'{base_product.name} added to your inventory.')
        else:
            messages.info(request, f'{base_product.name} already in your inventory.')
    return redirect('/seller/inventory/')

@seller_required
def toggle_product(request, sp_id):
    sp = get_object_or_404(SellerProduct, id=sp_id, shop=request.user.shop)
    sp.is_available = not sp.is_available
    sp.save()
    return redirect('/seller/inventory/')

@seller_required
def edit_product(request, sp_id):
    sp = get_object_or_404(SellerProduct, id=sp_id, shop=request.user.shop)
    if request.method == 'POST':
        sp.local_name = request.POST.get('local_name', '')
        sp.save()
        messages.success(request, 'Product updated.')
        return redirect(f'/seller/inventory/edit/{sp_id}/')
    return render(request, 'seller/edit_product.html', {
        'seller_product': sp,
        'unit_choices': ProductVariant.UNIT_CHOICES,
    })

@seller_required
def add_variant(request, sp_id):
    if request.method == 'POST':
        sp = get_object_or_404(SellerProduct, id=sp_id, shop=request.user.shop)
        ProductVariant.objects.create(
            seller_product=sp,
            unit=request.POST.get('unit'),
            custom_unit=request.POST.get('custom_unit', ''),
            quantity_per_unit=int(request.POST.get('quantity_per_unit', 1)),
            price=request.POST.get('price'),
            stock=int(request.POST.get('stock', 0))
        )
        messages.success(request, 'Variant added.')
    return redirect(f'/seller/inventory/edit/{sp_id}/')

@seller_required
def update_variant(request, variant_id):
    if request.method == 'POST':
        variant = get_object_or_404(ProductVariant, id=variant_id, seller_product__shop=request.user.shop)
        variant.unit = request.POST.get('unit')
        variant.custom_unit = request.POST.get('custom_unit', '')
        variant.quantity_per_unit = int(request.POST.get('quantity_per_unit', 1))
        variant.price = request.POST.get('price')
        variant.stock = int(request.POST.get('stock', 0))
        variant.save()
        messages.success(request, 'Variant updated.')
        return redirect(f'/seller/inventory/edit/{variant.seller_product.id}/')
    return redirect('/seller/inventory/')