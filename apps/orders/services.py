# apps/orders/services.py
from django.db import transaction
from apps.menu.models import MenuItem
from apps.tables.models import RestaurantTable
from .models import Order, OrderItem


def create_order_from_cart(cart_data, type_commande="sur_place", table_id=None, client_nom="", client_telephone="", adresse_livraison="", notes=""):
    """
    Crée une commande sécurisée depuis le panier client.
    RECALCULE et FIGE le prix unitaire et le total côté serveur depuis la BD.
    """
    if not cart_data or not isinstance(cart_data, dict):
        return None, "Le panier est vide ou invalide."

    table = None
    if type_commande == "sur_place" and table_id:
        try:
            table = RestaurantTable.objects.get(pk=table_id)
        except RestaurantTable.DoesNotExist:
            return None, "La table sélectionnée n'existe pas."

    with transaction.atomic():
        order = Order.objects.create(
            type_commande=type_commande,
            table=table,
            client_nom=client_nom.strip(),
            client_telephone=client_telephone.strip(),
            adresse_livraison=adresse_livraison.strip(),
            notes=notes.strip(),
            statut="en_attente"
        )

        total_calculer = 0
        for item_id_str, qty_val in cart_data.items():
            try:
                item_id = int(item_id_str)
                quantite = int(qty_val)
            except (ValueError, TypeError):
                continue

            if quantite <= 0:
                continue

            try:
                menu_item = MenuItem.objects.get(pk=item_id, disponible=True)
            except MenuItem.DoesNotExist:
                continue

            prix_unitaire = menu_item.get_prix_effectif()
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantite=quantite,
                prix_unitaire=prix_unitaire
            )
            total_calculer += (prix_unitaire * quantite)

        if not order.items.exists():
            transaction.set_rollback(True)
            return None, "Aucun article valide trouvé dans votre panier."

        order.total = total_calculer
        order.save(update_fields=["total"])

        if table:
            table.statut = "occupee"
            table.save(update_fields=["statut"])

    return order, None


def update_order_status(order, new_statut):
    """
    Met à jour le statut d'une commande en respectant les transitions métier.
    """
    valid_statuts = [s[0] for s in Order.STATUT_CHOICES]
    if new_statut not in valid_statuts:
        return False, "Statut invalide."

    order.statut = new_statut
    order.save(update_fields=["statut", "updated_at"])

    # Libération de la table si la commande est payée, servie ou annulée
    if new_statut in ["payee", "annulee"] and order.table:
        # Vérifier si d'autres commandes en cours occupent la même table
        commandes_en_cours = Order.objects.filter(
            table=order.table,
            statut__in=["en_attente", "preparation", "prete"]
        ).exclude(pk=order.pk).exists()

        if not commandes_en_cours:
            order.table.statut = "libre"
            order.table.save(update_fields=["statut"])

    return True, f"Statut mis à jour vers {order.get_statut_display()}."
