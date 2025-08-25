from fastapi import FastAPI
from app.routes.user import router as user_router
from app.db.database import init_db

app = FastAPI(title="Pdf Search App")

@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(
    user_router
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pdf Search App"}
