import pytest

from app.skills.healthlibrary.health import HealthSkill


class TestAvaSkill:
    health_skill = HealthSkill()

    @pytest.mark.asyncio
    async def test_health_skill(self, mock_input) -> None:
        results = await self.health_skill.trigger_skill(mock_input)
        assert len(results) is 3
