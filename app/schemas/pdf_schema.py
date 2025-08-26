from pydantic import BaseModel
import uuid
from datetime import datetime

class PdfDocumentCreate(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    file_name: str

class PdfDocument(PdfDocumentCreate):
    created_at: datetime

    class Config:
        from_attributes = True
