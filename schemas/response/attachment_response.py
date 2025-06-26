from pydantic import BaseModel
from schemas.attachment_schema import AttachmentInfo


class AttachmentResponse(BaseModel):
    status: str
    attachment_info: AttachmentInfo
