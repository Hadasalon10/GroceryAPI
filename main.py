# RAZA: This file should look empty only add the routes here and create the app.
# read about mvc pattern i expect every route to be super simple and cll a controller or serivce that will do the real job 
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


@app.patch("/products/{product_id}/amount", response_model=Product) # why patch and not put lets disscus on this super important to know :)
def update_product_amount(product_id: int, update: AmountUpdate):
    get_product_or_404(product_id)
    return storage.update_amount(product_id, update.amount)


@app.delete("/products/{product_id}", status_code=204) # I dont like magic numbers there is a packages that get this number as const thik some developers dont know what is 204? same for all
def delete_product(product_id: int):
    get_product_or_404(product_id)
    storage.delete(product_id)
