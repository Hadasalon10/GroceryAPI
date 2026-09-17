#think what if tomroww we will need to imlemnt it in a real db want we gonna do write this thing again? i would create a base class and inmemory class that will excted and overrid function

from itertools import count 
from typing import Optional

from models import Product, ProductCreate


class ProductStorage: # add proper error handling
    """In-memory storage for products. Replace with a real database later."""

    def __init__(self) -> None:
        self._products: dict[int, Product] = {}
        self._id_counter = count(start=1) # use a uuid insted of count think in the future this is a prodction service that lives 24/7 but can restart then all the count will be 1 again and some product will b overrided again think of it like a real db

    def get_all(self) -> list[Product]:
        return list(self._products.values())

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self._products.get(product_id)

    def add(self, data: ProductCreate) -> Product:
        product_id = next(self._id_counter)
        product = Product(id=product_id, **data.model_dump())
        self._products[product_id] = product
        return product

    def update_amount(self, product_id: int, amount: int) -> Optional[Product]:
        product = self._products.get(product_id)
        if product is None:
            return None
        product.amount = amount
        return product

    def delete(self, product_id: int) -> bool:
        return self._products.pop(product_id, None) is not None


storage = ProductStorage() # this creation should be a fastapi depdinces read about it or ask me if u need (think of it as a real db)
