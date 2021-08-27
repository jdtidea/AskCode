from typing import List, Optional

from app.models.core import BaseModel
from app.models.domains.domains import DomainsEnum


class RankingItem(BaseModel):
    id: str
    skill: str
    domainProbability: float
    domain: DomainsEnum
    heading: str
    content: str
    meta: Optional[dict]


class RankingRequest(BaseModel):
    query: str
    items: List[RankingItem]


# key is id, value is score
class RankingResponse(BaseModel):
    items: dict
