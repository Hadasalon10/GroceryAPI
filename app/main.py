"""App factory: creates the FastAPI instance, wires up routers, and maps
domain-level errors to HTTP responses. Nothing route-specific lives here.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.routers import products
from app.services.exceptions import ProductNotFoundError

app = FastAPI(title="Grocery Inventory API")


@app.exception_handler(ProductNotFoundError)
def handle_product_not_found(request: Request, exc: ProductNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


app.include_router(products.router)
