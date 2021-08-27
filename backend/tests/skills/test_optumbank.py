import pytest

from app.skills.optumbank.financial import FinancialSkill


class TestOptumBank:
    financial_skill = FinancialSkill()

    @pytest.mark.asyncio
    async def test_financial_skill(self, mock_input) -> None:
        results = await self.financial_skill.trigger_skill(mock_input)
        assert len(results) is 1
