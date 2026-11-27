# Librerias Estandar
import typing
from dataclasses import dataclass
from datetime import date

# Proyecto
from .entities_alarms import Alarm


@dataclass
class Product:
    id: int
    product_name: str
    description: str
    stock: int
    expiry_date: date
    alarms: typing.Optional[list[Alarm]] = None
