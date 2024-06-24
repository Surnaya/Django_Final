import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, RecipeForm
from .models import Recipe, RecipeCategory


def index(request):
    categories = RecipeCategory.objects.all()
    recipes = list(Recipe.objects.all())
    random_recipes = random.sample(recipes, 3) if len(recipes) >= 3 else recipes
    return render(request, 'recipesapp/index.html', {'categories': categories, 'recipes': random_recipes})


def recipe_list(request):
    recipes = Recipe.objects.all()
    categories = RecipeCategory.objects.all()
    return render(request, 'recipesapp/recipe_list.html', {'categories': categories, 'recipes': recipes})


def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    categories = RecipeCategory.objects.all()
    return render(request, 'recipesapp/recipe_detail.html', {'categories': categories, 'recipe': recipe})


def recipe_create(request):
    categories = RecipeCategory.objects.all()
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            # Save categories first
            form.save_m2m()

            # Handle new category
            new_category_name = form.cleaned_data.get('new_category')
            if new_category_name:
                new_category, created = RecipeCategory.objects.get_or_create(name=new_category_name)
                recipe.category.add(new_category)

            # Debugging output
            print(f"Recipe: {recipe}")
            print(f"Categories: {recipe.category.all()}")

            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipesapp/recipe_form.html', {'categories': categories, 'form': form})


def signup_view(request):
    categories = RecipeCategory.objects.all()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'categories': categories, 'form': form})


def login_view(request):
    categories = RecipeCategory.objects.all()
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
    return render(request, 'registration/login.html', {'categories': categories, 'form': form})


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('recipe_list')  # Redirect to the recipe list page
    else:
        return HttpResponseForbidden("You are not allowed to delete this recipe.")


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.author:
        return HttpResponseForbidden("You are not allowed to edit this recipe.")

    if request.method == 'POST':
        print('yes')
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()

            new_category_name = form.cleaned_data.get('new_category')
            if new_category_name:
                new_category, created = RecipeCategory.objects.get_or_create(name=new_category_name)
                recipe.category.add(new_category)

            return redirect('recipe_detail', pk=recipe.pk)
    else:
        print('no')
        form = RecipeForm(instance=recipe)
    return render(request, 'recipesapp/recipe_form.html', {'form': form, 'edit': True})


def category_list(request):
    category = RecipeCategory.objects.all()
    return render(request, 'recipesapp/category_list.html', {'category': category})


def category_detail(request, pk):
    categories = RecipeCategory.objects.all()
    category = get_object_or_404(RecipeCategory, pk=pk)
    recipes = Recipe.objects.filter(category=category)
    return render(request, 'recipesapp/category_detail.html', {'categories': categories, 'category': category, 'recipes': recipes})


def my_recipes(request):
    categories = RecipeCategory.objects.all()
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'recipesapp/my_recipes.html', {'categories': categories, 'recipes': recipes})
