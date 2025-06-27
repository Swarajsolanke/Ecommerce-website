from django.shortcuts import render, redirect,HttpResponseRedirect,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, ProductCategory, Wishlist
from django.db import transaction
from django.utils.html import escape
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.db.models import Q

# Create your views here.

# Home page
def home(request):
    featured_products = Product.objects.all()[:4]
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        wishlist_count = wishlist.products.count()
    return render(request, 'store/home.html', {'featured_products': featured_products, 'wishlist_count': wishlist_count})

# Products page
def products(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    selected_category = None
    # Auto-create demo categories/products if empty
    if not categories.exists() and not products.exists():
        with transaction.atomic():
            cat1 = ProductCategory.objects.create(name='Electronics')
            cat2 = ProductCategory.objects.create(name='Clothing')
            cat3 = ProductCategory.objects.create(name='Books')
            Product.objects.create(name='Smartphone', description='Latest smartphone with advanced features', price=499.99, category=cat1)
            Product.objects.create(name='Laptop', description='Powerful laptop for work and gaming', price=999.99, category=cat1)
            Product.objects.create(name='T-Shirt', description='Comfortable cotton t-shirt for daily wear', price=19.99, category=cat2)
            Product.objects.create(name='Jeans', description='Stylish blue jeans for casual look', price=39.99, category=cat2)
            Product.objects.create(name='Novel', description='Bestselling novel with gripping story', price=14.99, category=cat3)
        categories = ProductCategory.objects.all()
        products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
        selected_category = ProductCategory.objects.get(id=category_id)
    if query:
        # Enhanced search: search in name, description, and category
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__name__icontains=query)
        )
    wishlist_products = []
    wishlist_count = 0
    if request.user.is_authenticated:
        try:
            wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
            wishlist_products = list(wishlist.products.all())
            wishlist_count = wishlist.products.count()
        except Exception:
            wishlist_products = []
            wishlist_count = 0
    return render(request, 'store/products.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': selected_category,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count,
    })

# Cart page
def cart(request):
    wishlist_count = 0
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('signin'))
       # return render(request, 'store/signin.html', {'cart_items': [], 'total': 0, 'wishlist_count': wishlist_count})
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist_count = wishlist.products.count()
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total, 'wishlist_count': wishlist_count})

# Orders page
def orders(request):
    wishlist_count = 0
    if not request.user.is_authenticated:
        return render(request, 'store/orders.html', {'orders': [], 'wishlist_count': wishlist_count})
    orders = request.session.get('orders', [])
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist_count = wishlist.products.count()
    return render(request, 'store/orders.html', {'orders': orders, 'wishlist_count': wishlist_count})

# Checkout page
def checkout(request):
    wishlist_count = 0
    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in to checkout.')
        return redirect('signin')
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    order_summary = []
    total = 0
    for item in cart_items:
        order_summary.append({'name': item.product.name, 'quantity': item.quantity, 'price': float(item.product.price), 'subtotal': float(item.product.price) * item.quantity})
        total += item.product.price * item.quantity
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist_count = wishlist.products.count()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        address = request.POST.get('address', '').strip()
        email = request.POST.get('email', '').strip()
        if not name or not address or not email:
            messages.error(request, 'Please fill in all fields.')
        elif not cart_items:
            messages.error(request, 'Your cart is empty.')
        else:
            # Store order in session for demo
            orders = request.session.get('orders', [])
            for item in order_summary:
                orders.append({'name': item['name'], 'price': item['subtotal'], 'quantity': item['quantity'], 'address': escape(address), 'email': escape(email)})
            request.session['orders'] = orders
            # Clear cart
            cart.items.all().delete()
            messages.success(request, 'Order placed successfully!')
            return render(request, 'store/checkout.html', {'order_placed': True, 'order_summary': order_summary, 'total': total, 'wishlist_count': wishlist_count})
    return render(request, 'store/checkout.html', {'order_summary': order_summary, 'total': total, 'wishlist_count': wishlist_count})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('signup')
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'store/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('signin')
    return render(request, 'store/signin.html')

