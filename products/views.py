from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from products.models import Product

@require_POST
def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    quantity = int(request.POST.get("quantity", 1))
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + quantity

    # clear cart - TESTING ONLY
    # request.session["cart"] = {}

    request.session["cart"] = cart
    # print('cart session', request.session["cart"])

    # Return just the updated cart count in cart template partial
    return render(request, "products/cart.html", {"cart_total": sum(cart.values())})


@require_http_methods(["DELETE"])
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session["cart"] = cart

    # Rebuild context
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.live().filter(id__in=product_ids)

    items = []
    total_price = 0

    for product in products:
        quantity = cart.get(str(product.id), 0)
        total = product.price * quantity
        total_price += total
        first_image = product.product_images.first()

        items.append({
            "id": product.id,
            "title": product.title,
            "category": product.category,
            "price": product.price,
            "quantity": quantity,
            "total": total,
            "url": product.url,
            "image": first_image.image if first_image else None,
        })

    context = {
        "cart_items": items,
        "cart_total_price": total_price,
        "cart_total": sum(cart.values()),
        "cart": cart,
    }

    # This template includes the OOB partials
    return render(request, "products/cart.html", context)