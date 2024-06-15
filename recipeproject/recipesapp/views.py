from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, RecipeForm
from .models import Recipe, RecipeCategory


def index(request):
    return render(request, 'recipesapp/index.html')


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipesapp/recipe_list.html', {'recipes': recipes})


def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    return render(request, 'recipesapp/recipe_detail.html', {'recipe': recipe})

def recipe_create(request):
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
    return render(request, 'recipesapp/recipe_form.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
    return render(request, 'registration/login.html', {'form': form})
