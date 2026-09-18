"""Business logic for managing the product catalog.

Routers call into this service instead of talking to a repository directly,
so HTTP handling and inventory rules stay decoupled.
"""

from app.models.domain import Product
from app.models.schemas import ProductCreateRequest
from app.repositories.base import ProductRepository
from app.services.exceptions import ProductNotFoundError


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    def list_products(self) -> list[Product]:
        return self._repository.get_all()

    def get_product(self, product_id: int) -> Product:
        product = self._repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product

    def create_product(self, data: ProductCreateRequest) -> Product:
        product = Product(id=self._repository.next_id(), **data.model_dump())
        return self._repository.add(product)

    def update_amount(self, product_id: int, amount: int) -> Product:
        product = self.get_product(product_id)
        product.amount = amount
        return self._repository.update(product)

    def delete_product(self, product_id: int) -> None:
        self.get_product(product_id)
        self._repository.delete(product_id)
