from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.pdf import router as pdf_router
from app.db.database import init_db
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

app = FastAPI(title="Pdf Search App")

@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(user_router)
app.include_router(pdf_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pdf Search App"}
