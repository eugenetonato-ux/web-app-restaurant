# apps/menu/forms.py
from django import forms
from .models import Category, MenuItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["nom", "ordre_affichage", "actif"]


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["categorie", "nom", "description", "prix", "photo", "disponible"]