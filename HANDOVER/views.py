from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
import json, random
from decimal import Decimal
from django.db.models import Q
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

# SERVICE_VIEWS


def home(request):
    categories = Category.objects.all()
    new_services = Service.objects.order_by('-created_at')[:8]
    most_booked = Service.objects.order_by('-booking_count')[:8]
    discount_services = Service.objects.order_by('-discount_percentage')[:8]
    cleaning_services = Service.objects.filter(Q(name__icontains='cleaning'))[:8]
    installation_services = Service.objects.filter(Q(name__icontains='installation'))[:8]

    return render(request, 'index.html', {'categories': categories,'most_booked':most_booked, 'new_services': new_services, 'discount_services': discount_services, 'cleaning_services': cleaning_services, 'installation_services': installation_services})

def services(request):
    all_services = Service.objects.all()
    categories = Category.objects.all()
    in_cart = Service.objects.none()
    if request.user.is_authenticated:
        in_cart = Service.objects.filter(
            cart__user = request.user
        )
    return render(request, 'services.html', {'all_services':all_services, 'categories': categories, 'in_cart': in_cart})

def service(request, id):

    service = get_object_or_404(Service, id=id)
    other_services_in_cateogry = Service.objects.filter(
        category = service.category
    ).exclude(id=id)
    other_categories = Category.objects.exclude(id=service.category.id)
    in_cart=[]
    if request.user.is_authenticated:
        in_cart = Service.objects.filter(
            cart__user = request.user
        )
        print(in_cart)
    return render(
        request,
        'service.html',
        {
            'service': service,
            'other_services_in_category' : other_services_in_cateogry,
            'in_cart': in_cart,
            'other_categories': other_categories
        }
    )

def category(request, id):

    category = get_object_or_404(Category, id=id)
    other_categories = Category.objects.exclude(id=id)
    services = Service.objects.filter(category = category)
    if request.user.is_authenticated:
        in_cart = Service.objects.filter(
            cart__user = request.user
        )
    
    return render(request, 'category.html', {'category': category, 'services': services, 'in_cart': in_cart, 'other_categories':other_categories})

#CART_VIEWS

def add_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            service_id = data["service_id"]
            service = get_object_or_404(Service, id=service_id)
            if service:
                if (Cart.objects.filter(user = request.user.id, service_id = service_id)):
                    summary = cart_summary(request)
                    return JsonResponse({'status':'Service Already in Cart', **summary})
                else:
                    cart_item = Cart.objects.create(
                        user = request.user,
                        service = service
                    )
                    summary = cart_summary(request)
                    return JsonResponse({'status': 'Service added successfully',
                                        'cart_id': cart_item.id,
                                        'service_id': service.id,
                                        'service_name': service.name,
                                        'service_image': service.image,
                                        'service_duration': service.duration_text,
                                        'is_under_hour': service.is_under_hour,
                                        'service_url': reverse('service', kwargs={'id': service.id}),
                                        **summary})
            else:
                return JsonResponse({'status': 'No such service found'})
        else:
            return JsonResponse({'status': 'Login to Continue'})
    return redirect('home')

def update_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            cart_id = data['cart_id']

            cart = get_object_or_404(Cart, id=cart_id, user=request.user)
            
            if cart:
                cart.service_qty = data['qty']
                cart.save()
                summary = cart_summary(request)
                return JsonResponse({'status': 'Cart Updated', **summary})
            else:
                return JsonResponse({'status': 'No such service found in Cart'})
        return JsonResponse({'status': 'Login to Continue'}, status=401)
    return JsonResponse({'status': 'Invalid request'}, status=400)
    

def del_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            cart_id = data['cart_id']

            cart = get_object_or_404(Cart, id=cart_id, user=request.user)
            
            if cart:
                cart.delete()
                summary = cart_summary(request)
                return JsonResponse({'status': 'Cart removed', **summary})
            else:
                return JsonResponse({'status': 'No such service found in Cart'})
        return JsonResponse({'status': 'Login to Continue'}, status=401)
    return JsonResponse({'status': 'Invalid request'}, status=400)

def cartview(request):
    cart = Cart.objects.filter(user = request.user)
    summary = cart_summary(request)

    return render(request, 'cart.html', {'cart': cart, **summary})

