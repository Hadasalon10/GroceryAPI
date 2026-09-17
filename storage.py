// storage.py
from itertools import count
from typing import Optional

from models import Product, ProductCreate


class ProductStorage:
    """In-memory storage for products. Replace with a real database later."""

    def __init__(self) -> None:
        self._products: dict[int, Product] = {}
        self._id_counter = count(start=1)

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


storage = ProductStorage()
