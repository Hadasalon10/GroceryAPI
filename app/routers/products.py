"""HTTP layer for the /products endpoints.

Routes only translate between HTTP and the service layer - no storage or
business logic lives here. `ProductNotFoundError` is turned into a 404 by the
app-wide exception handler registered in app/main.py, so routes don't need
their own try/except.
"""

from fastapi import APIRouter, Depends, status

from app.dependencies import get_product_service
from app.models.schemas import (
    ProductAmountUpdateRequest,
    ProductCreateRequest,
    ProductResponse,
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
def get_products(
    service: ProductService = Depends(get_product_service),
) -> list[ProductResponse]:
    return service.list_products()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    return service.get_product(product_id)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreateRequest,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    return service.create_product(data)


@router.patch("/{product_id}/amount", response_model=ProductResponse)
def update_product_amount(
    product_id: int,
    data: ProductAmountUpdateRequest,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    return service.update_amount(product_id, data.amount)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
) -> None:
    service.delete_product(product_id)
