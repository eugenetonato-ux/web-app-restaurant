# apps/menu/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Category, MenuItem
from .forms import CategoryForm, MenuItemForm


# --- Catégories ---
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "Admin/menu_categories.html"
    context_object_name = "categories"


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "Admin/menu_categorie_form.html"
    success_url = reverse_lazy("menu_categories")


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "Admin/menu_categorie_form.html"
    success_url = reverse_lazy("menu_categories")


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "Admin/menu_categorie_confirm_delete.html"
    success_url = reverse_lazy("menu_categories")


# --- Articles ---
class MenuItemListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "Admin/menu_articles.html"
    context_object_name = "articles"


class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "Admin/menu_article_form.html"
    success_url = reverse_lazy("menu_articles")


class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "Admin/menu_article_form.html"
    success_url = reverse_lazy("menu_articles")


class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = "Admin/menu_article_confirm_delete.html"
    success_url = reverse_lazy("menu_articles")