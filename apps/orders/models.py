# apps/orders/models.py
import uuid
from django.db import models
from apps.tables.models import RestaurantTable
from apps.menu.models import MenuItem


class Order(models.Model):
    TYPE_CHOICES = [
        ("sur_place", "Sur place"),
        ("emporter", "À emporter"),
        ("livraison", "Livraison"),
    ]

    STATUT_CHOICES = [
        ("en_attente", "En attente"),
        ("preparation", "En préparation"),
        ("prete", "Prête"),
        ("servie", "Servie"),
        ("payee", "Payée"),
        ("annulee", "Annulée"),
    ]

    reference = models.CharField(max_length=30, unique=True, editable=False)
    table = models.ForeignKey(RestaurantTable, null=True, blank=True, on_delete=models.SET_NULL, related_name="commandes")
    type_commande = models.CharField(max_length=20, choices=TYPE_CHOICES, default="sur_place")
    client_nom = models.CharField(max_length=150, blank=True)
    client_telephone = models.CharField(max_length=30, blank=True)
    adresse_livraison = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="en_attente")
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0)  # FCFA
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Commandes"

    def save(self, *args, **kwargs):
        if not self.reference:
            short_id = uuid.uuid4().hex[:6].upper()
            self.reference = f"CMD-{short_id}"
        super().save(*args, **kwargs)

    def recalculer_total(self):
        tot = sum(item.prix_unitaire * item.quantite for item in self.items.all())
        self.total = tot
        self.save(update_fields=["total"])
        return tot

    def __str__(self):
        lbl_type = self.get_type_commande_display()
        if self.table:
            lbl_type += f" (Table N°{self.table.numero})"
        return f"Commande {self.reference} — {lbl_type} [{self.get_statut_display()}]"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=0)  # Figé au moment de la commande

    @property
    def sous_total(self):
        return self.prix_unitaire * self.quantite

    def __str__(self):
        return f"{self.quantite}x {self.menu_item.nom} ({self.sous_total} FCFA)"
