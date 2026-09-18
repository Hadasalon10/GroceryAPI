"""Internal domain representation of a product, as stored by the repository layer."""

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    cost: float
    amount: int
