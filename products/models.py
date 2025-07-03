from django.db import models
from django import forms
from django.utils.text import slugify

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField


from utils.breadcrumbs import get_breadcrumbs


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
        context['breadcrumbs'] = get_breadcrumbs(self)

        # Fetch and map dietary options from DB
        context['dietary_options'] = [
            {'label': option.name, 'value': option.name.lower()}
            for option in DietaryOption.objects.all()
        ]

        # Fetch and map categories from DB
        context['category_options'] = [
            {'label': category.name, 'value': category.name.lower()}
            for category in Category.objects.all()
        ]

        # Handle selected filters
        dietary_param = request.GET.get('dietary', '')
        categories_param = request.GET.get('categories', '')

        context['selected_dietary'] = dietary_param.split(',') if dietary_param else []
        context['selected_categories'] = categories_param.split(',') if categories_param else []

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


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, help_text="Description of the product category")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Product Categories"
        verbose_name = "Product Category"


class DietaryOption(models.Model):
    COLOUR_CHOICES = [
        ("#e7000b", "Red"),
        ("#5ea500", "Green"),
        ("#ff8904", "Orange"),
        ("#51a2ff", "Blue"),
        ("#c27aff", "Purple"),
        ("#fda5d5", "Pink"),
        ("#99a1af", "Gray"),
    ]
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, help_text="Optional description of the dietary option (e.g. Vegan, Gluten-Free)")
    colour = models.CharField(max_length=20, choices=COLOUR_CHOICES, default="gray")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
    category = models.ForeignKey(
        'products.Category', 
        null=True, blank=True, 
        on_delete=models.SET_NULL, 
        related_name='products'
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('category'),
        FieldPanel("dietary_options", widget=forms.CheckboxSelectMultiple),
        InlinePanel('product_images', label="Product Images", min_num=1, max_num=3),
    ]

    def __str__(self):
        return self.title
    
    def get_context(self, request):
        context = super().get_context(request)
        context['breadcrumbs'] = get_breadcrumbs(self)
        return context

    @property
    def first_image(self):
        return self.product_images.first().image if self.product_images.exists() else None