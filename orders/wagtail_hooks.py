from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Order, Address, DeliveryDetail, StoreSettings, OrderItem

@register_snippet
class OrdersSnippetViewSet(SnippetViewSet):
    model = Order
    # icon = "cart"
    add_to_admin_menu = True
    menu_label = "Orders"
    # menu_order = 200
    list_display = [
        "order_ref",
        "first_name",
        "last_name",
        "email",
        "phone",
        "address",
        "delivery_detail",
        ]
    search_fields = ["name",]
    # index_template_name = "wagtailsnippets/orders/order/index.html"
    index_template_name = "orders/admin/orders.html"
    # panels = [
    #     FieldPanel("name"),
    #     FieldPanel("description"),
    #     FieldPanel("colour"),
    # ]


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
