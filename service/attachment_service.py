import mimetypes
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, File, HTTPException
import uuid
import os
from models import Attachment
from schemas.response.attachment_response import AttachmentResponse
from schemas.attachment_schema import AttachmentInfo
from sqlalchemy import select
from fastapi.responses import FileResponse


class AttachmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def load_file(self, file: UploadFile = File(...)) -> AttachmentResponse:
        filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        file_path = os.path.join("attachments", filename)
        with open(file_path, "wb") as new_file:
            new_file.write(file.file.read())
        db_attachment = Attachment(
            path=file_path
        )
        self.db.add(db_attachment)
        await self.db.commit()
        await self.db.refresh(db_attachment)
        return AttachmentResponse(
            status="success",
            attachment_info=AttachmentInfo(
                id=db_attachment.id,
                path=db_attachment.path
            )
        )

    async def get_attachment(self, attachment_id: uuid.UUID):
        result = await self.db.execute(select(Attachment).where(Attachment.id == attachment_id))
        optional_attachment = result.scalar_one_or_none()
        if not optional_attachment:
            raise HTTPException(status_code=404, detail="Attachment not found")
        filename = os.path.basename(optional_attachment.path)
        mime_type, _ = mimetypes.guess_type(optional_attachment.path)
        if mime_type is None:
            mime_type = "application/octet-stream"
        return FileResponse(
            path=optional_attachment.path,
            filename=filename,
            media_type=mime_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
