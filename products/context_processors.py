def cart_total(request):
    cart = request.session.get("cart", {})
    cart_total = sum(cart.values())

    # print('cart total from CP', cart_total)
    return {
        "cart_total": cart_total
    }