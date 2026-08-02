# apps/dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),
    path("connexion/", views.connexion, name="connexion"),
    path("deconnexion/", views.deconnexion, name="deconnexion"),
    path("commande/<int:order_id>/changer-statut/", views.changer_statut_commande_quick, name="dashboard_quick_status"),
    path("api/recherche/", views.api_admin_search, name="dashboard_search_api"),
]