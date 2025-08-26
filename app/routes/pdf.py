from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.schemas.pdf_schema import PdfDocumentCreate, PdfDocument
from app.db.database import get_db
from app.utils.auth import get_current_user
from app.models.user_model import User
from app.services.pdf_extractor import extract_pdf_content
from app.services.pdf import create_pdf_document, get_pdf_document, get_user_pdfs
from app.services.embedding import embedding_service
from app.services.elastic_search import ElasticSearchDocument, ElasticSearchResponse, SearchRequest, search_service
import uuid
from typing import List

router = APIRouter()

@router.post("/upload-pdf", response_model=PdfDocument)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if file.content_type != "application/pdf":
        return {"error": "Invalid file type. Only PDF files are allowed."}
    
    try:
        pdf_file = await file.read()

        print("step 1")

        extracted_data = extract_pdf_content(pdf_file)

        print("step 2")

        if extracted_data.error:
            raise HTTPException(status_code=500, detail=f"Error extracting PDF content: {extracted_data.error}")
        
        pdf_id = uuid.uuid4()

        print("step 3")

        db_pdf = PdfDocumentCreate(
            id=pdf_id,
            user_id=current_user.id,
            file_name=file.filename,
        )

        print("step 4")

        response = create_pdf_document(db_pdf, db)

        print("step 5")

        if response is None:
            raise HTTPException(status_code=500, detail="Error saving PDF document to the database.")

        results: List[ElasticSearchDocument] = []
        for item in extracted_data.all_content:
            embedding = embedding_service.create_embedding(item.content)
            es_doc = ElasticSearchDocument(
                pdf_id=pdf_id,
                type=item.type,
                page_number=item.page_number,
                block_index=item.block_index,
                content=item.content,
                embedding=embedding
            )
            results.append(es_doc)

        print("step 6", "".join(x.type for x in results))

        print("step 6.1", search_service.ping())

        search_service.index_document(results)

        print("step 7")

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading/processing PDF: {str(e)}")
    

@router.post("/search", response_model=List[ElasticSearchResponse])
async def search(
    search_request: SearchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        query_embedding = embedding_service.create_embedding(search_request.query)

        if search_request.pdf_id:
            pdf_doc = get_pdf_document(search_request.pdf_id, db)
            if not pdf_doc or pdf_doc.user_id != current_user.id:
                raise HTTPException(status_code=404, detail="PDF document not found or access denied.")
            
        search_results = search_service.search(pdf_id=search_request.pdf_id, query_embedding=query_embedding)

        return search_results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching PDF: {str(e)}")
    
@router.get("/pdfs", response_model=List[PdfDocument])
def fetch_user_pdfs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        user_pdfs = get_user_pdfs(current_user.id, db)
        return user_pdfs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user PDFs: {str(e)}")
