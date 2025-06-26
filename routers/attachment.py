from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from database.get_session import get_db
from service.attachment_service import AttachmentService
from schemas.response.attachment_response import AttachmentResponse
from fastapi.responses import FileResponse
from uuid import UUID


router = APIRouter(
    prefix="/attachment",
    tags=["Attachment"]
)


@router.post("/load_file", response_model=AttachmentResponse)
async def load_file(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
        ):
    return await AttachmentService(db).load_file(file)


@router.get("/get", response_class=FileResponse)
async def get_attachment(attachment_id: UUID, db: AsyncSession = Depends(get_db)):
    return await AttachmentService(db).get_attachment(attachment_id)
