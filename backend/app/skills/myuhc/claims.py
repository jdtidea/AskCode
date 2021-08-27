from typing import List

from app.models.skills import DomainsEnum, Input, SkillResult, Variant
from app.skills import Skill


class ClaimsSkill(Skill):
    name = "MyUHC Claims"
    domains = [DomainsEnum.claims]

    async def trigger_skill(self, req: Input) -> List[SkillResult]:
        # TODO: Implement skill
        await super().trigger_skill(req)
        return [
            SkillResult(
                title="Check your claims",
                skill=self.name,
                domain=DomainsEnum.claims,
                variant=Variant.MD,
                content="""
You can find your claims information easily on [myuhc.com](https://www.myuhc.com/?srcName=MR_FAQ)

- Log in and go to Manage My Claims to see a list of your claims and if they’ve been processed.
- You can also call the number on your health plan ID card to talk with a representative about your claims.
""",
            )
        ]
