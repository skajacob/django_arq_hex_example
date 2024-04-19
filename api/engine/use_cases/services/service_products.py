"""Service for product uses_cases"""
# Standard Libraries
# Librerias Estandar
import typing

# Project Libraries
from api.engine.use_cases.ports.secondaries import repository_products as repository
from api.engine.use_cases.ports.primaries import manager_products as manager

# Entity
from api.engine.domain.entities import entities_products as entity


class ProductService(manager.ProductManager):
    """class to define the service for product uses cases"""

    def __init__(self, products_repository: repository.ProductRepository):
        self.products_repository = products_repository

    def list_products(self) -> typing.List[entity.Product]:
        return self.products_repository.list_products()

    def get_product(self, id: int) -> entity.Product:
        return self.products_repository.get_product(id=id)

    def create_product(
        self,
        product_name: str,
        description: str,
        stock: int,
        expiry_date: str,
    ) -> entity.Product:
        product = self.products_repository.create_product(
            product_name=product_name,
            description=description,
            stock=stock,
            expiry_date=expiry_date,
        )
        return product

    def update_product(
        self,
        id: typing.Optional[int],
        product_name: typing.Optional[str],
        description: typing.Optional[str],
        stock: typing.Optional[int],
        expiry_date: typing.Optional[str],
    ) -> entity.Product:
        product = self.products_repository.update_product(
            id=id,
            product_name=product_name,
            description=description,
            stock=stock,
            expiry_date=expiry_date,
        )
        return product

    def delete_product(
        self,
        id: int,
    ) -> None:
        self.products_repository.delete_product(
            id=id,
        )
        return None
