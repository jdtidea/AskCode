import pytest

from app.skills.ava.ava import AvaSkill


class TestAvaSkill:
    ava_skill = AvaSkill()

    @pytest.mark.asyncio
    async def test_ava_skill(self, mock_input) -> None:
        results = await self.ava_skill.trigger_skill(mock_input)
        # By default, ava will not return results unless there is a user authenticated
        assert len(results) is 0
