# apps/cashier/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.caisse_pos_view, name="caisse_pos"),
    path("encaisser/<int:order_id>/", views.encaisser_commande, name="caisse_encaisser"),
    path("ticket/<int:order_id>/", views.ticket_pos_view, name="caisse_ticket"),
]