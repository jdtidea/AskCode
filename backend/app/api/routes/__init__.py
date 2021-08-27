from fastapi import APIRouter

from app.api.routes.v0.search import router as search_router_v0
from app.api.routes.v1.search import router as search_router_v1
from app.api.routes.v2.search import router as search_router_v2

router = APIRouter()

router.include_router(search_router_v0, prefix="/search", tags=["search"])
router.include_router(search_router_v0, prefix="/v0/search", tags=["search"])
router.include_router(search_router_v1, prefix="/v1/search", tags=["search"])
router.include_router(search_router_v2, prefix="/v2/search", tags=["search"])
