"""API-facing request/response DTOs. Kept separate from the domain model (domain.py)
so the wire format can evolve independently of internal storage representation.
"""

from pydantic import BaseModel, ConfigDict, Field


class ProductCreateRequest(BaseModel):
    name: str
    cost: float = Field(gt=0)
    amount: int = Field(ge=0)


class ProductAmountUpdateRequest(BaseModel):
    amount: int = Field(ge=0)


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    cost: float
    amount: int
