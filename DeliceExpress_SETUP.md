# Délice Express — Mise en place du projet (Windows / PowerShell)

Ce guide applique l'architecture définie dans `DeliceExpress_skills-app.md` (apps, flux commande/caisse, sans facturation en ligne pour la Phase 1) et suit ton workflow habituel.

---

## 1. Création du dossier et de l'environnement virtuel

```powershell
mkdir DeliceExpress
cd DeliceExpress
python -m venv env
env\Scripts\activate
```

Tu dois voir `(env)` apparaître devant ton prompt avant de continuer.

---

## 2. Installation des dépendances

```powershell
python -m pip install --upgrade pip

pip install django
pip install djangorestframework
pip install requests
pip install python-dotenv
pip install python-decouple
pip install django-cors-headers
pip install pillow

# Génération PDF (reçus, rapport journalier)
pip install reportlab
pip install qrcode

# Traitement asynchrone (notifications, tâches différées)
pip install celery
pip install redis

# Base de données (SQLite en Phase 1, PostgreSQL prêt pour plus tard)
pip install psycopg2-binary

# Qualité de code
pip install black isort flake8
pip install pytest pytest-django factory-boy
```

Génère ton `requirements.txt` :

```powershell
pip freeze > requirements.txt
```

---

## 3. Démarrage du projet Django

```powershell
django-admin startproject config .
```

## 4. Création du dossier `apps/` et des applications

```powershell
mkdir apps
New-Item -Path apps\__init__.py -ItemType File

mkdir apps\staff, apps\menu, apps\tables, apps\orders, apps\cashier, apps\reports, apps\dashboard, apps\notifications, apps\api, apps\common, apps\website

python manage.py startapp staff apps/staff
python manage.py startapp menu apps/menu
python manage.py startapp tables apps/tables
python manage.py startapp orders apps/orders
python manage.py startapp cashier apps/cashier
python manage.py startapp reports apps/reports
python manage.py startapp dashboard apps/dashboard
python manage.py startapp notifications apps/notifications
python manage.py startapp api apps/api
python manage.py startapp common apps/common
python manage.py startapp website apps/website
```

### Corriger le `name` de chaque app

```python
# apps/menu/apps.py
from django.apps import AppConfig

class MenuConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.menu"   # ⚠️ à corriger dans chacune des 11 apps
```

Répète cette correction (`name = "apps.<nom_app>"`) dans les 11 fichiers `apps.py`.

---

## 5. Création des dossiers `templates/` et `static/`

```powershell
mkdir templates
mkdir templates\Base
mkdir templates\Website
mkdir templates\Admin
mkdir templates\Cashier
mkdir templates\Reports
mkdir templates\Emails

type nul > templates\Base\base.html
type nul > templates\Base\base_admin.html
type nul > templates\Website\home.html
type nul > templates\Website\menu.html
type nul > templates\Website\panier.html
type nul > templates\Admin\dashboard.html
type nul > templates\Admin\menu_liste.html
type nul > templates\Admin\tables_liste.html
type nul > templates\Admin\commandes.html
type nul > templates\Cashier\ticket.html
:: ticket.html = gabarit 80mm imprimé directement (window.print), PAS un PDF

type nul > templates\Reports\rapport_journalier.html
:: rapport_journalier.html sert de base HTML au générateur PDF (reportlab) — le livrable final est un .pdf

mkdir static\css, static\js, static\images, static\vendor
New-Item -Path static\css\style.css -ItemType File
New-Item -Path static\css\admin.css -ItemType File
New-Item -Path static\js\script.js -ItemType File
New-Item -Path static\js\panier.js -ItemType File

mkdir media
mkdir media\menu, media\logos

mkdir logs
mkdir backups
mkdir scripts
mkdir docs
```

---

## 6. Fichier `.env` (racine du projet)

```powershell
New-Item -Path .env -ItemType File
```

Contenu de `.env` :

```
DEBUG=True
SECRET_KEY=change-moi-en-production
ALLOWED_HOSTS=127.0.0.1,localhost

CURRENCY=FCFA
RESTAURANT_NAME=Délice Express

DEFAULT_FROM_EMAIL=noreply@delice-express.app
```

