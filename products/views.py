from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.shortcuts import render


@require_POST
def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})

    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1

    # clear cart - TESTING ONLY
    # request.session["cart"] = {}

    request.session["cart"] = cart
    # print('cart session', request.session["cart"])


    # Return just the updated cart count in cart template partial
    return render(request, "products/cart.html", {"cart_total": sum(cart.values())})