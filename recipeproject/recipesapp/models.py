from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipe_images/')
    category = models.ForeignKey('RecipeCategory', on_delete=models.SET_NULL, null=True, blank=True)
    cooking_time = models.IntegerField()  # in minutes
    ingredients = models.TextField()
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class RecipeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RecipeCategoryRelation(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(RecipeCategory, on_delete=models.CASCADE)
