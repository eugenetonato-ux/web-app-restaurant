# apps/cashier/services.py
from django.db import transaction
from apps.orders.services import update_order_status
from .models import Receipt


def process_payment(order, mode_paiement, montant_recu, staff_user):
    """
    Enregistre l'encaissement d'une commande, génère un reçu POS unique
    et bascule le statut de la commande à 'payee'.
    """
    if hasattr(order, "receipt"):
        return order.receipt, "Cette commande a déjà été encaissée."

    if order.statut == "annulee":
        return None, "Impossible d'encaisser une commande annulée."

    montant_recu_val = float(montant_recu or order.total)
    monnaie = max(0, montant_recu_val - float(order.total))

    with transaction.atomic():
        receipt = Receipt.objects.create(
            order=order,
            mode_paiement=mode_paiement,
            montant_recu=montant_recu_val,
            monnaie_rendue=monnaie,
            encaisse_par=staff_user
        )

        update_order_status(order, "payee")

    return receipt, None
