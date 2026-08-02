# apps/website/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from apps.menu.models import Category, MenuItem
from apps.tables.models import RestaurantTable
from apps.orders.models import Order
from apps.orders.services import create_order_from_cart


def home_view(request):
    """
    Page d'accueil publique inspirée de la Maquette 1 (Good Food / Fast Food).
    - Hero banner doré/jaune avec burger phare
    - 4 cartes de catégories colorées
    - Plats populaires et en promotion
    """
    categories = Category.objects.filter(actif=True)
    plats_populaires = MenuItem.objects.filter(disponible=True, est_populaire=True)[:8]
    plats_promo = MenuItem.objects.filter(disponible=True, est_promo=True)[:6]

    # Si aucun plat populaire/promo marqué, prendre les premiers articles
    if not plats_populaires.exists():
        plats_populaires = MenuItem.objects.filter(disponible=True)[:8]

    plat_hero = MenuItem.objects.filter(disponible=True, est_populaire=True).first()
    if not plat_hero:
        plat_hero = MenuItem.objects.filter(disponible=True).first()

    # Récupérer le panier depuis la session
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())

    context = {
        "categories": categories,
        "plats_populaires": plats_populaires,
        "plats_promo": plats_promo,
        "plat_hero": plat_hero,
        "cart_count": cart_count,
    }
    return render(request, "Website/home.html", context)


def menu_view(request):
    """
    Page du menu public complet avec filtre par catégorie.
    """
    cat_slug = request.GET.get("category")
    categories = Category.objects.filter(actif=True)
    articles = MenuItem.objects.filter(disponible=True)

    selected_category = None
    if cat_slug:
        selected_category = Category.objects.filter(slug=cat_slug, actif=True).first()
        if selected_category:
            articles = articles.filter(categorie=selected_category)

    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())

    context = {
        "categories": categories,
        "articles": articles,
        "selected_category": selected_category,
        "cart_count": cart_count,
    }
    return render(request, "Website/menu.html", context)


def panier_view(request):
    """
    Page du panier et de finalisation de la commande.
    """
    cart = request.session.get("cart", {})
    cart_items = []
    total_panier = 0

    for item_id_str, qty in cart.items():
        try:
            item = MenuItem.objects.get(pk=int(item_id_str), disponible=True)
            prix = item.get_prix_effectif()
            sous_total = prix * int(qty)
            total_panier += sous_total
            cart_items.append({
                "item": item,
                "quantite": qty,
                "prix_unitaire": prix,
                "sous_total": sous_total
            })
        except MenuItem.DoesNotExist:
            continue

    tables_libres = RestaurantTable.objects.filter(statut="libre")

    context = {
        "cart_items": cart_items,
        "total_panier": total_panier,
        "cart_count": sum(cart.values()),
        "tables_libres": tables_libres,
    }
    return render(request, "Website/panier.html", context)


def checkout_view(request):
    """
    Traitement POST de la prise de commande.
    """
    if request.method == "POST":
        cart = request.session.get("cart", {})
        if not cart:
            messages.error(request, "Votre panier est vide.")
            return redirect("website_panier")

        type_commande = request.POST.get("type_commande", "sur_place")
        table_id = request.POST.get("table_id")
        client_nom = request.POST.get("client_nom", "")
        client_telephone = request.POST.get("client_telephone", "")
        adresse_livraison = request.POST.get("adresse_livraison", "")
        notes = request.POST.get("notes", "")

        order, error = create_order_from_cart(
            cart_data=cart,
            type_commande=type_commande,
            table_id=table_id,
            client_nom=client_nom,
            client_telephone=client_telephone,
            adresse_livraison=adresse_livraison,
            notes=notes
        )

        if error:
            messages.error(request, error)
            return redirect("website_panier")

        # Vider le panier après succès
        request.session["cart"] = {}
        messages.success(request, f"Votre commande {order.reference} a bien été enregistrée !")
        return redirect("website_suivi", reference=order.reference)

    return redirect("website_panier")


def suivi_commande_view(request, reference):
    """
    Page de suivi de commande client.
    """
    order = get_object_or_404(Order, reference=reference)
    return render(request, "Website/suivi.html", {"order": order})


def api_add_to_cart(request):
    """
    API AJAX pour ajouter/modifier un article dans le panier session.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = str(data.get("item_id"))
            quantite = int(data.get("quantite", 1))
            action = data.get("action", "add")  # add, set, remove

            cart = request.session.get("cart", {})

            if action == "add":
                cart[item_id] = cart.get(item_id, 0) + quantite
            elif action == "set":
                if quantite > 0:
                    cart[item_id] = quantite
                else:
                    cart.pop(item_id, None)
            elif action == "remove":
                cart.pop(item_id, None)

            request.session["cart"] = cart
            cart_count = sum(cart.values())

            return JsonResponse({"success": True, "cart_count": cart_count, "cart": cart})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
