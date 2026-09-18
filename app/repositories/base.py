"""Repository interface for product persistence.

Defined as an abstract base class so the storage backend (JSON file, SQLite,
a real database later on) can be swapped without touching the service layer,
and so tests can inject a fake/in-memory implementation.
"""

from abc import ABC, abstractmethod

from app.models.domain import Product


class ProductRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Product]:
        """Return every stored product."""

    @abstractmethod
    def get_by_id(self, product_id: int) -> Product | None:
        """Return a single product, or None if it doesn't exist."""

    @abstractmethod
    def add(self, product: Product) -> Product:
        """Persist a new product."""

    @abstractmethod
    def update(self, product: Product) -> Product:
        """Persist changes to an existing product."""

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """Remove a product. Returns True if it existed."""

    @abstractmethod
    def next_id(self) -> int:
        """Return the next unused product id."""
