from fastapi import APIRouter

from api.v1.routes.auth import router as auth_router
from api.v1.routes.knowledge import router as knowledge_router
from api.v1.routes.chat import router as chat_router


api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(knowledge_router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
