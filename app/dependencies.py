"""FastAPI dependency providers.

Centralizing these makes the repository/service wiring swappable in one place
(e.g. pointing at a different storage backend) and lets tests override them
via `app.dependency_overrides`.
"""

from functools import lru_cache
from pathlib import Path

from fastapi import Depends

from app.repositories.base import ProductRepository
from app.repositories.json_file import JsonFileProductRepository
from app.services.product_service import ProductService

DATA_FILE_PATH = Path(__file__).resolve().parent.parent / "data" / "products.json"


@lru_cache
def get_product_repository() -> ProductRepository:
    return JsonFileProductRepository(DATA_FILE_PATH)


def get_product_service(
    repository: ProductRepository = Depends(get_product_repository),
) -> ProductService:
    return ProductService(repository)
