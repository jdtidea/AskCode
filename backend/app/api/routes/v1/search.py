from typing import Optional

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.models.ranking import RankingRequest
from app.models.user import UserPublic
from app.models.v1.search import SearchResult
from app.repositories.search import SearchRepository

router = APIRouter()


# double route annotation to work around a FastAPI redirect issue
# https://github.com/tiangolo/fastapi/issues/2060#issuecomment-770088270
@router.get("", response_model=SearchResult, name="search:search-query:v1")
@router.get("/", include_in_schema=False)
async def search(
    q: Optional[str] = "",
    search_repo: SearchRepository = Depends(SearchRepository),
    current_user: UserPublic = Depends(get_current_user),
) -> SearchResult:
    search_result = await search_repo.search_v1(query=q, user=current_user)
    return search_result


@router.get(
    "/unranked", response_model=RankingRequest, name="search:search-query:v1:unranked"
)
async def search(
    q: Optional[str] = "",
    search_repo: SearchRepository = Depends(SearchRepository),
    current_user: UserPublic = Depends(get_current_user),
) -> SearchResult:

    search_result = await search_repo.search_v1(
        query=q, user=current_user, unranked=True
    )

    return search_result
