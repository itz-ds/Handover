from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True)

    @property
    def as_class(self):
        return self.name.lower().strip().replace(' ','-')

    def __str__(self):
        return self.name

class Service(models.Model):

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.URLField()

    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(default=0)

    duration = models.DurationField()

    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    booking_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_new(self):
        return (timezone.now().date() - self.created_at.date()).days <= 45

    @property
    def on_discount(self):
        return self.discount_percentage > 0

    @property
    def discount_price(self):
        return self.price - (self.price * self.discount_percentage / 100)
    
    @property
    def saved_price(self):
        return self.price * self.discount_percentage / 100

    @property
    def is_under_hour(self):
        return int(self.duration.total_seconds()) <= 3600

    @property
    def is_quick_service(self):
        return int(self.duration.total_seconds()) <= 10800

    @property
    def duration_text(self):
        total_minutes = int(self.duration.total_seconds() // 60)

        hours = total_minutes // 60
        days = hours // 24
        minutes = total_minutes % 60

        if days:
            if days > 1:
                return f'{days} days'
            else:
                return f'{days} day'
        elif hours:
            if hours > 1:
                return f'{hours} hrs'
            else:
                return f'{hours} hr'
        elif minutes:
            if minutes > 1:
                return f'{minutes} mins'
            else:
                return f'{minutes} min'

    @property
    def is_upcoming(self):
        return (self.created_at.date() - timezone.now().date()).days > 0

    

    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    fullname = models.CharField(max_length = 150)
    profile_pic = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=10)
    street1 = models.CharField(max_length=150)
    street2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=150, default='India')

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    service = models.ForeignKey(
        Service,
        on_delete = models.CASCADE
    )
    service_qty = models.PositiveIntegerField(blank=False, null = False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.service.discount_price * self.service_qty

    def __str__(self):
        return '{} - {}'.format(self.id, self.user.username)

class Order(models.Model):

    user = models.ForeignKey(
            User,
            on_delete = models.CASCADE
        )
    fullname = models.CharField(max_length = 150)
    email = models.EmailField(max_length = 150)
    phone = models.CharField(max_length=10)
    street1 = models.CharField(max_length=150)
    street2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    country = models.CharField(max_length=150, default='India')
    zipcode = models.CharField(max_length=10)
    total_price = models.FloatField(null=False)
    payment_modes = (
        ('Cash On Delivery', 'Cash On Delivery'),
        ('UPI', 'UPI'),
        ('Internet Banking', 'Internet Banking'),
        ('Debit Card', 'Debit Card'),
        ('Credit Card', 'Credit Card'),
    )
    payment_mode = models.CharField(max_length=150, choices=payment_modes, default = 'Cash On Delivery')
    payment_id = models.CharField(max_length=250, null =True)
    order_statuses = (
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Cancelled','Cancelled'),
        ('On Service','On Service'),
        ('Completed','Completed'),
    )
    status = models.CharField(max_length=150,choices=order_statuses, default='Pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)

class OrderService(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.order.id} - {self.order.tracking_no}'
