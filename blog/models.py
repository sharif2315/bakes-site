from django.db import models
from django import forms
from django.utils import timezone
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag

from products.models import DietaryOption, Category
from utils.breadcrumbs import get_breadcrumbs


rt_features=['h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr']
rt_features_with_image = rt_features + ['image']

class RecipeIndex(Page):
    max_count = 1
    template = "recipes/recipes_index.html"
    subpage_types = ['blog.RecipePage']
    parent_page_types = ['home.HomePage']

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
        FieldPanel('description'),
        FieldPanel('featured_recipe'),
    ]

    def get_context(self, request: HttpRequest):
        context = super().get_context(request)

        query = request.GET.get('q')
        category_slugs = request.GET.getlist("category")
        dietary_slugs = request.GET.getlist("dietary")
        tag_names = request.GET.getlist('tags')

        # Exclude the featured recipe if it exists
        recipes = RecipePage.objects.live().order_by('-first_published_at') # [:3] for paging

        if query:
            vector = SearchVector("title", "description")
            search_query = SearchQuery(query)
            recipes = recipes.annotate(search=vector).filter(search=search_query)

        # Dietary filter (many-to-many)
        if dietary_slugs and dietary_slugs != ['']:
            recipes = recipes.filter(dietary_options__slug__in=dietary_slugs).distinct()

        # Category filter (foreign key)
        if category_slugs and category_slugs != ['']:
            recipes = recipes.filter(category__slug__in=category_slugs)

        if tag_names and tag_names != ['']:
            recipes = recipes.filter(tags__name__in=tag_names).distinct()

        if not query and self.featured_recipe:
            recipes = recipes.exclude(id=self.featured_recipe.id)

        context['recipes'] = recipes
        context['breadcrumbs'] = get_breadcrumbs(self)

        context["q"] = query
        context["selected_dietary"] = dietary_slugs
        context["selected_categories"] = category_slugs
        context["selected_tags"] = tag_names
        
        context["dietary_options"] = [
            {"label": d.name, "value": d.slug} for d in DietaryOption.objects.all()
        ]  
        
        context["category_options"] = [
            {"label": c.name, "value": c.slug} for c in Category.objects.all()
        ]

        context["tag_options"] = [
            {"label": t.name, "value": t.name} for t in Tag.objects.all()
        ]
        return context
    
    def serve(self, request):
        context = self.get_context(request)

        if request.headers.get("HX-Request") == "true":
            return render(request, "recipes/partials/_recipes_grid.html", context)

        return render(request, "recipes/recipes_index.html", context)


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
        features=rt_features_with_image,
    )
    method = RichTextField(
        blank=True,
        features=rt_features_with_image,
    )
    recipe_tips = RichTextField(
        blank=True,
        features=rt_features_with_image,
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

    def get_context(self, request):
        context = super().get_context(request)
        context['breadcrumbs'] = get_breadcrumbs(self)
        return context