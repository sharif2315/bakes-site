from django.urls import path
from .views import add_to_cart, remove_from_cart

urlpatterns = [
    path("add-to-cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart-remove-item/<int:product_id>/", remove_from_cart, name="remove_from_cart"),

]
