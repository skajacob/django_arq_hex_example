"""Products repository implementation"""
# Standard Libraries
# Librerias Estandar
import typing
from datetime import date
from datetime import datetime

# Engine
from api.engine.use_cases.ports.secondaries import repository_products as repository
from api.adapters.secondaries.db_orm import orm_mapper

# Entity
from api.engine.domain.entities import entities_products as entity
from api.engine.domain.exceptions import exceptions_products as exceptions
from apps.webApp.models import products as product_models

# Librerías de Terceros
# Models
from django.db import IntegrityError
from django.db.models import Count


class Product(repository.ProductRepository):
    def __init__(self, products_orm_model: product_models.Product):
        self._products_orm_model = products_orm_model

    def _get_orm(self, product_id: int):
        try:
            return self._products_orm_model.objects.get(id=product_id)
        except self._products_orm_model.DoesNotExist as error:
            raise exceptions.ProductDoesNotExist(product_id) from error

    def list_products(self) -> typing.List[entity.Product]:
        return [
            orm_mapper.constructor_products_entities(product)
            for product in self._products_orm_model.objects.all().prefetch_related(
                "alarms"
            )
        ]

    def get_product_with_alarms(
        self, from_date: str, to_date: str
    ) -> typing.List[entity.Product]:
        from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()

        products_with_alarms = self._products_orm_model.objects.filter(
            expiry_date__range=(from_date_obj, to_date_obj)
        ).prefetch_related("alarms")
        return [
            orm_mapper.constructor_products_entities(product)
            for product in products_with_alarms
        ]

    def get_product_without_asigned_alarms(self) -> typing.List[entity.Product]:
        return [
            orm_mapper.constructor_products_entities(product)
            for product in self._products_orm_model.objects.annotate(
                num_alarms=Count("alarms")
            ).filter(num_alarms=0)
        ]

    def get_product(self, id_product: int) -> entity.Product:
        return orm_mapper.constructor_products_entities(self._get_orm(id_product))

    def create_product(
        self,
        product_name: str,
        description: str,
        stock: int,
        expiry_date: date,
    ) -> entity.Product:
        try:
            product = self._products_orm_model.objects.create(
                product_name=product_name,
                description=description,
                stock=stock,
                expiry_date=expiry_date,
            )
        except IntegrityError as error:
            raise exceptions.ProductAlreadyExist(product_name) from error
        return orm_mapper.constructor_products_entities(product)

    def update_product(
        self,
        id: typing.Optional[int],
        product_name: typing.Optional[str],
        description: typing.Optional[str],
        stock: typing.Optional[int],
        expiry_date: typing.Optional[date],
    ) -> entity.Product:
        product = self._get_orm(id)

        if product_name is not None:
            product.product_name = product_name
        if description is not None:
            product.description = description
        if stock is not None:
            product.stock = stock
        if expiry_date is not None:
            product.expiry_date = expiry_date
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
        self._get_orm(id).delete()
