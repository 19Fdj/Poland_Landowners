from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging


configure_logging()

app = FastAPI(
    title="Poland Rural Landowner Finder API",
    version="0.1.0",
    description=(
        "Internal API for lawful cadastral parcel diligence. Ownership data must only be stored "
        "when supported by lawful/public/user-supplied sources and valid legal basis."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {"name": "Poland Rural Landowner Finder API", "docs": "/docs"}

