"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('service/<int:id>', views.service, name='service'),
    path('category/<int:id>', views.category, name='category'),

    path('cart/', views.cartview, name='cart'),
    path('add-cart/', views.add_cart, name='add_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('del-cart/', views.del_cart, name='del_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),

    path('user-board/', views.user_board, name='user_board'),
    path('user-details/', views.user_details, name='user_details'),
    path('user-bookings/', views.user_bookings, name='user_bookings'),
    path('bookings/<slug:tracking_no>', views.booking_details, name='booking_details'),
    path('user-register/', views.user_register, name='user_register'),
    path('user-login/', views.user_login, name='user_login'),
    path('user-logout/', views.user_logout, name='user_logout'),

    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]
