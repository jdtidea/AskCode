from typing import Optional

from app.models.domains.domains import DomainsEnum
from app.models.skills import SkillResult, Variant
from app.repositories.base import BaseRepository

# Repository to hold "golden" query results, or results that return an immediate answer,
# or trigger some skill directly for an answer
# Most of this is skeleton/pre-filled stuff until we have a model for golden answers


class GoldenRepository(BaseRepository):
    async def search(self, query: str) -> Optional[SkillResult]:  # noqa
        if "hsa balance" in query.lower():
            return SkillResult(
                title="Health Savings Account",
                skill="Optum Bank",
                domain=DomainsEnum.financial,
                variant=Variant.MD,
                content="""
#### Current Balance

$3924.31

##### UNITEDHEALTH GROUP
###### *****7094
                        """,
            )
        if "doctor visit" in query.lower():
            return SkillResult(
                title="Recent claims",
                skill="MyUHC",
                domain=DomainsEnum.claims,
                variant=Variant.MD,
                content="""
##### Northwell Health

[View Medical Claim #CJ30367294 >](https://google.com)

###### In-Network

| Amount Billed | Plan Paid | You May Owe |
| -- | -- | -- |
| $295.00 | $277.00 | $0.00 |

    """,
            )
        if "flu vaccine" in query.lower() or "flu shot" in query.lower():
            return SkillResult(
                title="Get your flu shot today",
                skill="MyUHC",
                domain=DomainsEnum.provider,
                variant=Variant.MD,
                content="""
Good news, your UnitedHealthcare health plan is provided through your employer!
Your flu shot is covered at $0 out-of-pocket. You can get a flu shot at more than 50,000 locations. 

[Find a nearby location](https://www.uhc.com/health-and-wellness/health-topics/flu/insurance-through-employer)
""",
            )
        return None
