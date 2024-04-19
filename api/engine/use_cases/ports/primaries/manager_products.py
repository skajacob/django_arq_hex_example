"""Primary ports for product service"""
# Standard Libraries
# Librerias Estandar
import typing
import abc

# Entity
from api.engine.domain.entities import entities_products as entity


class ProductManager(abc.ABC):
    """class to define the manager for products engine"""

    @abc.abstractmethod
    def list_products(
        self,
    ) -> typing.List[entity.Product]:
        ...

    @abc.abstractmethod
    def get_product(self, expiry_date: str) -> entity.Product:
        ...

    @abc.abstractmethod
    def create_product(
        self,
        product_name: str,
        description: str,
        stock: int,
        expiry_date: str,
    ) -> entity.Product:
        ...

    @abc.abstractmethod
    def update_product(
        self,
        id: int,
        product_name: str,
        description: str,
        stock: int,
        expiry_date: str,
    ) -> entity.Product:
        ...

    @abc.abstractmethod
    def delete_product(
        self,
        id: int,
    ) -> None:
        ...
