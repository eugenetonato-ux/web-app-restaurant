# apps/staff/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class StaffUser(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Administrateur"),
        ("serveur", "Serveur"),
        ("caisse", "Caissier / POS"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="serveur")
    telephone = models.CharField(max_length=30, blank=True)

    def is_admin_role(self):
        return self.is_superuser or self.role == "admin"

    def is_cashier_role(self):
        return self.is_superuser or self.role in ["admin", "caisse"]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"