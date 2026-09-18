from fastapi import status


def create_product(client, name="Apples", cost=2.5, amount=10):
    return client.post("/products", json={"name": name, "cost": cost, "amount": amount})


def test_get_products_empty(client):
    response = client.get("/products")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_product_returns_201_and_assigns_id(client):
    response = create_product(client)

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "Apples"
    assert body["cost"] == 2.5
    assert body["amount"] == 10


def test_create_product_rejects_invalid_payload(client):
    response = client.post("/products", json={"name": "Bad", "cost": -1, "amount": 5})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_get_product_by_id(client):
    created = create_product(client).json()

    response = client.get(f"/products/{created['id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == created


def test_get_product_not_found_returns_404(client):
    response = client.get("/products/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "999" in response.json()["detail"]


def test_update_product_amount(client):
    created = create_product(client, amount=5).json()

    response = client.patch(f"/products/{created['id']}/amount", json={"amount": 20})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["amount"] == 20


def test_update_amount_for_missing_product_returns_404(client):
    response = client.patch("/products/999/amount", json={"amount": 20})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_product(client):
    created = create_product(client).json()

    response = client.delete(f"/products/{created['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    follow_up = client.get(f"/products/{created['id']}")
    assert follow_up.status_code == status.HTTP_404_NOT_FOUND


def test_delete_missing_product_returns_404(client):
    response = client.delete("/products/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_products_persist_across_repository_instances(client, repository):
    create_product(client, name="Bananas")

    products = repository.get_all()

    assert len(products) == 1
    assert products[0].name == "Bananas"
