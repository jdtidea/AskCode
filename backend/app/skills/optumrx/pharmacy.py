from typing import List

from app.models.skills import DomainsEnum, Input, SkillResult, Variant
from app.skills import Skill


class PharmacySkill(Skill):
    name = "OptumRx"
    domains = [DomainsEnum.pharmacy]

    async def trigger_skill(self, req: Input) -> List[SkillResult]:
        await super().trigger_skill(req)
        # TODO: Implement skill
        return [
            SkillResult(
                title="Check your pharmacy and medication information",
                skill=self.name,
                domain=DomainsEnum.pharmacy,
                variant=Variant.MD,
                content="""
Refill and manage your prescriptions online. Compare prices. Fast, free home delivery.

- If you have your order number, you can [track your order](https://os.optumrx.com/order-search) on OptumRx without logging in.
- If you don't have your order number, track your order by signing in to [OptumRx](https://www.optumrx.com/public/landing) and clicking Order Status.
- You can place a new order by signing in to [OptumRx](https://www.optumrx.com/public/landing) and clicking Place an Order.
- Compare prices at different pharmacies before placing an order by signing in to [OptumRx](https://www.optumrx.com/public/landing) and clicking Price a Drug.
""",
            )
        ]
