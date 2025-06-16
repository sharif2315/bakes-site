# context_processors.py
from utils.products import build_cart_context


def cart_items(request):
    cart = request.session.get("cart", {})
    return build_cart_context(cart)