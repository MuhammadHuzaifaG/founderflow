from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import get_settings
from app.db import init_db

settings = get_settings()
init_db()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="FounderFlow AI: founder workflow assistant",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=r"https://.*\.github\.io",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "service": settings.app_name,
        "status": "running",
        "docs_url": "/docs",
    }

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": settings.app_name,
    }