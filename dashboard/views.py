from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from shops.models import Shop
from orders.models import Order
from products.models import BaseProduct

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('/')
    context = {
        'total_users': User.objects.count(),
        'total_sellers': User.objects.filter(role='seller').count(),
        'total_customers': User.objects.filter(role='customer').count(),
        'total_shops': Shop.objects.count(),
        'total_products': BaseProduct.objects.count(),
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'recent_orders': Order.objects.order_by('-created_at')[:10],
        'recent_sellers': User.objects.filter(role='seller').order_by('-date_joined')[:5],
    }
    return render(request, 'dashboard/admin.html', context)