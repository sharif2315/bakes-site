from products.models import Product


def cart_total(request):
    cart = request.session.get("cart", {})
    cart_total = sum(cart.values())
    
    return {
        "cart_total": cart_total
    }


def cart_items(request):
    cart = request.session.get("cart", {})

    if not cart:
        return {"cart_items": [], "cart_total_price": 0}

    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.live().filter(id__in=product_ids)

    items = []
    total_price = 0

    for product in products:
        quantity = cart.get(str(product.id), 0)
        price = product.price
        total = price * quantity
        total_price += total
        first_image = product.product_images.first()

        items.append({
            "id": product.id,
            "title": product.title,
            "category": product.category,
            "price": price,
            "quantity": quantity,
            "total": total,
            "url": product.url,
            "image": first_image.image if first_image else None,

        })

    return {
        "cart_items": items,
        "cart_total_price": total_price,
    }