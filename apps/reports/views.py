# apps/reports/views.py
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import DailyReport
from .services import calculate_period_stats, generate_or_update_report


def _parse_date(value, fallback):
    if value:
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            pass
    return fallback


@login_required(login_url="connexion")
def reports_home(request):
    today = date.today()
    date_debut = _parse_date(request.GET.get("date_debut"), today)
    date_fin = _parse_date(request.GET.get("date_fin"), date_debut)

    # Garde-fou : si la date de fin précède la date de début, on les inverse
    if date_fin < date_debut:
        date_debut, date_fin = date_fin, date_debut

    stats = calculate_period_stats(date_debut, date_fin)
    rapports_historique = DailyReport.objects.all()[:15]

    context = {
        "active_page": "rapports",
        "date_debut": date_debut,
        "date_fin": date_fin,
        "stats": stats,
        "rapports_historique": rapports_historique,
    }
    return render(request, "Reports/rapports.html", context)


@login_required(login_url="connexion")
def generer_rapport_action(request):
    if request.method == "POST":
        today = date.today()
        date_debut = _parse_date(request.POST.get("date_debut"), today)
        date_fin = _parse_date(request.POST.get("date_fin"), date_debut)

        if date_fin < date_debut:
            date_debut, date_fin = date_fin, date_debut

        report = generate_or_update_report(date_debut, date_fin, request.user)
        messages.success(request, f"Rapport généré avec succès ({report}) !")
        return redirect(f"/admin-panel/rapports/imprimer/{report.id}/")

    return redirect("reports_home")


@login_required(login_url="connexion")
def rapport_print_view(request, report_id):
    report = get_object_or_404(DailyReport, pk=report_id)
    stats = calculate_period_stats(report.date_debut, report.date_fin_effective)

    context = {
        "report": report,
        "stats": stats,
    }
    return render(request, "Reports/rapport_journalier.html", context)