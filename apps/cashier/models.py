# apps/cashier/models.py
import uuid
from django.db import models
from apps.orders.models import Order
from apps.staff.models import StaffUser


class Receipt(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ("especes", "Espèces"),
        ("mobile_money", "Mobile Money (Wave / Orange / MTN)"),
        ("carte", "Carte Bancaire"),
    ]

    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="receipt")
    numero_recu = models.CharField(max_length=30, unique=True, editable=False)
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES, default="especes")
    encaisse_par = models.ForeignKey(StaffUser, on_delete=models.PROTECT, related_name="recus_encaisses")
    montant_recu = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    monnaie_rendue = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Reçus Caisse (POS)"

    def save(self, *args, **kwargs):
        if not self.numero_recu:
            short_id = uuid.uuid4().hex[:6].upper()
            self.numero_recu = f"REC-{short_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reçu N°{self.numero_recu} — Commande {self.order.reference} ({self.order.total} FCFA)"
