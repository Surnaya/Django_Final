from django.contrib import admin
from .models import Recipe, RecipeCategory

admin.site.register(Recipe)
admin.site.register(RecipeCategory)