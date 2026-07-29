# Délice Express — Cahier des Charges Technique & Guide de Développement

**Stack technologique** : Django 5+ / Django REST Framework / PostgreSQL / Redis / Celery
**Objectif** : Plateforme web pour un restaurant — site public (commande en ligne) + back-office administrateur (gestion menu, tables, caisse POS, rapports).
**Authentification** :
- Site public : **aucun compte requis** pour commander (panier + coordonnées client simples). Compte optionnel pour l'historique.
- Back-office : authentification classique (email + mot de passe) réservée au personnel (admin, serveurs, caisse).

---

## 🛠️ 1. Installation & Configuration Initiale

```bash
django-admin startproject config delice_express
cd delice_express
python -m venv venv && source venv/bin/activate
```

### Dépendances principales

```bash
pip install django djangorestframework django-filter python-decouple pillow \
  qrcode[pil] reportlab psycopg2-binary django-cors-headers django-extensions \
  whitenoise gunicorn requests ipython pytest pytest-django factory-boy black isort flake8

pip install celery redis
```

### Variables d'environnement (`.env`)

```
DEBUG=False
SECRET_KEY=
DATABASE_URL=
REDIS_URL=

CURRENCY=FCFA
RESTAURANT_NAME=Délice Express

DEFAULT_FROM_EMAIL=
```

---

## 🏗️ 2. Architecture des dossiers

```
delice_express/
│
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
│
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── celery.py
│
├── apps/
│   ├── staff/               # Comptes personnel (admin, serveur, caisse) + rôles
│   ├── menu/                # Catégories + articles du menu (prix en FCFA)
│   ├── tables/               # Tables du restaurant (Table N°1, N°2...)
│   ├── orders/                # Panier, commandes, lignes de commande, statuts
│   ├── cashier/                 # Caisse POS, tickets, encaissement
│   ├── reports/                  # Rapport journalier, chiffre d'affaires
│   ├── dashboard/                  # Statistiques admin
│   ├── notifications/               # Email / futur SMS (confirmation commande)
│   ├── api/                           # API REST v1
│   ├── common/                          # Utilitaires partagés
│   └── website/                          # Site public (accueil, menu, panier)
│
├── templates/
├── static/
├── media/
└── docs/
```

### Détail des apps critiques

**`menu/`** : gestion des `Category` (ex: Burgers, Pizzas, Boissons, Desserts) et `MenuItem` (nom, description, prix FCFA, photo, disponibilité, catégorie). L'admin ajoute/modifie/désactive un article sans le supprimer (historique des commandes doit rester cohérent).

**`tables/`** : gestion des tables physiques du restaurant (`Table N°1`, `Table N°2`...) avec statut (`libre`, `occupée`, `réservée`). Une commande peut être liée à une table (sur place) ou marquée `à emporter` / `livraison`.

**`orders/`** : panier client (session ou localStorage côté front), transformation en `Order` avec `OrderItem[]`, statut (`en attente`, `en préparation`, `prête`, `servie`, `payée`, `annulée`), type (`sur_place`, `emporter`, `livraison`), table associée si applicable.

**`cashier/`** : encaissement d'une commande (espèces / mobile money), génération du **reçu caisse POS** (ticket format 80mm, pensé pour impression directe sur imprimante thermique — pas un PDF), lien 1-1 avec `Order`.

**`reports/`** : agrégation du **chiffre d'affaires journalier**, nombre de commandes, ticket moyen, top articles vendus ; génération d'un **rapport journalier au format PDF** (téléchargeable et imprimable en A4, via `reportlab`).

---

## 🔄 3. Flux clés de la plateforme

### Côté client (site public)
```
Arrivée sur le site
   ↓
Parcourt les catégories de menu
   ↓
Consulte les articles + prix (FCFA)
   ↓
Ajoute au panier (quantité modifiable)
   ↓
Passe commande
   → choisit : sur place (n° de table) / à emporter / livraison
   → renseigne nom + téléphone
   ↓
Confirmation de commande (email/SMS optionnel)
```

### Côté admin / staff
```
Connexion back-office (email + mot de passe)
   ↓
Dashboard : commandes du jour, CA du jour, statuts en cours
   ↓
Gestion menu : catégories + articles + prix FCFA
   ↓
Gestion tables : ajout/désactivation des tables
   ↓
Suivi des commandes : changement de statut (préparation → prête → servie)
   ↓
Caisse (POS) : encaissement + impression du reçu
   ↓
Fin de journée : impression du rapport journalier (CA, nb commandes, top ventes)
```

---

## 📊 4. Modèles de données (extraits clés)

### `Category` (menu)
```python
class Category(models.Model):
    nom = models.CharField(max_length=100)
    ordre_affichage = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
```

### `MenuItem` (menu)
```python
class MenuItem(models.Model):
    categorie = models.ForeignKey(Category, on_delete=models.PROTECT)
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=0)  # FCFA, pas de centimes
    photo = models.ImageField(upload_to="menu/", blank=True)
    disponible = models.BooleanField(default=True)
```

