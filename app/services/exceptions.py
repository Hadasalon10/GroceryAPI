"""Domain-level errors raised by the service layer.

Kept free of any HTTP concerns; routers translate these into the appropriate
HTTP response.
"""


class ProductNotFoundError(Exception):
    def __init__(self, product_id: int) -> None:
        self.product_id = product_id
        super().__init__(f"Product {product_id} not found")
