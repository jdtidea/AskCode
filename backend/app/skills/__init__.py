from typing import List

from loguru import logger

from app.models.domains.domains import DomainsEnum
from app.models.skills import Input, SkillResult


class Skill:
    def __init__(self):
        self.logger = logger

    name: str = ""
    alias: str = ""
    displayName: str = ""
    domains: List[DomainsEnum] = []

    async def trigger_skill(self, req: Input) -> List[SkillResult]:
        dimensions = {
            "custom_dimensions": {
                "skill": self.name,
                "query": req.raw_query,
            }
        }
        self.logger.bind(**dimensions).info(
            'Triggering skill "{name}" for query "{query}"'.format(
                name=self.name, query=req.raw_query
            )
        )
        return []
