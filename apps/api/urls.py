# apps/api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("menu/", views.api_menu_list, name="api_menu_list"),
    path("tables/", views.api_tables_status, name="api_tables_status"),
]