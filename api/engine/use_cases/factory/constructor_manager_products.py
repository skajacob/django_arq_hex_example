"""Constructor manager for product uses cases"""
# Project Libraries
from api.engine.use_cases.ports.secondaries import repository_products as repository
from api.engine.use_cases.ports.primaries import manager_products as manager
from api.engine.use_cases.services import service_products as service


def constructor_manager_products(
    products_repository: repository.ProductRepository,
) -> manager.ProductManager:
    return service.ProductService(products_repository=products_repository)
