# apps/reports/services.py
from datetime import date
from django.db.models import Sum, Count, Avg
from apps.orders.models import Order
from .models import DailyReport


def calculate_period_stats(date_debut, date_fin=None):
    """
    Calcule le CA, le nombre de commandes et le ticket moyen sur une période
    (bornes incluses). Si date_fin est vide ou égale à date_debut, la période
    se réduit à une seule journée — comportement identique à l'ancien système.
    """
    if not date_debut:
        date_debut = date.today()
    date_fin_effective = date_fin or date_debut

    commandes_payees = Order.objects.filter(
        created_at__date__gte=date_debut,
        created_at__date__lte=date_fin_effective,
        statut="payee"
    )

    agg = commandes_payees.aggregate(
        total_ca=Sum("total"),
        nb_cmd=Count("id"),
        moyenne=Avg("total")
    )

    ca = agg["total_ca"] or 0
    nb = agg["nb_cmd"] or 0
    ticket_moyen = agg["moyenne"] or 0

    return {
        "date_debut": date_debut,
        "date_fin": date_fin_effective,
        "chiffre_affaires": ca,
        "nombre_commandes": nb,
        "ticket_moyen": ticket_moyen,
        "commandes": commandes_payees
    }


def generate_or_update_report(date_debut, date_fin, staff_user):
    """
    Crée (ou met à jour si la même période existe déjà) le rapport clôturé
    correspondant à la période [date_debut, date_fin].
    """
    date_fin_effective = date_fin or date_debut
    stats = calculate_period_stats(date_debut, date_fin_effective)

    report, created = DailyReport.objects.update_or_create(
        date_debut=date_debut,
        date_fin=date_fin_effective,
        defaults={
            "chiffre_affaires": stats["chiffre_affaires"],
            "nombre_commandes": stats["nombre_commandes"],
            "ticket_moyen": stats["ticket_moyen"],
            "genere_par": staff_user
        }
    )

    return report


# --- Alias de compatibilité ---------------------------------------------
# apps/dashboard/views.py (et éventuellement d'autres modules) importent
# encore l'ancien nom à un seul jour. On le garde utilisable en attendant
# de basculer ces appelants sur calculate_period_stats.
def calculate_daily_stats(target_date=None):
    return calculate_period_stats(target_date, target_date)