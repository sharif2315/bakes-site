from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from utils.products import build_cart_context


@require_POST
def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    quantity = int(request.POST.get("quantity", 1))
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + quantity

    request.session["cart"] = cart

    # Return just the updated cart count in cart template partial
    return render(request, "products/cart/cart.html", {"cart_total": sum(cart.values())})


@require_http_methods(["DELETE"])
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session["cart"] = cart

    context = build_cart_context(cart)
    return render(request, "products/cart/cart.html", context)