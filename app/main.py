import logging
import os
from fastapi import FastAPI
from app.database import engine, Base
from app.routes import router

logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG", "False") == "True" else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

DEBUG = os.getenv("DEBUG", "False") == "True"

app = FastAPI(
    title="Address Book API",
    description="A minimal API to manage addresses with coordinate support.",
    version="1.0.0",
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
    openapi_url="/openapi.json" if DEBUG else None,
)

app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    logger.info("Address Book API started")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Address Book API shutdown")