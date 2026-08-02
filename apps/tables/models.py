# apps/tables/models.py
from django.db import models


class RestaurantTable(models.Model):
    STATUT_CHOICES = [
        ("libre", "Libre"),
        ("occupee", "Occupée"),
        ("reservee", "Réservée"),
    ]

    numero = models.PositiveIntegerField(unique=True)
    capacite = models.PositiveIntegerField(default=4)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="libre")
    emplacement = models.CharField(max_length=100, default="Salle Principale")

    class Meta:
        ordering = ["numero"]
        verbose_name_plural = "Tables"

    def __str__(self):
        return f"Table N°{self.numero} ({self.capacite} pers.)"
