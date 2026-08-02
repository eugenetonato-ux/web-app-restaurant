# apps/api/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.menu.models import MenuItem, Category
from apps.orders.models import Order
from apps.tables.models import RestaurantTable


@api_view(["GET"])
@permission_classes([AllowAny])
def api_menu_list(request):
    articles = MenuItem.objects.filter(disponible=True)
    data = [{
        "id": a.id,
        "nom": a.nom,
        "description": a.description,
        "prix": float(a.get_prix_effectif()),
        "categorie": a.categorie.nom,
        "photo": a.get_image_display(),
        "badge": a.badge,
        "note": float(a.note_etoiles)
    } for a in articles]
    return Response({"count": len(data), "results": data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_tables_status(request):
    tables = RestaurantTable.objects.all()
    data = [{
        "id": t.id,
        "numero": t.numero,
        "capacite": t.capacite,
        "statut": t.statut
    } for t in tables]
    return Response(data)
