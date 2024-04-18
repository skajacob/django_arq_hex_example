# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions
from drf_yasg.views import get_schema_view
from django.urls import re_path, include, path
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Cheaf API assesment",
        default_version="v1",
        description="Esta api es un ejemplo de como se puede implementar una api para la API de CHEAF",
    ),
    public=True,
    permission_classes=[DjangoModelPermissions],
    # authentication_classes=[IsAuthenticated],
)

urlpatterns = [
    path("", include("api.adapters.primaries.products.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
