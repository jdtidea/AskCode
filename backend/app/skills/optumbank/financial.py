from typing import List

from app.models.skills import DomainsEnum, Input, SkillResult, Variant
from app.skills import Skill


class FinancialSkill(Skill):
    name = "Optum Bank"
    domains = [DomainsEnum.financial]

    async def trigger_skill(self, req: Input) -> List[SkillResult]:
        # TODO: Implement skill
        await super().trigger_skill(req)
        return [
            SkillResult(
                title="Check your healthcare financial information",
                skill=self.name,
                domain=DomainsEnum.financial,
                variant=Variant.MD,
                content="""
Use our resources online to untangle your health finances to drive better health outcomes.

- You can check your balances and manage your accounts by logging in to [Optum Bank](https://healthsafeid.optumbank.com/) and going to your dashboard.
- Use our [Health Savings Account Calculator](http://cdn.optum.com/oh/ohb/calc/calc.htm) to determine your contribution amount.
- If you need to open a new account, use our [comparison tool](https://www.optumbank.com/health-accounts/account-comparison.html) to understand your options.
""",
            )
        ]
