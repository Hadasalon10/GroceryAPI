import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_product_repository
from app.main import app
from app.repositories.json_file import JsonFileProductRepository


@pytest.fixture
def repository(tmp_path):
    return JsonFileProductRepository(tmp_path / "products.json")


@pytest.fixture
def client(repository):
    app.dependency_overrides[get_product_repository] = lambda: repository
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
