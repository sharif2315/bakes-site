# home/context_processors.py
from blog.models import RecipeIndex

def recipe_index_link(request):
    recipe_index = RecipeIndex.objects.live().first()
    return {'recipe_index': recipe_index}
