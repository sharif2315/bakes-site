from django.urls import path
from . import views

urlpatterns = [
    path("checkout", views.checkout, name="checkout"),  
    
    path("order-confirmation/<str:order_ref>/", views.order_confirmation, name="order_confirmation"),  

    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart-remove-item/<int:product_id>/", views.remove_item_from_cart_slideover, name="remove_item_from_cart_slideover"),
    path("checkout-remove-item/<int:product_id>/", views.remove_item_from_checkout, name="remove_item_from_checkout"),
    path("checkout-update-item/<int:product_id>/", views.update_item_quantity, name="update_item_quantity"),
]
