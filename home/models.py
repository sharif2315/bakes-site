from django.db import models
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings


from wagtail.models import Page, Orderable
from wagtail.blocks import (
    StructBlock,CharBlock,TextBlock, ListBlock, ChoiceBlock  
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField
from modelcluster.fields import ParentalKey

from home.forms import ContactForm


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


class ContactSubmission(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.submitted_at:%Y-%m-%d}"


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


    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                # Save to database
                ContactSubmission.objects.create(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    message=form.cleaned_data['message'],
                )

                # Send email
                send_mail(
                    subject='Contact Form Submission',
                    message=form.cleaned_data['message'],
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_FORM_RECEIVER],
                )

                messages.success(request, "Thanks! Your message has been sent.")
                return redirect(request.path)
        else:
            form = ContactForm()

        context = self.get_context(request)
        context['form'] = form
        return render(request, self.template, context)

