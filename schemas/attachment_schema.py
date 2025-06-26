from pydantic import BaseModel
from uuid import UUID


class AttachmentInfo(BaseModel):
    id: UUID
    path: str
