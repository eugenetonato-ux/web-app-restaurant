# apps/dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("connexion/", views.connexion, name="connexion"),
    path("deconnexion/", views.deconnexion, name="deconnexion"),
    path("dashboard/", views.dashboard_home, name="dashboard_home"),
    path("tables/", views.tables_liste, name="tables_liste"),
    path("commandes/", views.commandes_liste, name="commandes_liste"),
]