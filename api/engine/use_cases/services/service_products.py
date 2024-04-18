"""Service for product uses_cases"""
# Standard Libraries
# Librerias Estandar
import typing

from api.engine.use_cases.ports.secondaries import repository_products as repository

# Project Libraries
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
        alarms: list,
    ) -> entity.Product:
        product = self.products_repository.create_product(
            product_name=product_name,
            description=description,
            stock=stock,
            expiry_date=expiry_date,
            alarms=alarms,
        )
        return product

    def update_product(
        self,
        id: int,
        product_name: str,
        description: str,
        stock: int,
        expiry_date: str,
        alarms: list,
    ) -> entity.Product:
        product = self.products_repository.update_product(
            id=id,
            product_name=product_name,
            description=description,
            stock=stock,
            expiry_date=expiry_date,
            alarms=alarms,
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

    # def create_alarm(
    #     self,
    #     product_name: str,
    #     alert_type: str,
    #     alert_date: str,
    #     is_active : bool,
    #     is_expired : bool
    # ) -> entity.Product:

    #     alarm = self.products_repository.create_alarm(
    #         product_name= product_name,
    #         alert_type= alert_type,
    #         alert_date= alert_date,
    #         is_active= is_active,
    #         is_expired = is_expired
    #     )
    #     return alarm

    # def update_alarm(
    #     self,
    #     id: int,
    #     product_name: str,
    #     alert_type: str,
    #     alert_date: str,
    #     is_active : bool,
    #     is_expired : bool
    # ) -> entity.Alarm:

    #     alarm = self.products_repository.update_alarm(
    #         id=id,
    #         product_name= product_name,
    #         alert_type= alert_type,
    #         alert_date= alert_date,
    #         is_active= is_active,
    #         is_expired = is_expired
    #     )
    #     return alarm
