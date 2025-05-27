from django.db import models

from wagtail.models import Page, Orderable
from wagtail.blocks import (
    StructBlock,CharBlock,TextBlock, ListBlock, ChoiceBlock  
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField
from modelcluster.fields import ParentalKey


class AboutFeatureBlock(StructBlock):
    svg_icon = CharBlock(help_text="SVG path or class")  # or use custom block to validate svg uploads
    title = CharBlock()
    description = TextBlock()


class AboutSectionBlock(StructBlock):
    image = ImageChooserBlock()
    title = CharBlock()
    description = TextBlock()
    features = ListBlock(
        AboutFeatureBlock(), 
        max_num=3    
    )
"""
{% for block in page.about_sections %}
    {% if block.block_type == 'about_section' %}

        <div>
            <p>{{ block.value.title }}</p>
            <p>{{ block.value.description }}</p>

            {% image block.value.image original as image %}
            <p>{{ image.url }}</p>
        </div>
        
    {% endif %}
{% endfor%}
"""
    # class Meta:
    #     template = "blocks/about_section.html"
    #     icon = "user"


class SvgIcon(models.Model):
    name = models.CharField(max_length=100)
    icon = models.TextField(help_text="Paste full inline SVG code here.")


    # panels = [
    #     FieldPanel('name'),
    #     FieldPanel('icon'),
    # ]

    def __str__(self):
        return self.name


class ContactMethod(Orderable):
    page = ParentalKey('home.HomePage', related_name='contact_methods')
    svg_icon = models.ForeignKey(SvgIcon, null=True, blank=True, on_delete=models.SET_NULL)
    contact_text = models.CharField(max_length=255)

    def __str__(self):
        return self.contact_text

    # panels = [
    #     FieldPanel('svg_icon'),
    #     FieldPanel('contact_text'),
    # ]


class GalleryImage(Orderable):
    page = ParentalKey('home.HomePage', related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    # panels = [
    #     FieldPanel('image'),
    # ]


class OpeningHour(Orderable):
    page = ParentalKey('home.HomePage', related_name='opening_hours')
    day = models.CharField(max_length=9)
    hours = models.CharField(max_length=50)

    # panels = [
    #     FieldPanel('day'),
    #     FieldPanel('hours'),
    # ]


# === Main HomePage ===

class HomePage(Page):
    template = "home/home_page.html"
    max_count = 1
    # subpage_types = ['blog.RecipeIndex']

    # Hero
    hero_title = models.CharField(max_length=255)
    hero_description = models.TextField()
    hero_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    hero_image_url = models.URLField(
        blank=True,
        help_text="Optional. Used only if uploaded image is not provided."
    )

        # About
    about_sections = StreamField(
        [("about_section", AboutSectionBlock())],
        use_json_field=True,
        blank=True,
        max_num=2,
        verbose_name="About Sections"
    )

    # Gallery
    gallery_title = models.CharField(max_length=255)

    # Contact
    contact_title = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        # Hero
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_description'),
            FieldPanel('hero_image'),
            FieldPanel('hero_image_url'),
        ], heading="Hero Section"),
        
        # About
        FieldPanel('about_sections'),

        # Gallery
        MultiFieldPanel([
            FieldPanel('gallery_title'),
            InlinePanel('gallery_images', label="Gallery Images"),
        ], heading="Gallery Section"),

        # Contact
        MultiFieldPanel([
            FieldPanel('contact_title'),
            InlinePanel('contact_methods', label="Contact Methods (max 3)", max_num=3),
        ], heading="Contact Section"),

        # Opening Hours
        InlinePanel('opening_hours', label="Opening Hours", max_num=7),
    ]
