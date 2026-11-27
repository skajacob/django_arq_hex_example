# Librerias Estandar
import typing
from dataclasses import dataclass
from datetime import date


@dataclass
class Alarm:
    id: int
    product_id: int
    alert_type: str
    alert_date: date
    is_active: typing.Optional[bool] = None
