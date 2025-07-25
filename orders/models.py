import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone

from products.models import Product
from .constants import DELIVERY_METHOD_CHOICES, DELIVERY_METHOD_DELIVERY


class Address(models.Model):
    street = models.CharField(max_length=100)
    town = models.CharField(max_length=20)
    postcode = models.CharField(max_length=10)

    @property
    def single_line(self):
        parts = [self.street, self.town, self.postcode]
        return ", ".join(part for part in parts if part)


class DeliveryDetail(models.Model):
    delivery_method = models.CharField(
        max_length=10,
        choices=DELIVERY_METHOD_CHOICES,
    )
    requested_delivery_date = models.DateField()
    additional_requirements = models.TextField(blank=True, null=True)


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("dispatched", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("collected", "Collected"),
    ]    
    STATUS_COLOR_MAP = {
        "pending": "bg-yellow-500",
        "confirmed": "bg-blue-500",
        "dispatched": "bg-purple-500",
        "delivered": "bg-green-500",
        "collected": "bg-green-500",
    }
    order_ref = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True, null=True)
    delivery_detail = models.ForeignKey('DeliveryDetail', on_delete=models.CASCADE)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    deposit_paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order for {self.first_name} {self.last_name} on {self.created_at}'
    
    def is_delivery(self):
        return self.delivery_detail.delivery_method == DELIVERY_METHOD_DELIVERY
    
    def check_order_validity(self):
        """
        Check if the order is still valid based on its creation time.
        This can be used to ensure that the order confirmation page is only accessible
        for a limited time after the order is placed.
        """
        max_age_hours = 48

        if self.created_at < timezone.now() - timedelta(hours=max_age_hours):
            return False
        return True
    
    def status_color(self):
        return self.STATUS_COLOR_MAP.get(self.status, "bg-neutral-400")    

    @property
    def subtotal(self):
        return sum(item.price * item.quantity for item in self.items.all())

    @property
    def total(self):
        return self.subtotal + self.delivery_charge
    
    @property
    def contact(self):
        return self.phone or self.email

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or ""




class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Copy of product price at time of order

    def __str__(self):
        return f'{self.product.title} x {self.quantity} - (£{self.get_total()})'
    
    def get_total(self):
        return self.quantity * self.price
    

"""
1.Add an expiration or max-age (optional)
If the order confirmation page is only meant to be viewed for a short period (e.g. 24 or 48h),
you can add a check to ensure that the order is still valid when the user tries to access it. This can be done by checking the `created_at` timestamp of the order.

if order.created_at < timezone.now() - timedelta(hours=48):
    raise Http404()

2. Dont display sensitive information - address, phone, email
"""