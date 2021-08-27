from typing import List

from app.models.skills import DomainsEnum, Input, SkillResult, Variant
from app.skills import Skill


class BenefitsSkill(Skill):
    name = "MyUHC Benefits"
    domains = [DomainsEnum.benefits]

    async def trigger_skill(self, req: Input) -> List[SkillResult]:
        # TODO: Implement skill
        await super().trigger_skill(req)
        return [
            SkillResult(
                title="Check your benefits",
                skill=self.name,
                domain=DomainsEnum.benefits,
                variant=Variant.MD,
                content="""
Checking your benefits can help you avoid cost surprises, so it's good to review what's covered and what’s not before you make an appointment.

- Log in to [myuhc.com](https://www.myuhc.com/?srcName=MR_FAQ) and go to Benefits & Coverage to review what's covered under your plan.
- If you want a copy of your coverage documents mailed to you, call the phone number on your health plan ID card and ask us to send you a copy.
""",
            )
        ]
