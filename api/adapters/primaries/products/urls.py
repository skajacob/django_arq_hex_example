# Librerías de Terceros
from django.urls import path

# Proyecto
from .products_views import ProductsViewSet, AlarmsViewSet

list_products = {"get": "list_products"}
create_product = {"post": "create_product"}
update_product = {"put": "update_product"}
delete_product = {"delete": "delete_product"}

create_alarm = {"post": "create_alarm"}


urlpatterns = [
    path(
        "products",
        ProductsViewSet.as_view(
            {**list_products, **create_product, **update_product, **delete_product}
        ),
        name="crud-products",
    ),
    path(
        "alarms",
        AlarmsViewSet.as_view({**create_alarm}),
        name="create_alarm",
    ),
]
