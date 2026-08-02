# apps/reports/models.py
from django.db import models
from apps.staff.models import StaffUser


class DailyReport(models.Model):
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True, help_text="Laisser vide pour un rapport d'une seule journée (= date_debut)")
    chiffre_affaires = models.DecimalField(max_digits=14, decimal_places=0)  # FCFA
    nombre_commandes = models.PositiveIntegerField(default=0)
    ticket_moyen = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    fichier_pdf = models.FileField(upload_to="reports/", blank=True, null=True)
    genere_par = models.ForeignKey(StaffUser, on_delete=models.PROTECT, related_name="rapports_generes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_debut"]
        verbose_name_plural = "Rapports"

    @property
    def date_fin_effective(self):
        return self.date_fin or self.date_debut

    @property
    def est_jour_unique(self):
        return self.date_fin_effective == self.date_debut

    def __str__(self):
        if self.est_jour_unique:
            periode = self.date_debut.strftime('%d/%m/%Y')
        else:
            periode = f"{self.date_debut.strftime('%d/%m/%Y')} au {self.date_fin_effective.strftime('%d/%m/%Y')}"
        return f"Rapport du {periode} — {self.chiffre_affaires} FCFA ({self.nombre_commandes} cmd)"