# apps/orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.OrderListView.as_view(), name="commandes_liste"),
    path("<int:pk>/", views.OrderDetailView.as_view(), name="commande_detail"),
    path("<int:pk>/statut/", views.changer_statut_commande, name="commande_change_status"),
]