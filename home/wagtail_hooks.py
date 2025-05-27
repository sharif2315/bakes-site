from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import SvgIcon

@register_snippet
class TagSnippetViewSet(SnippetViewSet):
    model = SvgIcon
    # icon = "tag"
    add_to_admin_menu = True
    menu_label = "SVG Icons"
    menu_order = 200
    list_display = ["name", "icon"]
    search_fields = ["name",]
    panels = [
        FieldPanel("name"),
        FieldPanel("icon"),
    ]
