import pytest

from app.skills.optumrx.pharmacy import PharmacySkill


class TestOptumRx:
    pharmacy_skill = PharmacySkill()

    @pytest.mark.asyncio
    async def test_financial_skill(self, mock_input) -> None:
        results = await self.pharmacy_skill.trigger_skill(mock_input)
        assert len(results) is 1
