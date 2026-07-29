# apps/menu/models.py
from django.db import models


class Category(models.Model):
    nom = models.CharField(max_length=100)
    ordre_affichage = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordre_affichage"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.nom


class MenuItem(models.Model):
    categorie = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="articles")
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=0)  # FCFA
    photo = models.ImageField(upload_to="menu/", blank=True, null=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} — {self.prix} FCFA"