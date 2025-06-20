# home/context_processors.py
from blog.models import RecipeIndex
from products.models import ProductListing
from home.models import HomePage, SocialMediaLink


def custom_context(request):
    product_listing = ProductListing.objects.live().only('title').first()
    recipe_index = RecipeIndex.objects.live().only('title').first()
    home_page = HomePage.objects.live().only('title').first()

    return {
        'product_listing': {
            'title': product_listing.title,
            'url': product_listing.url,
        } if product_listing else None,
        
        'recipe_index': {
            'title': recipe_index.title,
            'url': recipe_index.url,
        } if recipe_index else None,
        
        'home_page': {
            'title': home_page.title,
            'url': home_page.url,
        } if home_page else None,
    }

def get_social_links(request):
    social_links = SocialMediaLink.objects.all()
    return { 'social_links': social_links }