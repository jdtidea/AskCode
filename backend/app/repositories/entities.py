from typing import List

from app.core.breakers import entity_breaker
from app.repositories.base import BaseRepository


class EntityRepository(BaseRepository):
    @entity_breaker
    async def get_entities(self, query: str) -> List[str]:
        # TODO: Hook in to new entity/intent model
        return [
            "benefits",
            "provider",
            "claims",
            "bank",
            "financial",
            "rx",
            "pharmacy",
            "health",
        ]
