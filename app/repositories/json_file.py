"""JSON-file-backed implementation of ProductRepository.

Reads and writes the whole file on every operation. That's fine for the small,
single-process inventory this API manages, and it means the catalog survives
app restarts instead of living only in memory. The next product id is derived
from what's on disk (max existing id + 1) rather than an in-memory counter, so
ids don't collide or reset when the process restarts.
"""

import json
from pathlib import Path
from threading import Lock

from app.models.domain import Product
from app.repositories.base import ProductRepository


class JsonFileProductRepository(ProductRepository):
    def __init__(self, file_path: Path | str) -> None:
        self._file_path = Path(file_path)
        self._lock = Lock()
        if not self._file_path.exists():
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            self._write_all([])

    def _read_all(self) -> list[Product]:
        with self._file_path.open("r", encoding="utf-8") as f:
            raw_products = json.load(f)
        return [Product(**item) for item in raw_products]

    def _write_all(self, products: list[Product]) -> None:
        with self._file_path.open("w", encoding="utf-8") as f:
            json.dump([product.model_dump() for product in products], f, indent=2)

    def get_all(self) -> list[Product]:
        with self._lock:
            return self._read_all()

    def get_by_id(self, product_id: int) -> Product | None:
        with self._lock:
            products = self._read_all()
        return next((p for p in products if p.id == product_id), None)

    def add(self, product: Product) -> Product:
        with self._lock:
            products = self._read_all()
            products.append(product)
            self._write_all(products)
        return product

    def update(self, product: Product) -> Product:
        with self._lock:
            products = self._read_all()
            for index, existing in enumerate(products):
                if existing.id == product.id:
                    products[index] = product
                    break
            self._write_all(products)
        return product

    def delete(self, product_id: int) -> bool:
        with self._lock:
            products = self._read_all()
            remaining = [p for p in products if p.id != product_id]
            was_deleted = len(remaining) != len(products)
            if was_deleted:
                self._write_all(remaining)
        return was_deleted

    def next_id(self) -> int:
        with self._lock:
            products = self._read_all()
        return max((p.id for p in products), default=0) + 1
