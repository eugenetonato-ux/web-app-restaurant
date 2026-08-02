# apps/menu/forms.py
from django import forms
from .models import Category, MenuItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["nom", "ordre_affichage", "icone", "couleur_card", "actif"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "ex: Burgers, Pizzas..."}),
            "ordre_affichage": forms.NumberInput(attrs={"class": "form-control"}),
            "icone": forms.TextInput(attrs={"class": "form-control", "placeholder": "fa-hamburger"}),
            "couleur_card": forms.TextInput(attrs={"class": "form-control", "placeholder": "linear-gradient(135deg, #8E5CF7, #A881FC)"}),
            "actif": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            "categorie", "nom", "description", "prix", "prix_promo",
            "photo", "photo_url", "disponible", "est_populaire", "est_promo", "badge"
        ]
        widgets = {
            "categorie": forms.Select(attrs={"class": "form-select"}),
            "nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "ex: Double Cheeseburger"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "prix": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Prix en FCFA"}),
            "prix_promo": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Prix promo si applicable"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "photo_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
            "badge": forms.TextInput(attrs={"class": "form-control", "placeholder": "ex: HOT, NEW, -20%"}),
            "disponible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "est_populaire": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "est_promo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }