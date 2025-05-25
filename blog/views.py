from django.shortcuts import render

# Create your views here.
def recipes_index(request):
    """
    Render the recipes index page.
    """
    return render(request, "recipes/recipes_index.html", {'times': range(10)})

def recipe_post(request):
    """
    Render a single recipe post page."""
    return render(request, "recipes/recipe_post.html")