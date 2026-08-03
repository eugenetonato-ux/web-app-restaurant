# apps/dashboard/context_processors.py
"""
Injecte les variables utilisées par le panneau "Order Menu" de base_admin.html
(commandes_actives, ca_du_jour) sur TOUTES les pages admin — pas seulement le
Dashboard — pour que ce panneau reste à jour partout (Caisse POS, Gestion Menu,
Tables, etc.).
"""
from datetime import date
from apps.orders.models import Order
from apps.reports.services import calculate_daily_stats


def admin_right_panel(request):
    # On ne calcule rien sur le site public / la page de connexion :
    # seules les pages admin (utilisateur connecté) en ont besoin.
    if not request.user.is_authenticated:
        return {}

    commandes_actives = Order.objects.exclude(statut__in=["payee", "annulee"])[:10]
    stats = calculate_daily_stats(date.today())

    return {
        "commandes_actives": commandes_actives,
        "ca_du_jour": stats["chiffre_affaires"],
    }