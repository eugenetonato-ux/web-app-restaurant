# apps/orders/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Order
from .services import update_order_status


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "Admin/commandes.html"
    context_object_name = "commandes"
    paginate_by = 20

    def get_queryset(self):
        statut = self.request.GET.get("statut")
        qs = Order.objects.prefetch_related("items__menu_item", "table").all()
        if statut:
            qs = qs.filter(statut=statut)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "commandes"
        context["selected_statut"] = self.request.GET.get("statut", "")
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "Admin/commande_detail.html"
    context_object_name = "commande"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "commandes"
        return context


def changer_statut_commande(request, pk):
    if request.method == "POST":
        order = get_object_or_404(Order, pk=pk)
        new_statut = request.POST.get("statut")
        success, msg = update_order_status(order, new_statut)
        if success:
            messages.success(request, f"Commande {order.reference} : {msg}")
        else:
            messages.error(request, msg)
    return redirect("commandes_liste")
