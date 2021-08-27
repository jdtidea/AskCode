from typing import List

from app.models.ranking import RankingItem, RankingRequest
from app.models.skills import SkillResult
from app.models.v1.search import Result

from .score import score_result


def rank_results(
    query: str, skill_results: List[SkillResult], domains_dict={}
) -> List[Result]:
    ranked_results = []
    for result in skill_results:
        skill_score = score_result(query, result, domains_dict.get(result.domain, 0))
        ranked_result = Result.parse_obj(result)
        ranked_result.score = skill_score
        ranked_results.append(ranked_result)
    return sorted(ranked_results, key=lambda r: r.score, reverse=True)


def create_ranking_request(
    query: str, results: List[SkillResult], domains_dict
) -> RankingRequest:
    req = RankingRequest(query=query, items=[])
    for result in results:
        req.items.append(
            RankingItem(
                id=str(result.id),
                skill=result.skill,
                domainProbability=domains_dict.get(result.domain, 0),
                domain=result.domain,
                heading=result.title,
                content=result.content,
                meta=result.meta,
            )
        )
    return req
