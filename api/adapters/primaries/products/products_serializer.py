"""Serializer for products API"""
# Third-Party Libraries
# Librerías de Terceros
from rest_framework import serializers


class AlarmSerializer(serializers.Serializer):
    """Serializer for Alarms"""

    id = serializers.IntegerField(required=False)
    product_name = serializers.CharField()
    alert_type = serializers.CharField()
    alert_date = serializers.CharField()
    is_active = serializers.BooleanField()


class ProductSerializer(serializers.Serializer):
    """Serializer for Products"""

    id = serializers.IntegerField(required=False)
    product_name = serializers.CharField()
    description = serializers.CharField()
    stock = serializers.IntegerField()
    expiry_date = serializers.CharField()
    alarms = AlarmSerializer()


class ProductQueryParamsSerializer(serializers.Serializer):
    """Serializer for ProductsQueryParams"""

    id = serializers.IntegerField(required=False)
    from_date = serializers.CharField(required=False)
    to_dato = serializers.CharField(required=False)


class AlarmQueryParamsSerializer(serializers.Serializer):
    """Serializer for AlarmsQueryParams"""

    is_active = serializers.BooleanField(required=False)
