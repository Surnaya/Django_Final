from django.urls import path
from .views import index, recipe_create, recipe_detail, recipe_list, signup_view, login_view

urlpatterns = [
    path('', index, name='index'),
    path('recipes/', recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', recipe_detail, name='recipe_detail'),
    path('recipe/new/', recipe_create, name='recipe_create'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),

]