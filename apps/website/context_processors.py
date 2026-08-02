# apps/website/context_processors.py
from apps.menu.models import Category


def nav_categories(request):
    """
    Rend les catégories actives disponibles dans le menu de navigation
    (dropdown "Catégories") sur toutes les pages du site public.
    """
    return {
        "nav_categories": Category.objects.filter(actif=True).order_by("ordre_affichage", "nom")
    }
