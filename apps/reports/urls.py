# apps/reports/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.reports_home, name="reports_home"),
    path("generer/", views.generer_rapport_action, name="generer_rapport"),
    path("imprimer/<int:report_id>/", views.rapport_print_view, name="rapport_imprimer"),
]