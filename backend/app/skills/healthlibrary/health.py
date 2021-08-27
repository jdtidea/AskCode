import json
from typing import List

from loguru import logger

from app.core.breakers import health_library_breaker
from app.core.config import REQUEST_TIMEOUT, RemoteConfig, get_config
from app.core.http import async_client
from app.models.domains.health import HealthLibraryAPI, HealthLibraryResponse, HLDocs
from app.models.skills import DomainsEnum, Input, SkillResult, Variant
from app.skills import Skill


class HealthSkill(Skill):
    name = "HEALTH"
    alias = "health"
    domains = [DomainsEnum.health]

    async def trigger_skill(self, req: Input) -> List[SkillResult]:
        await super().trigger_skill(req)
        # get health library response
        health_library_response = await self.fetch_health_library_response(
            query=req.raw_query
        )
        results = []

        if health_library_response is not None and len(health_library_response) > 0:

            for text in health_library_response:
                results.append(
                    SkillResult(
                        title=text.lex_title,
                        url="https://healthlibrary.optum.com{url}".format(
                            url=text.url_t
                        ),
                        domain=DomainsEnum.health,
                        skill=self.name,
                        variant=Variant.MD,
                        content=text.description_t[0],
                    )
                )

        return results

    @health_library_breaker
    async def fetch_health_library_response(self, query) -> List[HLDocs]:
        try:
            params = HealthLibraryAPI(
                wt="json",
                q=query,
                start=0,
                languageCD="en",
                brandNM="optum",
                spellcheck="true",
            )
            async with async_client() as client:
                resp = await client.get(
                    url=get_config(RemoteConfig.HEALTH_URL),
                    params=params.dict(),
                    timeout=REQUEST_TIMEOUT,
                )
            data = json.loads(resp.text)
            # TODO: configure how many results are returned
            return HealthLibraryResponse(**data).response.docs[:3]
        except Exception as e:
            logger.error(e)
            return []
