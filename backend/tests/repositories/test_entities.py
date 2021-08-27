import pytest

from app.repositories.entities import EntityRepository


class TestDomains:
    repository = EntityRepository()

    @pytest.mark.asyncio
    async def test_response(self) -> None:
        results = await self.repository.get_entities("")
        assert results is not None
