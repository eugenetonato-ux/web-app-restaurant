# apps/dashboard/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


def connexion(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard_home")
        messages.error(request, "Identifiants incorrects.")

    return render(request, "Admin/connexion.html")


def deconnexion(request):
    logout(request)
    return redirect("connexion")


@login_required(login_url="connexion")
def dashboard_home(request):
    context = {
        "active_page": "dashboard",
        # TODO: remplacer par de vraies requêtes une fois les modèles Commande/Table branchés
        # ex: "ca_du_jour": Commande.objects.filter(...).aggregate(...)["total"],
        "ca_du_jour": 0,
        "nombre_commandes_jour": 0,
        "nombre_commandes_attente": 0,
        "tables_occupees": 0,
        "commandes_en_cours": [],
    }
    return render(request, "Admin/dashboard.html", context)


@login_required(login_url="connexion")
def tables_liste(request):
    context = {
        "active_page": "tables",
        # TODO: remplacer par Table.objects.all() une fois le modèle Table importé
        "tables": [],
    }
    return render(request, "Admin/tables_liste.html", context)


@login_required(login_url="connexion")
def commandes_liste(request):
    context = {
        "active_page": "commandes",
        # TODO: remplacer par Commande.objects.all() une fois le modèle Commande importé
        "commandes": [],
    }
    return render(request, "Admin/commandes.html", context)