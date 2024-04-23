"""views for products service"""
# Local utilities
from compartidos.serializers import NotFoundSerializer

# Database imports
from apps.webApp.models import products as products_models

# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

# Django REST Framework
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status

# Third party libraries
from drf_yasg.utils import swagger_auto_schema

# Proyecto
# Product & Alarm engine imports
from ....adapters.secondaries.factory import constructor_products as products_repo
from ....adapters.secondaries.factory import constructor_alarms as alarms_repo
from ....engine.domain.exceptions import exceptions_products as exceptions
from ....engine.use_cases import factory as engine
from . import products_serializer, utils

# product engine implementation
products_repository = products_repo.constructor_products(products_models.Product)
products_engine = engine.constructor_manager_products(products_repository)
# Alarm engine implementation
alarms_repository = alarms_repo.constructor_alarms(products_models.Alarm)
alarms_engine = engine.constructor_manager_alarms(alarms_repository)


class ProductsViewSet(viewsets.GenericViewSet):
    """
    Product's CRUD ViewSet
    """

    serializer_class = products_serializer.ProductSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = products_models.Product.objects.all()

    @swagger_auto_schema(
        query_serializer=products_serializer.ProductQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: products_serializer.ProductSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def list_products(self, request) -> Response:
        """view to list/get products"""
        product_query_params_serializer = (
            products_serializer.ProductQueryParamsSerializer(data=request.query_params)
        )
        product_query_params_serializer.is_valid(raise_exception=True)
        from_date = product_query_params_serializer.validated_data.get("from_date")
        to_date = product_query_params_serializer.validated_data.get("to_date")

        if from_date is not None and to_date is not None:
            try:
                products = products_engine.get_product_with_alarms(
                    from_date=from_date, to_date=to_date
                )
                product_data = utils.product_generator_data(products)
                get_product = products_serializer.ProductSerializer(data=product_data)
                get_product.is_valid(raise_exception=True)

                product = get_product.validated_data
                response_data = {
                    "detail": "",
                    "data": product,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"'{e}' exception raised in {__name__} at line 62")
                return Response(
                    data=exceptions.ProductWithExpiryDatesDoesNotExist(
                        from_date, to_date
                    ).message,
                    status=status.HTTP_404_NOT_FOUND,
                )

        products = products_engine.list_products()
        product_data = utils.product_generator_data(products)

        product_serializer = products_serializer.ProductSerializer(
            data=product_data, many=True
        )
        product_serializer.is_valid(raise_exception=True)

        response_data = {
            "detail": "",
            "data": product_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=products_serializer.ProductSwaggerSerializer(),
        responses={
            status.HTTP_201_CREATED: products_serializer.ProductSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: NotFoundSerializer,
        },
    )
    def create_product(self, request) -> Response:
        """view to create product"""
        product_serializer = products_serializer.ProductSerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)

        try:
            product = products_engine.create_product(
                product_name=product_serializer.validated_data.get("product_name"),
                description=product_serializer.validated_data.get("description"),
                stock=product_serializer.validated_data.get("stock"),
                expiry_date=product_serializer.validated_data.get("expiry_date"),
            )
            product = product.__dict__
        except Exception as e:
            print(f"'{e}' exception raised in {__name__} at line 119")
            return Response(
                data=exceptions.ProductAlreadyExist(
                    product_serializer.validated_data.get("product_name")
                ).message,
                status=status.HTTP_400_BAD_REQUEST,
            )

        product_serializer = products_serializer.ProductSerializer(data=product)
        product_serializer.is_valid(raise_exception=True)

        response_data = {
            "detail": "",
            "data": product_serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        query_serializer=products_serializer.ProductQueryParamsSerializer(),
        request_body=products_serializer.ProductSwaggerSerializer(),
        responses={
            status.HTTP_201_CREATED: products_serializer.ProductSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: NotFoundSerializer,
        },
    )
    def update_product(self, request) -> Response:
        """view for update product"""
        product_query_params_serializer = (
            products_serializer.ProductQueryParamsSerializer(data=request.query_params)
        )
        product_query_params_serializer.is_valid(raise_exception=True)

        product_id = product_query_params_serializer.validated_data.get("product_id")
        product_serializer = products_serializer.ProductSerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)

        try:
            product = products_engine.update_product(
                id=product_id,
                product_name=product_serializer.validated_data.get("product_name"),
                description=product_serializer.validated_data.get("description"),
                stock=product_serializer.validated_data.get("stock"),
                expiry_date=product_serializer.validated_data.get("expiry_date"),
            )

            product_dict = product.__dict__
            product_dict["alarms"] = [alarm.__dict__ for alarm in product.alarms]
        except Exception as e:
            print(f"'{e}' exception raised in {__name__} at line 173")
            return Response(
                data=exceptions.ProductDoesNotExist(product_id).message,
                status=status.HTTP_400_BAD_REQUEST,
            )

        product_serializer = products_serializer.ProductSerializer(data=product_dict)
        product_serializer.is_valid(raise_exception=True)

        response_data = {
            "detail": "",
            "data": product_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        query_serializer=products_serializer.ProductQueryParamsSerializer(),
        request_body=products_serializer.ProductSwaggerSerializer(),
        responses={
            status.HTTP_204_NO_CONTENT: "",
            status.HTTP_400_BAD_REQUEST: NotFoundSerializer,
        },
    )
    def delete_product(self, request) -> Response:
        product_query_params_serializer = (
            products_serializer.ProductQueryParamsSerializer(data=request.query_params)
        )
        product_query_params_serializer.is_valid(raise_exception=True)

        product_id = product_query_params_serializer.validated_data.get("product_id")

        try:
            product = products_engine.delete_product(id=product_id)
        except Exception as e:
            print(f"'{e}' exception raised in {__name__} at line 205")
            return Response(
                data=exceptions.ProductDoesNotExist(product_id).message,
                status=status.HTTP_400_BAD_REQUEST,
            )
        response_data = {
            "detail": f"Se elimino producto satisfactoriamente{product}",
            "data": "",
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class AlarmsViewSet(viewsets.GenericViewSet):
    """
    Alarms Create ViewSet
    """

    serializer_class = products_serializer.AlarmSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = products_models.Alarm.objects.all()

    @swagger_auto_schema(
        request_body=products_serializer.AlarmSwaggerSerializer(),
        responses={
            status.HTTP_201_CREATED: products_serializer.AlarmSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: NotFoundSerializer,
        },
    )
    def create_alarm(self, request) -> Response:
        """view to create product"""
        alarm_serializer = products_serializer.AlarmSerializer(data=request.data)
        alarm_serializer.is_valid(raise_exception=True)

        product_id = alarm_serializer.validated_data.get("product_id")

        try:
            product = get_object_or_404(products_models.Product, id=product_id)
            alarms = alarms_engine.create_alarm(
                product_id=product_id,
                alert_type=alarm_serializer.validated_data.get("alert_type"),
                alert_date=alarm_serializer.validated_data.get("alert_date"),
            )
            alarm = [alarm.__dict__ for alarm in alarms]
        except Exception as e:
            print(f"'{e}' exception raised in {__name__} at line 205")
            return Response(
                data=exceptions.ProductDoesNotExist(product_id).message,
                status=status.HTTP_400_BAD_REQUEST,
            )

        alarm_serializer = products_serializer.AlarmSerializer(data=alarm[0])
        alarm_serializer.is_valid(raise_exception=True)

        response_data = {
            "detail": "",
            "data": alarm_serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
