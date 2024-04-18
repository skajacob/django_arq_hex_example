from api.adapters.secondaries.db_orm.repository_implementation_products import (
    Product as ProductORM,
)
from api.engine.use_cases.ports.secondaries import repository_products as repository

# orm
from apps.webApp.models import products as product_models


def constructor_products(
    products_orm_model: product_models.Product,
) -> repository.ProductRepository:
    return ProductORM(products_orm_model=products_orm_model)
