

# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/admin-panel/", permanent=False)),
    path("django-admin/", admin.site.urls),
    path("api/v1/", include("apps.api.urls")),
    path("admin-panel/", include("apps.dashboard.urls")),
    path("admin-panel/menu/", include("apps.menu.urls")),
    path("admin-panel/tables/", include("apps.tables.urls")),
    path("admin-panel/commandes/", include("apps.orders.urls")),
    path("admin-panel/caisse/", include("apps.cashier.urls")),
    path("admin-panel/rapports/", include("apps.reports.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)