def cart_summary(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_count = cart_items.count()
    

    subtotal = 0
    for item in cart_items:
        subtotal += item.total_price

    total_discount = 0
    for item in cart_items:
        total_discount += item.total_discount

    actual_price = 0
    for item in cart_items:
        actual_price += item.actual_price

    gst = round(subtotal * Decimal("0.18"),2)
    total = subtotal + gst

    print(subtotal, actual_price)

    return {
        'cart_count': cart_count,
        'subtotal': subtotal,
        'actual_price': actual_price,
        'total_discount': total_discount,
        'gst': gst,
        'total': total
    }

def cart_data(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_count = cart_items.count()
    return {
        'cart_count': cart_count,
        'mini_cart': cart_items
    }


#CHECKOUT_VIEWS

@login_required(login_url='user_login')
def checkout(request):
    rawcart = Cart.objects.filter(user=request.user)

    for item in rawcart:
        if not item.service.is_active:
            Cart.objects.delete(id = item.id, user = request.user)

    cart = Cart.objects.filter(user=request.user)
    summary = cart_summary(request)
    profile = get_object_or_404(UserProfile, user=request.user)

    form = UserProfileForm(instance=profile)

    return render (request, 'checkout.html', {
        'cart': cart,
        **summary,
        'profile': profile,
        'form': form
    })

@login_required(login_url='user_login')
def place_order(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
            cart_items = Cart.objects.filter(user=request.user)
            summary = cart_summary(request)
            print(summary)
            new_order = Order()

            new_order.user = request.user
            new_order.fullname = user_profile.fullname
            new_order.email = request.user.email
            new_order.phone = user_profile.phone
            new_order.street1 = user_profile.street1
            new_order.street2 = user_profile.street2
            new_order.city = user_profile.city
            new_order.state = user_profile.state
            new_order.country = user_profile.country
            new_order.zipcode = user_profile.zipcode
            new_order.actual_price = summary['actual_price']
            new_order.gst = summary['gst']
            new_order.subtotal = summary['subtotal']
            new_order.total_price = summary['total']
            # new_order.payment_mode =
            # new_order.payment_id =
            # new_order.status =
            # new_order.message =
            new_order.tracking_no = trakenumber()
            new_order.save()

            for item in cart_items:
                OrderService.objects.create(
                    order = new_order,
                    service = item.service,
                    price = item.service.discount_price,
                    quantity = item.service_qty
                )

            Cart.objects.filter(user = request.user).delete()

            messages.success(request, 'Order Placed')
    return redirect('home')

def trakenumber():
    trackno = 'HD'+str(random.randint(11111111,99999999))
    while Order.objects.filter(tracking_no=trackno).exists():
        trackno = 'HD'+str(random.randint(11111111,99999999))

    return trackno


#USER_VIEWS

def user_board(request):
    if not request.user.is_authenticated:
            return redirect('home')

    profile, created = UserProfile.objects.get_or_create(
            user=request.user
        )

    bookings_count = Order.objects.filter(user = request.user).count()
    print(type(bookings_count), bookings_count)
    
    return render(request, 'user-board.html', {'profile': profile, 'created':created, 'bookings_count': bookings_count})

@login_required(login_url='user_login')
def user_bookings(request):

    orders = Order.objects.filter(user = request.user)

    context ={
        'orders': orders
    }
    return render(request, 'user-bookings.html', context)

@login_required(login_url='user_login')
def booking_details(request, tracking_no):

    order = Order.objects.get(tracking_no = tracking_no)
    services = OrderService.objects.filter(order = order)

    context ={
        'order': order,
        'services': services
    }
    return render(request, 'user-booking-details.html', context)

def user_details(request):
    if not request.user.is_authenticated:
        return redirect('home')

    profile = UserProfile.objects.get(
        user=request.user
    )
    
    if request.method == 'POST':

        form = UserProfileForm(request.POST, instance = profile)

        if form.is_valid():
            form.save()
            return redirect('user_board')
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'user-details.html', {'form':form, 'profile': profile})

def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CustomUserForm()
        if request.method == 'POST':
            form = CustomUserForm(request.POST)
            print(form.is_valid())
            if form.is_valid():
                form.save()
                return redirect('user_login')
            else:
                print(form.errors)
        return render(request, 'user-register.html', {'form':form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(
                request,
                username = username,
                password = password
                )
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in')
                return redirect('home')
            else:
                messages.error(request, 'Invalid Username or Password')
                return redirect('user_login')
        return render(request, 'user-login.html')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)   
        messages.success(request, 'Logged out')
    return redirect('home')
