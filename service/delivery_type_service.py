from sqlalchemy.ext.asyncio import AsyncSession
from schemas.delivery_type_schema import DeliveryTypeSchema, DeliveryTypeWithIdSchema
from schemas.response.delivery_type_response import DeliveryTypeResponse, DeliveryTypesResponse
from sqlalchemy import select
from models import DeliveryType
from fastapi import HTTPException


class DeliveryTypeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_delivery_type(self, payload: DeliveryTypeSchema) -> DeliveryTypeResponse:
        result = await self.db.execute(select(DeliveryType).where(DeliveryType.type == payload.type))
        optional_delivery_type = result.scalar_one_or_none()
        if optional_delivery_type:
            raise HTTPException(status_code=401, detail="Delivery type with this name already exist")
        db_delivery_type = DeliveryType(
            type=payload.type,
            cost=payload.cost
        )
        self.db.add(db_delivery_type)
        await self.db.commit()
        await self.db.refresh(db_delivery_type)
        return DeliveryTypeResponse(
            status="success",
            delivery_type_info=DeliveryTypeWithIdSchema(
                id=db_delivery_type.id,
                type=db_delivery_type.type,
                cost=db_delivery_type.cost
            )
        )

    async def get_delivery_types(self) -> DeliveryTypesResponse:
        result = await self.db.execute(select(DeliveryType))
        all_delivery_types = result.scalars().all()
        if all_delivery_types:
            delivery_types_schemas = [DeliveryTypeSchema.from_orm(delivery_type) for delivery_type in all_delivery_types]
        else:
            delivery_types_schemas = None
