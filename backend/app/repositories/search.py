import asyncio
import itertools
from typing import List, Union

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from httpx import HTTPError

from app.core.config import RemoteConfig, get_config
from app.models.domains.domains import DomainPercentage
from app.models.ranking import RankingRequest
from app.models.skills import Input, SkillResult, SkillTypeEnum
from app.models.user import UserPublic
from app.models.v0.search import SearchResult as SearchResultV0
from app.models.v1.search import SearchResult as SearchResultV1
from app.models.v2.search import SearchResult as SearchResultV2
from app.ranking.ranking import create_ranking_request, rank_results
from app.repositories.base import BaseRepository
from app.repositories.domains import DomainsRepository
from app.repositories.entities import EntityRepository
from app.repositories.golden import GoldenRepository
from app.skills import Skill
from app.skills.registry import get_registry_map


class SearchRepository(BaseRepository):
    def __init__(
        self,
        domains_repository=Depends(DomainsRepository),
        golden_repository=Depends(GoldenRepository),
        entity_repository=Depends(EntityRepository),
    ):
        super().__init__()
        self.domains_repository = domains_repository
        self.golden_repository = golden_repository
        self.entity_repository = entity_repository

    async def search_v0(self, query: str, user: UserPublic) -> SearchResultV0:
        domains = await self.get_domains(query)
        domains_dict = {d.domain: d.percentage for d in domains}
        skill_results = await self.search_router(query, user, domains)
        v0_result = SearchResultV0(query=query, domains=domains, results=[])
        v0_result.add_skill_results(skill_results)
        v0_result.results.sort(key=lambda d: domains_dict[d.domain], reverse=True)
        return v0_result

    async def search_v1(
        self, query: str, user: UserPublic, unranked: bool = False
    ) -> Union[SearchResultV1, RankingRequest]:
        domains = await self.get_domains(query)
        domains_dict = {d.domain: d.percentage for d in domains}
        skill_results = await self.search_router(query, user, domains)
        if unranked is True:
            return create_ranking_request(query, skill_results, domains_dict)
        ranked_results = rank_results(query, skill_results, domains_dict)
        result_v1 = SearchResultV1(query=query, results=ranked_results)

        return result_v1

    async def search_v2(
        self, query: str, user: UserPublic
    ) -> Union[SearchResultV2, RankingRequest]:
        registry_map = get_registry_map()
        entities = await self.entity_repository.get_entities(query)
        dynamic_skill_aliases = []
        static_skill_results = []
        for entity in entities:
            matched_skills = registry_map.get(entity, [])
            for matched_skill in matched_skills:
                if matched_skill.type is SkillTypeEnum.dynamic:
                    dynamic_skill_aliases.append(matched_skill.alias)
                else:
                    static_skill_results.append(matched_skill.to_result())
        # TODO: refactor
        dynamic_skills = []
        for dynamic_alias in dynamic_skill_aliases:
            skill = self.dynamic_skills.get(dynamic_alias)
            if skill is not None:
                dynamic_skills.append(skill)
        dynamic_results = await self.trigger_skills(dynamic_skills, query, user)
        results = dynamic_results + static_skill_results
        ranked_results = rank_results(query, results)
        result_v2 = SearchResultV2(query=query, results=ranked_results)

        return result_v2

    async def get_domains(self, query: str) -> List[DomainPercentage]:
        domains = await self.domains_repository.fetch_uhg_domain_response(query=query)
        return domains

    async def search_router(
        self, query: str, user: UserPublic, domains: List[DomainPercentage]
    ) -> List[SkillResult]:
        demo_whitelist = get_config(RemoteConfig.DEMO_USERS).split(",")
        if user is not None and user.id in demo_whitelist:
            result = await self.golden_repository.search(query)
            if result is not None:
                return result
        return await self.trigger_skills(self.skills, query, user)

    @staticmethod
    async def trigger_skills(
        skills: List[Skill], query: str, user: UserPublic
    ) -> List[SkillResult]:
        try:
            req = Input(raw_query=query, identity=user)
            results = await asyncio.gather(
                *[skill.trigger_skill(req) for skill in skills]
            )
            results_list = list(itertools.chain(*results))

        # TODO: Don't fail entire request if one or more skills fail
        except HTTPError as exc:
            logger.error(exc)
            headers = jsonable_encoder(exc.request.headers)
            headers.pop("authorization", None)

            detail = {
                "request": {
                    "headers": headers,
                    "method": exc.request.method,
                    "url": jsonable_encoder(exc.request.url),
                },
            }
            raise HTTPException(status_code=500, detail=detail)

        return results_list

    @staticmethod
    def filter_skills(skills: List[Skill]) -> List[Skill]:
        def within_threshold(skill: Skill) -> bool:
            # TODO: Only run skills that meet some threshold
            # TODO: Match skill<-->domain with "skill registry"
            return True

        return list(filter(within_threshold, skills))
