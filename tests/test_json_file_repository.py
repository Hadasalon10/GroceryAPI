from app.models.domain import Product
from app.repositories.json_file import JsonFileProductRepository


def make_repo(tmp_path, filename="products.json"):
    return JsonFileProductRepository(tmp_path / filename)


def test_new_repository_creates_empty_file(tmp_path):
    repo = make_repo(tmp_path)

    assert repo.get_all() == []
    assert (tmp_path / "products.json").exists()


def test_add_and_get_by_id(tmp_path):
    repo = make_repo(tmp_path)
    product = Product(id=1, name="Milk", cost=3.0, amount=4)

    repo.add(product)

    assert repo.get_by_id(1) == product
    assert repo.get_by_id(2) is None


def test_update_replaces_existing_product(tmp_path):
    repo = make_repo(tmp_path)
    repo.add(Product(id=1, name="Milk", cost=3.0, amount=4))

    updated = Product(id=1, name="Milk", cost=3.0, amount=9)
    repo.update(updated)

    assert repo.get_by_id(1).amount == 9


def test_delete_returns_true_when_removed(tmp_path):
    repo = make_repo(tmp_path)
    repo.add(Product(id=1, name="Milk", cost=3.0, amount=4))

    assert repo.delete(1) is True
    assert repo.get_by_id(1) is None
    assert repo.delete(1) is False


def test_next_id_increments_from_existing_data(tmp_path):
    repo = make_repo(tmp_path)
    assert repo.next_id() == 1

    repo.add(Product(id=1, name="Milk", cost=3.0, amount=4))
    assert repo.next_id() == 2


def test_data_survives_repository_restart(tmp_path):
    file_path = tmp_path / "products.json"
    first_repo = JsonFileProductRepository(file_path)
    first_repo.add(Product(id=1, name="Milk", cost=3.0, amount=4))

    second_repo = JsonFileProductRepository(file_path)

    assert second_repo.get_all() == [Product(id=1, name="Milk", cost=3.0, amount=4)]
    assert second_repo.next_id() == 2
