from app.schemas.pdf_schema import PdfDocumentCreate
from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
import datetime
import uuid
from app.models import PdfDocument

def create_pdf_document(pdf_document: PdfDocumentCreate, db: Session = Depends(get_db)):
    pdf = PdfDocument(**pdf_document.dict(), created_at=datetime.datetime.now())

    db.add(pdf)
    db.commit()
    db.refresh(pdf)
    return pdf

def get_pdf_document(pdf_id: uuid.UUID, db: Session = Depends(get_db)):
    return db.query(PdfDocument).filter(PdfDocument.id == pdf_id).first()

def get_user_pdfs(user_id: uuid.UUID, db: Session = Depends(get_db)):
    return db.query(PdfDocument).filter(PdfDocument.user_id == user_id).all()
