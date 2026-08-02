# apps/menu/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Catégories
    path("categories/", views.CategoryListView.as_view(), name="menu_categories"),
    path("categories/ajouter/", views.CategoryCreateView.as_view(), name="menu_categorie_create"),
    path("categories/ajouter-alt/", views.CategoryCreateView.as_view(), name="menu_categorie_ajouter"),
    path("categories/<int:pk>/modifier/", views.CategoryUpdateView.as_view(), name="menu_categorie_update"),
    path("categories/<int:pk>/modifier-alt/", views.CategoryUpdateView.as_view(), name="menu_categorie_modifier"),
    path("categories/<int:pk>/supprimer/", views.CategoryDeleteView.as_view(), name="menu_categorie_delete"),
    path("categories/<int:pk>/supprimer-alt/", views.CategoryDeleteView.as_view(), name="menu_categorie_supprimer"),

    # Articles
    path("articles/", views.MenuItemListView.as_view(), name="menu_articles"),
    path("articles/ajouter/", views.MenuItemCreateView.as_view(), name="menu_article_create"),
    path("articles/ajouter-alt/", views.MenuItemCreateView.as_view(), name="menu_article_ajouter"),
    path("articles/<int:pk>/modifier/", views.MenuItemUpdateView.as_view(), name="menu_article_update"),
    path("articles/<int:pk>/modifier-alt/", views.MenuItemUpdateView.as_view(), name="menu_article_modifier"),
    path("articles/<int:pk>/supprimer/", views.MenuItemDeleteView.as_view(), name="menu_article_delete"),
    path("articles/<int:pk>/supprimer-alt/", views.MenuItemDeleteView.as_view(), name="menu_article_supprimer"),
]