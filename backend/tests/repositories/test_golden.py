import pytest

from app.repositories.golden import GoldenRepository


class TestDomains:
    repository = GoldenRepository()

    @pytest.mark.asyncio
    async def test_hsa_response(self) -> None:
        results = await self.repository.search("hsa balance")
        assert results is not None

    @pytest.mark.asyncio
    async def test_doctor_visit(self) -> None:
        results = await self.repository.search("doctor visit")
        assert results is not None

    @pytest.mark.asyncio
    async def test_flu_vaccine(self) -> None:
        results = await self.repository.search("flu vaccine")
        assert results is not None
