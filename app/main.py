from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routes import recipes

app = FastAPI(title="Recipes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "*",
        "null",
    ]

)

app.include_router(recipes.router)

models.Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}