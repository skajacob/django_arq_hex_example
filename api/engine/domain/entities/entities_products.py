# Librerias Estandar
from dataclasses import dataclass


@dataclass
class Product:
    id: int
    product_name: str
    description: str
    stock: int
    expiry_date: str
