import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone
from products.models import Product


    # TODO: return error if both delivery and pickup are disabled
    # def save(self):
    #     if not self.allow_delivery and not self.allow_pickup:
    #         raise models.ValidationError("At least one of delivery or pickup must be enabled.")

    # TODO: if Pickup, order delivery_charge should be 0.00
    # TODO: Max row count for StoreSettings should be 1

class StoreSettings(models.Model):
    allow_delivery = models.BooleanField(default=True)
    allow_pickup = models.BooleanField(default=True)
    delivery_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=5.00,
        help_text="Charge for delivery service",
    )

    def __str__(self):
        return "Store Settings"

    class Meta:
        verbose_name = "Store Settings"
        verbose_name_plural = "Store Settings"

class Address(models.Model):
    street = models.CharField(max_length=100)
    town = models.CharField(max_length=20)
    postcode = models.CharField(max_length=10)


class DeliveryDetail(models.Model):
    delivery_method_choices = [
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
    ]
    delivery_method = models.CharField(
        max_length=10,
        choices=delivery_method_choices,
        default='delivery',
    )
    requested_delivery_date = models.DateField()
    additional_requirements = models.TextField(blank=True, null=True)


class Order(models.Model):
    order_ref = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True, null=True)
    delivery_detail = models.ForeignKey('DeliveryDetail', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Copy of product price at time of order

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