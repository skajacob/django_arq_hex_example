"""Serializer for products API"""
# Librerias Estandar
from datetime import datetime, date

# Librerías de Terceros
from rest_framework import serializers

# Proyecto
from ....engine.domain.exceptions import exceptions_dates as exceptions


def validate_fields(attrs):
    """function to valida date fiels fields"""
    # Validation for payment date, can't be before the current date.
    expiry_date = attrs.get("expiry_date")

    if expiry_date and expiry_date < datetime.now().date():
        raise exceptions.InvalidDate

    # Search date validation
    from_date = attrs.get("from_date")
    to_date = attrs.get("to_date")

    # Check if start_date or end_date is None, set default values
    if from_date is None:
        from_date = date.min
    if to_date is None:
        to_date = date.max

    if from_date > to_date:
        raise exceptions.InvalidSearchDate


class DetailAlarmSerializer(serializers.Serializer):
    "Serializer for Alarms detail"
    is_active = serializers.BooleanField()
    is_expired = serializers.BooleanField()
    days_until_activation = serializers.IntegerField()
    days_expired = serializers.IntegerField()


class AlarmSerializer(serializers.Serializer):
    """Serializer for Alarms"""

    id = serializers.IntegerField(required=False)
    product_id = serializers.IntegerField()
    alert_type = serializers.CharField()
    alert_date = serializers.DateField()
    is_active = serializers.BooleanField(required=False)
    detail = DetailAlarmSerializer(required=False)


class ProductSerializer(serializers.Serializer):
    """Serializer for Products"""

    id = serializers.IntegerField(required=False)
    product_name = serializers.CharField()
    description = serializers.CharField()
    stock = serializers.IntegerField()
    expiry_date = serializers.DateField()
    alarms = AlarmSerializer(required=False, many=True)


class ProductSwaggerSerializer(serializers.Serializer):
    """Serializer for Products"""

    id = serializers.IntegerField(required=False)
    product_name = serializers.CharField()
    description = serializers.CharField()
    stock = serializers.IntegerField()
    expiry_date = serializers.DateField()


class AlarmSwaggerSerializer(serializers.Serializer):
    """Serializer for Alarms"""

    id = serializers.IntegerField(required=False)
    product_id = serializers.IntegerField()
    alert_type = serializers.CharField()
    alert_date = serializers.DateField()


class ProductQueryParamsSerializer(serializers.Serializer):
    """Serializer for ProductsQueryParams"""

    product_id = serializers.IntegerField(required=False)
    from_date = serializers.CharField(required=False)
    to_date = serializers.CharField(required=False)


class AlarmQueryParamsSerializer(serializers.Serializer):
    """Serializer for AlarmsQueryParams"""

    is_active = serializers.BooleanField(required=False)
