from django.db import models
from django import forms
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from products.models import DietaryOption

from django.utils import timezone

rt_features=['h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr']

class RecipeIndex(Page):
    max_count = 1
    template = "recipes/recipes_index.html"
    # subpage_types = ['blog.RecipePage']
    parent_page_types = ['home.HomePage']

    subtitle = models.CharField(max_length=100, blank=True)
    description = RichTextField(
        blank=True,
        features=rt_features,
    )

    featured_recipe = models.ForeignKey(
        'blog.RecipePage', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+',
        help_text="Featured recipe to display on the Recipes Index page"
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('description'),
        FieldPanel('featured_recipe'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['recipes'] = RecipePage.objects.live().order_by('-first_published_at') #[:3] for paging
        return context


class RecipePageTags(TaggedItemBase):
    content_object = ParentalKey(
        'blog.RecipePage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class RecipePage(Page):
    parent_page_types = ['blog.RecipeIndex']
    subpage_types = []  # No subpages allowed
    template = "recipes/recipe_post.html"

    summary = models.CharField(
        max_length=255, 
        blank=True, 
    )
    main_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    description = RichTextField(
        blank=True,
        features=rt_features,
    )
    category = models.ForeignKey(
        'products.Category', 
        null=True, blank=True, 
        on_delete=models.SET_NULL, 
        related_name='recipes',
    )
    prepare = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Preparation time"
    )
    cook = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Cooking time"
    )
    # TODO: Update template to dispay prepare and cook times correctly
    serves = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Number of servings"
    )
    dietary_options = ParentalManyToManyField(
        DietaryOption, 
        blank=True,
        related_name="recipes",
    )
    ingredients = RichTextField(
        blank=True,
        features=rt_features,
    )
    method = RichTextField(
        blank=True,
        features=rt_features,
    )
    recipe_tips = RichTextField(
        blank=True,
        features=rt_features,
    )

    tags = ClusterTaggableManager(
        through=RecipePageTags,
        blank=True,
    )
    date_posted = models.DateField(
        "Date Posted",
        default=timezone.now,
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [   
                FieldPanel('summary'),
                FieldRowPanel([
                    FieldPanel('category'),
                   FieldPanel('date_posted'),
                ]),
                FieldPanel('main_image'),

            ],
            heading="Recipe Details",
        ),
        
        FieldRowPanel([
            FieldPanel("dietary_options", widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
        ]),
        FieldRowPanel([
            FieldPanel('prepare'),
            FieldPanel('cook'),
            FieldPanel('serves'),
        ]),
        FieldPanel('description'),
        FieldPanel('ingredients'),
        FieldPanel('method'),
        FieldPanel('recipe_tips'),
    ]

