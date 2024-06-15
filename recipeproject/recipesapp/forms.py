from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Recipe


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RecipeForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100, required=False, label='New Category')

    class Meta:
        model = Recipe
        fields = ['title', 'image', 'category', 'cooking_time', 'ingredients', 'description']