### `RestaurantTable` (tables)
```python
class RestaurantTable(models.Model):
    numero = models.PositiveIntegerField(unique=True)  # ex: 1, 2, 3...
    capacite = models.PositiveIntegerField(default=4)
    statut = models.CharField(max_length=20, default="libre")  # libre / occupee / reservee

    def __str__(self):
        return f"Table N°{self.numero}"
```

### `Order` (orders)
```python
class Order(models.Model):
    TYPE_CHOICES = [("sur_place", "Sur place"), ("emporter", "À emporter"), ("livraison", "Livraison")]
    STATUT_CHOICES = [("en_attente", "En attente"), ("preparation", "En préparation"),
                       ("prete", "Prête"), ("servie", "Servie"),
                       ("payee", "Payée"), ("annulee", "Annulée")]

    table = models.ForeignKey(RestaurantTable, null=True, blank=True, on_delete=models.SET_NULL)
    type_commande = models.CharField(max_length=20, choices=TYPE_CHOICES)
    client_nom = models.CharField(max_length=150, blank=True)
    client_telephone = models.CharField(max_length=30, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="en_attente")
    total = models.DecimalField(max_digits=12, decimal_places=0)  # FCFA
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey("menu.MenuItem", on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=0)  # figé au moment de la commande
```

### `Receipt` (cashier)
```python
class Receipt(models.Model):
    order = models.OneToOneField("orders.Order", on_delete=models.PROTECT)
    numero_recu = models.CharField(max_length=30, unique=True)
    mode_paiement = models.CharField(max_length=20)  # especes / mobile_money
    encaisse_par = models.ForeignKey("staff.StaffUser", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
```
> Rendu : template `Cashier/ticket.html` en format 80mm, imprimé directement depuis le navigateur (`window.print()` ou imprimante thermique) — **pas de génération PDF** pour le reçu.

### `DailyReport` (reports)
```python
class DailyReport(models.Model):
    date = models.DateField(unique=True)
    chiffre_affaires = models.DecimalField(max_digits=14, decimal_places=0)  # FCFA
    nombre_commandes = models.PositiveIntegerField()
    ticket_moyen = models.DecimalField(max_digits=12, decimal_places=0)
    fichier_pdf = models.FileField(upload_to="reports/", blank=True)
    genere_par = models.ForeignKey("staff.StaffUser", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
```
> Généré via `reports/pdf_generator.py` (reportlab) — format A4, téléchargeable et imprimable, archivé dans `media/reports/`.

---

## 🧠 5. Règles de développement (à respecter strictement)

- ❌ **INTERDIT** : logique métier dans les vues — tout passe par `services.py` de chaque app.
- ❌ **INTERDIT** : recalculer le prix d'un `OrderItem` a posteriori — le prix est figé au moment de la commande (`prix_unitaire`), même si le prix du `MenuItem` change ensuite.
- ❌ **INTERDIT** : supprimer un `MenuItem` déjà utilisé dans une commande — le désactiver (`disponible = False`) uniquement.
- ✅ **OBLIGATOIRE** : le total d'une commande est calculé et vérifié côté serveur (jamais confiance au total envoyé par le front).
- ✅ **OBLIGATOIRE** : un reçu (`Receipt`) n'est généré qu'après confirmation d'encaissement, jamais avant.
- ✅ **OBLIGATOIRE** : le rapport journalier se base uniquement sur les commandes au statut `payée`.
- ✅ **OBLIGATOIRE** : le reçu de caisse est un **ticket POS** (template HTML dédié, format 80mm, impression directe depuis le navigateur/imprimante thermique) — jamais un fichier PDF.
- ✅ **OBLIGATOIRE** : le rapport journalier est un **fichier PDF généré côté serveur** (via `reports/pdf_generator.py`, format A4, téléchargeable et imprimable) — jamais une simple vue HTML "print-friendly".

---

## 🚀 6. Checklist de développement

### Phase 1 — Socle fonctionnel
- [ ] Initialiser le projet Django + apps (`menu`, `tables`, `orders`, `cashier`, `reports`, `dashboard`, `staff`, `website`, `api`, `common`)
- [ ] Authentification staff (login classique, rôles admin/serveur/caisse)
- [ ] Modèles `Category`, `MenuItem`, `RestaurantTable`, `Order`, `OrderItem`, `Receipt`
- [ ] Site public : liste des catégories + menus avec prix FCFA
- [ ] Panier (session) + création de commande (sur place / emporter / livraison)
- [ ] Back-office : CRUD catégories + articles de menu
- [ ] Back-office : CRUD tables du restaurant
- [ ] Back-office : liste des commandes + changement de statut

### Phase 2 — Caisse & rapports
- [ ] Encaissement d'une commande (espèces / mobile money)
- [ ] Génération et impression du reçu POS (ticket 80mm)
- [ ] Dashboard : chiffre d'affaires du jour, nombre de commandes, top ventes
- [ ] Génération et impression du rapport journalier
- [ ] Notification email/SMS de confirmation de commande (optionnel)

### Phase 3 — Évolutions futures
- [ ] Compte client optionnel (historique de commandes, favoris)
- [ ] Programme de fidélité
- [ ] Paiement en ligne (Mobile Money / FedaPay)
- [ ] Réservation de table en ligne