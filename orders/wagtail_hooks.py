from django.urls import path, reverse
from wagtail.admin.menu import MenuItem
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail import hooks

from .views import view_orders, view_order_detail
from .models import Address, DeliveryDetail, StoreSettings, Order, OrderItem


@hooks.register('register_admin_urls')
def register_view_orders_url():
    return [
        path('orders/', view_orders, name="view_orders"),
        path('orders/<int:order_id>/', view_order_detail, name="view_order_detail"),
    ]

@hooks.register('register_admin_menu_item')
def register_view_orders_menu_item():
    return MenuItem('View Orders', reverse('view_orders'), icon_name='doc-full')


@register_snippet
class OrderSnippetViewSet(SnippetViewSet):
    model = Order
    add_to_admin_menu = True
    menu_label = "Orders"

@register_snippet
class OrderItemSnippetViewSet(SnippetViewSet):
    model = OrderItem
    add_to_admin_menu = True
    menu_label = "Order Items"


@register_snippet
class AddressSnippetViewSet(SnippetViewSet):
    model = Address
    add_to_admin_menu = True
    menu_label = "Addresses"
    list_display = [
        "street",
        "town",
        "postcode",
        ]
    search_fields = ["street", "town", "postcode"]
    panels = [
        FieldPanel("street"),
        FieldPanel("town"),
        FieldPanel("postcode"),
    ]


@register_snippet
class DeliveryDetailSnippetViewSet(SnippetViewSet):
    model = DeliveryDetail
    add_to_admin_menu = True
    menu_label = "Delivery Details"
    list_display = [
        "delivery_method",
        "requested_delivery_date",
        "additional_requirements",
        ]
    search_fields = ["delivery_method", "requested_delivery_date"]
    panels = [
        FieldPanel("delivery_method"),
        FieldPanel("requested_delivery_date"),
        FieldPanel("additional_requirements"),
    ]


@register_snippet
class StoreSettingsSnippetViewSet(SnippetViewSet):
    model = StoreSettings
    add_to_admin_menu = True
    menu_label = "Store Settings"
    list_display = [
        "allow_delivery",
        "allow_collection",
        "delivery_charge",
        ]
    search_fields = ["allow_delivery", "allow_collection", "delivery_charge"]
    panels = [
        FieldPanel("allow_delivery"),
        FieldPanel("allow_collection"),
        FieldPanel("delivery_charge"),
    ]
    # 🔒 Prevent creating more than one
    def has_add_permission(self, request):
        return not StoreSettings.objects.exists()
