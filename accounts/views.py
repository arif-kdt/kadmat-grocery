from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from shops.models import Shop
from .models import User

def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect_by_role(user)
        return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')

def redirect_by_role(user):
    if user.role == 'admin':
        return redirect('/dashboard/')
    elif user.role == 'seller':
        return redirect('/seller/')
    else:
        return redirect('/')

def register_customer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        full_name = request.POST.get('full_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'accounts/register_customer.html', {'error': 'Passwords do not match'})

        # Check if seller already exists with this username — add customer role to them
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            if existing_user.role == 'seller':
                if not existing_user.check_password(password1):
                    return render(request, 'accounts/register_customer.html', {'error': 'Username already taken by another account'})
                existing_user.is_customer = True
                existing_user.save()
                messages.success(request, 'Customer access added to your seller account.')
                login(request, existing_user)
                return redirect('/')
            return render(request, 'accounts/register_customer.html', {'error': 'Username already taken'})

        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register_customer.html', {'error': 'Email already registered'})

        names = full_name.split(' ', 1)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            phone=phone,
            role='customer',
            is_customer=True,
            is_seller=False,
            first_name=names[0],
            last_name=names[1] if len(names) > 1 else ''
        )
        login(request, user)
        messages.success(request, 'Account created successfully! Welcome to Kadmat Grocery.')
        return redirect('/')
    return render(request, 'accounts/register_customer.html')

def register_seller(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        full_name = request.POST.get('full_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        shop_name = request.POST.get('shop_name')
        shop_phone = request.POST.get('shop_phone')
        location = request.POST.get('location')

        if password1 != password2:
            return render(request, 'accounts/register_seller.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register_seller.html', {'error': 'Username already taken'})
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register_seller.html', {'error': 'Email already registered'})

        names = full_name.split(' ', 1)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            phone=phone,
            role='seller',
            is_seller=True,
            is_customer=True,
            first_name=names[0],
            last_name=names[1] if len(names) > 1 else ''
        )
        Shop.objects.create(
            seller=user,
            name=shop_name,
            phone=shop_phone,
            location=location
        )
        login(request, user)
        messages.success(request, 'Shop registered successfully! Welcome to Kadmat Grocery.')
        return redirect('/seller/')
    return render(request, 'accounts/register_seller.html')