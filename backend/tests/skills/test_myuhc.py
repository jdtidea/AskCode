import pytest

from app.skills.myuhc.benefits import BenefitsSkill
from app.skills.myuhc.claims import ClaimsSkill
from app.skills.myuhc.providers import ProvidersSkill


class TestMyUhc:
    benefits_skill = BenefitsSkill()
    claims_skill = ClaimsSkill()
    providers_skill = ProvidersSkill()

    @pytest.mark.asyncio
    async def test_benefits_skill(self, mock_input) -> None:
        results = await self.benefits_skill.trigger_skill(mock_input)
        assert len(results) is 1

    @pytest.mark.asyncio
    async def test_claims_skill(self, mock_input) -> None:
        results = await self.claims_skill.trigger_skill(mock_input)
        assert len(results) is 1

    @pytest.mark.asyncio
    async def test_providers_skill(self, mock_input) -> None:
        results = await self.providers_skill.trigger_skill(mock_input)
        assert len(results) is 1
