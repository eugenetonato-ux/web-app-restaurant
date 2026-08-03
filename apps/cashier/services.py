# apps/cashier/services.py
from django.db import transaction
from apps.orders.services import update_order_status
from .models import Receipt


def process_payment(order, mode_paiement, montant_recu, staff_user):
    """
    Enregistre l'encaissement d'une commande, génère un reçu POS unique
    et bascule le statut de la commande à 'payee'.

    Règles de sécurité / transparence :
    - order.total n'est JAMAIS modifié ici : le montant facturé au client
      reste celui figé à la création de la commande, quoi qu'il arrive.
    - Pour un paiement électronique (mobile money, carte), le montant reçu
      est forcément exact : toute valeur soumise par le formulaire est
      ignorée et remplacée par le total réel de la commande.
    - Pour un paiement en espèces, la commande ne peut pas être clôturée
      comme "payée" si le montant remis est inférieur au total dû.
    """
    if hasattr(order, "receipt"):
        return order.receipt, "Cette commande a déjà été encaissée."

    if order.statut == "annulee":
        return None, "Impossible d'encaisser une commande annulée."

    total_du = float(order.total)

    if mode_paiement != "especes":
        # Paiement électronique : pas de "monnaie", pas de saisie libre possible.
        montant_recu_val = total_du
    else:
        try:
            montant_recu_val = float(montant_recu)
        except (TypeError, ValueError):
            montant_recu_val = total_du

        if montant_recu_val < total_du:
            return None, (
                f"Montant reçu ({montant_recu_val:.0f} FCFA) insuffisant pour "
                f"couvrir le total de la commande ({total_du:.0f} FCFA). "
                f"Encaissement refusé."
            )

    monnaie = max(0, montant_recu_val - total_du)

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