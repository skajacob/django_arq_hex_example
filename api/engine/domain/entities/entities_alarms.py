# Librerias Estandar
from dataclasses import dataclass


@dataclass
class Alarm:
    id: int
    product_id: str
    alert_type: str
    alert_date: str
    is_active: bool
