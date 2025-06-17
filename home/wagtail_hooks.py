from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import SvgIcon, ContactSubmission, SocialMediaLink

@register_snippet
class TagSnippetViewSet(SnippetViewSet):
    model = SvgIcon
    icon = "doc-empty"
    add_to_admin_menu = True
    menu_label = "SVG Icons"
    menu_order = 230
    list_display = ["name", "icon"]
    search_fields = ["name",]
    panels = [
        FieldPanel("name"),
        FieldPanel("icon"),
    ]        

@register_snippet
class ContactSubmissionViewSet(SnippetViewSet):
    model = ContactSubmission
    icon = "mail"
    add_to_admin_menu = True
    menu_label = "Contact Submissions"
    menu_order = 250
    list_display = ["first_name", "last_name", "email", "submitted_at"]
    search_fields = ["first_name", "last_name", "email"]
    panels = [
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("email"),
        FieldPanel("message"),

    ]
    
    # def get_queryset(self):
    #     return self.model.objects.order_by("-submitted_at")

        # Disable add, edit, and delete


@register_snippet
class SocialMediaLinkViewSet(SnippetViewSet):
    model = SocialMediaLink
    icon = "media"
    add_to_admin_menu = True
    menu_label = "Social Links"
    menu_order = 240
    list_display = [
        "icon", 
        "url"
        ]
    search_fields = ["url", "icon"]
    panels = [
        FieldPanel("url"),
        FieldPanel("icon"),
    ]