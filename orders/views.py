from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from utils.products import build_cart_context


def checkout(request):
    return render(request, 'orders/checkout/checkout.html', {'custom_page_title': 'Checkout' })


@require_POST
def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    quantity = int(request.POST.get("quantity", 1))
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + quantity

    request.session["cart"] = cart

    # Return just the updated cart count in cart template partial
    return render(request, "orders/cart/cart.html", {"cart_total": sum(cart.values())})


@require_http_methods(["DELETE"])
def remove_item_from_cart_slideover(request, product_id):
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session["cart"] = cart

    context = build_cart_context(cart)
    return render(request, "orders/cart/cart.html", context)


@require_http_methods(["DELETE"])
def remove_item_from_checkout(request, product_id):
    cart = request.session.get("cart", {})

    # Remove item
    cart.pop(str(product_id), None)
    request.session["cart"] = cart

    context = build_cart_context(cart)

    return render(request, "orders/cart/_cart_update_fragments.html", context)


"""
fields for Order:

- first name, last name
- phone
- email
- address, drop off location? station?


- delivery option - pickup or delivery? depends on admins selection dropdown or single value
= requested delivery date
- Additional Requirements?

- total price

Settings:
- delivery charge
- email to, email from? or keep in settings via env vars?

"""
