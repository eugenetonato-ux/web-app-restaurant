# apps/tables/forms.py
from django import forms
from .models import RestaurantTable


class RestaurantTableForm(forms.ModelForm):
    class Meta:
        model = RestaurantTable
        fields = ["numero", "capacite", "statut", "emplacement"]
        widgets = {
            "numero": forms.NumberInput(attrs={"class": "form-control", "placeholder": "1, 2, 3..."}),
            "capacite": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Nombre de places"}),
            "statut": forms.Select(attrs={"class": "form-select"}),
            "emplacement": forms.TextInput(attrs={"class": "form-control", "placeholder": "Terrasse, VIP, Salle..."}),
        }
