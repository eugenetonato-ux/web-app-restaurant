# apps/dashboard/views.py
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from django.urls import reverse
from apps.menu.models import Category, MenuItem
from apps.tables.models import RestaurantTable
from apps.orders.models import Order
from apps.orders.services import update_order_status
from apps.reports.services import calculate_daily_stats


def connexion(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue, {user.get_full_name() or user.username} !")
            return redirect("dashboard_home")
        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, "Admin/connexion.html")


def deconnexion(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect("connexion")


@login_required(login_url="connexion")
def dashboard_home(request):
    """
    Tableau de bord Admin fidèle à la Maquette 2 (FoodMeal / Délice Express Admin) :
    - Carte de solde/CA du jour violette
    - Pilules de catégories
    - Grille de plats populaires
    - Panneau latéral droit des commandes actives & caisse rapide
    """
    today = date.today()
    stats = calculate_daily_stats(today)

    categories = Category.objects.filter(actif=True)
    cat_filter = request.GET.get("cat")
    popular_dishes = MenuItem.objects.filter(disponible=True)

    if cat_filter and cat_filter != "all":
        popular_dishes = popular_dishes.filter(categorie__id=cat_filter)
    else:
        popular_dishes = popular_dishes.filter(est_populaire=True)[:6]
        if not popular_dishes.exists():
            popular_dishes = MenuItem.objects.filter(disponible=True)[:6]

    commandes_actives = Order.objects.exclude(statut__in=["payee", "annulee"])[:10]
    tables_occupees = RestaurantTable.objects.filter(statut="occupee").count()
    tables_libres = RestaurantTable.objects.filter(statut="libre").count()
    commandes_attente_count = Order.objects.filter(statut="en_attente").count()

    context = {
        "active_page": "dashboard",
        "ca_du_jour": stats["chiffre_affaires"],
        "nombre_commandes_jour": stats["nombre_commandes"],
        "ticket_moyen": stats["ticket_moyen"],
        "commandes_attente_count": commandes_attente_count,
        "tables_occupees": tables_occupees,
        "tables_libres": tables_libres,
        "categories": categories,
        "selected_cat": cat_filter or "all",
        "popular_dishes": popular_dishes,
        "commandes_actives": commandes_actives,
    }
    return render(request, "Admin/dashboard.html", context)


@login_required(login_url="connexion")
def changer_statut_commande_quick(request, order_id):
    """
    Changement rapide de statut de commande depuis le dashboard.
    """
    if request.method == "POST":
        order = get_object_or_404(Order, pk=order_id)
        new_statut = request.POST.get("statut")
        success, msg = update_order_status(order, new_statut)
        if success:
            messages.success(request, f"Commande {order.reference} : {msg}")
        else:
            messages.error(request, msg)

    return redirect("dashboard_home")


@login_required(login_url="connexion")
def api_admin_search(request):
    """
    Recherche en direct (AJAX) dans le header admin, sur les Commandes
    (référence, nom client, téléphone) et les Plats du menu (nom).
    """
    query = request.GET.get("q", "").strip()

    resultats_commandes = []
    resultats_plats = []

    if len(query) >= 2:
        commandes = Order.objects.filter(
            Q(reference__icontains=query) |
            Q(client_nom__icontains=query) |
            Q(client_telephone__icontains=query)
        ).order_by("-created_at")[:6]

        for cmd in commandes:
            if cmd.table:
                type_lbl = f"Table N°{cmd.table.numero}"
            else:
                type_lbl = cmd.get_type_commande_display()
            resultats_commandes.append({
                "reference": cmd.reference,
                "sous_titre": f"{type_lbl} • {cmd.client_nom or 'Client'}",
                "total": str(cmd.total),
                "statut": cmd.get_statut_display(),
                "url": f"{reverse('caisse_pos')}?order_id={cmd.id}",
            })

        plats = MenuItem.objects.filter(nom__icontains=query).select_related("categorie")[:6]
        for plat in plats:
            resultats_plats.append({
                "nom": plat.nom,
                "categorie": plat.categorie.nom,
                "prix": str(plat.get_prix_effectif()),
                "disponible": plat.disponible,
                "url": reverse("menu_articles"),
            })

    return JsonResponse({
        "query": query,
        "commandes": resultats_commandes,
        "plats": resultats_plats,
    })