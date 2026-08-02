# apps/tables/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import RestaurantTable
from .forms import RestaurantTableForm


class TableListView(LoginRequiredMixin, ListView):
    model = RestaurantTable
    template_name = "Admin/tables_liste.html"
    context_object_name = "tables"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "tables"
        return context


class TableCreateView(LoginRequiredMixin, CreateView):
    model = RestaurantTable
    form_class = RestaurantTableForm
    template_name = "Admin/table_form.html"
    success_url = reverse_lazy("tables_liste")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "tables"
        return context


class TableUpdateView(LoginRequiredMixin, UpdateView):
    model = RestaurantTable
    form_class = RestaurantTableForm
    template_name = "Admin/table_form.html"
    success_url = reverse_lazy("tables_liste")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "tables"
        return context


def changer_statut_table(request, pk):
    if request.method == "POST":
        table = get_object_or_404(RestaurantTable, pk=pk)
        nouveau_statut = request.POST.get("statut")
        if nouveau_statut in ["libre", "occupee", "reservee"]:
            table.statut = nouveau_statut
            table.save(update_fields=["statut"])
            messages.success(request, f"Table N°{table.numero} passe au statut {table.get_statut_display()}.")
    return redirect("tables_liste")
