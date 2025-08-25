from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
import datetime
import uuid

class PdfDocument(Base):
    __tablename__ = "pdf_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    doc_id = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow())

    owner = relationship("User", back_populates="documents")