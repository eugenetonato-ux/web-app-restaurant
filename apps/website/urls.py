# apps/website/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="website_home"),
    path("menu/", views.menu_view, name="website_menu"),
    path("panier/", views.panier_view, name="website_panier"),
    path("passer-commande/", views.checkout_view, name="website_checkout"),
    path("suivi/<str:reference>/", views.suivi_commande_view, name="website_suivi"),
    path("api/cart/add/", views.api_add_to_cart, name="api_add_to_cart"),
]