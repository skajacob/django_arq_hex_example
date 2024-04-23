# Librerias Estandar
import typing
from dataclasses import dataclass

# Proyecto
from .entities_alarms import Alarm


@dataclass
class Product:
    id: int
    product_name: str
    description: str
    stock: int
    expiry_date: str
    alarms: typing.Optional[list[Alarm]] = None
