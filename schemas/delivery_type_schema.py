from pydantic import BaseModel
from uuid import UUID


class DeliveryTypeSchema(BaseModel):
    type: str
    cost: int


class DeliveryTypeWithIdSchema(DeliveryTypeSchema):
    id: UUID

    class Config:
        from_attributes = True
