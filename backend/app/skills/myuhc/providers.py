from typing import List

from app.models.skills import DomainsEnum, Input, SkillResult, Variant
from app.skills import Skill


class ProvidersSkill(Skill):
    name = "MyUHC Provider"
    domains = [DomainsEnum.provider]

    async def trigger_skill(self, req: Input) -> List[SkillResult]:
        # TODO: Implement skill
        await super().trigger_skill(req)
        return [
            SkillResult(
                title="Find Providers",
                skill=self.name,
                domain=DomainsEnum.provider,
                variant=Variant.MD,
                content="""
With almost every plan, you’ll pay less when you choose providers in your network.
Here are several easy ways to find network doctors, clinics and hospitals.

- If you have your health plan ID card, sign in to [myuhc.com](https://www.myuhc.com/?srcName=MR_FAQ). Go to your personalized home page and use the [provider search tool](https://connect.werally.com/plans/uhc) to look for doctors, clinics and hospitals in your network. Your search will show you a list of providers, plus you can see cost and quality ratings so you can choose what works best for you.
- If you don’t have your ID card yet, you can still use the [provider search tool](https://connect.werally.com/plans/uhc). Explore the list of doctors, clinics and providers to find one that's in your network so you’ll be ready when your plan starts.
- If you're on the go, try the [UnitedHealthcare app](https://www.uhc.com/individual-and-family/member-resources/health-care-tools/unitedhealthcare-app). You can use it to help search for network doctors, urgent care centers, clinics and hospitals on your smartphone. Even if you’re traveling at your child's sporting event or away from home visiting family or friends, a network option may be close by – and UnitedHealthcare app makes it easier to know your options.
""",
            )
        ]
