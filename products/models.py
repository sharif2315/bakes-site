from django.db import models
from django import forms

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel

from modelcluster.fields import ParentalKey, ParentalManyToManyField



class ProductListing(Page):
    max_count = 1
    template = "products/products_listing.html"
    parent_page_types = ['home.HomePage']
    subpage_types = ['products.Product']

    subtitle = models.CharField(max_length=100, blank=True)
    description = RichTextField(
        blank=True,
        features=['h2', 'h3', 'bold'],
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('description'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['products'] = Product.objects.live().order_by('-first_published_at')
        return context


class ProductImage(models.Model):
    product = ParentalKey('Product', related_name='product_images', on_delete=models.CASCADE)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+'
    )

    panels = [
        FieldPanel('image'),
    ]

    def __str__(self):
        return f"Image for {self.product.title}"


class DietaryOption(models.Model):
    COLOUR_CHOICES = [
        ("red", "Red"),
        ("green", "Green"),
        ("orange", "Orange"),
        ("blue", "Blue"),
        ("purple", "Purple"),
        ("gray", "Gray"),
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, help_text="Optional description of the dietary option (e.g. Vegan, Gluten-Free)")
    colour = models.CharField(max_length=20, choices=COLOUR_CHOICES, default="gray")

    def __str__(self):
        return self.name


class Product(Page):
    parent_page_types = ['products.ProductListing']
    subpage_types = []
    template = "products/product_detail.html"

    description = RichTextField(blank=False, features=['h2', 'h3', 'bold', 'italic'])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dietary_options = ParentalManyToManyField(
        "products.DietaryOption", 
        blank=True,
        related_name="products"
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel("dietary_options", widget=forms.CheckboxSelectMultiple),
        InlinePanel('product_images', label="Product Images", min_num=1, max_num=3),
    ]

    def __str__(self):
        return self.title