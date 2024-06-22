from django.urls import path
from .views import (index, recipe_create, recipe_detail, recipe_list,
                    signup_view, login_view, recipe_delete, recipe_edit,
                    category_list, category_detail, my_recipes)

urlpatterns = [
    path('', index, name='index'),
    path('recipes/', recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', recipe_detail, name='recipe_detail'),
    path('recipe/new/', recipe_create, name='recipe_create'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('recipe/<int:pk>/delete/', recipe_delete, name='recipe_delete'),
    path('recipe/<int:pk>/edit/', recipe_edit, name='recipe_edit'),
    path('category/', category_list, name='category_list'),  # маршрут для списка категорий
    path('category/<int:pk>/', category_detail, name='category_detail'),  # маршрут для рецептов категории
    path('my_recipes/', my_recipes, name='my_recipes'),
]