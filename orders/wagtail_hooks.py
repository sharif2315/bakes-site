from django.urls import path, reverse

from wagtail.admin.menu import MenuItem
from wagtail import hooks

from .views import view_orders, view_order_detail


@hooks.register('register_admin_urls')
def register_view_orders_url():
    return [
        path('orders/', view_orders, name="view_orders"),
        path('orders/<int:order_id>/', view_order_detail, name="view_order_detail"),
    ]

@hooks.register('register_admin_menu_item')
def register_view_orders_menu_item():
    return MenuItem('Orders', reverse('view_orders'), icon_name='doc-full', order=200)
