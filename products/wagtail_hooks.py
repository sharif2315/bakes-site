from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import DietaryOption, Category

@register_snippet
class TagSnippetViewSet(SnippetViewSet):
    model = DietaryOption
    add_to_admin_menu = True
    menu_label = "Dietary Options"
    menu_order = 200
    list_display = ["name", "description", "colour"]
    search_fields = ["name",]
    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("colour"),
    ]

@register_snippet
class CategoryViewSet(SnippetViewSet):
    model = Category
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Categories"
    menu_order = 210
    list_display = ["name", "description"]
    search_fields = ["name",]
    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]