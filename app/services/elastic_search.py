from elasticsearch import Elasticsearch
from app.config.config import settings
import uuid
from app.services.pdf_extractor import ExtractedContentFormat
from typing import List, Optional
from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str
    pdf_id: Optional[uuid.UUID] = None

class ElasticSearchDocument(ExtractedContentFormat):
    pdf_id: uuid.UUID
    embedding: List[float]

class ElasticSearchResponse(BaseModel):
    pdf_id: uuid.UUID
    type: str
    page_number: int
    block_index: int
    content: str

class ElasticSearchService:
    es: Elasticsearch

    def __init__(self, host:str, api_key: str):
        self.es = Elasticsearch(
            hosts=[host],
            api_key=api_key
        )

    def create_index(self):
        if not self.es.indices.exists(index=settings.INDEX_NAME):
            self.es.indices.create(
                index=settings.INDEX_NAME,
                body={
                    "mappings": {
                        "properties": {
                            "pdf_id": {"type": "keyword"},
                            "type": {"type": "keyword"},
                            "content": {"type": "text"},
                            "page_number": {"type": "integer"},
                            "block_index": {"type": "integer"},
                            "embedding": {
                                "type": "dense_vector",
                                "dims": 384,
                                "index": True,
                                "similarity": "cosine"
                            }
                            
                        }
                    }
                }
            )

    def index_document(self, documents: List[ElasticSearchDocument]):
        self.create_index()

        print("Indexing documents...")

        for doc in documents:
            if not doc.content.strip():
                continue

            print("Indexing document: 1")

            es_doc = ElasticSearchDocument(
                pdf_id=doc.pdf_id,
                type=doc.type,
                page_number=doc.page_number,
                block_index=doc.block_index,
                content=doc.content,
                embedding=doc.embedding
            )

            print("Indexing document: 2")

            self.es.index(index=settings.INDEX_NAME, document=es_doc.dict())

            print("Indexed document: 3")


    def search(self, pdf_id: uuid.UUID, query_embedding: List[float], topk: int = 5) -> List[ElasticSearchResponse]:
        knn_query = {
            "field": "embedding",
            "query_vector": query_embedding,
            "k": topk,
            "num_candidates": 50,
            "filter": {
                "term": {
                    "pdf_id": str(pdf_id)
                }
            }
        }

        response = self.es.search(
            index=settings.INDEX_NAME,
            knn=knn_query,
            source_excludes=["embedding"]
        )

        hits = response.get("hits", {}).get("hits", [])
        return [
            ElasticSearchResponse(
                pdf_id=pdf_id,
                type=hit["_source"].get("type"),
                page_number=hit["_source"].get("page_number"),
                block_index=hit["_source"].get("block_index"),
                content=hit["_source"].get("content"),
            )
            for hit in hits
        ]

search_service = ElasticSearchService(settings.ES_HOST, settings.ES_API_KEY)
