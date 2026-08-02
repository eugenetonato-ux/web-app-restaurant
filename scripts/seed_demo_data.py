# scripts/seed_demo_data.py
import os
import sys
import django

# Configuration de l'environnement Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.staff.models import StaffUser
from apps.menu.models import Category, MenuItem
from apps.tables.models import RestaurantTable
from apps.orders.models import Order, OrderItem
from apps.cashier.models import Receipt


def seed():
    print("--- Initialisation des donnees de demonstration Delice Express ---")

    # 1. Création utilisateur admin staff
    user, created = StaffUser.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@delice-express.app",
            "role": "admin",
            "first_name": "Zack",
            "last_name": "Admin",
            "is_staff": True,
            "is_superuser": True,
        }
    )
    if created:
        user.set_password("admin123")
        user.save()
        print("[OK] Superutilisateur Staff cree : admin / admin123")
    else:
        print("[INFO] Superutilisateur admin existe deja.")

    # 2. Création des Catégories
    cat_burgers, _ = Category.objects.get_or_create(
        nom="Burgers",
        slug="burgers",
        defaults={"ordre_affichage": 1, "icone": "fa-burger", "couleur_card": "linear-gradient(135deg, #8E5CF7, #A881FC)"}
    )
    cat_pizzas, _ = Category.objects.get_or_create(
        nom="Pizzas",
        slug="pizzas",
        defaults={"ordre_affichage": 2, "icone": "fa-pizza-slice", "couleur_card": "linear-gradient(135deg, #F5A623, #FFB72B)"}
    )
    cat_desserts, _ = Category.objects.get_or_create(
        nom="Desserts",
        slug="desserts",
        defaults={"ordre_affichage": 3, "icone": "fa-cookie", "couleur_card": "linear-gradient(135deg, #E8445C, #FF6B81)"}
    )
    cat_sandwiches, _ = Category.objects.get_or_create(
        nom="Sandwiches",
        slug="sandwiches",
        defaults={"ordre_affichage": 4, "icone": "fa-bread-slice", "couleur_card": "linear-gradient(135deg, #5CC98C, #7CE0A6)"}
    )
    cat_boissons, _ = Category.objects.get_or_create(
        nom="Boissons",
        slug="boissons",
        defaults={"ordre_affichage": 5, "icone": "fa-wine-glass", "couleur_card": "linear-gradient(135deg, #3B82F6, #60A5FA)"}
    )
    print("[OK] Categories creees")

    # 3. Articles du Menu (Maquette 1 & 2)
    items_data = [
        {
            "categorie": cat_burgers,
            "nom": "Grilled Double Cheese Burger",
            "description": "Double steak hache pur boeuf, mozzarella fondante, salade croquante et sauce speciale chef.",
            "prix": 4500,
            "photo_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&auto=format&fit=crop&q=80",
            "est_populaire": True,
            "badge": "HOT",
            "note_etoiles": 4.9
        },
        {
            "categorie": cat_burgers,
            "nom": "Classic Beef Royale",
            "description": "Steak pur boeuf grille au feu de bois, cheddar mature, cornichons doux et oignons caramelises.",
            "prix": 4000,
            "photo_url": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=500&auto=format&fit=crop&q=80",
            "est_populaire": True,
            "badge": "NEW",
            "note_etoiles": 4.8
        },
        {
            "categorie": cat_pizzas,
            "nom": "Tasty Yummy Cheesy Pizza",
            "description": "Pate artisanale levee 48h, triple fromage mozza-cheddar, origan et huile d'olive vierge.",
            "prix": 6500,
            "prix_promo": 5500,
            "est_promo": True,
            "photo_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&auto=format&fit=crop&q=80",
            "est_populaire": True,
            "badge": "-15%",
            "note_etoiles": 4.7
        },
        {
            "categorie": cat_pizzas,
            "nom": "Pepperoni Paradise",
            "description": "Sauce tomate italienne, genereuse couche de pepperoni piquant et fromage mozzarella.",
            "prix": 6000,
            "photo_url": "https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?w=500&auto=format&fit=crop&q=80",
            "est_populaire": True,
            "note_etoiles": 4.8
        },
        {
            "categorie": cat_desserts,
            "nom": "New Menu Galaxy Donuts Time!",
            "description": "Assortiment de 4 donuts moelleux au glacage chocolat vanille et pepites dorees.",
            "prix": 3000,
            "photo_url": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=500&auto=format&fit=crop&q=80",
            "est_populaire": True,
            "badge": "NEW",
            "note_etoiles": 4.9
        },
        {
            "categorie": cat_sandwiches,
            "nom": "Fresh Delicious Veg Sandwich",
            "description": "Pain toaste multigrains, avocat, tomates fraiches, concombre et sauce yaourt fines herbes.",
            "prix": 3500,
            "photo_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=500&auto=format&fit=crop&q=80",
            "est_populaire": False,
            "note_etoiles": 4.6
        },
        {
            "categorie": cat_boissons,
            "nom": "Coca-Cola Glace 50cl",
            "description": "Canette bien fraiche.",
            "prix": 1000,
            "photo_url": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&auto=format&fit=crop&q=80",
            "est_populaire": False,
            "note_etoiles": 5.0
        }
    ]

    for data in items_data:
        MenuItem.objects.get_or_create(
            nom=data["nom"],
            defaults=data
        )
    print("[OK] Articles du menu mecrees avec succes")

    # 4. Tables du Restaurant
    tables_data = [
        {"numero": 1, "capacite": 4, "statut": "libre", "emplacement": "Salle Principale"},
        {"numero": 2, "capacite": 2, "statut": "libre", "emplacement": "Terrasse"},
        {"numero": 3, "capacite": 6, "statut": "libre", "emplacement": "Espace VIP"},
        {"numero": 4, "capacite": 4, "statut": "libre", "emplacement": "Salle Principale"},
        {"numero": 5, "capacite": 8, "statut": "libre", "emplacement": "Espace Famille"},
    ]

    for tdata in tables_data:
        RestaurantTable.objects.get_or_create(
            numero=tdata["numero"],
            defaults=tdata
        )
    print("[OK] Tables du restaurant creees")

    print("\nDonnees de demonstration pretes avec succes !")

if __name__ == "__main__":
    seed()
