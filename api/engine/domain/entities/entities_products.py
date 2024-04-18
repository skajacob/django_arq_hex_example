# Librerias Estandar
from dataclasses import dataclass


@dataclass
class Product:
    id: int
    product_name: str
    description: str
    stock: int
    expiry_date: str
    alarms: list


@dataclass
class Alarm:
    id: int
    product_name: str
    alert_type: str
    alert_date: str
    is_active: bool
    is_expired: bool
