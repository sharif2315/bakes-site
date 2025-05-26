from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel


class RecipeIndex(Page):
    max_count = 1
    template = "recipes/recipes_index.html"
    # subpage_types = ['blog.RecipePage']

    subtitle = models.CharField(max_length=100, blank=True)
    description = RichTextField(
        blank=True,
        features=['h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr']
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('description'),
    ]

