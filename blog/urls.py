
from django.urls import path
from blog import views as recipe_views

urlpatterns = [
    path("recipes/", recipe_views.recipes_index, name="recipes_index"),
    path("recipes/1", recipe_views.recipe_post, name="recipes_post"),

]