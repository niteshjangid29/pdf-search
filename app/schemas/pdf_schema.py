from pydantic import BaseModel
import uuid

class PdfDocumentCreate(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    file_name: str

class PdfDocument(PdfDocumentCreate):
    created_at: str

    class Config:
        from_attributes = True
