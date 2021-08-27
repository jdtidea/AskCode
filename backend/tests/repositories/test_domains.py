import pytest

from app.repositories.domains import DomainsRepository


class TestDomains:
    repository = DomainsRepository()

    @pytest.mark.asyncio
    async def test_domains_response(self) -> None:
        domains = await self.repository.fetch_uhg_domain_response("I have back pain")
        assert domains is not None
