from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
from django.http import HttpResponseBadRequest, HttpRequest
from django.contrib.postgres.search import SearchVector, SearchQuery
from wagtail.admin.auth import permission_required

from utils.products import build_cart_context
from home.models import HomePage
from products.models import Product
from .models import OrderItem, Order, StoreSettings, DeliveryDetail
from .forms import OrderForm, AddressForm, DeliveryDetailForm
from .constants import DELIVERY_METHOD_COLLECTION, DELIVERY_METHOD_CHOICES


@require_POST
def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    quantity = int(request.POST.get("quantity", 1))
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + quantity

    request.session["cart"] = cart
    context = { "cart_total": sum(cart.values()) }

    # Return just the updated cart count in cart template partial
    return render(request, "orders/cart/_cart_update_fragments.html", context)


@require_http_methods(["DELETE"])
def remove_item_from_cart_slideover(request, product_id):
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session["cart"] = cart

    context = build_cart_context(cart)
    return render(request, "orders/cart/_cart_update_fragments.html", context)


@require_POST
def update_item_quantity(request, product_id):
    action = request.POST.get("action")
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)

    current_qty = cart.get(product_id_str, 1)

    if action == "increment":
        new_qty = current_qty + 1
    elif action == "decrement":
        new_qty = max(1, current_qty - 1)  # Prevent going below 1
    else:
        return HttpResponseBadRequest("Invalid action")

    cart[product_id_str] = new_qty
    request.session["cart"] = cart

    context = build_cart_context(cart)
    return render(request, "orders/cart/_cart_update_fragments.html", context)


def checkout(request):
    home_page_url = HomePage.objects.first().url if HomePage.objects.exists() else '/'
    cart = request.session.get('cart', {})
    # context = build_cart_context(cart)

    if not cart:
        return redirect(home_page_url)

    context = {
        'custom_page_title': 'Checkout',
        'breadcrumbs': [
            { 'title': 'Home', 'url': home_page_url },
            { 'title': 'Checkout' }
        ],
    }

    if request.method == 'POST':
        delivery_method = request.POST.get('delivery_method')

        order_form = OrderForm(request.POST)
        address_form = AddressForm(request.POST, delivery_method=delivery_method)
        delivery_form = DeliveryDetailForm(request.POST)

        context.update(build_cart_context(cart)) 

        if order_form.is_valid() and address_form.is_valid() and delivery_form.is_valid():
            # print("All forms are valid")
            address = address_form.save() if delivery_method != DELIVERY_METHOD_COLLECTION else None
            delivery_detail = delivery_form.save()

            order = order_form.save(commit=False)
            order.delivery_detail = delivery_detail
            
            if delivery_method == 'delivery':
                order.delivery_charge = StoreSettings.objects.first().delivery_charge  # or a fixed value
            else:
                order.delivery_charge = Decimal('0.00')

            if address:
                order.address = address
            order.save()

            # Add Order Items
            for item in context['cart_items']:
                OrderItem.objects.create(
                    order=order,
                    product=Product.objects.get(id=item['id']),
                    quantity=item['quantity'],
                    price=item['price'] / item['quantity']  # unit price
                )

            # Clear cart
            request.session['cart'] = {}
            return redirect('order_confirmation', order_ref=order.order_ref)
        else:            
            context['form_errors'] = True
            if order_form.errors:
                print("order form errors:", order_form.errors)
            
            if address_form.errors:
                print("Address Form errors:", address_form.errors)
            
            if delivery_form.errors:
                print("Delivery Form errors:", delivery_form.errors)
    else:
        settings = StoreSettings.objects.first()
        allowed_methods = []

        if settings.allow_delivery:
            allowed_methods.append('delivery')
        if settings.allow_collection:
            allowed_methods.append('collection') 
        
        order_form = OrderForm()
        address_form = AddressForm()
        delivery_form = DeliveryDetailForm()

        context.update({
            'allowed_methods': allowed_methods,
        })

    context.update({
        'order_form': order_form,
        'address_form': address_form,
        'delivery_form': delivery_form,
    })

    return render(request, 'orders/checkout/checkout.html', context)


@require_http_methods(["DELETE"])
def remove_item_from_checkout(request, product_id):
    cart = request.session.get("cart", {})

    # Remove item
    cart.pop(str(product_id), None)
    request.session["cart"] = cart

    context = build_cart_context(cart)
    return render(request, "orders/cart/_cart_update_fragments.html", context)


def order_confirmation(request, order_ref):
    # home_page_url = HomePage.objects.first().url if HomePage.objects.exists() else '/'
    
    order = Order.objects.get(order_ref=order_ref)

    for item in order.items.all():
        item.total_price = item.price * item.quantity
        item.first_image = item.product.product_images.first()
    
    context = {
        'custom_page_title': 'Order Confirmation',
        # 'breadcrumbs': [
        #     { 'title': 'Home', 'url': home_page_url },
        #     { 'title': 'Order Confirmation' }
        # ],
        'order': order,
    }
    return render(request, 'orders/checkout/order_confirmation.html', context)


# ADMIN VIEWS

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@permission_required('wagtailadmin.access_admin')
def view_orders(request: HttpRequest):
    query = request.GET.get('q')
    order_status = request.GET.get('order_status')
    delivery_method = request.GET.get('delivery_method')
    page = request.GET.get('page', 1)

    orders = Order.objects.select_related('address').order_by('-created_at')

    if query:
        search_vector = SearchVector(
            'first_name', 'last_name', 'email', 'phone', 'status', 
            'address__street', 'address__town', 'address__postcode'
        )
        search_query = SearchQuery(query)
        orders = orders.annotate(search=search_vector).filter(search=search_query)
    
    status_choices = [ val for val,label in Order.STATUS_CHOICES ]
    if order_status in status_choices:
        orders = orders.filter(status=order_status)

    if delivery_method in dict(DELIVERY_METHOD_CHOICES):
        orders = orders.filter(delivery_detail__delivery_method=delivery_method)
    
    paginator = Paginator(orders, 3)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = { 
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'delivery_methods': DELIVERY_METHOD_CHOICES,
    }

    if request.headers.get("HX-Request") == "true":
        return render(request, 'orders/admin/partials/_orders_table.html', context)

    return render(request, "orders/admin/orders.html", context)


@permission_required('wagtailadmin.access_admin')
@require_http_methods(["GET", "POST"])
def view_order_detail(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        deposit_paid = request.POST.get("deposit_paid") == "on"
        status = request.POST.get("status")

        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if status not in valid_statuses:
            return HttpResponseBadRequest("Invalid status.")        

        order.deposit_paid = deposit_paid
        order.status = status
        order.save()

        return redirect('view_order_detail', order_id=order.id)
    
    context = { 'order': order }
    return render(request, "orders/admin/order_detail.html", context)


@permission_required('wagtailadmin.access_admin')
@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    deposit_paid = request.POST.get("deposit_paid") == "on"
    status = request.POST.get("status")

    order.deposit_paid = deposit_paid
    order.status = status
    order.save()

    return render(request, "orders/admin/partials/order_detail_content.html", {"order": order})

