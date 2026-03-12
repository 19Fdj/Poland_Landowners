from fastapi import APIRouter

from app.api.routes import admin, auth, documents, exports, health, ownership, parcels

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(health.router, prefix="", tags=["health"])
api_router.include_router(parcels.router, prefix="/parcels", tags=["parcels"])
api_router.include_router(ownership.router, tags=["ownership"])
api_router.include_router(documents.router, tags=["documents"])
api_router.include_router(exports.router, tags=["exports"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
