# products/utils.py
from products.models import Product

def build_cart_context(cart):
    if not cart:
        return {
            "cart_items": [],
            "cart_total_price": 0,
            "cart_total": 0,
            "cart": {},
        }

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

    return {
        "cart_items": items,
        "cart_total_price": total_price,
        "cart_total": sum(cart.values()),
        "cart": cart,
    }
