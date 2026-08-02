# apps/cashier/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.orders.models import Order
from .services import process_payment


@login_required(login_url="connexion")
def caisse_pos_view(request):
    """
    Interface POS de la caisse basée sur le panneau latéral droit de la Maquette 2.
    """
    order_id = request.GET.get("order_id")
    commandes_non_payees = Order.objects.exclude(statut__in=["payee", "annulee"])

    selected_order = None
    if order_id:
        selected_order = get_object_or_404(Order, pk=order_id)
    elif commandes_non_payees.exists():
        selected_order = commandes_non_payees.first()

    context = {
        "active_page": "caisse",
        "commandes": commandes_non_payees,
        "selected_order": selected_order,
    }
    return render(request, "Cashier/caisse.html", context)


@login_required(login_url="connexion")
def encaisser_commande(request, order_id):
    """
    Traitement POST de l'encaissement et redirection vers l'impression du ticket.
    """
    if request.method == "POST":
        order = get_object_or_404(Order, pk=order_id)
        mode_paiement = request.POST.get("mode_paiement", "especes")
        montant_recu = request.POST.get("montant_recu", order.total)

        receipt, error = process_payment(order, mode_paiement, montant_recu, request.user)

        if error:
            messages.warning(request, error)
            return redirect(f"/admin-panel/caisse/ticket/{order.id}/")

        messages.success(request, f"Commande {order.reference} encaissée avec succès ! Ticket N°{receipt.numero_recu}")
        return redirect(f"/admin-panel/caisse/ticket/{order.id}/")

    return redirect("caisse_pos")


@login_required(login_url="connexion")
def ticket_pos_view(request, order_id):
    """
    Rendu du ticket caisse POS format 80mm prêt pour l'impression thermique (window.print()).
    """
    order = get_object_or_404(Order, pk=order_id)
    receipt = getattr(order, "receipt", None)

    context = {
        "order": order,
        "receipt": receipt,
    }
    return render(request, "Cashier/ticket.html", context)
