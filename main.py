from fastapi import FastAPI, HTTPException

from models import AmountUpdate, Product, ProductCreate
from storage import storage

app = FastAPI(title="Grocery Inventory API")


def get_product_or_404(product_id: int) -> Product:
    product = storage.get_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


@app.get("/products", response_model=list[Product])
def get_products():
    return storage.get_all()


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    return get_product_or_404(product_id)


@app.post("/products", response_model=Product, status_code=201)
def create_product(product: ProductCreate):
    return storage.add(product)


@app.patch("/products/{product_id}/amount", response_model=Product)
def update_product_amount(product_id: int, update: AmountUpdate):
    get_product_or_404(product_id)
    return storage.update_amount(product_id, update.amount)


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    get_product_or_404(product_id)
    storage.delete(product_id)
