from pydantic import BaseModel
from schemas.delivery_type_schema import DeliveryTypeWithIdSchema


class DeliveryTypeResponse(BaseModel):
    status: str
    delivery_type_info: DeliveryTypeWithIdSchema


class DeliveryTypesResponse(BaseModel):
    status: str
    delivery_types: list[DeliveryTypeWithIdSchema] | None
