from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'service_qty', 'created_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'fullname',
        'profile_pic',
        'phone',
        'street1',
        'street2',
        'city',
        'state',
        'zipcode',
        'country',
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "image",
        "price",
        "discount_percentage",
        "duration",
        "created_at",
        "booking_count",
        "rating",
        "is_active",
    )

    search_fields = (
        "name",
        "category__name",
    )

    list_filter = (
        "category",
        "is_active",
        "discount_percentage"
    )

    ordering = (
        "-booking_count",
    )

    readonly_fields = (
        "updated_at",
    )

    list_per_page = 20