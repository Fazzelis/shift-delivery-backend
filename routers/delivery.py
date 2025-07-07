from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.get_session import get_db
from schemas.response.delivery_type_response import DeliveryTypeResponse, DeliveryTypesResponse
from schemas.delivery_type_schema import DeliveryTypeSchema
from service.delivery_type_service import DeliveryTypeService


router = APIRouter(
    prefix="/delivery",
    tags=["Delivery"]
)


@router.post("/add-delivery-type", response_model=DeliveryTypeResponse)
async def add_delivery_type(
        payload: DeliveryTypeSchema,
        db: AsyncSession = Depends(get_db)
):
    return await DeliveryTypeService(db).add_delivery_type(payload=payload)


@router.get("/get-delivery-types", response_model=DeliveryTypesResponse)
async def get_delivery_types(
        db: AsyncSession = Depends(get_db)
):
    return await DeliveryTypeService(db).get_delivery_types()
