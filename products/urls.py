
from django.urls import path
from products import views as product_views

urlpatterns = [
    path("products/", product_views.products_listing, name="products_listings"),
    path("products/1", product_views.product_post, name="product_post"),

]