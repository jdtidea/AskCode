from typing import List, Optional

from app.models.core import CoreModel
from app.models.domains.domains import DomainPercentage, DomainsEnum
from app.models.skills import SkillResult, Variant


class Item(CoreModel):
    variant: Variant
    title: Optional[str]
    content: Optional[str]


class Result(CoreModel):
    heading: str
    skill: str
    domain: DomainsEnum
    items: List[Item]


class SearchBase(CoreModel):
    query: str
    domains: List[DomainPercentage]
    results: List[Result]


class SearchResult(SearchBase):
    # this is messy code, but v0 shouldn't be around much longer
    def add_skill_results(self, results: List[SkillResult]):
        for result in results:
            # Format static responses (1:1) the easy way
            if result.skill in [
                "MyUHC Claims",
                "MyUHC Benefits",
                "MyUHC Provider",
                "Optum Bank",
                "OptumRx",
            ]:
                self.results.append(
                    Result(
                        skill=result.skill,
                        domain=result.domain,
                        heading=result.title,
                        items=[Item(variant=result.variant, content=result.content)],
                    )
                )
            if result.skill == "AVA":
                ava_item = Item(
                    variant=result.variant, content=result.content, title=result.title
                )
                try:
                    ava_idx = [r.skill for r in self.results].index("AVA")
                    self.results[ava_idx].items.append(ava_item)
                except ValueError:
                    # We haven't created a top-level result for ava yet
                    self.results.append(
                        Result(
                            skill=result.skill,
                            domain=result.domain,
                            heading="Your benefit coverage",
                            items=[ava_item],
                        )
                    )

            if result.skill == "HEALTH":
                content = """
[{title}]({url})

{description}

""".format(
                    title=result.title, url=result.url, description=result.content
                )
                try:
                    health_idx = [r.skill for r in self.results].index("HEALTH")
                    self.results[health_idx].items[0].content += content
                except ValueError:
                    # We haven't created a top-level result for the health skill yet
                    self.results.append(
                        Result(
                            skill=result.skill,
                            domain=result.domain,
                            heading="Health & Wellness",
                            items=[Item(variant=result.variant, content=content)],
                        )
                    )
        if "HEALTH" in [r.skill for r in self.results]:
            health_idx = [r.skill for r in self.results].index("HEALTH")
            self.results[health_idx].items[
                0
            ].content += """

For more articles, visit [Optum Health Library](https://healthlibrary.optum.com)
"""
