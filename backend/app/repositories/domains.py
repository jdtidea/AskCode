import json
from typing import List

from loguru import logger

from app.core.breakers import domains_breaker
from app.core.config import REQUEST_TIMEOUT, RemoteConfig, get_config
from app.core.http import insecure_async_client
from app.models.domains.ava import Query
from app.models.domains.domains import DomainPercentage, DomainsEnum, UHGDomainsResponse
from app.repositories.base import BaseRepository


class DomainsRepository(BaseRepository):
    @staticmethod
    @domains_breaker
    async def fetch_uhg_domain_response(query: str) -> List[DomainPercentage]:

        data = Query(query=query)

        # get domains from UHG-Domains
        async with insecure_async_client() as client:
            header = {"Content-Type": "application/json"}
            resp = await client.post(
                get_config(RemoteConfig.UHG_DOMAINS_URL),
                headers=header,
                data=data.json(),
                timeout=REQUEST_TIMEOUT,
            )

        data = json.loads(resp.text)
        domains = UHGDomainsResponse(**data).domains
        logger.info(query, str(domains))
        domain_percentages = []
        for domain in domains:
            if domain[0] == "Provider":
                domain_percentages.append(
                    DomainPercentage(
                        domain=DomainsEnum.provider, percentage=float(domain[1])
                    )
                )
            elif domain[0] == "Benefit":
                domain_percentages.append(
                    DomainPercentage(
                        domain=DomainsEnum.benefits, percentage=float(domain[1])
                    )
                )
            elif domain[0] == "Pharmacy":
                domain_percentages.append(
                    DomainPercentage(
                        domain=DomainsEnum.pharmacy, percentage=float(domain[1])
                    )
                )
            elif domain[0] == "Health&Wellness":
                domain_percentages.append(
                    DomainPercentage(
                        domain=DomainsEnum.health, percentage=float(domain[1])
                    )
                )
            elif domain[0] == "Financial":
                domain_percentages.append(
                    DomainPercentage(
                        domain=DomainsEnum.financial, percentage=float(domain[1])
                    )
                )
            elif domain[0] == "Claims":
                domain_percentages.append(
                    DomainPercentage(
                        domain=DomainsEnum.claims, percentage=float(domain[1])
                    )
                )

        # TODO: this should be removed once the number of skills are the same as the number of domains
        # UHG Domains returns a list of list of string representing the domain, and percentage match

        return domain_percentages
