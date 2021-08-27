from typing import List, Optional

from app.models.core import CoreModel
from app.models.skills import SkillResult


class Result(SkillResult):
    score: Optional[float]


class SearchBase(CoreModel):
    query: str
    results: List[Result]


class SearchResult(SearchBase):
    pass
