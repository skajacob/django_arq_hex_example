"""Products repository implementation"""
# Standard Libraries
# Librerias Estandar
import typing

# Engine
from api.engine.use_cases.ports.secondaries import repository_products as repository
from api.engine.use_cases.factory import orm_mapper

# Entity
from api.engine.domain.entities import entities_products as entity

# ORM
from apps.webApp.models import products as product_models


class Product(repository.ProductRepository):
    def __init__(self, products_orm_model: product_models.Product):
        self._products_orm_model = products_orm_model

    def list_products(self) -> typing.List[entity.Product]:
        return [
            orm_mapper.constructor_products_entities(product)
            for product in self._products_orm_model.objects.all()
        ]

    def get_product(self, product_id: int) -> entity.Product:
        product = self._products_orm_model.objects.get(id=product_id)
        return orm_mapper.constructor_products_entities(product)

    def create_product(
        self,
        product_name: str,
        description: str,
        stock: int,
        expiry_date: str,
    ) -> entity.Product:
        product = self._products_orm_model.objects.create(
            product_name=product_name,
            description=description,
            stock=stock,
            expiry_date=expiry_date,
        )

        return orm_mapper.constructor_products_entities(product)

    def update_product(
        self,
        id: typing.Optional[int],
        product_name: typing.Optional[str],
        description: typing.Optional[str],
        stock: typing.Optional[int],
        expiry_date: typing.Optional[str],
    ) -> entity.Product:
        product = self._products_orm_model.objects.get(id=id)

        product.product_name = product_name if product_name else product.product_name
        product.description = description if description else product.description
        product.stock = stock if stock else product.stock
        product.expiry_date = expiry_date if expiry_date else product.expiry_date
        product.save(
            update_fields=[
                "product_name",
                "description",
                "stock",
                "expiry_date",
            ]
        )

        return orm_mapper.constructor_products_entities(product)

    def delete_product(self, id: int) -> None:
        product = self._products_orm_model.objects.get(id=id)
        product.delete()
