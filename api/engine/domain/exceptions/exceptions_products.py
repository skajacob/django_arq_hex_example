from compartidos.exceptions import ExceptionBase


class ProductDoesNotExist(ExceptionBase):
    """Product does not exist"""

    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = {"detail": f"El producto con el  {self.product_id} no existe"}


class ProductAlreadyExist(ExceptionBase):
    """Product already exist"""

    def __init__(self, product_name: str):
        self.product_name = product_name
        self.message = {
            "detail": f"El producto con el nombre: {self.product_name} ya existe"
        }


class ProductWithExpiryDatesDoesNotExist(ExceptionBase):
    """Product does not exist"""

    def __init__(self, from_date: str, to_date: str):
        self.from_date = from_date
        self.to_date = to_date
        self.message = {
            "detail": f"El busqueda con el rango de fechas {self.from_date} a {self.to_date} esta vacia"
        }
