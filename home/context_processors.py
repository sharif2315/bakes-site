# home/context_processors.py
from blog.models import RecipeIndex
from products.models import ProductListing

def custom_context(request):
    product_listing = ProductListing.objects.live().first()
    recipe_index = RecipeIndex.objects.live().first()
    return {
        'product_listing': product_listing, 
        'recipe_index': recipe_index,
        }