def signout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='signin')
def add_to_cart(request):
    product_id = request.GET.get('product_id')
    if not product_id:
        return redirect('products')
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return render(request, 'store/add_to_cart.html', {'product': product, 'in_cart': True})

@login_required(login_url='signin')
def order_product(request):
    product_id = request.GET.get('product_id')
    if not product_id:
        return redirect('products')
    product = Product.objects.get(id=product_id)
    # For demo, store orders in session or user object (in real app, use Order model)
    orders = request.session.get('orders', [])
    orders.append({'name': product.name, 'price': float(product.price)})
    request.session['orders'] = orders
    return render(request, 'store/add_to_cart.html', {'product': product, 'ordered': True})

@login_required(login_url='signin')
def profile(request):
    user = request.user
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        wishlist_count = wishlist.products.count()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'edit_profile':
            # Handle profile editing
            email = request.POST.get('email', '').strip()
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            
            if email:
                user.email = email
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
            
        elif action == 'change_password':
            # Handle password change
            current_password = request.POST.get('current_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return redirect('profile')
            
            if new_password1 != new_password2:
                messages.error(request, 'New passwords do not match.')
                return redirect('profile')
            
            if len(new_password1) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return redirect('profile')
            
            user.set_password(new_password1)
            user.save()
            messages.success(request, 'Password changed successfully! Please sign in again.')
            return redirect('signin')
            
        elif action == 'reset_password':
            # Handle password reset
            email = request.POST.get('reset_email', '').strip()
            
            if not email:
                messages.error(request, 'Please provide an email address.')
                return redirect('profile')
            
            try:
                user_to_reset = User.objects.get(email=email)
                request.session['reset_user_id'] = user_to_reset.id
                messages.success(request, f'Password reset link sent to {email}. Please check your email.')
                return redirect('password_reset_confirm')
            except ObjectDoesNotExist:
                messages.error(request, 'No user found with that email address.')
                return redirect('profile')
    
    return render(request, 'store/profile.html', {'user': user, 'wishlist_count': wishlist_count})

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
            request.session['reset_user_id'] = user.id
            return redirect('password_reset_confirm')
        except ObjectDoesNotExist:
            messages.error(request, 'No user found with that email.')
    return render(request, 'store/password_reset.html')

def password_reset_confirm(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, 'Invalid or expired password reset session.')
        return redirect('password_reset')
    if request.method == 'POST':
        password = request.POST.get('password', '').strip()
        password2 = request.POST.get('password2', '').strip()
        if not password or not password2:
            messages.error(request, 'Please fill in both password fields.')
        elif password != password2:
            messages.error(request, 'Passwords do not match.')
        else:
            user = User.objects.get(id=user_id)
            user.password = make_password(password)
            user.save()
            del request.session['reset_user_id']
            messages.success(request, 'Password reset successful. You can now sign in.')
            return redirect('signin')
    return render(request, 'store/password_reset_confirm.html')

@require_POST
@login_required(login_url='signin')
def place_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')
    orders = request.session.get('orders', [])
    for item in cart_items:
        orders.append({
            'name': item.product.name,
            'price': float(item.product.price) * item.quantity,
            'quantity': item.quantity
        })
    request.session['orders'] = orders
    cart.items.all().delete()
    messages.success(request, 'Order placed successfully!')
    return redirect('cart')

@require_POST
@login_required(login_url='signin')
def add_to_wishlist(request):
    product_id = request.POST.get('product_id')
    if not product_id:
        return redirect('products')
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect(request.META.get('HTTP_REFERER', 'products'))

@require_POST
@login_required(login_url='signin')
def remove_from_wishlist(request):
    product_id = request.POST.get('product_id')
    if not product_id:
        return redirect('wishlist')
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')

@login_required(login_url='signin')
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    count = products.count()
    return render(request, 'store/wishlist.html', {'products': products, 'count': count, 'wishlist_count': count})
