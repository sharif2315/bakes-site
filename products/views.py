from django.shortcuts import render


def products_listing(request):
    return render(request, "products/products_listing.html", {'times': range(10)})


def product_post(request):
    return render(request, "products/product_post.html")