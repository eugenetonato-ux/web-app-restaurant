# apps/tables/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.TableListView.as_view(), name="tables_liste"),
    path("ajouter/", views.TableCreateView.as_view(), name="table_create"),
    path("<int:pk>/modifier/", views.TableUpdateView.as_view(), name="table_update"),
    path("<int:pk>/statut/", views.changer_statut_table, name="table_change_status"),
]