Ajoute `.env` dans `.gitignore` :

```powershell
New-Item -Path .gitignore -ItemType File
Add-Content .gitignore "env/`n.env`n__pycache__/`n*.pyc`nmedia/`ndb.sqlite3`nlogs/"
```

---

## 7. Configuration `config/settings.py`

### a) Imports en haut du fichier

```python
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
```

### b) Variables sensibles depuis `.env`

```python
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")
CURRENCY = config("CURRENCY", default="FCFA")
```

### c) `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Tiers
    "rest_framework",
    "corsheaders",

    # Apps Délice Express
    "apps.staff",
    "apps.menu",
    "apps.tables",
    "apps.orders",
    "apps.cashier",
    "apps.reports",
    "apps.dashboard",
    "apps.notifications",
    "apps.api",
    "apps.common",
    "apps.website",
]
```

### d) `MIDDLEWARE`

```python
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

### e) Authentification (staff uniquement — voir §1 de `skills-app.md`)

```python
LOGIN_URL = "/admin-panel/connexion/"
LOGIN_REDIRECT_URL = "/admin-panel/dashboard/"
LOGOUT_REDIRECT_URL = "/"

AUTH_USER_MODEL = "staff.StaffUser"
```

> Rappel : le site public **ne nécessite pas de compte**. Seul le back-office (`/admin-panel/`) est protégé par authentification (email + mot de passe du personnel).

### f) Templates

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

### g) Static / Media

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
```

### h) Base de données (SQLite en Phase 1, PostgreSQL prêt pour plus tard)

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

### i) Django REST Framework

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
```

---

## 8. Configuration `config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("api/v1/", include("apps.api.urls")),
    path("", include("apps.website.urls")),
    path("admin-panel/", include("apps.dashboard.urls")),
    path("admin-panel/menu/", include("apps.menu.urls")),
    path("admin-panel/tables/", include("apps.tables.urls")),
    path("admin-panel/commandes/", include("apps.orders.urls")),
    path("admin-panel/caisse/", include("apps.cashier.urls")),
    path("admin-panel/rapports/", include("apps.reports.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 9. Migrations et super utilisateur

```powershell
python manage.py makemigrations
python manage.py migrate

LE SUPER USERS
	python manage.py createsuperuser

******Supprimer des super users 

Le plus simple est de passer par le shell Django :

bash
python manage.py shell
python
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(is_superuser=True).delete()

Ou en une seule commande depuis le terminal, sans ouvrir le shell interactif :

bash

python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.filter(is_superuser=True).delete()"

Avant de supprimer, tu peux lister les superusers existants pour vérifier lesquels seront touchés :

bash

python manage.py shell -c "from django.contrib.auth import get_user_model; print(list(get_user_model().objects.filter(is_superuser=True).values_list('username', 'email')))"

⚠️ Une fois tous les superusers supprimés, tu n'auras plus accès à l'admin Django

Voici l'équivalent pour supprimer les utilisateurs simples (non-superusers) :


python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.filter(is_superuser=False).delete()"





celery -A config worker --loglevel=info --pool=solo
```

---

## 10. Lancement du serveur

```powershell
python manage.py runserver
```

- Site public : `http://127.0.0.1:8000/`
- Back-office : `http://127.0.0.1:8000/admin-panel/`

---

## 11. Ordre de développement recommandé (Phase 1)

1. `apps/staff` — modèle `StaffUser` + connexion back-office
2. `apps/menu` — catégories + articles (prix FCFA)
3. `apps/tables` — gestion des tables du restaurant
4. `apps/website` — site public (catégories, menu, panier)
5. `apps/orders` — création de commande depuis le panier
6. `apps/dashboard` — vue d'ensemble commandes du jour
7. `apps/cashier` — encaissement + impression reçu POS
8. `apps/reports` — chiffre d'affaires + rapport journalier imprimable

---

## 12. Commandes utiles (rappel de ton workflow)

```powershell
# Vérifier le personnel enregistré
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.count()
>>> exit()

# Mise à jour GitHub
git status
git add .
git commit -m "mise a jour"
git push origin main
```