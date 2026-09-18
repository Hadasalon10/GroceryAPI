
# sepreate this file there is real models of product and there is a model for api stuff
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    name: str
    cost: float
    amount: int


class ProductCreate(BaseModel):
    name: str
    cost: float = Field(gt=0)
    amount: int = Field(ge=0)


class AmountUpdate(BaseModel):
    amount: int = Field(ge=0)
